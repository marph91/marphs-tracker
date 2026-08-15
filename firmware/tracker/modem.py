"""SIM7080G modem AT command layer."""

import time

import utilities
from machine import UART, Pin


class AtModem:
    """UART AT interface for the SIM7080G modem."""

    def __init__(self, uart=None):
        self.uart = uart or UART(
            1,
            baudrate=115200,
            tx=utilities.BOARD_MODEM_TXD_PIN,
            rx=utilities.BOARD_MODEM_RXD_PIN,
        )
        self._pwr = Pin(utilities.BOARD_MODEM_PWR_PIN, Pin.OUT)
        self._dtr = Pin(utilities.BOARD_MODEM_DTR_PIN, Pin.OUT)
        self._dtr.value(0)
        self._started = False

    def send_at(self, command, wait=1):
        if command:
            self.uart.write(command + "\r\n")
        time.sleep(wait)
        response = self.uart.read()
        if not response:
            return ""
        if isinstance(response, bytes):
            try:
                return response.decode("utf-8", "ignore").strip()
            except Exception:  # noqa: BLE001  # want to catch all exceptions
                return ""
        return str(response).strip()

    def wait_for_ok(self, retries=10, delay_s=1):
        for _ in range(retries):
            response = self.send_at("AT", wait=delay_s)
            if "OK" in response:
                return True
        return False

    def power_on(self):
        if self._started:
            return True

        retry = 0
        while retry <= 10:
            if self.wait_for_ok(retries=1, delay_s=1):
                self._started = True
                return True
            print(".", end="")
            retry += 1
            if retry > 10:
                self._pwr.value(0)
                time.sleep(0.1)
                self._pwr.value(1)
                time.sleep(1)
                self._pwr.value(0)
                retry = 0
                print("Retry start modem.")

        return False

    def check_sim(self, timeout_s=30):
        deadline = time.ticks_add(time.ticks_ms(), timeout_s * 1000)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            response = self.send_at("AT+CPIN?", wait=2)
            if "READY" in response:
                return True
            time.sleep(3)
        return False

    def power_off(self):
        self.send_at("AT+CPOWD=1", wait=3)
        self._started = False
