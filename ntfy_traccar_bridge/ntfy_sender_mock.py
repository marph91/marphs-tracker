import random
import time

import requests
import xxtea


def main():
    key = b"1234567890abcdef"

    while True:
        try:
            data = f"{random.random() * 180.0 - 90.0},{random.random() * 360.0 - 180.0}"
            encrypted = xxtea.encrypt_hex(data.encode("utf-8"), key)
            response = requests.post(
                "https://ntfy.adminforge.de/marphs-tracker/json", data=encrypted
            )
            response.raise_for_status()
            time.sleep(10)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
