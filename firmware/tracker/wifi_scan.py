"""WiFi scan helpers and device scan wrapper."""

import logger

try:
    # micropython
    import network
except ImportError:
    # python
    network = None  # needed for unit testing on native device


LOG = logger.Logger(__name__)


def format_bssid(bssid):
    """Format BSSID bytes as aa:bb:cc:dd:ee:ff."""
    return ":".join(f"{b:02x}" for b in bssid)


def normalize_scan_results(scan_results):
    """
    Convert raw WLAN scan tuples into normalized dicts.
    - Source: https://docs.micropython.org/en/latest/library/network.WLAN.html#network.WLAN.scan
    - Target: https://ichnaea.readthedocs.io/en/latest/api/geolocate.html#wifi-access-point-fields
    """
    normalized = []
    for ssid, bssid, channel, rssi, _security, _hidden in scan_results:
        normalized.append(
            {
                "macAddress": format_bssid(bssid),
                "ssid": ssid if isinstance(ssid, str) else ssid.decode("utf-8"),
                "signalStrength": int(rssi),
                "channel": channel,
            }
        )
    return normalized


def home_ssid_present(results, home_ssids):
    """Return True if at least one of the home_ssids appears in scan results."""
    if not home_ssids:
        return False
    for ap in results:
        if ap["ssid"] in home_ssids:
            LOG("home SSID detected")
            return True
    return False


def top_aps(results, n=5):
    """Return top N APs by signal strength."""
    ranked = sorted(results, key=lambda ap: ap["signalStrength"], reverse=True)
    return ranked[:n]


def scan_wifi():
    """Activate WiFi, scan APs, deactivate WiFi, return normalized results."""
    if network is None:
        raise RuntimeError("network module unavailable")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    try:
        raw = wlan.scan()
    finally:
        wlan.active(False)
    scan_results = normalize_scan_results(raw)
    LOG(f"scan found {len(scan_results)} APs")
    return scan_results
