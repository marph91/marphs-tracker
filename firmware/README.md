# LilyGo T-SIM7080G S3 MicroPython Tracker

Battery-friendly location tracker for the [LilyGo T-SIM7080G S3](https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G-MicroPython). Each wake cycle:

1. Deep sleep (timer wake, default 60 minutes)
2. Scan WiFi
3. If home SSID is visible → sleep again (no transmit)
4. If ≥5 APs → POST top 5 BSSID/RSSI over cellular data HTTPS
5. Else → acquire GNSS fix → POST lat/lon over cellular data HTTPS
6. Deep sleep

## Configuration

Edit [`config.py`](config.py) before deployment:

- `SLEEP_MINUTES_HOME` — wake interval (default `60`)
- `HOME_SSIDS` — skip transmit when this network is seen
- `NTFY_URL` — ingest endpoint for POST requests
- `CELLULAR_DATA_APN`, `CELLULAR_DATA_USER`, `CELLULAR_DATA_PASSWORD` — carrier settings

## POST payload

WiFi path:

```json
{
  "source": "wifi",
  "wifiAccessPoints": [
    { "macAddress": "aa:bb:cc:dd:ee:ff", "signalStrength": -51 }
  ]
}
```

GNSS path:

```json
{ "source": "gnss", "lat": 48.137154, "lon": 11.576124 }
```

## Flashing

1. Install [esptool](https://github.com/espressif/esptool) and flash the LilyGo MicroPython firmware from their repo.
2. Copy `main.py`, `config.py`, `tracker/`, and `lib/` to the device.
3. Set `main.py` as the boot script (or rename/copy to device root `main.py`).

## Host tests

```bash
pip install -r requirements-dev.txt
pytest
```

Tests cover payload shape, WiFi scan logic, and cycle decision flow with mocks (no hardware required).

## Hardware notes

- GNSS and cellular cannot run simultaneously on SIM7080G; the firmware disables GNSS before cellular data.
- Keep PMU BLDO1 enabled while talking to the modem.
- SIM must be inserted before modem power-on.

## Project layout

- `main.py` — boot entry
- `config.py` — runtime settings
- `tracker/` — firmware modules
- `lib/` — vendored LilyGo board support (`utilities.py`, `XPowersLib.py`)
- `tests/` — host-side pytest suite
