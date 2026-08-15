# source: https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G-MicroPython/blob/377b15a71fde63463ef67a450856571dc5516a8a/lib/XPowersLib.py

AXP2101_SLAVE_ADDRESS = 0x34
XPOWERS_AXP2101_STATUS1 = 0x00
XPOWERS_AXP2101_STATUS2 = 0x01
XPOWERS_AXP2101_IC_TYPE = 0x03
XPOWERS_AXP2101_INPUT_VOL_LIMIT_CTRL = 0x15
XPOWERS_AXP2101_INPUT_CUR_LIMIT_CTRL = 0x16
XPOWERS_AXP2101_DCDC5_VOL_VAL = 0x19
XPOWERS_AXP2101_VOFF_SET = 0x24
XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL = 0x27
XPOWERS_AXP2101_ADC_CHANNEL_CTRL = 0x30
XPOWERS_AXP2101_ADC_DATA_RELUST4 = 0x38
XPOWERS_AXP2101_ADC_DATA_RELUST5 = 0x39
XPOWERS_AXP2101_INTEN1 = 0x40
XPOWERS_AXP2101_INTEN2 = 0x41
XPOWERS_AXP2101_INTEN3 = 0x42
XPOWERS_AXP2101_INTSTS1 = 0x48
XPOWERS_AXP2101_INTSTS2 = 0x49
XPOWERS_AXP2101_INTSTS3 = 0x4A
XPOWERS_AXP2101_IPRECHG_SET = 0x61
XPOWERS_AXP2101_ICC_CHG_SET = 0x62
XPOWERS_AXP2101_ITERM_CHG_SET_CTRL = 0x63
XPOWERS_AXP2101_CV_CHG_VOL_SET = 0x64
XPOWERS_AXP2101_BAT_DET_CTRL = 0x68
XPOWERS_AXP2101_CHGLED_SET_CTRL = 0x69
XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL = 0x80
XPOWERS_AXP2101_DC_VOL0_CTRL = 0x82
XPOWERS_AXP2101_DC_VOL1_CTRL = 0x83
XPOWERS_AXP2101_DC_VOL2_CTRL = 0x84
XPOWERS_AXP2101_DC_VOL3_CTRL = 0x85
XPOWERS_AXP2101_DC_VOL4_CTRL = 0x86
XPOWERS_AXP2101_LDO_ONOFF_CTRL0 = 0x90
XPOWERS_AXP2101_LDO_ONOFF_CTRL1 = 0x91
XPOWERS_AXP2101_LDO_VOL0_CTRL = 0x92
XPOWERS_AXP2101_LDO_VOL1_CTRL = 0x93
XPOWERS_AXP2101_LDO_VOL4_CTRL = 0x96
XPOWERS_AXP2101_LDO_VOL5_CTRL = 0x97
XPOWERS_AXP2101_LDO_VOL6_CTRL = 0x98
XPOWERS_AXP2101_LDO_VOL7_CTRL = 0x99
XPOWERS_AXP2101_LDO_VOL8_CTRL = 0x9A
XPOWERS_AXP2101_LOW_BAT_WARN_SET = 0x1A
XPOWERS_AXP2101_BAT_PERCENT_DATA = 0xA4
XPOWERS_AXP2101_ADC_DATA_RELUST6 = 0x3A
XPOWERS_AXP2101_ADC_DATA_RELUST7 = 0x3B
XPOWERS_AXP2101_ALL_IRQ = 0xFFFFFFFF

XPOWERS_CHG_LED_OFF = 0
XPOWERS_CHG_LED_BLINK_1HZ = 1
XPOWERS_CHG_LED_BLINK_4HZ = 2
XPOWERS_CHG_LED_ON = 3
XPOWERS_CHG_LED_CTRL_CHG = 4

XPOWERS_AXP2101_BLDO1_VOL_STEPS = 100
XPOWERS_AXP2101_BLDO1_VOL_MIN = 500
XPOWERS_AXP2101_BLDO1_VOL_MAX = 3500

XPOWERS_AXP2101_BLDO2_VOL_STEPS = 100
XPOWERS_AXP2101_BLDO2_VOL_MIN = 500
XPOWERS_AXP2101_BLDO2_VOL_MAX = 3500

XPOWERS_AXP2101_DCDC3_VOL1_MIN = 500
XPOWERS_AXP2101_DCDC3_VOL1_MAX = 1200
XPOWERS_AXP2101_DCDC3_VOL_STEPS1 = 10

XPOWERS_AXP2101_DCDC3_VOL2_MIN = 1220
XPOWERS_AXP2101_DCDC3_VOL2_MAX = 1540
XPOWERS_AXP2101_DCDC3_VOL_STEPS2 = 20
XPOWERS_AXP2101_DCDC3_VOL_STEPS2_BASE = 71
XPOWERS_AXP2101_DCDC2_VOL_STEPS1 = 10
XPOWERS_AXP2101_DCDC2_VOL_STEPS2 = 20
XPOWERS_AXP2101_DCDC2_VOL1_MIN = 500

XPOWERS_AXP2101_DCDC3_VOL3_MIN = 1550
XPOWERS_AXP2101_DCDC3_VOL3_MAX = 3400
XPOWERS_AXP2101_DCDC3_VOL_STEPS3 = 100
XPOWERS_AXP2101_DCDC3_VOL_STEPS3_BASE = 88

XPOWERS_AXP2101_DCDC2_VOL_STEPS2_BASE = 71
XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MIN = 2600
XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MAX = 3300
XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_STEPS = 100

XPOWERS_AXP2101_VBUS_VOL_LIM_4V36 = 6
XPOWERS_AXP2101_VBUS_CUR_LIM_1500MA = 4
XPOWERS_AXP2101_INTSTS_CNT = 3
XPOWERS_AXP2101_ALL_IRQ = 0xFFFFFFFF
intRegister = [0] * 3
statusRegister = [0] * 3

XPOWERS_AXP2101_WARNING_LEVEL1_IRQ = 64
XPOWERS_AXP2101_WARNING_LEVEL2_IRQ = 128
XPOWERS_AXP2101_PKEY_LONG_IRQ = 1024
XPOWERS_AXP2101_BAT_REMOVE_IRQ = 4096
XPOWERS_AXP2101_BAT_INSERT_IRQ = 8192
XPOWERS_AXP2101_VBUS_REMOVE_IRQ = 16384
XPOWERS_AXP2101_VBUS_INSERT_IRQ = 32768
XPOWERS_AXP2101_PKEY_SHORT_IRQ = 2048
XPOWERS_AXP2101_BAT_CHG_START_IRQ = 524288
XPOWERS_AXP2101_BAT_CHG_DONE_IRQ = 1048576

XPOWERS_AXP2101_CHG_CUR_0MA = 0
XPOWERS_AXP2101_PRECHARGE_50MA = 2
XPOWERS_AXP2101_CHG_VOL_4V2 = 3
XPOWERS_AXP2101_CHG_CUR_200MA = 8
XPOWERS_AXP2101_CHG_ITERM_25MA = 1
XPOWERS_AXP2101_CHG_VOL_4V1 = 2
XPOWERS_AXP2101_CHG_CUR_1000MA = 16
XPOWERS_AXP2101_CHG_VOL_MAX = 6
XPOWERS_AXP2101_DCDC1_VOL_STEPS = 100
XPOWERS_AXP2101_DCDC1_VOL_MIN = 1500
XPOWERS_AXP2101_DCDC3_VOL_MIN = 500
XPOWERS_AXP2101_DCDC4_VOL_STEPS1_BASE = 0
XPOWERS_AXP2101_DCDC4_VOL_STEPS2_BASE = 71
XPOWERS_AXP2101_DCDC4_VOL_STEPS1 = 10
XPOWERS_AXP2101_DCDC4_VOL_STEPS2 = 20
XPOWERS_AXP2101_DCDC4_VOL1_MIN = 500
XPOWERS_AXP2101_DCDC4_VOL1_MAX = 1200
XPOWERS_AXP2101_DCDC4_VOL2_MIN = 1220
XPOWERS_AXP2101_DCDC4_VOL2_MAX = 1840
XPOWERS_AXP2101_DCDC5_VOL_STEPS = 100
XPOWERS_AXP2101_DCDC5_VOL_MIN = 1400
XPOWERS_AXP2101_DCDC5_VOL_1200MV = 1200
XPOWERS_AXP2101_ALDO1_VOL_STEPS = 100
XPOWERS_AXP2101_ALDO1_VOL_MIN = 500
XPOWERS_AXP2101_ALDO2_VOL_STEPS = 100
XPOWERS_AXP2101_ALDO2_VOL_MIN = 500
XPOWERS_AXP2101_ALDO3_VOL_MIN = 500
XPOWERS_AXP2101_ALDO4_VOL_MIN = 500
XPOWERS_AXP2101_CPUSLDO_VOL_STEPS = 50
XPOWERS_AXP2101_CPUSLDO_VOL_MIN = 500
XPOWERS_AXP2101_DLDO1_VOL_STEPS = 100
XPOWERS_AXP2101_DLDO1_VOL_MIN = 500
XPOWERS_AXP2101_DLDO2_VOL_STEPS = 100
XPOWERS_AXP2101_DLDO2_VOL_MIN = 500
XPOWERS_POWEROFF_4S = 0
XPOWERS_POWEROFF_6S = 1
XPOWERS_POWEROFF_8S = 2
XPOWERS_POWEROFF_10S = 3
XPOWERS_POWERON_128MS = 0
XPOWERS_POWERON_512MS = 1
XPOWERS_POWERON_1S = 2
XPOWERS_POWERON_2S = 3


# Function to simulate PMU functionalities
class XPowersPMU:
    def begin(self, i2c, address, sda, scl):
        self.i2c = i2c
        self.address = address
        try:
            # Read a register (choose an appropriate register to read for confirmation)
            i2c.readfrom_mem(
                address, 0x00, 1
            )  # Replace 0x00 with an actual register address
            return True
        except OSError:
            return False

    def readRegister(self, reg):
        try:
            return self.i2c.readfrom_mem(self.address, reg, 1)[0]
        except:  # noqa: E722
            return -1

    def readRegisterH5L8(self, highReg, lowReg):
        h5 = self.readRegister(highReg)
        l8 = self.readRegister(lowReg)
        if h5 == -1 or l8 == -1:
            return 0
        return ((h5 & 0x1F) << 8) | l8

    def readRegisterH6L8(self, highReg, lowReg):
        h6 = self.readRegister(highReg)
        l8 = self.readRegister(lowReg)
        if h6 == -1 or l8 == -1:
            return 0
        return ((h6 & 0x3F) << 8) | l8

    def writeRegister(self, reg, val):
        try:
            self.i2c.writeto_mem(self.address, reg, bytes([val]))
            return True
        except:  # noqa: E722
            return False

    def disableDC(self, num):
        if num == 1:
            return self.clrRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 0)
        elif num == 2:
            return self.clrRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 1)
        elif num == 3:
            return self.clrRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 2)
        elif num == 4:
            return self.clrRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 3)
        elif num == 5:
            return self.clrRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 4)
        return False

    def disableALDO(self, num):
        if num == 1:
            return self.clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 0)
        elif num == 2:
            return self.clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 1)
        elif num == 3:
            return self.clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 2)
        elif num == 4:
            return self.clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 3)

    def disableBLDO(self, num):
        if num == 1:
            return self.clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 4)
        elif num == 2:
            return self.clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 5)

    def disableCPUSLDO(self):
        return self.clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 6)

    def disableDLDO(self, num):
        if num == 1:
            return self.clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 7)
        elif num == 2:
            return self.clrRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 0)

    def clrRegisterBit(self, registers, bit):
        val = self.readRegister(registers)
        if val == -1:
            return False
        # Clear the specified bit
        val &= ~(1 << bit)
        return self.writeRegister(registers, val)

    def setBLDO1Voltage(self, millivolt):
        if millivolt % XPOWERS_AXP2101_BLDO1_VOL_STEPS != 0:
            print(f"Mistake ! The steps must be {XPOWERS_AXP2101_BLDO1_VOL_STEPS} mV")
            return False
        if millivolt < XPOWERS_AXP2101_BLDO1_VOL_MIN:
            print(
                f"Mistake ! BLDO1 minimum output voltage is {XPOWERS_AXP2101_BLDO1_VOL_MIN} mV"
            )
            return False
        elif millivolt > XPOWERS_AXP2101_BLDO1_VOL_MAX:
            print(
                f"Mistake ! BLDO1 maximum output voltage is {XPOWERS_AXP2101_BLDO1_VOL_MAX} mV"
            )
            return False
        val = self.readRegister(XPOWERS_AXP2101_LDO_VOL4_CTRL)
        if val == -1:
            return False
        voltage_step = (
            millivolt - XPOWERS_AXP2101_BLDO1_VOL_MIN
        ) // XPOWERS_AXP2101_BLDO1_VOL_STEPS
        val &= 0xE0
        val |= voltage_step
        return self.writeRegister(XPOWERS_AXP2101_LDO_VOL4_CTRL, val)

    def enableBLDO1(self):
        return self.setRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 4)

    def setRegisterBit(self, registers, bit):
        val = self.readRegister(registers)
        if val == -1:
            return False
        val |= 1 << bit
        return self.writeRegister(registers, val)

    def setDC3Voltage(self, millivolt):
        val = self.readRegister(XPOWERS_AXP2101_DC_VOL2_CTRL)
        if val == -1:
            return False
        val &= 0x80
        if (
            XPOWERS_AXP2101_DCDC3_VOL1_MIN
            <= millivolt
            <= XPOWERS_AXP2101_DCDC3_VOL1_MAX
        ):
            if millivolt % XPOWERS_AXP2101_DCDC3_VOL_STEPS1 != 0:
                print(
                    f"Mistake ! The steps must be {XPOWERS_AXP2101_DCDC3_VOL_STEPS1} mV"
                )
                return False
            voltage_step = (
                millivolt - XPOWERS_AXP2101_DCDC3_VOL1_MIN
            ) // XPOWERS_AXP2101_DCDC3_VOL_STEPS1
            val |= voltage_step
            return self.writeRegister(XPOWERS_AXP2101_DC_VOL2_CTRL, val)
        elif (
            XPOWERS_AXP2101_DCDC3_VOL2_MIN
            <= millivolt
            <= XPOWERS_AXP2101_DCDC3_VOL2_MAX
        ):
            if millivolt % XPOWERS_AXP2101_DCDC3_VOL_STEPS2 != 0:
                print(
                    f"Mistake ! The steps must be {XPOWERS_AXP2101_DCDC3_VOL_STEPS2} mV"
                )
                return False
            voltage_step = (
                millivolt - XPOWERS_AXP2101_DCDC3_VOL2_MIN
            ) // XPOWERS_AXP2101_DCDC3_VOL_STEPS2
            val |= voltage_step + XPOWERS_AXP2101_DCDC3_VOL_STEPS2_BASE
            return self.writeRegister(XPOWERS_AXP2101_DC_VOL2_CTRL, val)
        elif (
            XPOWERS_AXP2101_DCDC3_VOL3_MIN
            <= millivolt
            <= XPOWERS_AXP2101_DCDC3_VOL3_MAX
        ):
            if millivolt % XPOWERS_AXP2101_DCDC3_VOL_STEPS3 != 0:
                print(
                    f"Mistake ! The steps must be {XPOWERS_AXP2101_DCDC3_VOL_STEPS3} mV"
                )
                return False
            voltage_step = (
                millivolt - XPOWERS_AXP2101_DCDC3_VOL3_MIN
            ) // XPOWERS_AXP2101_DCDC3_VOL_STEPS3
            val |= voltage_step + XPOWERS_AXP2101_DCDC3_VOL_STEPS3_BASE
            return self.writeRegister(XPOWERS_AXP2101_DC_VOL2_CTRL, val)
        print(f"Mistake ! DC3 voltage {millivolt} mV is out of range")
        return False

    def enableDC3(self):
        return self.setRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 2)

    def setBLDO2Voltage(self, millivolt):
        if millivolt % XPOWERS_AXP2101_BLDO2_VOL_STEPS != 0:
            print(f"Mistake ! The steps must be {XPOWERS_AXP2101_BLDO2_VOL_STEPS} mV")
            return False
        if millivolt < XPOWERS_AXP2101_BLDO2_VOL_MIN:
            print(
                f"Mistake ! BLDO2 minimum output voltage is {XPOWERS_AXP2101_BLDO2_VOL_MIN} mV"
            )
            return False
        elif millivolt > XPOWERS_AXP2101_BLDO2_VOL_MAX:
            print(
                f"Mistake ! BLDO2 maximum output voltage is {XPOWERS_AXP2101_BLDO2_VOL_MAX} mV"
            )
            return False
        val = self.readRegister(XPOWERS_AXP2101_LDO_VOL5_CTRL)
        if val == -1:
            return False
        val &= 0xE0
        voltage_step = (
            millivolt - XPOWERS_AXP2101_BLDO2_VOL_MIN
        ) // XPOWERS_AXP2101_BLDO2_VOL_STEPS
        val |= voltage_step
        return self.writeRegister(XPOWERS_AXP2101_LDO_VOL5_CTRL, val)

    def enableBLDO2(self):
        return self.setRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 5)

    def disableTSPinMeasure(self):
        return self.clrRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 1)

    def disableBattVoltageMeasure(self):
        return self.clrRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 0)

    def disableTemperatureMeasure(self):
        return self.clrRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 4)

    def disableVbusVoltageMeasure(self):
        return self.clrRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 2)

    def disableSystemVoltageMeasure(self):
        return self.clrRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 3)

    def getChipID(self):
        return self.readRegister(XPOWERS_AXP2101_IC_TYPE)

    def setVbusVoltageLimit(self, opt):
        val = self.readRegister(XPOWERS_AXP2101_INPUT_VOL_LIMIT_CTRL)
        if val == -1:
            return False
        val &= 0xF0
        self.writeRegister(XPOWERS_AXP2101_INPUT_VOL_LIMIT_CTRL, val | (opt & 0x0F))

    def setVbusCurrentLimit(self, opt):
        val = self.readRegister(XPOWERS_AXP2101_INPUT_CUR_LIMIT_CTRL)
        if val == -1:
            return False
        val &= 0xF8
        return (
            self.writeRegister(XPOWERS_AXP2101_INPUT_CUR_LIMIT_CTRL, val | (opt & 0x07))
            == 0
        )

    def setSysPowerDownVoltage(self, millivolt):
        if millivolt % XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_STEPS:
            print(
                f"Mistake! The steps must be {XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_STEPS} mV"
            )
            return False
        if millivolt < XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MIN:
            print(
                f"Mistake! The minimum settable voltage of VSYS is {XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MIN} mV"
            )
            return False
        elif millivolt > XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MAX:
            print(
                f"Mistake! The maximum settable voltage of VSYS is {XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MAX} mV"
            )
            return False
        val = self.readRegister(XPOWERS_AXP2101_VOFF_SET)
        if val == -1:
            return False
        val &= 0xF8
        new_value = (
            millivolt - XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_MIN
        ) // XPOWERS_AXP2101_VSYS_VOL_THRESHOLD_STEPS
        return self.writeRegister(XPOWERS_AXP2101_VOFF_SET, val | new_value) == 0

    def enableBattDetection(self):
        return self.setRegisterBit(XPOWERS_AXP2101_BAT_DET_CTRL, 0)

    def enableVbusVoltageMeasure(self):
        return self.setRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 2)

    def enableBattVoltageMeasure(self):
        return self.setRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 0)

    def enableSystemVoltageMeasure(self):
        return self.setRegisterBit(XPOWERS_AXP2101_ADC_CHANNEL_CTRL, 3)

    def disableIRQ(self, opt):
        return self.setInterruptImpl(opt, False)

    def setInterruptImpl(self, opts, enable):
        res = 0
        data = 0
        value = 0
        # print(f"{'ENABLE' if enable else 'DISABLE'} - HEX: 0x{opts:X}")
        if opts & 0x0000FF:  # Check if any of the lower 8 bits are set
            value = opts & 0xFF
            # Read current INTEN1 register value
            data = self.readRegister(XPOWERS_AXP2101_INTEN1)
            intRegister[0] = (data | value) if enable else (data & ~value)
            res |= self.writeRegister(XPOWERS_AXP2101_INTEN1, intRegister[0])
        if opts & 0x00FF00:  # Check if the next 8 bits are set
            value = (opts >> 8) & 0xFF
            # Read current INTEN2 register value
            data = self.readRegister(XPOWERS_AXP2101_INTEN2)
            intRegister[1] = (data | value) if enable else (data & ~value)
            res |= self.writeRegister(XPOWERS_AXP2101_INTEN2, intRegister[1])
        if opts & 0xFF0000:  # Check if the highest 8 bits are set
            value = (opts >> 16) & 0xFF
            # Read current INTEN3 register value
            data = self.readRegister(XPOWERS_AXP2101_INTEN3)
            intRegister[2] = (data | value) if enable else (data & ~value)
            res |= self.writeRegister(XPOWERS_AXP2101_INTEN3, intRegister[2])
        return res == 0

    def clearIrqStatus(self):
        for i in range(XPOWERS_AXP2101_INTSTS_CNT):
            self.writeRegister(XPOWERS_AXP2101_INTSTS1 + i, 0xFF)
            statusRegister[i] = 0

    def enableIRQ(self, opt):
        return self.setInterruptImpl(opt, True)

    def setPrechargeCurr(self, opt):
        val = self.readRegister(XPOWERS_AXP2101_IPRECHG_SET)
        if val == -1:
            return
        val &= 0xFC
        self.writeRegister(XPOWERS_AXP2101_IPRECHG_SET, val | opt)

    def setChargerConstantCurr(self, opt):
        if opt > XPOWERS_AXP2101_CHG_CUR_1000MA:
            return False
        val = self.readRegister(XPOWERS_AXP2101_ICC_CHG_SET)
        if val == -1:
            return False
        val &= 0xE0
        return self.writeRegister(XPOWERS_AXP2101_ICC_CHG_SET, val | opt) == 0

    def setChargerTerminationCurr(self, opt):
        val = self.readRegister(XPOWERS_AXP2101_ITERM_CHG_SET_CTRL)
        if val == -1:
            return
        val &= 0xF0
        self.writeRegister(XPOWERS_AXP2101_ITERM_CHG_SET_CTRL, val | opt)

    def setChargeTargetVoltage(self, opt):
        if opt >= XPOWERS_AXP2101_CHG_VOL_MAX:
            return False
        val = self.readRegister(XPOWERS_AXP2101_CV_CHG_VOL_SET)
        if val == -1:
            return False
        val &= 0xF8
        return self.writeRegister(XPOWERS_AXP2101_CV_CHG_VOL_SET, val | opt) == 0

    def getLowBatWarnThreshold(self):
        val = self.readRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET)
        if val == -1:
            return 0
        val &= 0xF0
        val >>= 4
        return val

    def setLowBatWarnThreshold(self, percentage):
        if percentage < 5 or percentage > 20:
            return
        val = self.readRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET)
        if val == -1:
            return
        val &= 0x0F
        new_value = val | ((percentage - 5) << 4)
        self.writeRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET, new_value)

    def getLowBatShutdownThreshold(self):
        val = self.readRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET)
        if val == -1:
            return 0
        return val & 0x0F

    def setLowBatShutdownThreshold(self, opt):
        opt = min(opt, 15)
        val = self.readRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET)
        if val == -1:
            return
        val &= 0xF0
        self.writeRegister(XPOWERS_AXP2101_LOW_BAT_WARN_SET, val | opt)

    def getRegisterBit(self, registers, bit):
        val = self.readRegister(registers)
        if val == -1:
            return False
        return (val & (1 << bit)) != 0

    def isBatteryConnect(self):
        return self.getRegisterBit(XPOWERS_AXP2101_STATUS1, 3)

    def getBattVoltage(self):
        if not self.isBatteryConnect():
            return 0
        return self.readRegisterH5L8(XPOWERS_AXP2101_BAT_PERCENT_DATA)

    def isVbusGood(self):
        return self.getRegisterBit(XPOWERS_AXP2101_STATUS1, 5)

    def isVbusIn(self):
        return (
            self.getRegisterBit(XPOWERS_AXP2101_STATUS2, 3) == 0 and self.isVbusGood()
        )

    def getVbusVoltage(self):
        if not self.isVbusIn():
            return 0
        return self.readRegisterH6L8(
            XPOWERS_AXP2101_ADC_DATA_RELUST4, XPOWERS_AXP2101_ADC_DATA_RELUST5
        )

    def getSystemVoltage(self):
        return self.readRegisterH6L8(
            XPOWERS_AXP2101_ADC_DATA_RELUST6, XPOWERS_AXP2101_ADC_DATA_RELUST7
        )

    def getBatteryPercent(self):
        if not self.isBatteryConnect():
            return -1
        return self.readRegister(XPOWERS_AXP2101_BAT_PERCENT_DATA)

    def getChargerConstantCurr(self):
        val = self.readRegister(XPOWERS_AXP2101_ICC_CHG_SET)
        if val == -1:
            return 0
        return val & 0x1F

    def isEnableDC(self, num):
        if num == 1:
            return self.getRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 0)
        elif num == 2:
            return self.getRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 1)
        elif num == 3:
            return self.getRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 2)
        elif num == 4:
            return self.getRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 3)
        elif num == 5:
            return self.getRegisterBit(XPOWERS_AXP2101_DC_ONOFF_DVM_CTRL, 4)

    def getDCVoltage(self, num):
        if num == 1:
            return (
                self.readRegister(XPOWERS_AXP2101_DC_VOL0_CTRL) & 0x1F
            ) * XPOWERS_AXP2101_DCDC1_VOL_STEPS + XPOWERS_AXP2101_DCDC1_VOL_MIN
        elif num == 2:
            val = self.readRegister(XPOWERS_AXP2101_DC_VOL1_CTRL)
            if val == -1:
                return 0
            val &= 0x7F
            if val < XPOWERS_AXP2101_DCDC2_VOL_STEPS2_BASE:
                return (
                    val * XPOWERS_AXP2101_DCDC2_VOL_STEPS1
                ) + XPOWERS_AXP2101_DCDC2_VOL1_MIN
            else:
                return (val * XPOWERS_AXP2101_DCDC2_VOL_STEPS2) - 200
            return 0
        elif num == 3:
            val = self.readRegister(XPOWERS_AXP2101_DC_VOL2_CTRL) & 0x7F
            if val == -1:
                return 0
            val &= 0x7F
            if val < XPOWERS_AXP2101_DCDC3_VOL_STEPS2_BASE:
                return (
                    val * XPOWERS_AXP2101_DCDC3_VOL_STEPS1
                ) + XPOWERS_AXP2101_DCDC3_VOL_MIN
            elif (
                val >= XPOWERS_AXP2101_DCDC3_VOL_STEPS2_BASE
                and val < XPOWERS_AXP2101_DCDC3_VOL_STEPS3_BASE
            ):
                return (val * XPOWERS_AXP2101_DCDC3_VOL_STEPS2) - 200
            else:
                return (val * XPOWERS_AXP2101_DCDC3_VOL_STEPS3) - 7200
            return 0
        elif num == 4:
            val = self.readRegister(XPOWERS_AXP2101_DC_VOL3_CTRL)
            if val == -1:
                return 0
            val &= 0x7F
            if val < XPOWERS_AXP2101_DCDC4_VOL_STEPS2_BASE:
                return (
                    val * XPOWERS_AXP2101_DCDC4_VOL_STEPS1
                ) + XPOWERS_AXP2101_DCDC4_VOL1_MIN
            else:
                return (val * XPOWERS_AXP2101_DCDC4_VOL_STEPS2) - 200
            return 0
        elif num == 5:
            val = self.readRegister(XPOWERS_AXP2101_DC_VOL4_CTRL)
            if val == -1:
                return 0
            val &= 0x1F
            if val == XPOWERS_AXP2101_DCDC5_VOL_VAL:
                return XPOWERS_AXP2101_DCDC5_VOL_1200MV
            return (
                val * XPOWERS_AXP2101_DCDC5_VOL_STEPS
            ) + XPOWERS_AXP2101_DCDC5_VOL_MIN

    def isEnableALDO(self, num):
        if num == 1:
            return self.getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 0)
        elif num == 2:
            return self.getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 1)
        elif num == 3:
            return self.getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 2)
        elif num == 4:
            return self.getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 3)

    def getALDOVoltage(self, num):
        if num == 1:
            val = self.readRegister(XPOWERS_AXP2101_LDO_VOL0_CTRL) & 0x1F
            return val * XPOWERS_AXP2101_ALDO1_VOL_STEPS + XPOWERS_AXP2101_ALDO1_VOL_MIN
        elif num == 2:
            val = self.readRegister(XPOWERS_AXP2101_LDO_VOL1_CTRL) & 0x1F
            return val * XPOWERS_AXP2101_ALDO2_VOL_STEPS + XPOWERS_AXP2101_ALDO2_VOL_MIN
        elif num == 3:
            val = self.readRegister(XPOWERS_AXP2101_LDO_VOL1_CTRL) & 0x1F
            return val * XPOWERS_AXP2101_ALDO2_VOL_STEPS + XPOWERS_AXP2101_ALDO3_VOL_MIN
        elif num == 4:
            val = self.readRegister(XPOWERS_AXP2101_LDO_VOL1_CTRL) & 0x1F
            return val * XPOWERS_AXP2101_ALDO2_VOL_STEPS + XPOWERS_AXP2101_ALDO4_VOL_MIN

    def isEnableBLDO(self, num):
        if num == 1:
            return self.getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 4)
        elif num == 2:
            return self.getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 5)

    def getBLDOVoltage(self, num):
        if num == 1:
            val = self.readRegister(XPOWERS_AXP2101_LDO_VOL4_CTRL)
            if val == -1:
                return 0
            val &= 0x1F
            return val * XPOWERS_AXP2101_BLDO1_VOL_STEPS + XPOWERS_AXP2101_BLDO1_VOL_MIN
        elif num == 2:
            val = self.readRegister(XPOWERS_AXP2101_LDO_VOL5_CTRL)
            if val == -1:
                return 0
            val &= 0x1F
            return val * XPOWERS_AXP2101_BLDO2_VOL_STEPS + XPOWERS_AXP2101_BLDO2_VOL_MIN

    def isEnableCPUSLDO(self):
        return self.getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 6)

    def getCPUSLDOVoltage(self):
        val = self.readRegister(XPOWERS_AXP2101_LDO_VOL6_CTRL)
        if val == -1:
            return 0
        val &= 0x1F
        return val * XPOWERS_AXP2101_CPUSLDO_VOL_STEPS + XPOWERS_AXP2101_CPUSLDO_VOL_MIN

    def isEnableDLDO(self, num):
        if num == 1:
            return self.getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL0, 7)
        elif num == 2:
            return self.getRegisterBit(XPOWERS_AXP2101_LDO_ONOFF_CTRL1, 0)

    def getDLDOVoltage(self, num):
        if num == 1:
            val = self.readRegister(XPOWERS_AXP2101_LDO_VOL7_CTRL)
            if val == -1:
                return 0
            val &= 0x1F
            return val * XPOWERS_AXP2101_DLDO1_VOL_STEPS + XPOWERS_AXP2101_DLDO1_VOL_MIN
        if num == 2:
            val = self.readRegister(XPOWERS_AXP2101_LDO_VOL8_CTRL)
            if val == -1:
                return 0
            val &= 0x1F
            return val * XPOWERS_AXP2101_DLDO2_VOL_STEPS + XPOWERS_AXP2101_DLDO2_VOL_MIN

    def getIrqStatus(self):
        status_register = [
            self.readRegister(XPOWERS_AXP2101_INTSTS1),
            self.readRegister(XPOWERS_AXP2101_INTSTS2),
            self.readRegister(XPOWERS_AXP2101_INTSTS3),
        ]
        return (
            (status_register[0] << 16) | (status_register[1] << 8) | status_register[2]
        )

    def IS_BIT_SET(self, value, bitmask):
        return (value & bitmask) != 0

    def getChargingLedMode(self):
        val = self.readRegister(XPOWERS_AXP2101_CHGLED_SET_CTRL)
        if val == -1:
            return XPOWERS_CHG_LED_OFF
        val >>= 1
        if (val & 0x02) == 0x02:
            val >>= 4
            return val & 0x03
        return XPOWERS_CHG_LED_CTRL_CHG

    def setChargingLedMode(self, mode):
        if mode == XPOWERS_CHG_LED_ON:
            val = self.readRegister(XPOWERS_AXP2101_CHGLED_SET_CTRL)
            if val == -1:
                return
            val &= 0xC8
            val |= 0x05
            val |= mode << 4
            self.writeRegister(XPOWERS_AXP2101_CHGLED_SET_CTRL, val)
        elif mode == XPOWERS_CHG_LED_CTRL_CHG:
            val = self.readRegister(XPOWERS_AXP2101_CHGLED_SET_CTRL)
            if val == -1:
                return
            val &= 0xF9
            self.writeRegister(XPOWERS_AXP2101_CHGLED_SET_CTRL, val | 0x01)

    def setPowerKeyPressOffTime(self, opt):
        val = self.readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL)
        if val == -1:
            return False
        val &= 0xF3
        return (
            self.writeRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL, val | (opt << 2))
            == 0
        )

    def getPowerKeyPressOffTime(self):
        return (self.readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL) & 0x0C) >> 2

    def setPowerKeyPressOnTime(self, opt):
        val = self.readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL)
        if val == -1:
            return False
        val &= 0xFC
        return 0 == self.writeRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL, val | opt)

    def getPowerKeyPressOnTime(self):
        val = self.readRegister(XPOWERS_AXP2101_IRQ_OFF_ON_LEVEL_CTRL)
        if val == -1:
            return 0
        return val & 0x03

    def isVbusInsertIrq(self):
        mask = XPOWERS_AXP2101_VBUS_INSERT_IRQ >> 8
        if intRegister[1] & mask:
            return self.IS_BIT_SET(statusRegister[1], mask)
        return False

    def isVbusRemoveIrq(self):
        mask = XPOWERS_AXP2101_VBUS_REMOVE_IRQ >> 8
        if intRegister[1] & mask:
            return self.IS_BIT_SET(statusRegister[1], mask)
        return False

    def isBatInsertIrq(self):
        mask = XPOWERS_AXP2101_BAT_INSERT_IRQ >> 8
        if intRegister[1] & mask:
            return self.IS_BIT_SET(statusRegister[1], mask)
        return False

    def isBatRemoveIrq(self):
        mask = XPOWERS_AXP2101_BAT_REMOVE_IRQ >> 8
        if intRegister[1] & mask:
            return self.IS_BIT_SET(statusRegister[1], mask)
        return False

    def isPekeyShortPressIrq(self):
        mask = XPOWERS_AXP2101_PKEY_SHORT_IRQ >> 8
        if intRegister[1] & mask:
            return self.IS_BIT_SET(statusRegister[1], mask)
        return False

    def isPekeyLongPressIrq(self):
        mask = XPOWERS_AXP2101_PKEY_LONG_IRQ >> 8
        if intRegister[1] & mask:
            return self.IS_BIT_SET(statusRegister[1], mask)
        return False

    def isCharging(self):
        return (self.readRegister(XPOWERS_AXP2101_STATUS2) >> 5) == 0x01
