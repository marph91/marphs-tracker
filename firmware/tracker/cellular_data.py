"""NB-IoT or LTE-M registration and HTTPS POST via SIM7080G AT commands."""

import re
import time

from tracker.payload import obfuscate_payload, serialize_payload


class CellularDataError(Exception):
    pass


class CellularDataClient:
    """Configure cellular data bearer and send HTTPS POST requests."""

    def __init__(self, modem, config):
        self.modem = modem
        self.config = config
        self._connected = False

    def _send_http_chunk(self, conn_id, data):
        # TODO: https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G/issues/96#issuecomment-2586446251
        # print("[CELLULAR] chunk:", data)
        self.modem.send_at(f"AT+CASEND={conn_id},{len(data)}", wait=5, await_string=">")
        self.modem.send_at(data, wait=5, await_string="OK")

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

    def connect(self):
        apn = self.config.CELLULAR_DATA_APN

        # Disable RF
        self.modem.send_at("AT+CFUN=0", wait=3, await_string="OK")

        # Preferred Mode:
        # 2 Automatic
        # 13 GSM only
        # 38 LTE only
        # 51 GSM and LTE only
        self.modem.send_at("AT+CNMP=2", wait=2, await_string="OK")
        # Preferred Selection between CAT-M and NB-IoT:
        # 1 CAT-M
        # 2 NB-Iot
        # 3 CAT-M and NB-IoT
        self.modem.send_at("AT+CMNB=1", wait=2, await_string="OK")

        self.modem.send_at(f'AT+CGDCONT=1,"IP","{apn}"', wait=2, await_string="OK")
        self.modem.send_at(f'AT+CNCFG=0,1,"{apn}"', await_string="OK")

        if self.config.CELLULAR_DATA_USER:
            self.modem.send_at(
                f'AT+CNCFG=0,3,"{self.config.CELLULAR_DATA_USER}","{self.config.CELLULAR_DATA_PASSWORD}"',
                await_string="OK",
            )

        # enable RF
        self.modem.send_at("AT+CFUN=1", wait=3, await_string="OK")

        deadline = time.ticks_add(time.ticks_ms(), 60000)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            response = self.modem.send_at("AT+CEREG?", await_string="OK")
            # <n> = 1 Enable network registration unsolicited result code
            # <stat>
            # 1 Registered, home network
            # 5 Registered, roaming
            if "CEREG: 0,1" in response or "CEREG: 0,5" in response:
                break
        else:
            print(f"[CELLULAR] {response}")
            raise CellularDataError("network registration timed out")
        print("[CELLULAR] network registration successful")

        # activate network bearer
        self.modem.send_at("AT+CNACT=0,1", wait=5, await_string="OK")

        self._connected = True
        return True

    def post_json(self, url, payload):
        if not self._connected:
            self.connect()

        secure, host, port, path = self._parse_url(url)
        body = obfuscate_payload(serialize_payload(payload))
        conn_id = 0

        # allowed to fail if there is no connection with ID 0
        self.modem.send_at(f"AT+CACLOSE={conn_id}", await_string=["OK", "ERROR"])
        self.modem.send_at(f"AT+CACID={conn_id}", await_string="OK")

        if secure:
            self.modem.send_at('AT+CSSLCFG="sslversion",0,3', await_string="OK")
            self.modem.send_at(f"AT+CASSLCFG={conn_id},SSL,1", await_string="OK")
            self.modem.send_at('AT+CSSLCFG="ctxindex",0', await_string="OK")
            self.modem.send_at(f'AT+CSSLCFG="sni",0,"{host}"', await_string="OK")
            print("[CELLULAR] SSL configured")

        self.modem.send_at(
            f'AT+CAOPEN={conn_id},0,"TCP","{host}",{port}',
            wait=20,
            await_string="OK",
        )
        print("[CELLULAR] TCP connection opened")

        header_data = (
            f"POST {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"  # host_header
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        self._send_http_chunk(conn_id, header_data)
        print("[CELLULAR] HTTP header sent")
        self._send_http_chunk(conn_id, body)
        print("[CELLULAR] HTTP body sent")

        deadline = time.ticks_add(time.ticks_ms(), 60000)
        received_bytes = 0
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            response = self.modem.send_at("AT+CARECV?", await_string="OK")
            match = re.search(r"\+CARECV:\s*\d+,(\d+)", response)
            if match:
                received_bytes = int(match.group(1))
                if received_bytes > 0:
                    break

        if received_bytes <= 0:
            print(f"[CELLULAR] {response}")
            raise CellularDataError("no HTTP response received")

        self.modem.send_at(
            f"AT+CARECV={conn_id},{received_bytes}",
            wait=5,
            await_string="HTTP/1.1 200 OK",
        )
        self.modem.send_at(f"AT+CACLOSE={conn_id}", await_string="OK")

    def disconnect(self):
        # it's ok to fail if the network is deactivated already
        self.modem.send_at("AT+CNACT=0,0", wait=3)
        self._connected = False
