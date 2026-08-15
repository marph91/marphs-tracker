"""NB-IoT registration and HTTPS POST via SIM7080G AT commands."""

import re
import time

from tracker.payload import serialize_payload


class NbiotError(Exception):
    pass


class NbiotClient:
    """Configure NB-IoT bearer and send HTTPS POST requests."""

    def __init__(self, modem, config):
        self.modem = modem
        self.config = config
        self._connected = False

    def _send_http_chunk(self, conn_id, data):
        response = self.modem.send_at(f"AT+CASEND={conn_id},{len(data)}", wait=2)
        if ">" not in response and "OK" not in response and "DOWNLOAD" not in response:
            return False
        self.modem.uart.write(data)
        if not data.endswith("\r\n"):
            self.modem.uart.write("\r\n")
        time.sleep(2)
        self.modem.send_at("", wait=1)
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
        if "OK" not in response:
            raise NbiotError("failed to disable RF")

        self.modem.send_at("AT+CNMP=38", wait=2)
        self.modem.send_at("AT+CMNB=2", wait=2)

        if self.config.NBIOT_BANDS:
            self.modem.send_at(
                f'AT+CBANDCFG="NB-IoT",{self.config.NBIOT_BANDS}', wait=2
            )

        if self.config.NBIOT_OPERATOR:
            self.modem.send_at(
                f'AT+COPS=0,0,"{self.config.NBIOT_OPERATOR}",9',
                wait=3,
            )

        response = self.modem.send_at(f'AT+CGDCONT=1,"IP","{apn}"', wait=2)
        if "OK" not in response:
            raise NbiotError("failed to set CGDCONT APN")

        response = self.modem.send_at(f'AT+CNCFG=0,1,"{apn}"', wait=2)
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
            if "OK" not in response:
                raise NbiotError("failed to set NB-IoT credentials")

        response = self.modem.send_at("AT+CFUN=1", wait=3)
        if "OK" not in response:
            raise NbiotError("failed to enable RF")

        deadline = time.ticks_add(time.ticks_ms(), 180000)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            response = self.modem.send_at("AT+CEREG?", wait=2)
            match = re.search(r"\+CEREG:\s*\d+,(\d+)", response)
            if match and int(match.group(1)) in (1, 5):
                break
            time.sleep(3)
        else:
            raise NbiotError("network registration timed out")

        response = self.modem.send_at("AT+CNACT=0,1", wait=5)
        if "OK" not in response:
            raise NbiotError("failed to activate network bearer")

        self._connected = True
        return True

    def post_json(self, url, payload):
        if not self._connected:
            self.connect()

        secure, host, port, path = self._parse_url(url)
        body = serialize_payload(payload)
        conn_id = 0

        self.modem.send_at(f"AT+CACLOSE={conn_id}", wait=2)
        self.modem.send_at(f"AT+CACID={conn_id}", wait=1)

        if secure:
            self.modem.send_at('AT+CSSLCFG="sslversion",0,3', wait=1)
            self.modem.send_at(f"AT+CASSLCFG={conn_id},SSL,1", wait=1)
            self.modem.send_at('AT+CSSLCFG="ctxindex",0', wait=1)
            self.modem.send_at(f'AT+CSSLCFG="sni",0,"{host}"', wait=2)

        response = self.modem.send_at(
            f'AT+CAOPEN={conn_id},0,"TCP","{host}",{port}',
            wait=8,
        )
        if "OK" not in response and "+CAOPEN" not in response:
            raise NbiotError("failed to open HTTPS connection")

        request_line = f"POST {path} HTTP/1.1"
        host_header = f"Host: {host}"
        content_type = "Content-Type: application/json"
        content_length = f"Content-Length: {len(body)}"
        connection = "Connection: close"

        for chunk in (
            request_line,
            host_header,
            content_type,
            content_length,
            connection,
            "",
        ):
            if not self._send_http_chunk(conn_id, chunk):
                raise NbiotError("failed to send HTTP headers")

        if not self._send_http_chunk(conn_id, body):
            raise NbiotError("failed to send HTTP body")

        deadline = time.ticks_add(time.ticks_ms(), 60000)
        received = 0
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            response = self.modem.send_at("AT+CARECV?", wait=2)
            match = re.search(r"\+CARECV:\s*\d+,(\d+)", response)
            if match:
                received = int(match.group(1))
                if received > 0:
                    break
            time.sleep(2)

        if received <= 0:
            raise NbiotError("no HTTP response received")

        response = self.modem.send_at(f"AT+CARECV={conn_id},{received}", wait=5)
        self.modem.send_at(f"AT+CACLOSE={conn_id}", wait=2)

        if (
            " 200 " not in response
            and " 201 " not in response
            and " 204 " not in response
        ):
            raise NbiotError(f"HTTP POST failed: {response[:200]}")

        return response

    def disconnect(self):
        self.modem.send_at("AT+CNACT=0,0", wait=3)
        self._connected = False
