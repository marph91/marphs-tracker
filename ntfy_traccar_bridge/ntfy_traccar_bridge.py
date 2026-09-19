"""Polls ntfy notifications from the ntfy server (in the web) and forwards them to the Traccar server (in the local network)."""

import datetime as dt
import json
import pathlib
import sys
import time
from urllib.parse import urlencode

import requests

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "firmware"))

import config as firmware_config


def xor_crypt(data, key):
    """Apply simple xor."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


class MessageConverter:
    """Converts a ntfy message to a traccar message."""

    def __init__(self) -> None:
        self.beacondb_url = "https://api.beacondb.net/v1/geolocate"

    def handle_ntfy_message(self, message):
        # https://docs.ntfy.sh/subscribe/api/#subscribe-as-json-stream
        message_json = json.loads(message)
        if message_json["event"] != "message":
            return
        message_deobfuscated = json.loads(
            xor_crypt(
                bytes.fromhex(message_json["message"]),
                firmware_config.ENCRYPTION_KEY,
            ).decode("utf-8")
        )

        # Format: https://www.traccar.org/osmand/
        traccar_data = {"timestamp": int(message_json["time"])}
        if (battery := message_deobfuscated.get("batt")) is not None:
            traccar_data["batt"] = battery

        # Data for resolving the location with wifi and cell tower data.
        # Not relevant for the GNSS path, since the location is available there.
        beacondb_data = {}

        if "gnss" in message_deobfuscated:
            traccar_data.update(message_deobfuscated["gnss"])

        if "wifiAccessPoints" in message_deobfuscated:
            beacondb_data["wifiAccessPoints"] = message_deobfuscated["wifiAccessPoints"]

            # TODO: OsmAnd format supports multiple WIFI, but there would be multiple
            # "wifi" keys in python. Just return the strongest wifi for now.
            # - there are at least 5 wifi APs (config)
            # - they are sorted by signal strength already
            strongest_wifi = message_deobfuscated["wifiAccessPoints"][0]
            traccar_data["wifi"] = (
                f"{strongest_wifi['macAddress']},{int(strongest_wifi['signalStrength'])}"
            )

        if message_deobfuscated.get("cellTowers"):
            beacondb_data["cellTowers"] = message_deobfuscated["cellTowers"]

            # There should be only one cell tower.
            # It's thw cell tower over which the data was sent.
            strongest_cell_tower = message_deobfuscated["cellTowers"][0]
            traccar_data["cell"] = ",".join(
                map(
                    str,
                    (
                        strongest_cell_tower["mobileCountryCode"],
                        strongest_cell_tower["mobileNetworkCode"],
                        strongest_cell_tower["locationAreaCode"],
                        strongest_cell_tower["cellId"],  # TODO: cellId or psc?
                        int(strongest_cell_tower["signalStrength"]),
                    ),
                )
            )

        # resolve location by wifi APs and cell towers with beaconDB
        if beacondb_data and not "lat" in traccar_data:
            location, accuracy = self.get_location_from_beacondb(beacondb_data)
            if location is None:
                print(f"Location couldn't be resolved: {beacondb_data}")
            else:
                print(f"Resolved location: {location}")
                traccar_data.update(
                    {
                        "lat": location["lat"],
                        "lon": location["lng"],
                        "accuracy": accuracy,
                    }
                )

        # finally send all the data to the traccar instance
        self.send_to_traccar(traccar_data)

    def get_location_from_beacondb(self, device_data):
        # https://beacondb.net/
        # https://ichnaea.readthedocs.io/en/latest/api/geolocate.html

        data = {
            # device data contains wifi access points and cell towers
            **device_data,
            # don't resolve by IP, since this would yield the location of the scripts machine
            "considerIp": False,
        }
        headers = {"User-Agent": "Marph's User Agent 1.0"}

        response = requests.post(self.beacondb_url, json=data, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return None, None
        return response.json().get("location"), response.json().get("accuracy")

    def send_to_traccar(self, data):
        # save locations to log file
        date = dt.datetime.fromtimestamp(data["timestamp"], tz=dt.UTC)
        log_file = pathlib.Path(__file__).parent / f"log/{date.year}.csv"
        log_file.parent.mkdir(exist_ok=True)
        with log_file.open("a") as f:
            f.write(",".join(f"{key}={value}" for key, value in data.items()) + "\n")

        # Format: https://www.traccar.org/osmand/
        query = {"id": firmware_config.DEVICE_ID, **data}
        print(query)
        response = requests.get(f"{firmware_config.TRACCAR_URL}?{urlencode(query)}")
        response.raise_for_status()


def main():
    message_converter = MessageConverter()

    while True:
        try:
            resp = requests.get(firmware_config.TARGET_URL, stream=True)
            for line in resp.iter_lines():  # this blocks
                if line:
                    message_converter.handle_ntfy_message(line)
        except Exception as exc:  # noqa: BLE001  # want to catch all exceptions
            print(exc)
            print("Restarting")
            time.sleep(5)


if __name__ == "__main__":
    main()
