import json

import config
from tracker.payload import (
    build_gps_payload,
    build_wifi_payload,
    obfuscate_payload,
    serialize_payload,
    xor_crypt,
)


def test_build_wifi_payload_shape():
    payload = build_wifi_payload(
        [
            {"macAddress": "aa:bb:cc:dd:ee:01", "signalStrength": -40},
            {"macAddress": "aa:bb:cc:dd:ee:02", "signalStrength": -55},
        ],
        100,
    )
    assert payload["type"] == "wifi"
    assert len(payload["wifiAccessPoints"]) == 2
    assert payload["wifiAccessPoints"][0]["macAddress"] == "aa:bb:cc:dd:ee:01"


def test_build_gps_payload_shape():
    payload = build_gps_payload(48.137154, 11.576124, 20)
    assert payload == {
        "type": "gps",
        "lat": 48.137154,
        "lon": 11.576124,
        "battery_level": 20,
    }


def test_serialize_payload_roundtrip():
    payload = build_wifi_payload(
        [{"macAddress": "aa:bb:cc:dd:ee:ff", "signalStrength": -51}], -1
    )
    serialized = serialize_payload(payload)
    parsed = json.loads(serialized)
    assert parsed["type"] == "wifi"
    assert parsed["wifiAccessPoints"][0]["signalStrength"] == -51


def test_obfuscate_payload():
    data = "test string"
    obfuscated_data = obfuscate_payload(data)
    assert data == xor_crypt(
        bytes.fromhex(obfuscated_data), config.ENCRYPTION_KEY
    ).decode("utf-8")
