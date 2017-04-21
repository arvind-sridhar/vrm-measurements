'''
Created on Apr 21, 2017

@author: rid
'''

class InstrParent():

    def setVoltage(self, volt) -> None: raise NotImplementedError
    def getVoltage(self): raise NotImplementedError
    def setVoltageProtection(self, volt:float) -> None: raise NotImplementedError
    def getVoltageProtection(self): raise NotImplementedError
    def clearDisplay(self): raise NotImplementedError
    def setMaxCurrent(self, curr:float) -> None: raise NotImplementedError
    def getMaxCurrent(self): raise NotImplementedError
    def measureVoltage(self): raise NotImplementedError
    def measureCurrent(self): raise NotImplementedError
    def release(self): raise NotImplementedError
    def set4Point(self, is4Point:bool) -> None: raise NotImplementedError
    def get4Point(self)                     : raise NotImplementedError
    # def reduce_harmonics(self, gpibAddr, mode): raise NotImplementedError
    def optimize_snr(self, mode)             : raise NotImplementedError
    def reduce_phasenoise(self, mode)       : raise NotImplementedError
    def optimize_pll_phasenoise(self, mode): raise NotImplementedError
    def setPowerDBm(self, pwr)              : raise NotImplementedError
    def setPowerDBmIncr(self, incr)        : raise NotImplementedError
    def getPowerDBm(self)->float: raise NotImplementedError
    def setFrequency(self, freq)            : raise NotImplementedError
    def getFrequency(self)->float: raise NotImplementedError
    def setTimeReference(self)              : raise NotImplementedError
    def setTimeRange(self, time)            : raise NotImplementedError
    def getTimeRange(self)                  : raise NotImplementedError
    def setVoltageRange(self, volt:float) -> None: raise NotImplementedError
    def getVoltageRange(self)               : raise NotImplementedError
    def clearProtection(self)               : raise NotImplementedError
    def isProtectionTriggered(self)         : raise NotImplementedError
    def getAmplitude(self)->float: raise NotImplementedError
    def setAveraging(self, avg) -> None       : raise NotImplementedError    
    def getTimeDiffToChannel180(self)->float: raise NotImplementedError
    def setPhaseOffsetDeg(self, deg) -> None  : raise NotImplementedError
    def getPhaseOffsetDeg(self) -> float      : raise NotImplementedError
    def setSkew(self, skew:float) -> None      : raise NotImplementedError
