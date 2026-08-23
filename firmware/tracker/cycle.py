"""Tracker wake cycle orchestration."""

from tracker.payload import build_gps_payload, build_wifi_payload
from tracker.wifi_scan import home_ssid_present, top_aps


# TODO: replace with enum when available:
# https://github.com/micropython/micropython/issues/8545
class CycleState:
    PMU_INIT_FAILED = 0
    HOME = 1
    MODEM_POWER_ON_FAILED = 2
    SIM_NOT_READY = 3
    WIFI_SENT = 4
    GPS_SENT = 5
    NO_FIX = 6
    POST_FAILED = 7
    CONFIG_ERROR = 8


def run_cycle(config, hw_functions):
    """
    Execute one tracker cycle.

    hw_functions are the functions that actually need access to the hardware.
    Pass them here to allow native tests with mocks.
    hw_functions must provide:
        pmu, modem,
        scan_wifi, gps, cellular_data, sleep, log
    """
    log = hw_functions.get("log", print)

    if not hw_functions["pmu"].begin():
        log("PMU init failed")
        return CycleState.PMU_INIT_FAILED

    # WiFi scan runs before modem power-on so home detection avoids cellular data.
    results = hw_functions["scan_wifi"]()
    log(f"wifi scan found {len(results)} APs")

    if home_ssid_present(results, config.HOME_SSIDS):
        log("home SSID detected, skipping transmit")
        return CycleState.HOME

    if not hw_functions["modem"].power_on():
        log("modem power on failed")
        return CycleState.MODEM_POWER_ON_FAILED

    if not hw_functions["modem"].check_sim():
        log("SIM not ready")
        return CycleState.SIM_NOT_READY

    payload = None
    outcome = None
    battery_percent = hw_functions["pmu"].get_battery_percent()

    if len(results) >= config.WIFI_MIN_APS:
        access_points = top_aps(results, config.WIFI_TOP_N)
        payload = build_wifi_payload(access_points, battery_percent)
        outcome = CycleState.WIFI_SENT
        log(f"using wifi path with {len(access_points)} APs")
    else:
        log(f"fewer than {config.WIFI_MIN_APS} APs, using GPS path")
        if not hw_functions["gps"].enable():
            log("failed to enable GPS")
            return CycleState.NO_FIX

        try:
            hw_functions["gps"].config()
            fix = hw_functions["gps"].get_fix(config.GPS_FIX_TIMEOUT_S)
        finally:
            hw_functions["gps"].disable()

        if not fix:
            log("GPS fix timeout")
            return CycleState.NO_FIX

        payload = build_gps_payload(fix["lat"], fix["lon"], battery_percent)
        outcome = CycleState.GPS_SENT
        log(f"GPS fix acquired: {fix['lat']}, {fix['lon']}")
    log(f"{battery_percent=}")

    try:
        hw_functions["cellular_data"].connect()
        hw_functions["cellular_data"].post_json(config.NTFY_URL, payload)
    except Exception as exc:  # noqa: BLE001  # want to catch all exceptions
        log(f"cellular data POST failed: {exc}")
        return CycleState.POST_FAILED if payload else CycleState.CONFIG_ERROR
    finally:
        hw_functions["cellular_data"].disconnect()

    return outcome
