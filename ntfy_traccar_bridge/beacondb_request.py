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
            {"macAddress": "00:00:08:EE:7A:A5", "signalStrength": -50}
        ],
        "considerIp": False,
    }

    beacondb_request(data)
