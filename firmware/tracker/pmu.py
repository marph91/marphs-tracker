"""AXP2101 PMU helpers for modem and GPS power rails."""

import utilities
import XPowersLib
from machine import I2C, Pin


class PmuController:
    """Manage LilyGo board power rails."""

    def __init__(self):
        self._pmu = XPowersLib.XPowersPMU()
        self._initialized = False
        self.i2c = I2C(0, scl=Pin(utilities.I2C_SCL), sda=Pin(utilities.I2C_SDA))

    def begin(self):
        """Initialize PMU and enable level shifter + modem + GPS rails."""
        if self._initialized:
            return True

        if not self._pmu.begin(
            self.i2c,
            XPowersLib.AXP2101_SLAVE_ADDRESS,
            utilities.I2C_SDA,
            utilities.I2C_SCL,
        ):
            print("PMU init failed")
            return False

        self._pmu.setBLDO1Voltage(3000)
        self._pmu.enableBLDO1()

        self.enable_modem()
        self.enable_gps_antenna()

        self._pmu.disableTSPinMeasure()
        self._initialized = True
        return True

    def is_usb_connected(self):
        # only useful after "begin()"
        return self._pmu.isVbusIn()

    def enable_modem(self):
        # SIM7080 Modem main power channel 2700 - 3400V
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
        print("Disabling PMU measurements and unused rails...")

        # Disable PMU measurements
        self._pmu.disableBattVoltageMeasure()
        self._pmu.disableTemperatureMeasure()
        self._pmu.disableVbusVoltageMeasure()
        self._pmu.disableSystemVoltageMeasure()
        self._pmu.disableTSPinMeasure()

        # Disable unused PMU power rails
        for i in range(1, 5):
            self._pmu.disableALDO(i)

        # BLDO1 is the level-converter supply
        self._pmu.disableBLDO(1)
        # GPS supply
        self.disable_gps_antenna()  # self._pmu.disableBLDO(2)

        # DC2 = unused
        self._pmu.disableDC(2)
        # DC3 = SIM7080G
        self.disable_modem()  # self._pmu.disableDC(3)
        # DC4 = unused
        self._pmu.disableDC(4)
        # DC5 = NFC
        self._pmu.disableDC(5)

        # CPU/unused LDOs
        self._pmu.disableCPUSLDO()
        self._pmu.disableDLDO(1)
        self._pmu.disableDLDO(2)

    def get_battery_percent(self):
        return self._pmu.getBatteryPercent()

    def get_battery_voltage(self):
        return self._pmu.getBattVoltage()
