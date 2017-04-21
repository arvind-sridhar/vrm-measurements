'''
Created on Apr 21, 2017

@author: rid

copied from lku
'''

from measurement.instruments.instrParentClass import InstrParent 

class SMU2420(InstrParent):
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
    