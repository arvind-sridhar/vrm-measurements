#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A class implementing different sub-classes for measurement equipment
Lukas Kull, 2013

rid:Edited 2016
"""

import vxi11, visa

from measurement.instruments import *
from measurement.instruments.instrParentClass import InstrParent


# If a function is called on a wrong object and is not available,an error occurs
class MeasurementEquipment():
#------------------------------------------------------------------------------ 
    def __init__(self, gpibMode, gpibAddr=0, gpibName=""):

        # Import and decorate functions
        for fname in dir( InstrParent):
            
            def methodX(self, gpibAddr, channel, *kwars):
                return getattr(self.instrDict[gpibAddr][channel], fname)(*kwars)
            
            if not fname.startswith("__"):
                setattr(self, fname, methodX)
        
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
        elif instrId == 'Broken':
            instrObj = E8251ABroken(instr, channel, alreadyExisting)
            raise NotImplementedError
        
        
        else:
            print('Instrument ' + instrId + ' at GPIB port ' + str(gpibAddr) + ' not supported.')
            return
        # The gpib Address  and channel number are added, since one 'device' per channel
        # is added.
        
        # If no device was added, a sub-dict has to be created first.
        if not gpibAddr in self.instrDict:
            self.instrDict[gpibAddr] = {}
        
        self.instrDict[gpibAddr][channel] = instrObj
        
        
    '''
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

    '''

