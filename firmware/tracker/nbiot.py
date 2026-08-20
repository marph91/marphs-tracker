"""NB-IoT registration and HTTPS POST via SIM7080G AT commands."""

import re
import time

from tracker.payload import obfuscate_payload, serialize_payload


class NbiotError(Exception):
    pass


class NbiotClient:
    """Configure NB-IoT bearer and send HTTPS POST requests."""

    def __init__(self, modem, config, log=print):
        self.modem = modem
        self.config = config
        self._connected = False
        self.log = log

    def _send_http_chunk(self, conn_id, data):
        self.log("chunk:", data)
        response = self.modem.send_at(f"AT+CASEND={conn_id},{len(data)}", wait=2)
        self.log(response)
        if ">" not in response and "OK" not in response and "DOWNLOAD" not in response:
            return False
        self.modem.uart.write(data)
        time.sleep(2)
        response = self.modem.send_at("", wait=1)
        self.log(response)
        return True

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
        apn = self.config.NBIOT_APN

        response = self.modem.send_at("AT+CFUN=0", wait=3)
        self.log(response)
        if "OK" not in response:
            raise NbiotError("failed to disable RF")

        response = self.modem.send_at("AT+CNMP=2", wait=2)  # automatic
        self.log(response)
        response = self.modem.send_at("AT+CMNB=3", wait=2)  # CAT-M and NB-IoT
        self.log(response)

        if self.config.NBIOT_BANDS:
            response = self.modem.send_at(
                f'AT+CBANDCFG="NB-IoT",{self.config.NBIOT_BANDS}', wait=2
            )
            self.log(response)

        if self.config.NBIOT_OPERATOR:
            response = self.modem.send_at(
                f'AT+COPS=0,0,"{self.config.NBIOT_OPERATOR}",9',
                wait=3,
            )
            self.log(response)

        response = self.modem.send_at(f'AT+CGDCONT=1,"IP","{apn}"', wait=2)
        self.log(response)
        if "OK" not in response:
            raise NbiotError("failed to set CGDCONT APN")

        response = self.modem.send_at(f'AT+CNCFG=0,1,"{apn}"', wait=2)
        self.log(response)
        if "OK" not in response:
            raise NbiotError("failed to set CNCFG APN")

        if self.config.NBIOT_USER:
            response = self.modem.send_at(
                'AT+CNCFG=0,3,"{}","{}"'.format(
                    self.config.NBIOT_USER,
                    self.config.NBIOT_PASSWORD or "",
                ),
                wait=2,
            )
            self.log(response)
            if "OK" not in response:
                raise NbiotError("failed to set NB-IoT credentials")

        response = self.modem.send_at("AT+CFUN=1", wait=3)
        self.log(response)
        if "OK" not in response:
            raise NbiotError("failed to enable RF")

        deadline = time.ticks_add(time.ticks_ms(), 180000)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            response = self.modem.send_at("AT+CEREG?", wait=2)
            self.log(response)
            match = re.search(r"\+CEREG:\s*\d+,(\d+)", response)
            if match and int(match.group(1)) in (1, 5):
                break
            time.sleep(3)
        else:
            raise NbiotError("network registration timed out")
        self.log("NB IOT: network registration successful")

        response = self.modem.send_at("AT+CNACT=0,1", wait=5)
        self.log(response)
        if "OK" not in response:
            raise NbiotError("failed to activate network bearer")

        self._connected = True
        return True

    def post_json(self, url, payload):
        if not self._connected:
            self.connect()

        secure, host, port, path = self._parse_url(url)
        body = obfuscate_payload(serialize_payload(payload))
        conn_id = 0

        response = self.modem.send_at(f"AT+CACLOSE={conn_id}", wait=2)
        self.log(response)
        response = self.modem.send_at(f"AT+CACID={conn_id}", wait=1)
        self.log(response)

        if secure:
            response = self.modem.send_at('AT+CSSLCFG="sslversion",0,3', wait=1)
            self.log(response)
            response = self.modem.send_at(f"AT+CASSLCFG={conn_id},SSL,1", wait=1)
            self.log(response)
            response = self.modem.send_at('AT+CSSLCFG="ctxindex",0', wait=1)
            self.log(response)
            response = self.modem.send_at(f'AT+CSSLCFG="sni",0,"{host}"', wait=2)
            self.log(response)

        response = self.modem.send_at(
            f'AT+CAOPEN={conn_id},0,"TCP","{host}",{port}',
            wait=8,
        )
        self.log(response)
        if "OK" not in response and "+CAOPEN" not in response:
            raise NbiotError("failed to open HTTPS connection")

        header_data = (
            f"POST {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"  # host_header
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        if not self._send_http_chunk(conn_id, header_data):
            raise NbiotError("failed to send HTTP headers")
        # TODO: https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G/issues/96#issuecomment-2586446251

        if not self._send_http_chunk(conn_id, body):
            raise NbiotError("failed to send HTTP body")

        deadline = time.ticks_add(time.ticks_ms(), 60000)
        received = 0
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            response = self.modem.send_at("AT+CARECV?", wait=2)
            self.log(response)
            match = re.search(r"\+CARECV:\s*\d+,(\d+)", response)
            if match:
                received = int(match.group(1))
                if received > 0:
                    break
            time.sleep(2)

        if received <= 0:
            raise NbiotError("no HTTP response received")

        response_carecv = self.modem.send_at(f"AT+CARECV={conn_id},{received}", wait=5)
        self.log(response_carecv)
        response = self.modem.send_at(f"AT+CACLOSE={conn_id}", wait=2)
        self.log(response)

        if (
            " 200 " not in response_carecv
            and " 201 " not in response_carecv
            and " 204 " not in response_carecv
        ):
            raise NbiotError(f"HTTP POST failed: {response_carecv[:200]}")

        return response_carecv

    def disconnect(self):
        response = self.modem.send_at("AT+CNACT=0,0", wait=3)
        self.log(response)
        self._connected = False
