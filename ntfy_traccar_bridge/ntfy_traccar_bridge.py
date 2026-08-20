import base64
import json
import pathlib
import sys

import requests

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "firmware"))

import config as firmware_config


class MessageConverter:
    """Converts a ntfy message to a traccar message."""

    def __init__(self) -> None:
        self.beacondb_url = "https://api.beacondb.net/v1/geolocate"

    def handle_ntfy_message(self, message):
        # https://docs.ntfy.sh/subscribe/api/#subscribe-as-json-stream
        try:
            message_json = json.loads(message)
            if message_json["event"] != "message":
                return
            message_deobfuscated = json.loads(
                base64.b64decode(message_json["message"]).decode()
            )

            match message_deobfuscated["type"]:
                case "gps":
                    lat = message_deobfuscated["lat"]
                    lon = message_deobfuscated["lon"]
                case "wifi":
                    location = self.get_location_from_beacondb(
                        message_deobfuscated["wifiAccessPoints"]
                    )
                    if location is None:
                        print(
                            f"Location couldn't be resolved: {message_deobfuscated['wifiAccessPoints']}"
                        )
                        return
                    lat = location["lat"]
                    lon = location["lng"]
                case _:
                    print("Unknown format")
                    return

            self.convert_to_traccar_format(lat, lon, int(message_json["time"]) * 1000)
        except Exception as exc:  # want to catch all exceptions
            print(exc)
            raise

    def get_location_from_beacondb(self, access_points):
        # https://beacondb.net/
        # https://ichnaea.readthedocs.io/en/latest/api/geolocate.html

        data = {
            "wifiAccessPoints": access_points,
            # don't resolve by IP, since this would yield the location of the scripts machine
            "considerIp": False,
        }
        headers = {"User-Agent": "Marph's User Agent 1.0"}

        response = requests.post(self.beacondb_url, json=data, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return None
        return response.json().get("location")

    def convert_to_traccar_format(self, lat, lon, timestamp):
        # Actually, it's OsmAnd format: https://www.traccar.org/osmand/
        response = requests.get(
            f"{firmware_config.TRACCAR_URL}?id={firmware_config.DEVIE_ID}&{lat=}&{lon=}&{timestamp=}"
        )
        response.raise_for_status()


def main():
    message_converter = MessageConverter()

    resp = requests.get(firmware_config.NTFY_URL, stream=True)
    for line in resp.iter_lines():
        if line:
            message_converter.handle_ntfy_message(line)


if __name__ == "__main__":
    main()
