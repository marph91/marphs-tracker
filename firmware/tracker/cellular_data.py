"""NB-IoT or LTE-M registration and HTTPS POST via SIM7080G AT commands."""

import re
import time

from logger import Logger, get_line

from tracker.modem import ModemError
from tracker.payload import obfuscate_payload, serialize_payload

LOG = Logger(__name__)


class CellularDataError(Exception):
    pass


def parse_cell_data(response):
    # AT+CPSI?\r\r\n+CPSI: LTE CAT-M1,Online,262-02,0xAAB4,8596225,147,EUTRAN-BAND20,6300,3,3,-16,-103,-74,7\r\n\r\nOK\r\n
    if "+CPSI: " not in response:
        return None

    data = response.split("+CPSI: ", 1)[1].split("\n", 1)[0]
    # <System Mode>
    # "NO SERVICE"
    # "GSM"
    # "LTE CAT-M1"
    # "LTE NB-IOT"
    if not data.startswith("LTE "):
        return None  # TODO: support GSM

    (
        _system_mode,
        _operation_mode,
        mcc_mnc,
        tracing_area_code,
        serving_cell_id,
        physical_cell_id,
        _frequency_band,
        _absolute_radio_frequency_channel_number,
        _dlbw,
        _ulbw,
        _rsrq,
        _rsrp,
        rssi,
        _rssn_r,
    ) = data.split(",")
    mobile_country_code, mobile_network_code = mcc_mnc.split("-", 1)

    # Format: https://ichnaea.readthedocs.io/en/latest/api/geolocate.html#cell-tower-fields
    return {
        "radioType": "lte",
        "mobileCountryCode": int(mobile_country_code),
        "mobileNetworkCode": int(mobile_network_code),
        "locationAreaCode": int(tracing_area_code, 16),
        "cellId": int(serving_cell_id),
        "psc": int(physical_cell_id),
        "signalStrength": int(rssi),
    }


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
        LOG("COPS - Operator Selection: {}".format(get_line(response, "+COPS:")))
        response = self.modem.send_at("AT+CPSI?", await_all=["OK"])
        LOG("CPSI - UE System Information: {}".format(get_line(response, "+CPSI:")))
        response = self.modem.send_at("AT+CSQ", await_all=["OK"])
        LOG("CSQ - Signal Quality Report: {}".format(get_line(response, "+CSQ:")))
        response = self.modem.send_at("AT+CEREG?", await_all=["OK"])
        LOG(
            "CEREG - EPS Network Registration Status: {}".format(
                get_line(response, "+CEREG:")
            )
        )

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
            LOG(
                "CEREG - EPS Network Registration Status: {}".format(
                    get_line(response, "+CEREG:")
                )
            )
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
        LOG("network registration successful")

        # activate network bearer
        self.modem.send_at("AT+CNACT=0,1", wait=5, await_all=["OK"])
        LOG("activating bearer successful")

        response = self.modem.send_at("AT+CNACT?", await_all=["OK"])
        LOG("CNACT - APP Network Active: {}".format(get_line(response, "+CNACT:")))
        response = self.modem.send_at("AT+CGPADDR", await_all=["OK"])
        LOG("CGPADDR - PDP Address: {}".format(get_line(response, "+CGPADDR:")))
        response = self.modem.send_at("AT+CASTATE?", await_all=["OK"])
        LOG(
            "CASTATE - TCP/UDP Connection State: {}".format(
                get_line(response, "+CASTATE:")
            )
        )

        self._connected = True
        return True

    def post_json(self, url, payload):
        if not self._connected:
            self.connect()

        # enrich the wifi data with cell data for better localization
        if "wifiAccessPoints" in payload:
            LOG("enrich wifi payload with cell data")
            response = self.modem.send_at("AT+CPSI?", await_all=["OK"])
            payload["cellTowers"] = [parse_cell_data(response)]

        LOG("post json payload")
        LOG(payload)

        secure, host, port, path = self._parse_url(url)
        conn_id = 0

        # allowed to fail if there is no connection with ID 0
        self.modem.send_at(f"AT+CACLOSE={conn_id}", await_any=["OK", "ERROR"])
        self.modem.send_at(f"AT+CACID={conn_id}", await_all=["OK"])

        # # debug: ping quad9 server before SSL layer
        # # AT+SNPING4=<URL>,<count>,<size>,<timeout>
        # self.modem.send_at(
        #     'AT+SNPING4="9.9.9.9",1,16,5000', wait=5, await_all=["SNPING4:", "OK"]
        # )
        # LOG("ping successful")

        if secure:
            # <sslversion>
            # 0 QAPI_NET_SSL_PROTOCOL_UNKNOWN
            # 1 QAPI_NET_SSL_PROTOCOL_TLS_1_0
            # 2 QAPI_NET_SSL_PROTOCOL_TLS_1_1
            # 3 QAPI_NET_SSL_PROTOCOL_TLS_1_2
            # 4 QAPI_NET_SSL_PROTOCOL_DTLS_1_0
            # 5 QAPI_NET_SSL_PROTOCOL_DTLS_1_2
            self.modem.send_at('AT+CSSLCFG="sslversion",0,3', await_all=["OK"])
            self.modem.send_at(f"AT+CASSLCFG={conn_id},SSL,1", await_all=["OK"])
            self.modem.send_at('AT+CSSLCFG="ctxindex",0', await_all=["OK"])
            # SNI = Server Name Indication
            self.modem.send_at(f'AT+CSSLCFG="sni",0,"{host}"', await_all=["OK"])
            LOG("SSL configured")

        # log some SSL parameters
        # response = self.modem.send_at("AT+CSSLCFG?", await_all=["OK"])
        # LOG(f"CSSLCFG - SSL Parameters of a Context Identifier: {response}")
        response = self.modem.send_at("AT+CASSLCFG?", await_all=["OK"])
        LOG(
            "CASSLCFG - SSL Certificate and Timeout Parameters: {}".format(
                get_line(response, "+CASSLCFG:")
            )
        )

        # async - CDNSGIP can arrive before OK
        # DNS resolving is also part of the next CAOPEN command, but the command here
        # allows to measure time.
        self.modem.send_at(f'AT+CDNSGIP="{host}"', wait=5, await_all=["CDNSGIP:", "OK"])
        LOG("DNS resolved")

        # check the modem time
        # timezone is in quarters - for example 08 means 2 hours offset
        response = self.modem.send_at("AT+CCLK?", await_all=["OK"])
        LOG("CCLK - Clock: {}".format(get_line(response, "+CCLK:")))
        if "80/01/06" in response:
            # TODO: NTP?
            approximate_time = "26/09/14,00:00:00+00"
            LOG(f"Modem time is wrong. Trying with {approximate_time=}.")
            self.modem.send_at(f'AT+CCLK="{approximate_time}"', await_all=["OK"])

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
        try:
            response = self.modem.send_at(
                f'AT+CAOPEN={conn_id},0,"TCP","{host}",{port}',
                wait=30,  # TinyGSM waits for 75 s by default
                # async - CAOPEN can arrive before OK
                await_all=[f"+CAOPEN: {conn_id},", "OK"],
            )
        except ModemError:
            LOG(
                "CAOPEN - Open a TCP/UDP Connection: {}".format(
                    get_line(response, "+CAOPEN:")
                )
            )
            response = self.modem.send_at("AT+CASTATE?", await_all=["OK"])
            LOG(
                "CASTATE - TCP/UDP Connection State: {}".format(
                    get_line(response, "+CASTATE:")
                )
            )
            raise
        if f"+CAOPEN: {conn_id},0" in response:
            LOG("TCP connection opened")
        else:
            LOG(
                "CAOPEN - Open a TCP/UDP Connection: {}".format(
                    get_line(response, "+CAOPEN:")
                )
            )
            response = self.modem.send_at("AT+CASTATE?", await_all=["OK"])
            LOG(
                "CASTATE - TCP/UDP Connection State: {}".format(
                    get_line(response, "+CASTATE:")
                )
            )
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
            LOG(
                "CARECV - Receive Data via an Established Connection: {}".format(
                    get_line(response, "+CARECV:")
                )
            )
            match = re.search(r"\+CARECV:\s*\d+,(\d+)", response)
            if match:
                received_bytes = int(match.group(1))
                if received_bytes > 0:
                    LOG("CARECV bytes received")
                    break
            # response = self.modem.send_at("AT+CASTATE?")
            # LOG(f"CASTATE {response=}")

        if received_bytes <= 0:
            LOG(f"{response=}")
            raise CellularDataError("no HTTP response received")

        self.modem.send_at(
            f"AT+CARECV={conn_id},{received_bytes}", wait=5, await_all=["HTTP/1.1 200"]
        )

        # TODO: The modem can only read 1460 bytes at a time.
        # Read everything properly instead only the first chunk.
        # response = self.modem.send_at("AT+CARECV?")
        # LOG(f"{response=}")

        # TODO: await_all=["OK"] fails sometimes. Probably because of the previous command.
        self.modem.send_at(f"AT+CACLOSE={conn_id}")

    def disconnect(self):
        # it's ok to fail if the network is deactivated already
        self.modem.send_at("AT+CNACT=0,0")
        self._connected = False
