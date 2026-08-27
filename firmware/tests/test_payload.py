import json

import config
from tracker.payload import (
    build_gnss_payload,
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
    )
    assert payload["source"] == "wifi"
    assert len(payload["wifiAccessPoints"]) == 2
    assert payload["wifiAccessPoints"][0]["macAddress"] == "aa:bb:cc:dd:ee:01"


def test_build_gnss_payload_shape():
    payload = build_gnss_payload({"lat": 48.137154, "lon": 11.576124, "batt": 20})
    assert payload == {
        "source": "gnss",
        "lat": 48.137154,
        "lon": 11.576124,
        "batt": 20,
    }


def test_serialize_payload_roundtrip():
    payload = build_wifi_payload(
        [{"macAddress": "aa:bb:cc:dd:ee:ff", "signalStrength": -51}]
    )
    serialized = serialize_payload(payload)
    parsed = json.loads(serialized)
    assert parsed["source"] == "wifi"
    assert parsed["wifiAccessPoints"][0]["signalStrength"] == -51


def test_obfuscate_payload():
    data = "test string"
    obfuscated_data = obfuscate_payload(data)
    assert data == xor_crypt(
        bytes.fromhex(obfuscated_data), config.ENCRYPTION_KEY
    ).decode("utf-8")
