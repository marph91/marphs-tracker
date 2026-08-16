import base64
import json
import random
import time

import requests


def main():
    while True:
        try:
            data = json.dumps(
                {
                    "type": "gps",
                    "lat": random.random() * 180.0 - 90.0,
                    "lon": random.random() * 360.0 - 180.0,
                }
            )
            # encrypted = xxtea.encrypt_hex(data.encode("utf-8"), key)
            obfuscated = base64.b64encode(data.encode()).decode()
            response = requests.post(
                "https://ntfy.adminforge.de/marphs-tracker/json", data=obfuscated
            )
            response.raise_for_status()
            time.sleep(10)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
