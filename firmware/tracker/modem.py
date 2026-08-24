"""SIM7080G modem AT command layer."""

import time

import utilities
from machine import UART, Pin


class ModemError(Exception):
    pass


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

    def send_at(self, command, wait=1, await_string=""):
        if command:
            self.uart.write(command + "\r\n")

        if await_string:
            if isinstance(await_string, str):
                await_string = [await_string]
            response = ""
            deadline = time.ticks_add(time.ticks_ms(), wait * 1000)
            while time.ticks_diff(deadline, time.ticks_ms()) > 0:
                partial_response = self.uart.read()
                if partial_response:
                    response += partial_response.decode("utf-8", "ignore")
                    if any(string in response for string in await_string):
                        return response
                time.sleep(0.1)
            raise ModemError(
                f"await_string timeout, {command=}, {response=}, {await_string=}"
            )

        time.sleep(wait)
        response = self.uart.read()
        if not response:
            return ""
        return response.decode("utf-8", "ignore")

    def power_on(self):
        if self._started:
            return True

        print("Power modem")
        retry = 0
        while retry <= 10:
            if self.send_at("AT"):
                self._started = True
                return True
            retry += 1
            print(f"{retry=}")
            if retry > 10:
                self._pwr.value(0)
                time.sleep(0.1)
                self._pwr.value(1)
                time.sleep(1)
                self._pwr.value(0)
                retry = 0
                print("Retry start modem")

        print("modem power on failed")
        return False

    def check_sim(self):
        try:
            self.send_at("AT+CPIN?", wait=30, await_string="CPIN: READY")
            return True
        except ModemError as exc:
            print(exc)
            return False

    def power_off(self):
        print("Powering off SIM7080G and modem network LED")
        # it's ok to fail if the LED is off already
        self.send_at("AT+CNETLIGHT=0")
        # it's ok to fail if the modem is off already
        self.send_at("AT+CPOWD=1")
        self._started = False
