"""Tracker wake cycle orchestration."""

import logger

from tracker.payload import build_gnss_payload, build_wifi_payload
from tracker.wifi_scan import home_ssid_present, top_aps

LOG = logger.Logger(__name__)


# TODO: replace with enum when available:
# https://github.com/micropython/micropython/issues/8545
class CycleState:
    PMU_INIT_FAILED = 0
    HOME = 1
    MODEM_POWER_ON_FAILED = 2
    SIM_NOT_READY = 3
    NO_FIX = 6
    POST_FAILED = 7
    CONFIG_ERROR = 8
    FINISHED = 9


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

    if home_ssid_present(results, config.HOME_SSIDS):
        return CycleState.HOME

    if not hw_functions["modem"].power_on():
        return CycleState.MODEM_POWER_ON_FAILED

    if not hw_functions["modem"].check_sim():
        return CycleState.SIM_NOT_READY

    payload = None
    battery_percent = hw_functions["pmu"].get_battery_percent()
    # TODO: Include timestamp here already?
    # seconds_since_2000 = hw_functions["modem"].get_time()

    if len(results) >= config.WIFI_MIN_APS:
        access_points = top_aps(results, config.WIFI_TOP_N)
        payload = build_wifi_payload(access_points, battery_percent)
        LOG(f"using wifi path with {len(access_points)} APs")
    else:
        LOG(f"fewer than {config.WIFI_MIN_APS} APs, using GNSS path")
        if not hw_functions["gnss"].enable():
            return CycleState.NO_FIX

        try:
            hw_functions["gnss"].config()
            fix = hw_functions["gnss"].get_fix(config.GNSS_FIX_TIMEOUT_S)
        finally:
            hw_functions["gnss"].disable()

        if not fix:
            return CycleState.NO_FIX

        payload = build_gnss_payload(fix["lat"], fix["lon"], battery_percent)
    LOG(f"{battery_percent=}")

    try:
        hw_functions["cellular_data"].connect()
        hw_functions["cellular_data"].post_json(config.NTFY_URL, payload)
    except Exception as exc:  # noqa: BLE001  # want to catch all exceptions
        LOG(f"{exc}")
        return CycleState.POST_FAILED if payload else CycleState.CONFIG_ERROR
    finally:
        hw_functions["cellular_data"].disconnect()

    return CycleState.FINISHED
