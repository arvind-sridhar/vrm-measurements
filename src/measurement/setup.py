#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A class implementing the measurement setup
Lukas Kull, 2013
"""

import math

from measurement import equipment
from measurement.configFiles import configParent


# from Common import GF1408_MConfig
class MeasurementSetup():
#------------------------------------------------------------------------------ 
    def __init__(self, config:configParent):
        
        self.DEBUGLEVEL = 0
        # GF1408_MConfig contains the configuration of the equipment, i.e. which type, which connections between instruments.
        # self.Cfg = GF1408_MConfig.ConfigHybrid()
        # self.Cfg = GF1408_MConfig.Config()
        self.Cfg = config
        self.measSetupInit = False
        self.setupBackgroundModify = False
        
        self.MeasurementEquip = equipment.MeasurementEquipment(self.Cfg.GPIB['MODE'], self.Cfg.GPIB['ADDR'], self.Cfg.GPIB['NAME'])
        
        
    def listInstruments(self):
        return self.MeasurementEquip.listInstruments()

    def initAllInstr(self):
        if self.measSetupInit:
            return
        for name in self.Cfg.Supply:
            self.MeasurementEquip.addInstr(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'])
            self.MeasurementEquip.setMaxCurrent(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'], self.Cfg.Supply[name]['MaxCurrent'])
            # Reassure that the setting is correct
            curr = self.MeasurementEquip.getMaxCurrent(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'])
            if abs(curr - self.Cfg.Supply[name]['MaxCurrent']) / curr > 0.05:
                print('Supply ' + name + ' setting of MaxCurrent to ' + str(self.Cfg.Supply[name]['MaxCurrent']) + ' failed.')

            if 'enable4Point' in self.Cfg.Supply[name]:
                self.setSupply4Point(name, self.Cfg.Supply[name]['enable4Point'])

            # by calling the 'get' function, the GUI is updated through the sendEvent function
            self.getSupplyVoltage(name)
            self.getSupplyMaxCurrent(name)
        for name in self.Cfg.SigGen:
            typeName = ''
            if 'Type' in self.Cfg.SigGen[name]:
                typeName = self.Cfg.SigGen[name]['Type']
            self.MeasurementEquip.addInstr(self.Cfg.SigGen[name]['GPIB'], 0, typeName)
            # by calling the 'get' function, the GUI is updated through the sendEvent function
            self.getSigGenFrequency(name)
            self.getSigGenPowerDBm(name)
            # Phase offset Deg is not implemented in all SigGens
            # self.getSigGenPhaseOffsetDeg(name)
        for name in self.Cfg.Scope:
            self.MeasurementEquip.addInstr(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'])
            self.MeasurementEquip.setAveraging(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'], self.Cfg.Scope[name]['Average'])
            if 'Skew' in self.Cfg.Scope[name]:
                self.MeasurementEquip.setSkew(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'], self.Cfg.Scope[name]['Skew'])
            self.getScopeTimeRange(name)
            self.getScopeVoltageRange(name)
        self.measSetupInit = True
    def closeAllInstr(self):
        self.MeasurementEquip.closeAllInstr()
    def resetAllInstr(self):
        self.MeasurementEquip.resetAllInstr()
        # This is required to make sure, the trigger amplitude is never zero.
        for name in self.Cfg.SigGen:
            if 'DefaultPowerDBm' in self.Cfg.SigGen[name]:
                self.setSigGenPowerDBm(name, self.Cfg.SigGen[name]['DefaultPowerDBm'])
            if 'DefaultFrequency' in self.Cfg.SigGen[name]:
                self.setSigGenFrequency(name, self.Cfg.SigGen[name]['DefaultFrequency'])

    def registerEventHandler(self, equipType, name:str, equipProperty, func, scaleFactor=1, units='') -> None:
        '''Allows updating e.g. UI when instrument changes

        This function allows to register a function, which is called, when the specified instrument changes.
        eqipProperty can be e.g. Voltage, measureVoltage, Current, measureCurrent, ... see Functions below.

        :param equipType: 'Scope', 'SigGen' or 'Supply'
        :param name:
        :param equipProperty: can be e.g. Voltage, measureVoltage, Current, measureCurrent
        :param func(function): Func takes exactly one argument, which is the value.
        :param scaleFactor(float):
        :param units:
        '''
        
        if (equipType == 'Supply'):
            if not 'EventHandler' in self.Cfg.Supply[name]:
                self.Cfg.Supply[name]['EventHandler'] = {}
            self.Cfg.Supply[name]['EventHandler'][equipProperty] = {'Func': func, 'ScaleFactor': scaleFactor, 'Units': units}
        if (equipType == 'SigGen'):
            if not 'EventHandler' in self.Cfg.SigGen[name]:
                self.Cfg.SigGen[name]['EventHandler'] = {}
            self.Cfg.SigGen[name]['EventHandler'][equipProperty] = {'Func': func, 'ScaleFactor': scaleFactor, 'Units': units}
        if (equipType == 'Scope'):
            if not 'EventHandler' in self.Cfg.Scope[name]:
                self.Cfg.Scope[name]['EventHandler'] = {}
            self.Cfg.Scope[name]['EventHandler'][equipProperty] = {'Func': func, 'ScaleFactor': scaleFactor, 'Units': units}
        if (equipType == 'ControlAmplitude'):
            if not 'EventHandler' in self.Cfg.ControlAmplitude[name]:
                self.Cfg.ControlAmplitude[name]['EventHandler'] = {}
            self.Cfg.ControlAmplitude[name]['EventHandler'][equipProperty] = {'Func': func, 'ScaleFactor': scaleFactor, 'Units': units}
        if (equipType == 'ControlSkew'):
            if not 'EventHandler' in self.Cfg.ControlSkew[name]:
                self.Cfg.ControlSkew[name]['EventHandler'] = {}
            self.Cfg.ControlSkew[name]['EventHandler'][equipProperty] = {'Func': func, 'ScaleFactor': scaleFactor, 'Units': units}
    
    def getConfiguration(self):
        '''
        This function is used to return all settings in order to write them to file
        '''
        configList = list()
        if (self.measSetupInit):
            for i in self.Cfg.Supply:
                tmpList = []
                tmpList.append('Supply:' + i)
                tmpList.append('SetV:' + str(self.getSupplyVoltage(i)) + 'V')
                tmpList.append('Is4Pt:' + str(self.getSupply4Point(i)))
                tmpList.append('Voltage:' + str(self.measureSupplyVoltage(i)) + 'V')
                tmpList.append('Current:' + str(self.measureSupplyCurrent(i)) + 'A')
                configList.append(tmpList)
            for i in self.Cfg.SigGen:
                tmpList = []
                tmpList.append('SigGen:' + i)
                tmpList.append('SetPwrDBm:' + str(self.getSigGenPowerDBm(i)) + 'dBm')
                tmpList.append('SetFrequency:' + str(self.getSigGenFrequency(i)) + 'Hz')
                configList.append(tmpList)
            for i in self.Cfg.Scope:
                tmpList = []
                tmpList.append('Scope:' + i)
                tmpList.append('VoltageRange:' + str(self.getScopeVoltageRange(i)) + 'V')
                tmpList.append('TimeRange:' + str(self.getScopeTimeRange(i)) + 's')
                tmpList.append('Amplitude:' + str(self.getScopeAmplitude(i)) + 'V')
                tmpList.append('Frequency:' + str(self.getScopeFrequency(i)) + 'Hz')
                configList.append(tmpList)
        return configList
    # Simplify by returning the voltage directly when setting
    def setSupplyVoltage(self, name, volt):
        self.MeasurementEquip.setVoltage(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'], volt)
        return self.getSupplyVoltage(name)
    def setSupplyVoltageProtection(self, name, volt):
        self.MeasurementEquip.setVoltageProtection(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'], volt)
        return self.getSupplyVoltageProtection(name)
    def getSupplyVoltageProtection(self, name):
        val = self.MeasurementEquip.getVoltageProtection(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'])
        self.sendEvent('Supply', name, 'VoltageProtection', val)
        return val
    def getSupplyVoltage(self, name):
        val = self.MeasurementEquip.getVoltage(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'])
        self.sendEvent('Supply', name, 'Voltage', val)
        return val
    def setSupplyMaxCurrent(self, name, curr):
        self.MeasurementEquip.setMaxCurrent(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'], curr)
        return self.getSupplyVoltage(name)
    def getSupplyMaxCurrent(self, name):
        val = self.MeasurementEquip.getMaxCurrent(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'])
        self.sendEvent('Supply', name, 'MaxCurrent', val)
        return val
    def measureSupplyVoltage(self, name):
        val = self.MeasurementEquip.measureVoltage(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'])
        # val = round(val, 3)
        self.sendEvent('Supply', name, 'measureVoltage', val)
        return val
    def measureSupplyCurrent(self, name):
        val = self.MeasurementEquip.measureCurrent(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'])
        self.sendEvent('Supply', name, 'measureCurrent', val)
        # val = round(val, 5)
        return val
    def clearSupplyProtection(self, name):
        if self.Cfg.Supply[name]['allow4Point']:
            self.MeasurementEquip.clearProtection(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'])
            val = self.isSupplyProtectionTriggered(name)
        else:
            val = False
        return val
    def isSupplyProtectionTriggered(self, name):
        if self.Cfg.Supply[name]['allow4Point']:
            val = self.MeasurementEquip.isProtectionTriggered(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'])
        else:
            val = False
        self.sendEvent('Supply', name, 'OV', val)
        return val
    def setSupply4Point(self, name, is4Point):
        if self.Cfg.Supply[name]['allow4Point']:
            self.MeasurementEquip.set4Point(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'], is4Point)
            val = self.getSupply4Point(name)
        else:
            val = False
        return val
    def getSupply4Point(self, name):
        val = self.MeasurementEquip.get4Point(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'])
        self.sendEvent('Supply', name, '4Point', val)
        return val
    def setSigGenHarmonics(self, name, mode):
        self.MeasurementEquip.reduce_harmonics(self.Cfg.SigGen[name]['GPIB'], mode)
    def setSigGenSNR(self, name, mode):
        self.MeasurementEquip.optimize_snr(self.Cfg.SigGen[name]['GPIB'], mode)
    def setSigGenPLLPhaseNoise(self, name, mode):
        self.MeasurementEquip.optimize_pll_phasenoise(self.Cfg.SigGen[name]['GPIB'], mode)
    def setSigGenPhaseNoise(self, name, mode):
        self.MeasurementEquip.reduce_phasenoise(self.Cfg.SigGen[name]['GPIB'], mode)

    # TODO:  Simplify by returning the set power directly when setting
    def setSigGenPowerDBm(self, name, power):
        channel = 0
        if 'Channel' in self.Cfg.SigGen[name]:
            channel = self.Cfg.SigGen[name]['Channel']

        print('setSigGenPower', power)
        self.MeasurementEquip.setPowerDBm(self.Cfg.SigGen[name]['GPIB'], channel, power)
        val = self.getSigGenPowerDBm(name)
        # Set all the other signal generators, which are linked to this
        for nameC in self.Cfg.SigGenConnect:
            if self.Cfg.SigGenConnect[nameC]['SigGen'] == name:
                if ('Amplitude' in self.Cfg.SigGenConnect[nameC]['Connect']):
                    self.setSigGenPowerDBm(nameC, power)
        if name in self.Cfg.SigGenScopeConnect:
            scope = self.Cfg.SigGenScopeConnect[name]['Scope']
            if type(scope) is tuple:
                for i in range(len(scope)):
                    self.setScopeVoltageRange(scope[i], self.dBmToAmp(power) * self.Cfg.SigGenScopeConnect[name]['AmplitudeScaleFactor'])
            else:
                self.setScopeVoltageRange(scope, self.dBmToAmp(power) * self.Cfg.SigGenScopeConnect[name]['AmplitudeScaleFactor'])
        return val
    def setSigGenPowerDBmIncr(self, name, incr):
        channel = 0
        if 'Channel' in self.Cfg.SigGen[name]:
            channel = self.Cfg.SigGen[name]['Channel']

        self.MeasurementEquip.setPowerDBmIncr(self.Cfg.SigGen[name]['GPIB'], channel, incr)
    def getSigGenPowerDBm(self, name):
        channel = 0
        if 'Channel' in self.Cfg.SigGen[name]:
            channel = self.Cfg.SigGen[name]['Channel']
        val = self.MeasurementEquip.getPowerDBm(self.Cfg.SigGen[name]['GPIB'], channel)
        self.sendEvent('SigGen', name, 'Amplitude', self.dBmToAmp(val))
        return val
    def setSigGenFrequency(self, name, freq):
        if freq <= 0: freq = 1000
        channel = 0
        if 'Channel' in self.Cfg.SigGen[name]:
            channel = self.Cfg.SigGen[name]['Channel']

        self.MeasurementEquip.setFrequency(self.Cfg.SigGen[name]['GPIB'], channel, freq)
        val = self.getSigGenFrequency(name)
        # Set all the other signal generators, which are linked to this
        for nameC in self.Cfg.SigGenConnect:
            if self.Cfg.SigGenConnect[nameC]['SigGen'] == name:
                if ('Frequency' in self.Cfg.SigGenConnect[nameC]['Connect']):
                    fScaleFactor = 1
                    if 'FrequencyScaleFactor' in self.Cfg.SigGenConnect[nameC]:
                        fScaleFactor = self.Cfg.SigGenConnect[nameC]['FrequencyScaleFactor']
                    self.setSigGenFrequency(nameC, freq * fScaleFactor)
        if name in self.Cfg.SigGenScopeConnect:
            scope = self.Cfg.SigGenScopeConnect[name]['Scope']
            if type(scope) is tuple:
                for i in range(len(scope)):
                    self.setScopeTimeRange(scope[i], 1 / freq * 4)
            else:
                self.setScopeTimeRange(scope, 1 / freq * 4)
        return val
    def getSigGenFrequency(self, name):
        channel = 0
        if 'Channel' in self.Cfg.SigGen[name]:
            channel = self.Cfg.SigGen[name]['Channel']
        val = self.MeasurementEquip.getFrequency(self.Cfg.SigGen[name]['GPIB'], channel)
        self.sendEvent('SigGen', name, 'Frequency', val)
        return val
    def setSigGenPhaseOffsetDeg(self, name, deg):
        channel = 0
        if 'Channel' in self.Cfg.SigGen[name]:
            channel = self.Cfg.SigGen[name]['Channel']
        self.MeasurementEquip.setPhaseOffsetDeg(self.Cfg.SigGen[name]['GPIB'], channel, deg)
        val = self.getSigGenPhaseOffsetDeg(name)
        # self.sendEvent('Scope', name, 'VoltageRange', val)
        return val
    def getSigGenPhaseOffsetDeg(self, name):
        channel = 0
        if 'Channel' in self.Cfg.SigGen[name]:
            channel = self.Cfg.SigGen[name]['Channel']
        val = self.MeasurementEquip.getPhaseOffsetDeg(self.Cfg.SigGen[name]['GPIB'], channel)
        self.sendEvent('SigGen', name, 'PhaseOffset', val)
        return val
    def releaseAll(self):
        '''
        Release all the equipment for local control
        '''
        for name in self.Cfg.Supply:
            self.MeasurementEquip.release(self.Cfg.Supply[name]['GPIB'], self.Cfg.Supply[name]['Channel'])
        for name in self.Cfg.SigGen:
            self.MeasurementEquip.release(self.Cfg.SigGen[name]['GPIB'], 0)
        for name in self.Cfg.Scope:
            self.MeasurementEquip.release(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'])
    def setScopeTimeRange(self, name, time):
        self.MeasurementEquip.setTimeRange(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'], time)
        val = self.getScopeTimeRange(name)
        return val
    def getScopeTimeRange(self, name):
        val = self.MeasurementEquip.getTimeRange(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'])
        self.sendEvent('Scope', name, 'TimeRange', val)
        return val
    def setScopeVoltageRange(self, name, volt):
        self.MeasurementEquip.setVoltageRange(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'], volt)
        val = self.getScopeVoltageRange(name)
        return val
    def setScopeAveraging(self, name, avg):
        self.MeasurementEquip.setAveraging(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'], avg)
    def getScopeVoltageRange(self, name):
        val = self.MeasurementEquip.getVoltageRange(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'])
        self.sendEvent('Scope', name, 'VoltageRange', val)
        return val
    def clearScopeDisp(self, name):
        self.MeasurementEquip.clearDisplay(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'])
    def setTimeReference(self, name):
        self.MeasurementEquip.setTimeReference(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'])
    def getScopeAmplitude(self, name):
        val = self.MeasurementEquip.getAmplitude(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'])
        self.sendEvent('Scope', name, 'Amplitude', val)
        # val = round(val, 4)
        return val
    def getScopeFrequency(self, name):
        val = self.MeasurementEquip.getFrequency(self.Cfg.Scope[name]['GPIB'], self.Cfg.Scope[name]['Channel'])
        self.sendEvent('Scope', name, 'Frequency', val)
        # val = round(val, -5)
    def getScopeTimeDiffToChannel180(self, name):
        '''

        The 180 means that the time difference between the channels is calculated from the rising edge
        of the first channel to the falling edge of the second channel, i.e. 180 phase shift. Therefore
        the optimization is easier to get 0 deg for a clean differential signal.

        :param name(str): Instrument Name
        '''
        name1 = self.Cfg.ControlSkew[name]['Scope'][0]
        name2 = self.Cfg.ControlSkew[name]['Scope'][1]
        val = self.MeasurementEquip.getTimeDiffToChannel180(self.Cfg.Scope[name1]['GPIB'], self.Cfg.Scope[name1]['Channel'], self.Cfg.Scope[name2]['GPIB'], self.Cfg.Scope[name2]['Channel'])
        self.sendEvent('ControlSkew', name, 'Skew', val)
        return val
    def setSigGenSkew(self, name, targetPhaseSkew):
        self.setupBackgroundModify = True
        clockFreq = self.getSigGenFrequency('Clock')

        if not name in self.Cfg.ControlSkew:
            return
        typeC = self.Cfg.ControlSkew[name]['Type']

        if not typeC.lower() == 'differential':
            print("this has to be implemented (setupSetSigGenSkew)")
        
        # The first entry of sigGenList is connected to the first entry of scopeList
        sigGenList = self.Cfg.ControlSkew[name]['SigGen']
        scopeList = self.Cfg.ControlSkew[name]['Scope']

        sigGenFreq = self.getSigGenFrequency(sigGenList[0])
        sigGenTrigFreq = sigGenFreq
        # The trigger of the sampling scope needs to be <2GHz, therefore divide.
        # In order to get the frequency precise, divide by 2, 5, 10, 20, 50, 100 (only 2 addtional digits needed in siggen)
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2.5
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2.5
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        self.setSigGenFrequency('Clock', sigGenTrigFreq)

        # refresh precision time reference
        # self.setTimeReference(scopeList[0])
        # self.clearScopeDisp(scopeList[0])

        # set time range to 2 periods
        for scope in scopeList:
            self.setScopeTimeRange(scope, 2 / sigGenFreq)
        # self.clearScopeDisp(scopeList[0])
            
        # Repeat the iteration twice
        for n in range(10):
            # sigGenFreq = self.getSigGenFrequency(sigGenList[0]) # LKU
#             sigGenFreq = self.getScopeFrequency(scopeList[0])
            # set time range to 4 periods
#             for i in range(len(scopeList)):
#                 self.setScopeTimeRange(scopeList[i], 4/sigGenFreq)
                          
            self.clearScopeDisp(scopeList[0])
            measuredSkew = self.getScopeTimeDiffToChannel180(name)

            measuredPhaseOffset = measuredSkew * sigGenFreq * 360
            # print(measuredPhaseOffset)
            newPhaseOffset = targetPhaseSkew - measuredPhaseOffset

#            print('Measured Phase Off:', measuredPhaseOffset)
#            print('Target Phase Off:', targetPhaseSkew)
            print('Remaining Phase Off: ' + str(newPhaseOffset) + "(needs to be <0.1) N: " + str(n))
            
            # Stop when precision reached (0.1 deg)
            if abs(newPhaseOffset) < 0.1:
                break

            # Normalize to -180 to 179 deg.
            newPhaseOffset = (newPhaseOffset + 180) % 360 - 180
            self.setSigGenPhaseOffsetDeg(sigGenList[0], newPhaseOffset)
            if self.DEBUGLEVEL > 0: print('Target phase on SigGen: ' + str(targetPhaseSkew))
#            time.sleep(1)
        self.getScopeTimeDiffToChannel180(name)

        self.setSigGenFrequency('Clock', clockFreq)
        self.setupBackgroundModify = False
    def getSigGenSkew(self, name):
        self.setupBackgroundModify = True
        clockFreq = self.getSigGenFrequency('Clock')

        if not name in self.Cfg.ControlSkew:
            return
        typeC = self.Cfg.ControlSkew[name]['Type']

        if not typeC.lower() == 'differential':
            print("this has to be implemented (setupSetSigGenSkew)")
        
        # The first entry of sigGenList is connected to the first entry of scopeList
        sigGenList = self.Cfg.ControlSkew[name]['SigGen']
        scopeList = self.Cfg.ControlSkew[name]['Scope']

        sigGenFreq = self.getSigGenFrequency(sigGenList[0])
        sigGenTrigFreq = sigGenFreq
        # The trigger of the sampling scope needs to be <2GHz, therefore divide.
        # In order to get the frequency precise, divide by 2, 5, 10, 20, 50, 100 (only 2 addtional digits needed in siggen)
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2.5
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2.5
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        self.setSigGenFrequency('Clock', sigGenTrigFreq)

        # refresh precision time reference
        self.setTimeReference(scopeList[0])

        # set time range to 2 periods
        for scope in scopeList:
            self.setScopeTimeRange(scope, 2 / sigGenFreq)
        self.clearScopeDisp(scopeList[0])
            
        measuredSkew = self.getScopeTimeDiffToChannel180(name)

        self.setSigGenFrequency('Clock', clockFreq)
        self.setupBackgroundModify = False
        return measuredSkew
    def setSigGenAmplitude(self, name, amplitudeFS, backoff, mismatch):
        self.setupBackgroundModify = True
        clockFreq = self.getSigGenFrequency('Clock')

        amplitude = amplitudeFS * 10 ** (-backoff / 20)
        typeC = self.Cfg.ControlAmplitude[name]['Type']

        sigGenAmplitude = amplitude
        if typeC.lower() == 'differential':
            sigGenAmplitude = 0.5 * sigGenAmplitude
        if typeC.lower() == 'hybrid':
            sigGenAmplitude = sigGenAmplitude
        
        print('Desired Amplitude:', sigGenAmplitude)
        # The first entry of sigGenList is connected to the first entry of scopeList
        sigGenList = self.Cfg.ControlAmplitude[name]['SigGen']
        scopeList = self.Cfg.ControlAmplitude[name]['Scope']

        inFreq = self.getSigGenFrequency(sigGenList[0])
        sigGenTrigFreq = inFreq
        # The trigger of the sampling scope needs to be <2GHz, therefore divide.
        # In order to get the frequency precise, divide by 2, 5, 10, 20, 50, 100 (only 2 addtional digits needed in siggen)
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2.5
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2.5
        if sigGenTrigFreq > 3.2e9: sigGenTrigFreq = sigGenTrigFreq / 2
        self.setSigGenFrequency('Clock', sigGenTrigFreq)

        for scope, sigGen in zip(scopeList, sigGenList):
            voltRange = sigGenAmplitude * self.Cfg.SigGenScopeConnect[sigGen]['AmplitudeScaleFactor']
            self.setScopeVoltageRange(scope, voltRange)
        # self.clearScopeDisp(scopeList[0])
        for sigGen in sigGenList:
            currentSigGenAmplitudeDBm = self.getSigGenPowerDBm(sigGen)
            diff = self.AmpToDBm(sigGenAmplitude / 2) - self.Cfg.SigGen[sigGen]['Attenuation'] - currentSigGenAmplitudeDBm
            # self.setSigGenPowerDBm(sigGen, self.AmpToDBm(sigGenAmplitude/2)-self.Cfg.SigGen[sigGen]['Attenuation'])
            self.setSigGenPowerDBmIncr(sigGen, diff)
        
        # self.clearScopeDisp(scopeList[0])
        # refresh precision time reference
        # self.setTimeReference(scopeList[0])
        
        sigGenAmplitudeList = [sigGenAmplitude, sigGenAmplitude * 10 ** (mismatch / 20)]
        # step = 2
        # radix = 1.8
        # n = 10
        # for i in range(n):
        #     self.clearScopeDisp(scopeList[0])

        #     for scope, sigGen, sigGenAmplitude in zip(scopeList, sigGenList, sigGenAmplitudeList):
        #         currentSetAmplitudeDBm = self.getSigGenPowerDBm(sigGen)
        #         print(scope, sigGen)
        #         print('Desired Amplitude:', sigGenAmplitude)
        #         if typeC.lower() == 'hybrid':
        #             # calculate the amplitude if the two phases are not correct
        #             amp1 = self.getScopeAmplitude(scopeList[0])
        #             amp2 = self.getScopeAmplitude(scopeList[1])
        #             measuredSkew = self.MeasurementEquip.getTimeDiffToChannel180(self.Cfg.Scope[scopeList[0]]['GPIB'], self.Cfg.Scope[scopeList[0]]['Channel'], self.Cfg.Scope[scopeList[1]]['GPIB'], self.Cfg.Scope[scopeList[1]]['Channel'])

        #             phaseErrRad = measuredSkew*self.getSigGenFrequency(sigGen)*2*math.pi
        #             currentMeasuredAmplitude = ((amp1+amp2*math.cos(phaseErrRad))**2+amp2*math.sin(phaseErrRad)**2)**0.5
        #         if typeC.lower() == 'differential':
        #             currentMeasuredAmplitude = self.getScopeAmplitude(scope)

        #         print('Current Measured Amplitude:', currentMeasuredAmplitude)
        #         print('Current Set:', currentSetAmplitudeDBm)
        #         # print('Current Set Amplitude:', self.getSigGenPowerDBm(sigGen))
        #         # print('Current Set Frequency:', self.getSigGenFrequency(sigGen))

        #         if currentMeasuredAmplitude > sigGenAmplitude:
        #             currentSetAmplitudeDBm = currentSetAmplitudeDBm - step
        #         else:
        #             currentSetAmplitudeDBm = currentSetAmplitudeDBm + step

        #         print('Next Set:', currentSetAmplitudeDBm)
        #         self.setSigGenPowerDBm(sigGen, currentSetAmplitudeDBm)

        #     step = step/radix


        # # Repeat the iteration twice
        for n in range(10):
            maxDiff = 0
            self.clearScopeDisp(scopeList[0])
            for scope, sigGen, sigGenAmplitude in zip(scopeList, sigGenList, sigGenAmplitudeList):
                # print(sigGen)
                # currentMeasuredFreq = self.getScopeFrequency(scope)
                # print('Current Freq:', currentMeasuredFreq)
                currentMeasuredAmplitude = 0
                if typeC.lower() == 'hybrid':
                    # calculate the amplitude if the two phases are not correct
                    amp1 = self.getScopeAmplitude(scopeList[0])
                    amp2 = self.getScopeAmplitude(scopeList[1])
                    measuredSkew = self.MeasurementEquip.getTimeDiffToChannel180(self.Cfg.Scope[scopeList[0]]['GPIB'], self.Cfg.Scope[scopeList[0]]['Channel'], self.Cfg.Scope[scopeList[1]]['GPIB'], self.Cfg.Scope[scopeList[1]]['Channel'])
                    i = 1
                    phaseErrRad = measuredSkew * self.getSigGenFrequency(sigGenList[i]) * 2 * math.pi
                    currentMeasuredAmplitude = ((amp1 + amp2 * math.cos(phaseErrRad)) ** 2 + amp2 * math.sin(phaseErrRad) ** 2) ** 0.5
                if typeC.lower() == 'differential':
                    currentMeasuredAmplitude = self.getScopeAmplitude(scope)
                    # print(str(scope)+': Measured Amp (mV)'+str(currentMeasuredAmplitude))
                    
        #         # Redo if the amplitude is close to infinity, i.e. out of specs.
        #         # This usually happens when the amplitude on the scope
        #         # is out of range
        #         if currentMeasuredAmplitude>10:
        #             self.setSigGenPowerDBm(sigGenList[i], 0)
        #             self.clearScopeDisp(scopeList[0])
        #             if typeC.lower() == 'hybrid':
        #                 # calculate the amplitude if the two phases are not correct
        #                 amp1 = self.getScopeAmplitude(scopeList[0])
        #                 amp2 = self.getScopeAmplitude(scopeList[1])
        #                 measuredSkew = self.MeasurementEquip.getTimeDiffToChannel180(self.Cfg.Scope[scopeList[0]]['GPIB'], self.Cfg.Scope[scopeList[0]]['Channel'], self.Cfg.Scope[scopeList[1]]['GPIB'], self.Cfg.Scope[scopeList[1]]['Channel'])

        #                 phaseErrRad = measuredSkew*self.getSigGenFrequency(sigGenList[i])*2*math.pi
        #                 currentMeasuredAmplitude = ((amp1+amp2*math.cos(phaseErrRad))**2+amp2*math.sin(phaseErrRad)**2)**0.5
        #             if typeC.lower() == 'differential':
        #                 currentMeasuredAmplitude = self.getScopeAmplitude(scopeList[i])
                
        #         # if typeC.lower() == 'differential':
        #         #     # set voltage range with a factor 'AmplitudeScaleFactor'
        #         #     self.setScopeVoltageRange(scopeList[i], sigGenAmplitude*self.Cfg.SigGenScopeConnect[sigGenList[i]]['AmplitudeScaleFactor'])
        #         #     # set time range to 2 periods
        #         #     # self.setScopeTimeRange(scopeList[i], 3/currentMeasuredFreq)
        #         # if typeC.lower() == 'hybrid':
        #         #     self.setScopeVoltageRange(scopeList[0], sigGenAmplitude*self.Cfg.SigGenScopeConnect[sigGenList[i]]['AmplitudeScaleFactor'])
        #         #     self.setScopeVoltageRange(scopeList[1], sigGenAmplitude*self.Cfg.SigGenScopeConnect[sigGenList[i]]['AmplitudeScaleFactor'])
        #         #     # self.setScopeTimeRange(scopeList[0], 3/currentMeasuredFreq)
        #         #     # self.setScopeTimeRange(scopeList[1], 3/currentMeasuredFreq)
        #         self.clearScopeDisp(scopeList[0])
    
                # print('Current Amplitude:',currentMeasuredAmplitude)
                currentSigGenAmplitudeDBm = self.getSigGenPowerDBm(sigGen)
                currentSigGenAmplitude = self.dBmToAmp(currentSigGenAmplitudeDBm)
                newSigGenAmplitude = currentSigGenAmplitude / (currentMeasuredAmplitude / sigGenAmplitude)
                diffDBm = self.AmpToDBm(newSigGenAmplitude) - currentSigGenAmplitudeDBm
                maxDiff = max([maxDiff, abs(diffDBm)])
                print(str(sigGen) + ': Diff in dBm: ' + str(diffDBm) + '(needs to be <0.01) N: ' + str(n))
                if abs(diffDBm) < 0.01:
                    continue  # with next sigGen
                # print('Current SigGenAmplitude:', currentSigGenAmplitude)
                # print('New SigGenAmplitude:', newSigGenAmplitude)
                # self.setSigGenPowerDBm(sigGen, self.AmpToDBm(newSigGenAmplitude))
                self.setSigGenPowerDBmIncr(sigGen, diffDBm)
                # print(str(sigGen)+': set to dBm: '+str(self.AmpToDBm(newSigGenAmplitude)))
            
            # stop when max difference < 0.01dBm
            if maxDiff < 0.01:
                # print('Diff', diffDBm)
                break
        #         if self.DEBUGLEVEL>0: print('Target amplitude on SigGen: '+str(sigGenAmplitude))
            # time.sleep(1)
        self.setSigGenFrequency('Clock', clockFreq)
        self.setupBackgroundModify = False
    def sendEvent(self, equipType, name, equipProperty, val):
        if equipType == 'Supply':
            equip = self.Cfg.Supply
        elif equipType == 'SigGen':
            equip = self.Cfg.SigGen
        elif equipType == 'Scope':
            equip = self.Cfg.Scope
        elif equipType == 'ControlSkew':
            equip = self.Cfg.ControlSkew
        elif equipType == 'ControlAmplitude':
            equip = self.Cfg.ControlAmplitude
        if 'EventHandler' in equip[name] and equipProperty in equip[name]['EventHandler']:
            equip[name]['EventHandler'][equipProperty]['Func'](equipType, name, equipProperty, val, equip[name]['EventHandler'][equipProperty]['ScaleFactor'], equip[name]['EventHandler'][equipProperty]['Units'])
    
    def getConfig(self):
        return self.Cfg
    
    # -2dBm = 250mVp = 500mVpp
    
    def dBmToAmp(self, power):
        return (10 ** (power / 10) / 1000 * 50 * 2) ** 0.5
    def dBmToAmpRms(self, power):
        return (10 ** (power / 10) / 1000 * 50) ** 0.5
    def AmpToDBm(self, amp):
        if amp == 0:
            return -135
        return 10 * math.log(amp ** 2 * 1000 / 2 / 50, 10)
    def AmpRmsToDBm(self, amp):
        if amp == 0:
            return -135
        return 10 * math.log(amp ** 2 * 1000 / 50, 10)

