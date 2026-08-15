"""AXP2101 PMU helpers for modem and GPS power rails."""

import utilities
import XPowersLib
from machine import I2C, Pin


class PmuController:
    """Manage LilyGo board power rails."""

    def __init__(self):
        self._pmu = XPowersLib.XPowersPMU()
        self._initialized = False

    def begin(self):
        """Initialize PMU and enable level shifter + modem + GPS rails."""
        if self._initialized:
            return True

        i2c = I2C(0, scl=Pin(utilities.I2C_SCL), sda=Pin(utilities.I2C_SDA))
        if not self._pmu.begin(
            i2c,
            XPowersLib.AXP2101_SLAVE_ADDRESS,
            utilities.I2C_SDA,
            utilities.I2C_SCL,
        ):
            return False

        self._pmu.setBLDO1Voltage(3000)
        self._pmu.enableBLDO1()

        self._pmu.setDC3Voltage(3000)
        self._pmu.enableDC3()

        self._pmu.setBLDO2Voltage(3300)
        self._pmu.enableBLDO2()

        self._pmu.disableTSPinMeasure()
        self._initialized = True
        return True

    def enable_modem(self):
        self._pmu.setDC3Voltage(3000)
        self._pmu.enableDC3()

    def disable_modem(self):
        self._pmu.disableDC(3)

    def enable_gps_antenna(self):
        self._pmu.setBLDO2Voltage(3300)
        self._pmu.enableBLDO2()

    def disable_gps_antenna(self):
        self._pmu.disableBLDO(2)

    def power_down_for_sleep(self):
        """Disable modem and GPS rails before ESP deep sleep."""
        self.disable_modem()
        self.disable_gps_antenna()
