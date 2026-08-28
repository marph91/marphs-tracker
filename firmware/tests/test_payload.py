import json

import config
from tracker.payload import (
    obfuscate_payload,
    serialize_payload,
    xor_crypt,
)


def test_serialize_payload_roundtrip():
    payload = {
        "wifiAccessPoints": [{"macAddress": "aa:bb:cc:dd:ee:ff", "signalStrength": -51}]
    }
    serialized = serialize_payload(payload)
    parsed = json.loads(serialized)
    assert parsed == payload


def test_obfuscate_payload():
    data = "test string"
    obfuscated_data = obfuscate_payload(data)
    assert data == xor_crypt(
        bytes.fromhex(obfuscated_data), config.ENCRYPTION_KEY
    ).decode("utf-8")
