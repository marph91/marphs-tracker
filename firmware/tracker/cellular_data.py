"""NB-IoT or LTE-M registration and HTTPS POST via SIM7080G AT commands."""

import re
import time

import logger

from tracker.payload import obfuscate_payload, serialize_payload

LOG = logger.Logger(__name__)


class CellularDataError(Exception):
    pass


class CellularDataClient:
    """Configure cellular data bearer and send HTTPS POST requests."""

    def __init__(self, modem, config):
        self.modem = modem
        self.config = config
        self._connected = False

    def _send_http_chunk(self, conn_id, data: bytes):
        # TODO: https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G/issues/96#issuecomment-2586446251
        # LOG("chunk:", data)
        self.modem.send_at(f"AT+CASEND={conn_id},{len(data)}", wait=5, await_all=[">"])
        # raw write - sends bytes and doesn't append additional "\r\n"
        self.modem.uart.write(data)
        self.modem.send_at("", wait=5, await_all=["OK"])

    def _parse_url(self, url):
        secure = url.startswith("https://")
        stripped = url[8:] if secure else url[7:]
        slash = stripped.find("/")
        if slash == -1:
            host = stripped
            path = "/"
        else:
            host = stripped[:slash]
            path = stripped[slash:]
        port = 443 if secure else 80
        return secure, host, port, path

    def collect_registration_information(self):
        response = self.modem.send_at("AT+COPS?", await_all=["OK"])
        LOG(f"COPS - Operator Selection: {response.splitlines()[2]}")
        response = self.modem.send_at("AT+CPSI?", await_all=["OK"])
        LOG(f"CPSI - UE System Information: {response.splitlines()[2]}")
        response = self.modem.send_at("AT+CSQ", await_all=["OK"])
        LOG(f"CSQ - Signal Quality Report: {response.splitlines()[2]}")
        response = self.modem.send_at("AT+CEREG?", await_all=["OK"])
        LOG(f"CEREG - EPS Network Registration Status: {response.splitlines()[2]}")

    def connect(self):
        LOG("connecting")
        apn = self.config.CELLULAR_DATA_APN

        # Disable RF
        self.modem.send_at("AT+CFUN=0", wait=3, await_all=["OK"])

        # Preferred Mode:
        # 2 Automatic
        # 13 GSM only
        # 38 LTE only
        # 51 GSM and LTE only
        self.modem.send_at("AT+CNMP=2", wait=2, await_all=["OK"])
        # Preferred Selection between CAT-M and NB-IoT:
        # 1 CAT-M
        # 2 NB-Iot
        # 3 CAT-M and NB-IoT
        self.modem.send_at("AT+CMNB=1", wait=2, await_all=["OK"])

        self.modem.send_at(f'AT+CGDCONT=1,"IP","{apn}"', wait=2, await_all=["OK"])
        self.modem.send_at(f'AT+CNCFG=0,1,"{apn}"', await_all=["OK"])

        if self.config.CELLULAR_DATA_USER:
            self.modem.send_at(
                f'AT+CNCFG=0,3,"{self.config.CELLULAR_DATA_USER}","{self.config.CELLULAR_DATA_PASSWORD}"',
                await_all=["OK"],
            )

        # enable RF
        self.modem.send_at("AT+CFUN=1", wait=3, await_all=["OK"])

        deadline = time.ticks_add(time.ticks_ms(), 60000)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            response = self.modem.send_at("AT+CEREG?")
            # <n> = 1 Enable network registration unsolicited result code
            # <stat>
            # 0 Not registered, MT is not currently searching an operator to
            #   register to.The GPRS service is disabled, the UE is allowed to attach
            #   for GPRS if requested by the user.
            # 1 Registered, home network.
            # 2 Not registered, but MT is currently trying to attach or searching an
            #   operator to register to. The GPRS service is enabled, but an allowable
            #   PLMN is currently not available. The UE will start a GPRS attach as
            #   soon as an allowable PLMN is available.
            # 3 Registration denied, The GPRS service is disabled, the UE is not
            #   allowed to attach for GPRS if it is requested by the user.
            # 4 Unknown
            # 5 Registered, roaming
            if "CEREG: 0,1" in response or "CEREG: 0,5" in response:
                break
        else:
            self.collect_registration_information()
            raise CellularDataError("network registration timed out")
        self.collect_registration_information()
        LOG("network registration successful")

        # activate network bearer
        self.modem.send_at("AT+CNACT=0,1", wait=5, await_all=["OK"])
        LOG("activating bearer successful")

        self._connected = True
        return True

    def post_json(self, url, payload):
        if not self._connected:
            self.connect()

        LOG("post json payload")

        secure, host, port, path = self._parse_url(url)
        conn_id = 0

        # allowed to fail if there is no connection with ID 0
        self.modem.send_at(f"AT+CACLOSE={conn_id}", await_any=["OK", "ERROR"])
        self.modem.send_at(f"AT+CACID={conn_id}", await_all=["OK"])

        if secure:
            self.modem.send_at('AT+CSSLCFG="sslversion",0,3', await_all=["OK"])
            self.modem.send_at(f"AT+CASSLCFG={conn_id},SSL,1", await_all=["OK"])
            self.modem.send_at('AT+CSSLCFG="ctxindex",0', await_all=["OK"])
            self.modem.send_at(f'AT+CSSLCFG="sni",0,"{host}"', await_all=["OK"])
            LOG("SSL configured")

        # async - CDNSGIP can arrive before OK
        # DNS resolving is also part of the next CAOPEN command, but the command here
        # allows to measure time.
        self.modem.send_at(f'AT+CDNSGIP="{host}"', wait=5, await_all=["CDNSGIP:", "OK"])
        LOG("DNS resolved")

        # <result>
        # 0 Success
        # 1 Socket error
        # 2 No memory
        # 3 Connection limit
        # 4 Parameter invalid
        # 6 Invalid IP address
        # 7 Not support the function
        # 12 Can’t bind the port
        # 13 Can’t listen the port
        # 20 Can’t resolv the host
        # 21 Network not active
        # 23 Remote refuse
        # 24 Certificate’s time expired
        # 25 Certificate’s common name does not match
        # 26 Certificate’s common name does not match and time expired
        # 27 Connect failed
        response = self.modem.send_at(
            f'AT+CAOPEN={conn_id},0,"TCP","{host}",{port}',
            wait=30,
            # async - CAOPEN can arrive before OK
            await_all=[f"+CAOPEN: {conn_id},", "OK"],
        )
        if f"+CAOPEN: {conn_id},0" in response:
            LOG("TCP connection opened")
        else:
            raise CellularDataError("CAOPEN failed")

        body = obfuscate_payload(serialize_payload(payload)).encode("utf-8")
        header_data = (
            f"POST {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"  # host_header
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode()
        self._send_http_chunk(conn_id, header_data)
        LOG("HTTP header sent")
        self._send_http_chunk(conn_id, body)
        LOG("HTTP body sent")

        deadline = time.ticks_add(time.ticks_ms(), 20000)
        received_bytes = 0
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            response = self.modem.send_at("AT+CARECV?")
            match = re.search(r"\+CARECV:\s*\d+,(\d+)", response)
            if match:
                received_bytes = int(match.group(1))
                if received_bytes > 0:
                    LOG("CARECV bytes received")
                    break
            LOG("CARECV no bytes received - trying again")
            # response = self.modem.send_at("AT+CASTATE?")
            # LOG(f"CASTATE {response=}")

        if received_bytes <= 0:
            LOG(f"{response=}")
            raise CellularDataError("no HTTP response received")

        self.modem.send_at(
            f"AT+CARECV={conn_id},{received_bytes}",
            wait=5,
            await_all=["HTTP/1.1 200", "OK"],
        )
        self.modem.send_at(f"AT+CACLOSE={conn_id}", await_all=["OK"])

    def disconnect(self):
        # it's ok to fail if the network is deactivated already
        self.modem.send_at("AT+CNACT=0,0", wait=3)
        self._connected = False
