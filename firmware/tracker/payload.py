"""Build unified JSON payloads for HTTPS POST."""

import config

try:
    # micropython
    import ujson as json
except ImportError:
    # python
    import json


def serialize_payload(payload):
    """Serialize payload dict to JSON string."""
    return json.dumps(payload, separators=(",", ":"))


def xor_crypt(data, key):
    """Apply simple xor."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def obfuscate_payload(payload):
    """Apply simple xor."""
    return xor_crypt(payload.encode("utf-8"), config.ENCRYPTION_KEY).hex()
