"""Sends requests with the correct layout, but random data to the ntfy server. Mocks the location tracker device"""

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
                    "wifiAccessPoints": [
                        {
                            "macAddress": "0c:c5:74:47:16:10",
                            "signalStrength": -39,
                            "channel": random.randint(1, 13),
                        },
                        {
                            "macAddress": "1e:ed:6f:cd:74:45",
                            "signalStrength": -55,
                            "channel": random.randint(1, 13),
                        },
                        {
                            "macAddress": "1c:ed:6f:cd:74:45",
                            "signalStrength": -55,
                            "channel": random.randint(1, 13),
                        },
                        {
                            "macAddress": "ec:6c:9a:13:e1:ce",
                            "signalStrength": -57,
                            "channel": random.randint(1, 13),
                        },
                        {
                            "macAddress": "6c:15:db:27:9c:6e",
                            "signalStrength": -62,
                            "channel": random.randint(1, 13),
                        },
                        # {
                        #     "macAddress": "36:2C:C4:88:DA:EE",
                        #     "signalStrength": random.random() * -100,
                        #     "channel": random.randint(1, 13),
                        # },
                        # {
                        #     "macAddress": "1C:ED:6F:CD:74:46",
                        #     "signalStrength": random.random() * -100,
                        #     "channel": random.randint(1, 13),
                        # },
                        # {
                        #     "macAddress": "44:15:24:01:80:25",
                        #     "signalStrength": random.random() * -100,
                        #     "channel": random.randint(1, 13),
                        # },
                        # {
                        #     "macAddress": "1E:ED:6F:CD:74:46",
                        #     "signalStrength": random.random() * -100,
                        #     "channel": random.randint(1, 13),
                        # },
                    ],
                    "cellTowers": [
                        {
                            "radioType": "lte",
                            "mobileCountryCode": 262,
                            "mobileNetworkCode": 2,
                            "locationAreaCode": 0xAAB4,
                            "cellId": 8596225,
                            "psc": 147,
                            "signalStrength": -74,
                        }
                    ],
                    "batt": 55,
                }
            )
            obfuscated = xor_crypt(
                data.encode("utf-8"), firmware_config.ENCRYPTION_KEY
            ).hex()
            response = requests.post(firmware_config.TARGET_URL, data=obfuscated)
            response.raise_for_status()
            time.sleep(10)

            # GNSS based location
            data = json.dumps(
                {
                    "gnss": {
                        "lat": random.random() * 180.0 - 90.0,
                        "lon": random.random() * 360.0 - 180.0,
                        "altitude": random.randint(-10, 100),
                        "speed": random.random() * 1000.0,
                        "heading": random.random() * 360.0,
                        "hdop": random.random() * 100.0,
                    },
                    "batt": 44,
                }
            )
            # encrypted = xxtea.encrypt_hex(data.encode("utf-8"), key)
            obfuscated = xor_crypt(
                data.encode("utf-8"), firmware_config.ENCRYPTION_KEY
            ).hex()
            response = requests.post(firmware_config.TARGET_URL, data=obfuscated)
            response.raise_for_status()
            time.sleep(10)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
