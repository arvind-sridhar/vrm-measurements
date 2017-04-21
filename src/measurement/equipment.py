#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A class implementing different sub-classes for measurement equipment
Lukas Kull, 2013
"""

import time, vxi11, visa


class MeasurementEquipment():
#------------------------------------------------------------------------------ 
    def __init__(self, gpibMode, gpibAddr=0, gpibName=""):
        
        self.GPIBADDRESS = gpibAddr
        self.GPIBNAME = gpibName
        # self.GPIBADDRESS = "0.4.68.123"
        self.VOLTAGEPROTECTIONLEVEL = 1.05
        # Equivalent to 2Vpp,diff
        self.POWERPROTECTIONLEVELDBM = 15
        self.instrDict = {}

        # self.MODE = 'vx11'
        # self.MODE = 'visa'
        self.MODE = gpibMode
        
        if self.MODE is 'visa':
            self.rm = visa.ResourceManager()
        
    def listInstruments(self):
        strRet = ''
        for i in range(0, 31):
            if self.MODE is 'vx11':
                instr = vxi11.Instrument(self.GPIBADDRESS, self.GPIBNAME + "," + str(i))
            else:
                instr = self.rm.open_resource("GPIB::%i::INSTR" % i)

            try:
                strRet = strRet + 'ID ' + str(i) + ': ' + instr.ask("*IDN?") + '\n'
            except:
                strRet = strRet + 'ID ' + str(i) + ':'
        return strRet
    def closeAllInstr(self):
        for gpibAddr in self.instrDict:
            for channel in self.instrDict[gpibAddr]:
                self.instrDict[gpibAddr][channel].close()
    def resetAllInstr(self):
        for gpibAddr in self.instrDict:
            alreadyReset = False
            for channel in self.instrDict[gpibAddr]:
                # A device at a certain channel has to be reset only once, not
                # once per channel.
                self.instrDict[gpibAddr][channel].reset(alreadyReset)
                alreadyReset = True
    
    # channel is the channel of the power supply if it is a multiple channel supply
    def addInstr(self, gpibAddr, channel=0, typeName=''):
        instr = None
        # It seems that the Ethernet-GPIB box does not support too many sockets.
        # Therefore reuse the same connection for multiple channels and do 
        # not open a separate connection to the same instrument for each channel.
        alreadyExisting = gpibAddr in self.instrDict
        if alreadyExisting:
            for ch in self.instrDict[gpibAddr]:
                # First instr is ok, as all are the same.
                instr = self.instrDict[gpibAddr][ch].getInstr()
                break
        else:
            if self.MODE is 'vx11':
                # instr = vxi11.Instrument(self.GPIBADDRESS, "hpib,"+str(gpibAddr))
                instr = vxi11.Instrument(self.GPIBADDRESS, self.GPIBNAME + "," + str(gpibAddr))
            else:
                instr = self.rm.open_resource("GPIB::%i::INSTR" % gpibAddr)

        # Use equipment name, which is second in a list of comma-separated
        # values, returned by IDN. Strip spaces.
        instrId = typeName
        if typeName == '':
            try:
                instrId = instr.ask("*IDN?").split(',')[1].strip()
            except Exception as e:
                raise Exception('GPIB: Something\'s wrong with GPIB %d (wrong ID, not connected, powered off?). Exception type is %s' % (gpibAddr, e))
                
        print('ID ' + str(gpibAddr) + ': ' + instrId)
        
        # find out if this gpibAddr was already used once. This would mean
        # that the specified equipment was already initialized. This helps
        # to prevent double reset and clearing of other presets.
        # Therefore pass the alreadyExisting to the object
        if instrId == 'E3644A' or instrId == 'E3642A' or instrId == 'E3633A':
            instrObj = E3644A(instr, self.VOLTAGEPROTECTIONLEVEL, alreadyExisting)
        elif instrId == 'N6705A':
            instrObj = N6705A(instr, channel, self.VOLTAGEPROTECTIONLEVEL, alreadyExisting)
        elif instrId == 'N6705B':
            instrObj = N6705B(instr, channel, self.VOLTAGEPROTECTIONLEVEL, alreadyExisting)
        elif instrId == 'E8251A' or instrId == 'E8257C' or instrId == 'E8257D':
            instrObj = E8251A(instr, self.POWERPROTECTIONLEVELDBM, alreadyExisting)
        elif instrId == 'MODEL 2420':
            instrObj = SMU2420(instr, self.POWERPROTECTIONLEVELDBM, alreadyExisting)
        elif instrId == '86100C':
            instrObj = I86100C(instr, channel, alreadyExisting)
        elif instrId == '8780A':
            instrObj = H8780A(instr, channel, alreadyExisting)
        else:
            print('Instrument ' + instrId + ' at GPIB port ' + str(gpibAddr) + ' not supported.')
            return
        # The gpib Address  and channel number are added, since one 'device' per channel
        # is added.
        
        # If no device was added, a sub-dict has to be created first.
        if not gpibAddr in self.instrDict:
            self.instrDict[gpibAddr] = {}
        
        self.instrDict[gpibAddr][channel] = instrObj
        
    # If a function is called on a wrong object and is not available,
    # an error occurs
    def setVoltage(self, gpibAddr, channel, volt):
        self.instrDict[gpibAddr][channel].setVoltage(volt)
    def getVoltage(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].getVoltage()
    def setVoltageProtection(self, gpibAddr, channel, volt):
        self.instrDict[gpibAddr][channel].setVoltageProtection(volt)
    def getVoltageProtection(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].getVoltageProtection()
    def clearDisplay(self, gpibAddr, channel):
        self.instrDict[gpibAddr][channel].clearDisplay()
    def setMaxCurrent(self, gpibAddr, channel, curr):
        self.instrDict[gpibAddr][channel].setMaxCurrent(curr)
    def getMaxCurrent(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].getMaxCurrent()
    def measureVoltage(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].measureVoltage()
    def measureCurrent(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].measureCurrent()
    def release(self, gpibAddr, channel):
        self.instrDict[gpibAddr][channel].release()
    def set4Point(self, gpibAddr, channel, is4Point):
        self.instrDict[gpibAddr][channel].set4Point(is4Point)
    def get4Point(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].get4Point()
    def reduce_harmonics(self, gpibAddr, mode):
        self.instrDict[gpibAddr][0].lowband_filter(mode)
    def optimize_snr(self, gpibAddr, mode):
        self.instrDict[gpibAddr][0].optimize_snr(mode)
    def reduce_phasenoise(self, gpibAddr, mode):
        self.instrDict[gpibAddr][0].reduce_phasenoise(mode)
    def optimize_pll_phasenoise(self, gpibAddr, mode):
        self.instrDict[gpibAddr][0].optimize_pll_phasenoise(mode)
    def setPowerDBm(self, gpibAddr, channel, pwr):
        self.instrDict[gpibAddr][channel].setPowerDBm(pwr)
    def setPowerDBmIncr(self, gpibAddr, channel, incr):
        self.instrDict[gpibAddr][channel].setPowerDBmIncr(incr)
    def getPowerDBm(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].getPowerDBm()
    def setFrequency(self, gpibAddr, channel, freq):
        self.instrDict[gpibAddr][channel].setFrequency(freq)
    def getFrequency(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].getFrequency()
    def setTimeReference(self, gpibAddr, channel):
        self.instrDict[gpibAddr][channel].setTimeReference()
    def setTimeRange(self, gpibAddr, channel, time):
        self.instrDict[gpibAddr][channel].setTimeRange(time)
    def getTimeRange(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].getTimeRange()
    def setVoltageRange(self, gpibAddr, channel, volt):
        self.instrDict[gpibAddr][channel].setVoltageRange(volt)
    def getVoltageRange(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].getVoltageRange()
    def clearProtection(self, gpibAddr, channel):
        self.instrDict[gpibAddr][channel].clearProtection()
    def isProtectionTriggered(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].isProtectionTriggered()
    def getAmplitude(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].getAmplitude()
    def setAveraging(self, gpibAddr, channel, avg):
        self.instrDict[gpibAddr][channel].setAveraging(avg)
    def getTimeDiffToChannel180(self, gpibAddr, channel, gpibAddr2, channel2):
        return self.instrDict[gpibAddr][channel].getTimeDiffToChannel180(self.instrDict[gpibAddr2][channel2].getSourceName())
    def setPhaseOffsetDeg(self, gpibAddr, channel, deg):
        self.instrDict[gpibAddr][channel].setPhaseOffsetDeg(deg)
    def getPhaseOffsetDeg(self, gpibAddr, channel):
        return self.instrDict[gpibAddr][channel].getPhaseOffsetDeg()
    def setSkew(self, gpibAddr, channel, skew):
        self.instrDict[gpibAddr][channel].setSkew(skew)
#    def setPowerOffsetDBm(self, gpibAddr, channel, pwr):
#        self.instrDict[gpibAddr][channel].setPowerOffsetDBm(pwr)
#    def getPowerOffsetDBm(self, gpibAddr, channel):
#        return self.instrDict[gpibAddr][channel].getPowerOffsetDBm()

#===============================================================================
# 
#===============================================================================

class E3644A():
    """Agilent DC Power Supply"""
    # channel is not used in this class
    def __init__(self, instr, voltageProtectionLevel, alreadyReset):
        self.instr = instr
        # Double protection: set max voltage in pwr supply
        # and do not allow setting of higher voltage in Python
        self.voltageProtectionLevel = voltageProtectionLevel

        # Reset is currently called separately when the button is
        # pressed.
        
        # Set maximum allowed voltage level
        self.instr.write("VOLT:PROT:LEV " + str(voltageProtectionLevel) + 'V')
        # Init to 0V
        self.instr.write("VOLT:RANG P8V")
    def reset(self, alreadyReset=False):
        if not alreadyReset:
            self.instr.write("*RST")
            self.instr.write("*CLS")
        self.instr.write("VOLT 0V")
        self.instr.write("OUTP ON")
    def setVoltage(self, volt):
        if volt > self.voltageProtectionLevel:
            print('Voltage too high! Set: ' + str(volt) + ', Allowed: ' + str(self.voltageProtectionLevel))
            return
        self.instr.write("VOLT " + str(volt) + "V")
        self.instr.write("OUTP ON")
    def getVoltage(self):
        return float(self.instr.ask("VOLT?"))
    def setMaxCurrent(self, curr):
        self.instr.write("CURR:LEV " + str(curr) + "A")
    def getMaxCurrent(self):
        return float(self.instr.ask("CURR:LEV?"))
    def measureVoltage(self):
        return float(self.instr.ask("MEAS:VOLT?"))
    def measureCurrent(self):
        return float(self.instr.ask("MEAS:CURR?"))
    def get4Point(self):
        return False
    def release(self):
        # Release remote control by GPIB and allow local control
        # If it is not working, try instr.unlock() or inst.local()
        self.instr.write("SYST:COMM:RLST LOC")
    def getInstr(self):
        return self.instr
    def close(self):
        self.instr.close()

#===============================================================================
# 
#===============================================================================

class SMU2420():
    """Keithley 2420 Source Meter"""
    # channel is not used in this class
    def __init__(self, instr, voltageProtectionLevel, alreadyReset):
        self.instr = instr
        # Double protection: set max voltage in pwr supply
        # and do not allow setting of higher voltage in Python
        self.voltageProtectionLevel = voltageProtectionLevel

        # Reset is currently called separately when the button is
        # pressed.
        
        # Set maximum allowed voltage level
        self.instr.write("SOUR:VOLT:PROT:LEV " + str(voltageProtectionLevel))
        # Init to 0V
        # self.instr.write("VOLT:RANG P8V")
    def reset(self, alreadyReset=False):
        if not alreadyReset:
            self.instr.write("*RST")
            self.instr.write("*CLS")
        self.instr.write("VOLT 0V")
        self.instr.write("OUTP ON")
    def setVoltage(self, volt):
        if volt > self.voltageProtectionLevel:
            print('Voltage too high! Set: ' + str(volt) + ', Allowed: ' + str(self.voltageProtectionLevel))
            return
        self.instr.write("SOUR:VOLT:LEV " + str(volt))
        # self.instr.write("OUTP ON")
    def getVoltage(self):
        return float(self.instr.ask("SOUR:VOLT:IMM:AMPL?"))
    def setMaxCurrent(self, curr):
        self.instr.write("SENS:CURR:PROT:LEV " + str(curr))
    def getMaxCurrent(self):
        return float(self.instr.ask("SENS:CURR:PROT:LEV?"))
    def measureVoltage(self):
        self.instr.write("INIT")  # Initialize
        out = str.split(self.instr.ask("FETC?"), ',')  # split the string.
        return float(out[0])

    def measureCurrent(self):
        self.instr.write("INIT")  # Initialize
        out = str.split(self.instr.ask("FETC?"), ',')  # split the string.
        return float(out[1])

    def get4Point(self):
        return False
    def release(self):
        # Release remote control by GPIB and allow local control
        # If it is not working, try instr.unlock() or inst.local()
        self.instr.write("SYST:COMM:RLST LOC")
    def getInstr(self):
        return self.instr
    def close(self):
        self.instr.close()

#===============================================================================
#  One class equals one channel of the N6705
#===============================================================================

class N6705A():
    """4 channel power supply"""
    def __init__(self, instr, channel, voltageProtectionLevel, alreadyReset):
        self.instr = instr
        self.channel = channel
        self.voltageProtectionLevel = voltageProtectionLevel
        # Set maximum allowed voltage level
        self.instr.write("VOLT:PROT:LEV " + str(voltageProtectionLevel) + "V,(@" + str(channel) + ")")
        # Init to 0V
        self.instr.write("VOLT:RANG 5,(@" + str(channel) + ")")
    def reset(self, alreadyReset=False):
        if not alreadyReset:
            self.instr.write("*RST")
            self.instr.write("*CLS")
        self.instr.write("VOLT:SENS:SOUR INT,(@" + str(self.channel) + ")")
        self.instr.write("VOLT 0V,(@" + str(self.channel) + ")")
        self.instr.write("OUTP ON,(@" + str(self.channel) + ")")
    def setVoltage(self, volt):
        if volt > self.voltageProtectionLevel:
            print('Voltage too high! Set: ' + str(volt) + ', Allowed: ' + str(self.voltageProtectionLevel))
            return
        self.instr.write("VOLT " + str(volt) + "V,(@" + str(self.channel) + ")")
        self.instr.write("OUTP ON,(@" + str(self.channel) + ")")
    def getVoltage(self):
        return float(self.instr.ask("VOLT? (@" + str(self.channel) + ")"))
    def setVoltageProtection(self, volt):
        self.voltageProtectionLevel = volt
        self.instr.write("VOLT:PROT:LEV " + str(self.voltageProtectionLevel) + "V,(@" + str(self.channel) + ")")
    def getVoltageProtection(self):
        return float(self.instr.ask("VOLT:PROT:LEV? (@" + str(self.channel) + ")"))
    def setMaxCurrent(self, curr):
        self.instr.write("CURR:LEV " + str(curr) + "A,(@" + str(self.channel) + ")")
    def getMaxCurrent(self):
        return float(self.instr.ask("CURR:LEV? (@" + str(self.channel) + ")"))
    def measureVoltage(self):
        return float(self.instr.ask("MEAS:VOLT? (@" + str(self.channel) + ")"))
    def measureCurrent(self):
        return float(self.instr.ask("MEAS:CURR? (@" + str(self.channel) + ")"))
    def clearProtection(self):
        self.instr.write("POW:PROT:CLE (@" + str(self.channel) + ")")
    def isProtectionTriggered(self):
        # return self.instr.ask("POW:PROT:CLE? (@"+str(self.channel)+")")
        return False
    # Enable or disable 4 point measurement. EXT means enable
    def set4Point(self, is4Point):
        if is4Point:
            self.instr.write("VOLT:SENS:SOUR EXT,(@" + str(self.channel) + ")")
        else:
            self.instr.write("VOLT:SENS:SOUR INT,(@" + str(self.channel) + ")")
    def get4Point(self):
        return self.instr.ask("VOLT:SENS:SOUR? (@" + str(self.channel) + ")") == "EXT"
    def release(self):
        # Release remote control by GPIB and allow local control
        # If it is not working, try instr.unlock() or inst.local()
        self.instr.write("SYST:COMM:RLST LOC")
    def getInstr(self):
        return self.instr
    def close(self):
        self.instr.close()

class N6705B(N6705A):
    def __init__(self, instr, channel, voltageProtectionLevel, alreadyReset):
        N6705A.__init__(self, instr, channel, voltageProtectionLevel, alreadyReset)
    def setMaxCurrent(self, curr):
        self.instr.write("CURR:LIM " + str(curr) + ",(@" + str(self.channel) + ")")
    def getMaxCurrent(self):
        return float(self.instr.ask("CURR:LIM? (@" + str(self.channel) + ")"))

class E8251A():
    """Signal generators"""
    # channel is not used in this class
    def __init__(self, instr, powerProtectionLevel, alreadyReset):
        self.instr = instr
        self.powerProtectionLevel = powerProtectionLevel
        self.highPowerProtectionLevel = powerProtectionLevel + 5
        self.highPowerThreshold = 7e9
        self.highPowerThreshold2 = 20e9
        # Set maximum allowed voltage level
        self.instr.write("UNIT:POWER DBM")
        self.instr.write("OUTP ON")

    def reset(self, alreadyReset=False):
        if not alreadyReset:
            self.instr.write("*RST")
            self.instr.write("*CLS")
        self.instr.write("POW -135DBM")
        self.instr.write("OUTP ON")

    # set Power in dBm
    def setPowerDBm(self, power):
        if power > self.powerProtectionLevel:
            freq = self.getFrequency()
            if freq < self.highPowerThreshold or (power > self.highPowerProtectionLevel and freq < self.highPowerThreshold2):
                print('Power too high! Set: ' + str(power) + ', Allowed: ' + str(self.powerProtectionLevel))
                return
        # print(power)
        self.setPowerDBmIncr(power - self.getPowerDBm())
        # self.instr.write("POW "+str(power)+"DBM")

    def setPowerDBmIncr(self, incr):
        power = self.getPowerDBm()
        if (power + incr) > self.powerProtectionLevel:
            freq = self.getFrequency()
            if freq < self.highPowerThreshold or ((power + incr) > self.highPowerProtectionLevel and freq < self.highPowerThreshold2):
                print('Power too high! Set: ' + str(power) + ', Allowed: ' + str(self.powerProtectionLevel))
                return
        self.instr.write("POW:STEP " + str(round(abs(incr), 2)) + "DB")
        if incr < 0:
            self.instr.write("POW DOWN")
        else:
            self.instr.write("POW UP")
            
    def getPowerDBm(self):
        return float(self.instr.ask("POW?"))
    def setFrequency(self, freq):
        if freq < self.highPowerThreshold:
            if self.getPowerDBm() > self.powerProtectionLevel:
                self.setPowerDBm(self.powerProtectionLevel - 5)
                print('Power reduced for safety because frequency is too low.')
        self.instr.write("FREQ " + str(freq) + "HZ")
    def getFrequency(self):
        return float(self.instr.ask("FREQ?"))
    def setPhaseOffsetDeg(self, deg):
        self.instr.write("PHAS:REF")
        self.instr.write("PHAS " + str(deg) + "DEG")
    def getPhaseOffsetDeg(self):
        return float(self.instr.ask("PHAS?")) / 2 / 3.1415926 * 360
#    def setPowerOffsetDBm(self, power):
#        self.instr.write("POW:OFFS "+str(power)+"DBM")
#    def getPowerOffsetDBm(self):
#        return float(self.instr.ask("POW:OFFS?"))
    def lowband_filter(self, mode):
        print('reduce_harmonics:', mode)
        # This filter reduces harmonics below 2GHz
        # mode 1: on, mode 0: off
        self.instr.write("LBF " + str(mode))
    def optimize_snr(self, mode):
        print('optimize_snr:', mode)
        # Optimize the attenuator and ALC to provide optimal SNR
        # mode 1: on, mode 0: off
        self.instr.write("POW:NOIS " + str(mode))
    def reduce_phasenoise(self, mode):
        # enables low phase for < 250 MHz
        print('reduce_phasenoise:', mode)
        if mode == 0:
            self.instr.write("FREQ:LBP NORM")
        else:
            self.instr.write("FREQ:LBP LNO")

    def optimize_pll_phasenoise(self, mode):
        # sets the PLL bandwidth to optimize phase noise
        # for offset above (mode 2) and below (mode 1) 150kHz
        print('optimize_pll_phasenoise:', mode)
        self.instr.write("FREQ:SYNT " + str(mode))

            
    def release(self):
        # Release remote control by GPIB and allow local control
        # If it is not working, try instr.unlock() or inst.local()
        self.instr.write("SYST:COMM:RLST LOC")
    def getInstr(self):
        return self.instr
    def close(self):
        self.instr.close()

class E8251ABroken(E8251A):
    def __init__(self, instr, powerProtectionLevel, alreadyReset):
        self.E8251A.__init__(self, instr, powerProtectionLevel, alreadyReset)
        
        self.validRangeList = {100000000.0: [(0.13, 0.13), (0.16999999999999998, 0.17699999999999999), (0.23999999999999994, 0.24099999999999994), (0.3999999999999998, 0.40799999999999981), (0.70999999999999963, 0.71899999999999964)], 1100000000.0: [(0.20999999999999996, 0.20999999999999996), (0.34999999999999987, 0.35399999999999987), (0.61999999999999977, 0.62599999999999978)], 6100000000.0: [(0.19999999999999996, 0.20199999999999996), (0.33999999999999986, 0.34199999999999986), (0.59999999999999976, 0.60399999999999976)], 8100000000.0: [(0.19999999999999996, 0.19999999999999996), (0.32999999999999985, 0.33799999999999986), (0.58999999999999975, 0.59799999999999975)], 10100000000.0: [(0.18999999999999995, 0.19799999999999995), (0.32999999999999985, 0.33399999999999985), (0.57999999999999974, 0.58899999999999975)], 12100000000.0: [(0.18999999999999995, 0.19699999999999995), (0.32999999999999985, 0.33399999999999985), (0.58999999999999975, 0.59099999999999975)], 14100000000.0: [(0.18999999999999995, 0.19199999999999995), (0.3199999999999999, 0.3249999999999999), (0.53999999999999981, 0.54899999999999982), (0.56299999999999972, 0.57699999999999974), (0.96999999999999953, 0.97499999999999953)], 2990000000.0: [(0.20999999999999996, 0.21399999999999997), (0.35999999999999988, 0.36199999999999988), (0.63999999999999968, 0.63999999999999968)], 18100000000.0: [(0.15999999999999998, 0.16499999999999998), (0.17799999999999999, 0.18199999999999997), (0.29999999999999993, 0.30799999999999994), (0.5199999999999998, 0.5209999999999998), (0.9199999999999996, 0.9229999999999996)], 19900000000.0: [(0.15999999999999998, 0.16299999999999998), (0.29999999999999993, 0.30199999999999994), (0.50999999999999979, 0.51099999999999979), (0.89999999999999958, 0.90399999999999958)], 16100000000.0: [(0.15999999999999998, 0.16899999999999998), (0.17799999999999999, 0.18699999999999997), (0.30999999999999994, 0.31599999999999995), (0.5299999999999998, 0.53299999999999981), (0.93999999999999961, 0.94499999999999962)], 2500000000.0: [(0.20999999999999996, 0.21299999999999997), (0.35999999999999988, 0.36099999999999988), (0.62999999999999967, 0.63699999999999968)], 2100000000.0: [(0.20999999999999996, 0.21099999999999997), (0.34999999999999987, 0.35699999999999987), (0.61999999999999977, 0.62899999999999978)], 3100000000.0: [(0.20999999999999996, 0.21399999999999997), (0.35999999999999988, 0.36099999999999988), (0.62999999999999967, 0.63699999999999968)], 4100000000.0: [(0.19999999999999996, 0.20499999999999996), (0.33999999999999986, 0.34599999999999986), (0.60999999999999976, 0.61299999999999977)]}
#    def setPowerDBm(self, power):
#        amp = 
#        if power > self.powerProtectionLevel:
#            print('Power too high! Set: '+str(power)+', Allowed: '+str(self.powerProtectionLevel))
#            return
#        freq = self.getFrequency()
#        # Find closest frequency match
#        err = 1e20
#        bestMatchFreq = 0
#        for i in self.validRangeList.keys():
#            if abs(i-freq) < err:
#                err = abs(i-freq)
#                bestMatchFreq = i
#        
#        self.validVoltage = False
#        for i in self.validRangeList[bestMatchFreq]:
#            if 
#        self.instr.write("POW "+str(power)+"DBM")

class H8780A():
    # channel is not used in this class
    def __init__(self, instr, powerProtectionLevel, alreadyReset):
        self.instr = instr
        self.powerProtectionLevel = powerProtectionLevel

        # Since this device does not allow to read out all the values,
        # they are stored in local variables.
        self.currentFreq = 0
        self.currentAmpDBm = -110
        # Set maximum allowed voltage level
        
    def reset(self, alreadyReset=False):
        if not alreadyReset:
            self.instr.write("PR")
            self.instr.write("SP0")
        self.instr.write("LV -110 DBM")
        self.instr.write("RF1")
    # set Power in dBm
    def setPowerDBm(self, power):
        if power > self.powerProtectionLevel:
            print('Power too high! Set: ' + str(power) + ', Allowed: ' + str(self.powerProtectionLevel))
            return
        self.instr.write("LV " + str(power) + " DBM")
        self.currentAmpDBm = power
        self.instr.write("RF1")
    def getPowerDBm(self):
        return self.currentAmpDBm
    def setFrequency(self, freq):
        self.instr.write("FR " + str(freq) + " HZ")
        self.currentFreq = freq
    def getFrequency(self):
        return self.currentFreq
    def release(self):
        # Release remote control by GPIB and allow local control
        # If it is not working, try instr.unlock() or inst.local()
        return
#        self.instr.write("RL1")
    def getInstr(self):
        return self.instr
    def close(self):
        self.instr.close()

class I86100C():
    """Sampling Scope"""
    # channel is not used in this class
    def __init__(self, instr, channel, alreadyReset):
        self.instr = instr
        self.channel = channel
        
        # if not alreadyReset:
        #    self.reset()
        self.source = 'CHANNEL' + str(self.channel)
        # self.setSource()
        self.instr.write(self.source + " ON")
    def setSource(self):
        self.instr.write("MEAS:SOUR " + str(self.source))
    def getSourceName(self):
        return self.source

    def reset(self, alreadyReset=False):
        if not alreadyReset:
        # Reset everything and clear registers
            self.instr.write("*RST")
            self.instr.write("*CLS")
        self.instr.write(self.source + " ON")
    # set Power in dBm
    def getAmplitude(self):
        # Convert to reasonable value
        self.setSource()
        r = 0
        try:
            # VAMP seems to measure unprecise compared to VPP
            # r = self.instr.ask("MEAS:VAMP?")
            r = self.instr.ask("MEAS:VPP?")
        except:
            r = 0
        return float(r)
    def getFrequency(self):
        self.setSource()
        # Convert to reasonable value
        r = 0
        try:
            r = self.instr.ask("MEAS:FREQ?")
        except:
            r = 0
        return float(r)
    def setTimeReference(self):
        self.instr.write("TIMEBASE:PRECISION:TREFERENCE")
    def setTimeRange(self, time):
        self.setSource()
        self.instr.write("TIMEBASE:RANGE " + str(time))
    def setAveraging(self, avg):
        self.setSource()
        self.instr.write("ACQUIRE:COUNT " + str(avg))
        self.instr.write("ACQUIRE:POINTS 3000")
        self.instr.write("ACQUIRE:AVERAGE ON")
    def setSkew(self, skew):
        self.setSource()
        self.instr.write("CAL:SKEW " + self.getSourceName() + "," + str(skew))
    def clearDisplay(self):
        self.setSource()
        avg = self.instr.ask("ACQUIRE:COUNT?")
        #pts = self.instr.ask("WAVEFORM:POINTS?")
        # print('Waveform points:', int(pts))
        self.instr.write("CDISPLAY")
        # time.sleep(int(avg)*0.033)
        time.sleep(int(avg) * 0.1)
        # self.instr.write("CDISP")
    def getTimeRange(self):
        self.setSource()
        return float(self.instr.ask("TIMEBASE:RANGE?"))
    def setVoltageRange(self, volt):
        self.instr.write(str(self.source) + ":RANGE " + str(volt))
    def getVoltageRange(self):
        return float(self.instr.ask(str(self.source) + ":RANGE?"))
    # Returns the time between the rising edge of the first channel and the falling edge
    # of the second channel.
    def getTimeDiffToChannel180(self, channel):
        self.instr.write("MEAS:DEF DELT,RIS,1,MIDD,FALL,1,MIDD")
        return float(self.instr.ask("MEAS:DELT? " + str(self.source) + "," + str(channel)))

    def release(self):
        # Release remote control by GPIB and allow local control
        # If it is not working, try instr.unlock() or inst.local()
        self.instr.write("SYST:COMM:RLST LOC")
    def getInstr(self):
        return self.instr
    def close(self):
        self.instr.close()
