"""GNSS fix acquisition via SIM7080G AT commands."""

import time

import logger

LOG = logger.Logger(__name__)


def parse_fix(response):
    if "+CGNSINF:" not in response:
        return None

    try:
        data = response.split("+CGNSINF: ", 1)[1].split("\n", 1)[0]
        # HDOP = Horizontal Dilution of Precision
        (
            _run,
            fix_status,
            _timestamp,
            latitude_str,
            longitude_str,
            altitude_str,
            speed_str,
            course_str,
            _fix_mode,
            _,
            hdop_str,
            _pdop,
            _vdop,
            _,
            _satellites_in_view,
            _,
            _hpa,
            _vpa,
        ) = data.split(",")

        if fix_status != "1":
            return None

        latitude = 0.0 if not latitude_str else float(latitude_str)
        longitude = 0.0 if not longitude_str else float(longitude_str)
        altitude = 0.0 if not altitude_str else float(altitude_str)
        speed = 0.0 if not speed_str else float(speed_str)
        course = 0.0 if not course_str else float(course_str)
        hdop = 9999.9 if not hdop_str else float(hdop_str)
    except ValueError:
        return None

    if latitude == 0.0 and longitude == 0.0:
        return None

    # Format: https://www.traccar.org/osmand/
    return {
        "lat": latitude,
        "lon": longitude,
        "altitude": altitude,
        "speed": speed,
        "heading": course,
        "hdop": hdop,
    }


class GnssReader:
    """Read GNSS coordinates from modem AT+CGNSINF."""

    def __init__(self, pmu, modem):
        self.pmu = pmu
        self.modem = modem

    def config(self):
        self.modem.send_at("AT+CGNSPWR=0", wait=2, await_all=["OK"])

        # GPS,GLONASS,BEIDOU,GALILEAN,QZSS
        # "For <glo mode>,<bd mode>,<gal mode> and <qzss mode>,
        #  Only one of the four parameters can be set to 1."
        # https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G/blob/1f49d041e11c1af5ca7c32bb604f65da8e4394ae/examples/MinimalModemGPSExample/MinimalModemGPSExample.ino#L154
        # response = self.modem.send_at("AT+CGNSMOD?", wait=2)
        # LOG(response)
        self.modem.send_at("AT+CGNSMOD=1,0,0,1,0", wait=2, await_all=["OK"])
        LOG("Setting systems successful")

        # self.modem.send_at("AT+SGNSCFG?", wait=2, await_all=["OK"])

        # <mode>
        # 0 Turn off GNSS.
        # 1 Turn on GNSS and get location information once.
        # 2 Turn on GNSS and get multiple location information.

        # mode 1:
        # <powerlevel>
        # 0 Use all technologies available to calculate location.
        # 1 Use all low power technologies to calculate location.
        # 2 Use only low and medium power technologies to calculate location.
        # self.modem.send_at("AT+SGNSCMD=1,0", wait=2, await_all=["OK"])
        # LOG("Setting command successful")

        # mode 2:
        # <minInterval>
        # minInterval is the minimum time interval in milliseconds that must
        # elapse between position reports. default value is 1000.
        # <minDistance>
        # Minimum distance in meters that must be traversed between position
        # reports. Setting this interval to 0 will be a pure time-based
        # tracking/batching.
        # <accuracy>
        # 0 Accuracy is not specified, use default.
        # 1 Low Accuracy for location is acceptable.
        # 2 Medium Accuracy for location is acceptable.
        # 3 Only High Accuracy for location is acceptable.
        self.modem.send_at("AT+SGNSCMD=2,1000,0,1", wait=2, await_all=["OK"])
        LOG("Setting command successful")

        # Turn off GNSS
        self.modem.send_at("AT+SGNSCMD=0", wait=2, await_all=["OK"])
        LOG("Configuration finished successful")

        self.modem.send_at("AT+CGNSPWR=1", wait=2, await_all=["OK"])

    def enable(self):
        self.pmu.enable_gnss_antenna()
        response = self.modem.send_at("AT+CGNSPWR=1", wait=2, await_all=["OK"])
        return "OK" in response

    def disable(self):
        response = self.modem.send_at("AT+CGNSPWR=0", wait=2, await_all=["OK"])
        self.pmu.disable_gnss_antenna()
        return "OK" in response

    def get_fix(self, timeout_s=60, poll_s=2):
        start_time_ms = time.ticks_ms()
        deadline_ms = time.ticks_add(start_time_ms, timeout_s * 1000)
        while time.ticks_diff(deadline_ms, time.ticks_ms()) > 0:
            response = self.modem.send_at("AT+CGNSINF", await_all=["OK"])
            # LOG(response)
            current_time_s = time.ticks_diff(time.ticks_ms(), start_time_ms) // 1000
            fix = parse_fix(response)
            if fix:
                LOG(f"Fix after {current_time_s} seconds")
                LOG(fix)
                return fix
            LOG(f"No fix after {current_time_s} seconds")
            time.sleep(poll_s)
        LOG("fix timeout")
        return None
