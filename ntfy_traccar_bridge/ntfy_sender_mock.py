"""Sends requests with the correct layout, but random data to the NTFY server. Mocks the location tracker device"""

import json
import pathlib
import random
import sys
import time

import requests

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "firmware"))

import config as firmware_config


def xor_crypt(data, key):
    """Apply simple xor."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def main():
    while True:
        try:
            # WIFI based location
            data = json.dumps(
                {
                    "source": "wifi",
                    "wifiAccessPoints": [
                        {
                            "macAddress": "36:2C:C4:88:DA:EE",
                            "signalStrength": random.random() * -100,
                        },
                        {
                            "macAddress": "1C:ED:6F:CD:74:46",
                            "signalStrength": random.random() * -100,
                        },
                        {
                            "macAddress": "44:15:24:01:80:25",
                            "signalStrength": random.random() * -100,
                        },
                        {
                            "macAddress": "1E:ED:6F:CD:74:46",
                            "signalStrength": random.random() * -100,
                        },
                    ],
                    "batt": 55,
                }
            )
            obfuscated = xor_crypt(
                data.encode("utf-8"), firmware_config.ENCRYPTION_KEY
            ).hex()
            response = requests.post(firmware_config.NTFY_URL, data=obfuscated)
            response.raise_for_status()
            time.sleep(10)

            # GNSS based location
            data = json.dumps(
                {
                    "source": "gnss",
                    "lat": random.random() * 180.0 - 90.0,
                    "lon": random.random() * 360.0 - 180.0,
                    "altitude": random.randint(-10, 100),
                    "speed": random.random() * 1000.0,
                    "heading": random.random() * 360.0,
                    "hdop": random.random() * 100.0,
                    "batt": 44,
                }
            )
            # encrypted = xxtea.encrypt_hex(data.encode("utf-8"), key)
            obfuscated = xor_crypt(
                data.encode("utf-8"), firmware_config.ENCRYPTION_KEY
            ).hex()
            response = requests.post(firmware_config.NTFY_URL, data=obfuscated)
            response.raise_for_status()
            time.sleep(10)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
