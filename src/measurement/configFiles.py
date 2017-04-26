'''
Created on Apr 21, 2017

@author: rid
'''

from hammerhead import Hammerhead

class configParent():
    '''
    classdocs
    '''
    INST = None

    def __init__(self):
        '''
        Constructor
        '''
        self.Supply = {}
        self.SigGen = {}
        self.SigGenConnect = {}
        # The max sampling scope frequency is 4G for the trigger input
        self.Scope = {}
        self.SigGenScopeConnect = {}
        # The first 'Input' refers to the Scope. It will be connected to the SigGen Input
        # Channel refers to the scope
        self.ControlAmplitude = {}
        self.ControlSkew = {}
        
        
        
        self.GPIB = {}
        #self.GPIB['MODE'] = 'vx11'
        self.GPIB['MODE'] = 'visa'
        #self.GPIB['ADDR'] = '9.4.68.123'
        #self.GPIB['NAME'] = 'gpib0' #gpib0 for the keysight E5810B and hpib for the old LAN box
        self.GPIB['NAME'] = 'hpib' #gpib0 for the keysight E5810B and hpib for the old LAN box
        self.GPIB['ADDR'] = '9.4.68.124'

        self.HH = {}
        self.HH['ADDR'] = Hammerhead.HOST #'hh3.zurich.ibm.com'
        
    def makeSupply(self,_GPIB:int,_Channel:int,_allow4Point:bool,_MaxCurrent:float)->dict:
        return {'GPIB': _GPIB, 'Channel': _Channel, 'allow4Point': _allow4Point, 'MaxCurrent': _MaxCurrent}
    
