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
from tracker.wifi_scan import scan_wifi, send_heartbeat

LOG = logger.Logger(__name__.strip("_"))


def main():
    LOG("Starting main script")

    pmu = PmuController()
    modem = AtModem()
    hw_functions = {
        "pmu": pmu,
        "modem": modem,
        "scan_wifi": scan_wifi,
        "send_heartbeat": send_heartbeat,
        "gnss": GnssReader(pmu, modem),
        "cellular_data": CellularDataClient(modem, config),
    }

    cycle_state = CycleState.NONE
    start_time_ms = time.ticks_ms()
    try:
        cycle_state = run_cycle(config, hw_functions)
        LOG(f"{cycle_state=}")
    except Exception as exc:  # noqa: BLE001  # want to catch all remaining exceptions
        LOG("Cycle failed. TODO: catch this exception:")
        LOG(f"{exc}")
    elapsed_time_ms = time.ticks_diff(time.ticks_ms(), start_time_ms)
    LOG(f"Cycle time: {elapsed_time_ms / 1000} s")

    # sleep
    if pmu.get_battery_percent() == -1:
        # prevent boot loop to allow debugging
        # stop the script with ctrl+c
        LOG("Don't go to sleep, since the battery is not connected.")
    else:
        # sleep some time depending on the state
        sleep_minutes = (
            config.SLEEP_MINUTES_HOME
            if cycle_state == CycleState.HOME
            else config.SLEEP_MINUTES_AWAY
        )
        sleep_ms = int(sleep_minutes) * 60 * 1000
        LOG(f"Going to sleep for {sleep_ms / 1000} seconds")
        machine.deepsleep(sleep_ms)


if __name__ == "__main__":
    main()
