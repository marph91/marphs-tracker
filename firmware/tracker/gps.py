"""GPS fix acquisition via SIM7080G AT commands."""

import time


class GpsReader:
    """Read GPS coordinates from modem AT+CGNSINF."""

    def __init__(self, pmu, modem):
        self.pmu = pmu
        self.modem = modem

    def config(self):
        self.modem.send_at("AT+CGNSPWR=0", wait=2, await_string="OK")

        # GPS,GLONASS,BEIDOU,GALILEAN,QZSS
        # "For <glo mode>,<bd mode>,<gal mode> and <qzss mode>,
        #  Only one of the four parameters can be set to 1."
        # https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G/blob/1f49d041e11c1af5ca7c32bb604f65da8e4394ae/examples/MinimalModemGPSExample/MinimalModemGPSExample.ino#L154
        # response = self.modem.send_at("AT+CGNSMOD?", wait=2)
        # print(response)
        self.modem.send_at("AT+CGNSMOD=1,0,0,1,0", wait=2, await_string="OK")
        print("GPS: Setting systems successful")

        # self.modem.send_at("AT+SGNSCFG?", wait=2, await_string="OK")

        # <mode>
        # 0 Turn off GNSS.
        # 1 Turn on GNSS and get location information once.
        # 2 Turn on GNSS and get multiple location information.

        # mode 1:
        # <powerlevel>
        # 0 Use all technologies available to calculate location.
        # 1 Use all low power technologies to calculate location.
        # 2 Use only low and medium power technologies to calculate location.
        # self.modem.send_at("AT+SGNSCMD=1,0", wait=2, await_string="OK")
        # print("GPS: Setting command successful")

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
        self.modem.send_at("AT+SGNSCMD=2,1000,0,1", wait=2, await_string="OK")
        print("GPS: Setting command successful")

        # Turn off GNSS
        self.modem.send_at("AT+SGNSCMD=0", wait=2, await_string="OK")
        print("GPS: Configuration finished successful")

        self.modem.send_at("AT+CGNSPWR=1", wait=2, await_string="OK")

    def enable(self):
        self.pmu.enable_gps_antenna()
        response = self.modem.send_at("AT+CGNSPWR=1", wait=2, await_string="OK")
        return "OK" in response

    def disable(self):
        response = self.modem.send_at("AT+CGNSPWR=0", wait=2, await_string="OK")
        self.pmu.disable_gps_antenna()
        return "OK" in response

    def _parse_fix(self, response):
        if "+CGNSINF:" not in response:
            return None

        data = response.split("+CGNSINF: ", 1)[1].split("\n", 1)[0]
        values = data.split(",")
        if len(values) < 5:
            return None
        if values[1] != "1":
            return None

        try:
            lat = float(values[3])
            lon = float(values[4])
        except ValueError:
            return None

        if lat == 0.0 and lon == 0.0:
            return None

        return {"lat": lat, "lon": lon}

    def get_fix(self, timeout_s=60, poll_s=2):
        start_time_ms = time.ticks_ms()
        deadline_ms = time.ticks_add(start_time_ms, timeout_s * 1000)
        while time.ticks_diff(deadline_ms, time.ticks_ms()) > 0:
            response = self.modem.send_at("AT+CGNSINF", await_string="OK")
            # print(response)
            current_time_s = time.ticks_diff(time.ticks_ms(), start_time_ms) // 1000
            fix = self._parse_fix(response)
            if fix:
                print(f"GPS: Fix after {current_time_s} seconds")
                print(fix)
                return fix
            print(f"GPS: No fix after {current_time_s} seconds")
            time.sleep(poll_s)
        print("GPS fix timeout")
        return None
