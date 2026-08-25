"""SIM7080G modem AT command layer."""

import time

import logger
import utilities
from machine import UART, Pin

LOG = logger.Logger(__name__)


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

    def send_at(self, command, wait=1, await_any=None, await_all=None):
        if command:
            self.uart.write(command + "\r\n")

        if await_any is not None or await_all is not None:
            response = ""
            deadline = time.ticks_add(time.ticks_ms(), wait * 1000)
            while time.ticks_diff(deadline, time.ticks_ms()) > 0:
                partial_response = self.uart.read()
                if partial_response:
                    response += partial_response.decode("utf-8", "ignore")
                    # only consider complete lines
                    complete_lines = "".join(
                        line
                        for line in response.splitlines(keepends=True)
                        if line.endswith("\r\n")
                    )
                    if (
                        await_any
                        and any(string in complete_lines for string in await_any)
                        or await_all
                        and all(string in complete_lines for string in await_all)
                    ):
                        return response
                time.sleep(0.1)
            raise ModemError(
                f"await timeout, {command=}, {response=}, {await_any=}, {await_all=}"
            )

        time.sleep(wait)
        response = self.uart.read()
        if not response:
            return ""
        return response.decode("utf-8", "ignore")

    def power_on(self):
        if self._started:
            return True

        LOG("Power on")
        retry = 0
        while retry <= 10:
            if self.send_at("AT"):
                response = self.send_at("AT+CGMR", await_all=["OK"])
                LOG(
                    f"CGMR - TA Revision Identification of Software Release: {response.splitlines()[2]}"
                )
                self._started = True
                return True
            retry += 1
            LOG(f"{retry=}")
            if retry > 10:
                self._pwr.value(0)
                time.sleep(0.1)
                self._pwr.value(1)
                time.sleep(1)
                self._pwr.value(0)
                retry = 0
                LOG("Retry start")

        LOG("power on failed")
        return False

    def check_sim(self):
        for _ in range(3):
            try:
                response = self.send_at(
                    "AT+CPIN?", wait=5, await_all=["CPIN: READY", "OK"]
                )
                return True
            except ModemError:
                LOG("SIM not ready. Trying again")
        LOG(f"CPIN {response=}")
        return False

    def power_off(self):
        LOG("Powering off SIM7080G and modem network LED")
        # it's ok to fail if the LED is off already
        self.send_at("AT+CNETLIGHT=0")
        # it's ok to fail if the modem is off already
        self.send_at("AT+CPOWD=1")
        self._started = False
