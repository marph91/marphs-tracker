# Tracker configuration - edit before deploying to device.

# Time between tracking attempts. Affects power consumption and data usage.
SLEEP_MINUTES = 60

# SSID of your home Wi-Fi.
#
# If this SSID is detected during the Wi-Fi scan,
# the tracker assumes that it is at home and does not
# transmit any tracking data.
HOME_SSID = "YourHomeSSID"

# HTTP endpoint receiving the payload.
HTTPS_URL = "https://example.com/ingest"

# If fewer than this number of Wi-Fi access points
# are detected, GNSS is used instead.
WIFI_MIN_APS = 5
# Maximum number of Wi-Fi APs included in the payload. Affects data usage.
WIFI_TOP_N = 5
GPS_FIX_TIMEOUT_S = 120

# NB-IoT provider settings (fill in before use)
NBIOT_APN = ""
NBIOT_OPERATOR = ""
NBIOT_USER = ""
NBIOT_PASSWORD = ""
NBIOT_BANDS = ""

DEVICE_ID = ""
