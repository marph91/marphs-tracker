"""GPS fix acquisition via SIM7080G AT commands."""

import time


class GpsReader:
    """Read GPS coordinates from modem AT+CGNSINF."""

    def __init__(self, pmu, modem):
        self.pmu = pmu
        self.modem = modem

    def enable(self):
        self.pmu.enable_gps_antenna()
        response = self.modem.send_at("AT+CGNSPWR=1", wait=2)
        return "OK" in response

    def disable(self):
        response = self.modem.send_at("AT+CGNSPWR=0", wait=2)
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

    def get_fix(self, timeout_s=120, poll_s=2):
        deadline = time.ticks_add(time.ticks_ms(), timeout_s * 1000)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            response = self.modem.send_at("AT+CGNSINF", wait=poll_s)
            fix = self._parse_fix(response)
            if fix:
                return fix
            time.sleep(poll_s)
        return None
