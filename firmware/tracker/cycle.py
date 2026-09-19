"""Tracker wake cycle orchestration."""

import logger

from tracker.wifi_scan import home_ssid_present, top_aps

LOG = logger.Logger(__name__)


# TODO: replace with enum when available:
# https://github.com/micropython/micropython/issues/8545
class CycleState:
    NONE = "NONE"
    PMU_INIT_FAILED = "PMU_INIT_FAILED"
    HOME = "HOME"
    MODEM_POWER_ON_FAILED = "MODEM_POWER_ON_FAILED"
    SIM_NOT_READY = "SIM_NOT_READY"
    NO_FIX = "NO_FIX"
    POST_FAILED = "POST_FAILED"
    CONFIG_ERROR = "CONFIG_ERROR"
    SLEEP_PREPARATION_FAILED = "SLEEP_PREPARATION_FAILED"
    FINISHED = "FINISHED"


def prepare_for_sleep(pmu, modem):
    # based on:
    # - https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G-MicroPython/blob/377b15a71fde63463ef67a450856571dc5516a8a/examples/MinimalModemAndEspSleep/MinimalModemAndEspSleep.py
    # - https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G/issues/168

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


def run_cycle(config, hw_functions):
    """
    Execute one tracker cycle.

    hw_functions are the functions that actually need access to the hardware.
    Pass them here to allow native tests with mocks.
    hw_functions must provide:
        pmu, modem,
        scan_wifi, gnss, cellular_data, sleep, log
    """
    if not hw_functions["pmu"].begin():
        return CycleState.PMU_INIT_FAILED

    # WiFi scan runs before modem power-on so home detection avoids cellular data.
    results = hw_functions["scan_wifi"]()

    battery_percent = hw_functions["pmu"].get_battery_percent()
    if battery_percent != -1:
        LOG(f"{battery_percent=}")

    home_ssid = home_ssid_present(results, config.HOME_SSIDS)
    if home_ssid:
        # send heartbeat if configured
        home_password = config.HOME_PASSWORDS[config.HOME_SSIDS.index(home_ssid)]
        if home_password:
            hw_functions["send_heartbeat"](
                home_ssid, home_password, config.TARGET_URL, battery_percent
            )
        return CycleState.HOME

    hw_functions["pmu"].enable_modem()
    if not hw_functions["modem"].power_on():
        return CycleState.MODEM_POWER_ON_FAILED

    if not hw_functions["modem"].check_sim():
        return CycleState.SIM_NOT_READY

    payload = {"batt": battery_percent}
    # TODO: Include timestamp here already?
    # seconds_since_2000 = hw_functions["modem"].get_time()

    if len(results) >= config.WIFI_MIN_APS:
        access_points = top_aps(results, config.WIFI_TOP_N)
        payload["wifiAccessPoints"] = list(access_points)
        LOG(f"using wifi path with {len(access_points)} APs")
    else:
        LOG(f"fewer than {config.WIFI_MIN_APS} APs, using GNSS path")
        hw_functions["pmu"].enable_gnss_antenna()
        if not hw_functions["gnss"].enable():
            return CycleState.NO_FIX

        try:
            hw_functions["gnss"].config()
            gnss_fix = hw_functions["gnss"].get_fix(config.GNSS_FIX_TIMEOUT_S)
        except Exception as exc:  # noqa: BLE001  # want to catch all exceptions
            LOG(f"{exc}")
            return CycleState.NO_FIX
        finally:
            hw_functions["gnss"].disable()

        if not gnss_fix:
            return CycleState.NO_FIX

        payload["gnss"] = gnss_fix

    try:
        hw_functions["cellular_data"].connect()
        hw_functions["cellular_data"].post_json(config.TARGET_URL, payload)
    except Exception as exc:  # noqa: BLE001  # want to catch all exceptions
        LOG(f"{exc}")
        return CycleState.POST_FAILED if payload else CycleState.CONFIG_ERROR
    finally:
        hw_functions["cellular_data"].disconnect()

    try:
        prepare_for_sleep(hw_functions["pmu"], hw_functions["modem"])
    except Exception as exc:  # noqa: BLE001  # want to catch all exceptions
        LOG(f"{exc}")
        return CycleState.SLEEP_PREPARATION_FAILED

    return CycleState.FINISHED
