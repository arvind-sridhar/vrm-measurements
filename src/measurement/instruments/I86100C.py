'''
Created on Apr 21, 2017

@author: rid

copied from lku
'''
import time

from measurement.instruments.instrParentClass import InstrParent 


class I86100C(InstrParent):
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
        # pts = self.instr.ask("WAVEFORM:POINTS?")
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
