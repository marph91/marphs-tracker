"""Build unified JSON payloads for HTTPS POST."""

try:
    # micropython
    import ubinascii as binascii
    import ujson as json
except ImportError:
    # python
    import binascii
    import json


def build_wifi_payload(access_points):
    """Return wifi payload dict with top access points."""
    return {
        "type": "wifi",
        "wifiAccessPoints": list(access_points),
    }


def build_gps_payload(lat, lon):
    """Return gps payload dict with coordinates."""
    return {
        "type": "gps",
        "lat": lat,
        "lon": lon,
    }


def serialize_payload(payload):
    """Serialize payload dict to JSON string."""
    return json.dumps(payload, separators=(",", ":"))


def obfuscate_payload(payload):
    return binascii.b2a_base64(payload.encode()).decode().strip()
