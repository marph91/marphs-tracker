import base64
import json

import requests


class MessageConverter:
    """Converts a ntfy message to a traccar message."""

    def __init__(self) -> None:
        self.key = b"1234567890abcdef"  # TODO: read from config file
        self.traccar_url = "http://192.168.111.23:5055"  # TODO: read from config file

    def handle_ntfy_message(self, message):
        # https://docs.ntfy.sh/subscribe/api/#subscribe-as-json-stream
        try:
            message_json = json.loads(message)
            if message_json["event"] != "message":
                return
            message_deobfuscated = json.loads(
                base64.b64decode(message_json["message"]).decode()
            )
            print(message_json, message_deobfuscated)
            match message_deobfuscated["type"]:
                case "gps":
                    lat = message_deobfuscated["lat"]
                    lon = message_deobfuscated["lon"]
                case "wifi":
                    return
                case _:
                    print("Unknown format")
                    return

            self.convert_to_traccar_format(lat, lon, int(message_json["time"]) * 1000)
        except Exception as exc:  # want to catch all exceptions
            print(exc)
            raise

    def convert_to_traccar_format(self, lat, lon, timestamp):
        # Actually, it's OsmAnd format: https://www.traccar.org/osmand/
        print(f"{self.traccar_url}?id=0&{lat=}&{lon=}&{timestamp=}")
        response = requests.get(f"{self.traccar_url}?id=0&{lat=}&{lon=}&{timestamp=}")
        response.raise_for_status()


def main():
    message_converter = MessageConverter()

    resp = requests.get("https://ntfy.adminforge.de/marphs-tracker/json", stream=True)
    for line in resp.iter_lines():
        if line:
            message_converter.handle_ntfy_message(line)


if __name__ == "__main__":
    main()
