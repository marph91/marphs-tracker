"""Polls NTFY notifications from the NTFY server (in the web) and forwards them to the Traccar server (in the local network)."""

import datetime as dt
import json
import pathlib
import sys

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
        try:
            message_json = json.loads(message)
            if message_json["event"] != "message":
                return
            message_deobfuscated = json.loads(
                xor_crypt(
                    bytes.fromhex(message_json["message"]),
                    firmware_config.ENCRYPTION_KEY,
                ).decode("utf-8")
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

            self.send_to_traccar(
                int(message_json["time"]),
                lat,
                lon,
                message_deobfuscated["battery_level"],
            )
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

    def send_to_traccar(self, timestamp_s, lat, lon, battery_level):
        # save locations to log file
        date = dt.datetime.fromtimestamp(timestamp_s, tz=dt.UTC)
        log_file = pathlib.Path(__file__).parent / f"log/{date.year}.csv"
        log_file.parent.mkdir(exist_ok=True)
        with log_file.open("a") as f:
            f.write(
                f"{date.replace(microsecond=0).isoformat()},{lat},{lon},{battery_level}\n"
            )

        # Actually, it's OsmAnd format: https://www.traccar.org/osmand/
        timestamp = timestamp_s * 1000
        response = requests.get(
            f"{firmware_config.TRACCAR_URL}?id={firmware_config.DEVICE_ID}&{timestamp=}&{lat=}&{lon=}&batt={battery_level}"
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
