"""Configuration of the location tracker - used by the firmware and local scripts."""

try:
    # micropython
    from micropython import const
except ImportError:
    # python
    const = lambda x: x

# Time between tracking attempts. Affects power consumption and data usage.
SLEEP_MINUTES_HOME = const(30)  # sleep for a longer time when home
SLEEP_MINUTES_AWAY = const(5)  # track more often when away

# SSID of your home WiFis.
# If any of these SSIDs are detected during the WiFi scan,
# the tracker assumes that it is at home and does not
# transmit any tracking data.
HOME_SSIDS = const(("YourHomeWifiSSID", "SecondHomeSSID"))

# Passwords of the home WiFis. Have to correspond to "HOME_SSIDS".
# If the password is set, a "heartbeat" (only battery level) is sent when in home WiFi.
HOME_PASSWORDS = const((None, None))

# HTTP endpoint receiving the payload from the device.
TARGET_URL = const("https://httpbin.org/post")
# encryption parameters for the data
ENCRYPTION_KEY = const(b"secret_key")

# If fewer than this number of WiFi access points
# are detected, GNSS is used instead.
WIFI_MIN_APS = const(5)
# Maximum number of WiFi APs included in the payload. Affects data usage.
WIFI_TOP_N = const(5)
GNSS_FIX_TIMEOUT_S = const(60)

# Cellular data provider settings (fill in before use)
CELLULAR_DATA_APN = const("")
CELLULAR_DATA_USER = const("")
CELLULAR_DATA_PASSWORD = const("")

# Traccar settings
TRACCAR_URL = const("http://home.lab:5055")
DEVICE_ID = const(0)
