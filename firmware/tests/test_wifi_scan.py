from tracker.wifi_scan import (
    format_bssid,
    home_ssid_present,
    normalize_scan_results,
    top_aps,
)


def _sample_results():
    return [
        {"ssid": "HomeNet", "macAddress": "aa:bb:cc:dd:ee:01", "signalStrength": -40},
        {"ssid": "Cafe", "macAddress": "aa:bb:cc:dd:ee:02", "signalStrength": -55},
        {"ssid": "Guest", "macAddress": "aa:bb:cc:dd:ee:03", "signalStrength": -70},
        {"ssid": "Office", "macAddress": "aa:bb:cc:dd:ee:04", "signalStrength": -65},
        {"ssid": "Shop", "macAddress": "aa:bb:cc:dd:ee:05", "signalStrength": -80},
        {"ssid": "Other", "macAddress": "aa:bb:cc:dd:ee:06", "signalStrength": -90},
    ]


def test_format_bssid_from_bytes():
    assert (
        format_bssid(bytes([0xDE, 0xAD, 0xBE, 0xEF, 0x00, 0x01])) == "de:ad:be:ef:00:01"
    )


def test_normalize_scan_results():
    raw = [
        ("Test", bytes([0x11, 0x22, 0x33, 0x44, 0x55, 0x66]), 1, -42.45, 3, False),
    ]
    results = normalize_scan_results(raw)
    assert results[0]["macAddress"] == "11:22:33:44:55:66"
    assert results[0]["ssid"] == "Test"
    assert results[0]["signalStrength"] == -42
    assert results[0]["channel"] == 1


def test_home_ssid_present():
    results = _sample_results()
    assert home_ssid_present(results, "HomeNet")
    assert not home_ssid_present(results, "Missing")


def test_top_aps_returns_best_rssi_first():
    top = top_aps(_sample_results(), n=5)
    assert len(top) == 5
    assert top[0]["macAddress"] == "aa:bb:cc:dd:ee:01"
    assert top[0]["signalStrength"] == -40
    assert top[-1]["signalStrength"] == -80


def test_top_aps_with_fewer_than_five():
    results = _sample_results()[:3]
    top = top_aps(results, n=5)
    assert len(top) == 3
