"""WiFi scan helpers and device scan wrapper."""

import logger
import requests

from tracker.payload import obfuscate_payload, serialize_payload

try:
    # micropython
    import machine
    import network
except ImportError:
    # python
    # needed for unit testing on native device
    machine = None
    network = None


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
            return ap["ssid"]
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


def send_heartbeat(ssid, password, url, battery_level):
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)  # TODO: harmonize with "scan_wifi"
        if not wlan.isconnected():
            LOG(f'connecting to network "{ssid}"')
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                machine.idle()
            LOG("connected to network")

        LOG("send heartbeat")
        payload = {"batt": battery_level}
        response = requests.post(
            url, data=obfuscate_payload(serialize_payload(payload)).encode("utf-8")
        )
        if 200 <= response.status_code <= 299:
            LOG("heartbeat sent successfully")
        else:
            LOG(f"heartbeat failed - HTTP status code: {response.status_code}")
    except Exception as exc:  # noqa: BLE001  # want to catch all remaining exceptions
        LOG(f"{exc}")
    finally:
        wlan.active(False)
