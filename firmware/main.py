"""Boot entry: run one tracker cycle then deep sleep."""

import config
import machine
from tracker.cycle import run_cycle
from tracker.gps import GpsReader
from tracker.modem import AtModem
from tracker.nbiot import NbiotClient
from tracker.pmu import PmuController
from tracker.wifi_scan import scan_wifi


def main():
    pmu = PmuController()
    modem = AtModem()
    hw_functions = {
        "pmu": pmu,
        "modem": modem,
        "scan_wifi": scan_wifi,
        "gps": GpsReader(pmu, modem, print),
        "nbiot": NbiotClient(modem, config, print),
        "log": print,
        "sleep_minutes": lambda minutes: machine.deepsleep(int(minutes) * 60 * 1000),
    }

    run_cycle(config, hw_functions)


if __name__ == "__main__":
    main()
