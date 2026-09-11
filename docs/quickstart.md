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

1. Adapt the [configuration file](../firmware/config.py) according to your needs.
2. Install [esptool](https://github.com/espressif/esptool) and flash the [LilyGo MicroPython firmware](https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G-MicroPython/tree/377b15a71fde63463ef67a450856571dc5516a8a/firmware) from their repo.
3. Upload the scripts at ./firmware
4. Reboot
