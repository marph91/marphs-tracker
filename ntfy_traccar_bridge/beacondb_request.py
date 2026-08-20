import sys

import requests


def beacondb_request(data):
    # https://beacondb.net/
    # https://ichnaea.readthedocs.io/en/latest/api/geolocate.html

    url = "https://api.beacondb.net/v1/geolocate"
    headers = {"User-Agent": "Marph's User Agent 1.0"}

    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print("Not found")
        sys.exit()
    print(response.text)
    # response.raise_for_status()
    location = response.json().get("location")
    # if (location := response.json().get("location")) is None:
    #     return
    print(response.json())
    print(location["lat"], location["lng"])


if __name__ == "__main__":
    # sample data: "nmcli dev wifi"
    data = {
        "wifiAccessPoints": [
            # {"macAddress": "0C:C5:74:47:16:10", "signalStrength": -51},
            {"macAddress": "EC:6C:9A:13:E1:CE", "signalStrength": -30},
            {"macAddress": "1E:ED:6F:CD:74:46", "signalStrength": -30},
            {"macAddress": "78:DD:12:BE:31:52", "signalStrength": -30},
            {"macAddress": "80:3F:5D:68:D3:D6", "signalStrength": -30},
        ],
        "considerIp": False,
    }

    beacondb_request(data)
