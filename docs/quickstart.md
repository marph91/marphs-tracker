## Prerequisites

- Lilygo T-SIM7080G
- IoT SIM card
- 18650 battery
- [Traccar](https://www.traccar.org/) instance
- Server that can run Python scripts (to bridge between the device and the Traccar instance)

## Hardware

1. Connect the GNSS and LTE antennas to your device.
2. Configure the SIM card as explained below.
3. Insert the 18650 battery or connect a USB cable for testing locally.
4. (optional) put everything in a [self-printed case](https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G/tree/master/shell).

### SIM card

- Insert to phone
- Deactivate PIN
- Read APN and credentials. For example:
  - APN: web.vodafone.de
  - User, Password: "not defined"
- Charge 5 €
- Insert to device

## Software

### Setting up the device

1. Clone this repo
2. Adapt the [configuration file](../firmware/config.py) according to your needs.
3. Install [esptool](https://github.com/espressif/esptool) and flash the [LilyGo MicroPython firmware](https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G-MicroPython/tree/377b15a71fde63463ef67a450856571dc5516a8a/firmware) from their repo.
4. Upload the [firmware](../firmware/) with [flash_firmware.bash](../flash_firmware.bash)
5. Reboot

### Setting up the Server

1. Clone this repo
2. Adapt the [configuration file](../firmware/config.py) according to your needs.
3. Start the script [`ntfy_traccar_bridge.py`](../ntfy_traccar_bridge/ntfy_traccar_bridge.py) and make sure it runs always.
   1. Option 1: Via systemd. For example using [this service](../ntfy_traccar_bridge/ntfy-traccar-bridge.service).
      1. Create a symlink `ln -s ~/.config/systemd/user/ /path/to/marphs-tracker/ntfy_traccar_bridge/ntfy-traccar-bridge.service`
      2. Enable the service `systemctl --user enable ntfy-traccar-bridge.service`
      3. Start the service `systemctl --user start ntfy-traccar-bridge.service`
      4. Check the log: `systemctl --user status ntfy-traccar-bridge.service` or `journalctl --user -u ntfy-traccar-bridge`
   2. Option 2: Via cron. For example `@reboot sleep 60; python3 /path/to/marphs-tracker/ntfy_traccar_bridge/ntfy_traccar_bridge.py`
   3. You can also use another service of your choice.
