'''
Created on Apr 21, 2017

@author: rid
'''

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

    def makeSupply(self,_GPIB:int,_Channel:int,_allow4Point:bool,_MaxCurrent:float)->dict:
        return {'GPIB': _GPIB, 'Channel': _Channel, 'allow4Point': _allow4Point, 'MaxCurrent': _MaxCurrent}
    
    @staticmethod
    def singleton():
        self = configParent
        
        if(self.INST==None):
            return self()
        return self.INST
