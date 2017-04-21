'''
Created on Apr 21, 2017

@author: rid

copied from lku
'''
from measurement.instruments.instrParentClass import InstrParent 


class E8251A(InstrParent):
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
