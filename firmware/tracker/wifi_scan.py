"""WiFi scan helpers and device scan wrapper."""

import logger

try:
    import network
except ImportError:
    network = None  # needed for unit testing on native device


LOG = logger.Logger(__name__)


def _decode_ssid(ssid):
    if isinstance(ssid, bytes):
        return ssid.decode("utf-8", "ignore")
    return ssid or ""


def format_bssid(bssid):
    """Format BSSID bytes or string as aa:bb:cc:dd:ee:ff."""
    if isinstance(bssid, (bytes, bytearray)):
        return ":".join(f"{b:02x}" for b in bssid)
    if isinstance(bssid, str):
        return bssid.lower()
    raise TypeError("unsupported bssid type")


def normalize_scan_results(scan_results):
    """Convert raw WLAN scan tuples into normalized dicts."""
    normalized = []
    for ssid_raw, bssid_raw, _channel, rssi_raw, _security, _hidden in scan_results:
        ssid = _decode_ssid(ssid_raw)
        bssid = format_bssid(bssid_raw)
        rssi = int(rssi_raw)
        normalized.append({"ssid": ssid, "bssid": bssid, "rssi": rssi})
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
    """Return top N APs by RSSI."""
    ranked = sorted(results, key=lambda ap: ap["rssi"], reverse=True)
    top = ranked[:n]
    return [
        {
            "macAddress": ap["bssid"],
            "signalStrength": ap["rssi"],
        }
        for ap in top
    ]


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
