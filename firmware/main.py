"""Boot entry: run one tracker cycle then deep sleep."""

import time

import config
import logger
import machine
from tracker.cellular_data import CellularDataClient
from tracker.cycle import CycleState, run_cycle
from tracker.gnss import GnssReader
from tracker.modem import AtModem
from tracker.pmu import PmuController
from tracker.wifi_scan import scan_wifi

LOG = logger.Logger(__name__.strip("_"))


def sleep(time_ms, pmu, modem):
    # based on:
    # - https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G-MicroPython/blob/377b15a71fde63463ef67a450856571dc5516a8a/examples/MinimalModemAndEspSleep/MinimalModemAndEspSleep.py
    # - https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G/issues/168

    # This is not necessary, since the MicroPico VSCode extension opens always
    # the prompt instead of executing main.py.
    # if pmu.is_usb_connected():
    #     # prevent boot loop to allow debugging
    #     LOG("Don't go to sleep, since USB is connected.")
    #     return

    modem.power_off()
    pmu.power_down_for_sleep()

    # TODO: needed?
    # -------------------------------------------------------------
    # Put unused GPIOs into low-power states
    # -------------------------------------------------------------
    # def input_pin(pin):
    #     machine.Pin(pin, machine.Pin.IN)

    # def pulldown_pin(pin):
    #     machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)

    # # I2C
    # input_pin(utilities.I2C_SDA)
    # input_pin(utilities.I2C_SCL)

    # # SD card
    # input_pin(38)  # SDMMC_CLK
    # input_pin(39)  # SDMMC_CMD
    # input_pin(40)  # SDMMC_DATA

    # # LEDs / miscellaneous inputs
    # pulldown_pin(8)
    # pulldown_pin(9)
    # pulldown_pin(10)

    # # User/application inputs
    # pulldown_pin(11)
    # pulldown_pin(12)

    # # PWM
    # pulldown_pin(14)

    # # PN532 reset
    # pulldown_pin(16)

    # # Camera / unused pins
    # pulldown_pin(1)
    # pulldown_pin(2)

    # pulldown_pin(21)
    # pulldown_pin(45)
    # pulldown_pin(46)
    # pulldown_pin(47)
    # pulldown_pin(48)

    # -------------------------------------------------------------
    # UARTs
    # -------------------------------------------------------------
    # Stop modem UART
    modem.uart.deinit()

    # UART2/NFC is not used here.
    # uart2.deinit()

    # -------------------------------------------------------------
    # ESP32 deep sleep
    # -------------------------------------------------------------
    LOG(f"Going to sleep for {time_ms / 1000} seconds")
    machine.deepsleep(time_ms)


def main():
    LOG("Starting main script")

    pmu = PmuController()
    modem = AtModem()
    hw_functions = {
        "pmu": pmu,
        "modem": modem,
        "scan_wifi": scan_wifi,
        "gnss": GnssReader(pmu, modem),
        "cellular_data": CellularDataClient(modem, config),
    }

    start_time_ms = time.ticks_ms()
    cycle_state = run_cycle(config, hw_functions)
    elapsed_time_ms = time.ticks_diff(time.ticks_ms(), start_time_ms)
    LOG(f"{cycle_state=}")
    LOG(f"Cycle time: {elapsed_time_ms / 1000} s")

    # sleep some time depending on the state
    sleep_minutes = (
        config.SLEEP_MINUTES_HOME
        if cycle_state == CycleState.HOME
        else config.SLEEP_MINUTES_AWAY
    )
    sleep(int(sleep_minutes) * 60 * 1000, pmu, modem)


if __name__ == "__main__":
    main()
