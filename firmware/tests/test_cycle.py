from unittest.mock import Mock

import config as default_config
import pytest
from tracker.cycle import CycleState, run_cycle


def _sample_results(count=6):
    return [
        {
            "ssid": f"AP{i}",
            "bssid": f"aa:bb:cc:dd:ee:{i:02x}",
            "rssi": -40 - i,
        }
        for i in range(count)
    ]


@pytest.fixture
def hw_functions():
    gps = Mock()
    gps.enable.return_value = True
    gps.get_fix.return_value = None

    pmu = Mock()
    modem = Mock()

    return {
        "pmu": pmu,
        "modem": modem,
        "scan_wifi": Mock(return_value=_sample_results()),
        "gps": gps,
        "nbiot": Mock(),
        "sleep_minutes": Mock(),
        "log": Mock(),
    }


def test_home_ssid_skips_transmit(hw_functions):
    hw_functions["scan_wifi"].return_value = _sample_results() + [
        {"ssid": default_config.HOME_SSID, "bssid": "ff:ff:ff:ff:ff:ff", "rssi": -30}
    ]
    hw_functions["gps"].get_fix.return_value = {"lat": 1.0, "lon": 2.0}

    outcome = run_cycle(default_config, hw_functions)
    assert outcome == CycleState.HOME
    hw_functions["gps"].enable.assert_not_called()
    hw_functions["nbiot"].connect.assert_not_called()


def test_wifi_path_posts_without_gps(hw_functions):
    config = default_config
    hw_functions["scan_wifi"].return_value = _sample_results(config.WIFI_TOP_N + 1)
    hw_functions["gps"].get_fix.return_value = {"lat": 1.0, "lon": 2.0}
    hw_functions["nbiot"].connect.return_value = True

    outcome = run_cycle(config, hw_functions)
    assert outcome == CycleState.WIFI_SENT
    hw_functions["gps"].enable.assert_not_called()
    hw_functions["nbiot"].post.assert_called_once()
    payload = hw_functions["nbiot"].post.call_args[0][1]
    assert payload["type"] == "wifi"
    assert len(payload["wifiAccessPoints"]) == config.WIFI_TOP_N


def test_gps_path_disables_gps_before_nbiot(hw_functions):
    config = default_config
    hw_functions["scan_wifi"].return_value = _sample_results(config.WIFI_MIN_APS - 1)
    hw_functions["gps"].get_fix.return_value = {"lat": 48.1, "lon": 11.5}

    outcome = run_cycle(config, hw_functions)
    assert outcome == CycleState.GPS_SENT
    assert hw_functions["gps"].disable.call_count == 1
    assert hw_functions["nbiot"].connect.call_count == 1
    assert hw_functions["nbiot"].post.call_count == 1


def test_gps_timeout_skips_post(hw_functions):
    config = default_config
    hw_functions["scan_wifi"].return_value = _sample_results(config.WIFI_MIN_APS - 1)

    outcome = run_cycle(config, hw_functions)
    assert outcome == CycleState.NO_FIX
    hw_functions["nbiot"].connect.assert_not_called()


def test_post_failure_returns_post_failed(hw_functions):
    hw_functions["nbiot"].connect.side_effect = RuntimeError("network down")

    outcome = run_cycle(default_config, hw_functions)
    assert outcome == CycleState.POST_FAILED
