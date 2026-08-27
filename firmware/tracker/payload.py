"""Build unified JSON payloads for HTTPS POST."""

import config

try:
    # micropython
    import ujson as json
except ImportError:
    # python
    import json


def build_wifi_payload(access_points, battery_level):
    """Return wifi payload dict with top access points."""
    return {
        "type": "wifi",
        "battery_level": battery_level,
        "wifiAccessPoints": list(access_points),
    }


def build_gnss_payload(lat, lon, battery_level):
    """Return gnss payload dict with coordinates."""
    return {
        "type": "gnss",
        "battery_level": battery_level,
        "lat": lat,
        "lon": lon,
    }


def serialize_payload(payload):
    """Serialize payload dict to JSON string."""
    return json.dumps(payload, separators=(",", ":"))


def xor_crypt(data, key):
    """Apply simple xor."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def obfuscate_payload(payload):
    """Apply simple xor."""
    return xor_crypt(payload.encode("utf-8"), config.ENCRYPTION_KEY).hex()
