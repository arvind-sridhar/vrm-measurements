'''
Created on Apr 21, 2017

@author: rid
'''

from measurement.configFiles import configParent

class GF1408config(configParent):
    '''
    classdocs
    
    '''
    
    VDD_MAXI = 0.25
    VD_MAXI = 0.02
    FAST_CLK = "FAST_CLK"
    VDD = 'VDD'
    VD = 'VD'
    
    def __init__(self):
        '''
        Constructor
        '''
        super(GF1408config, self).__init__()
        
        
        
        cls = self.__class__
        
        self.Supply['VDD']  = self.makeSupply(3, 0, False, cls.VDD_MAXI)
        self.Supply['VD']   = self.makeSupply(4, 0, False, cls.VD_MAXI)
        
        for name in self.Supply:
            print(name)
        
        
        '''
        CLK_NAME = cls.FAST_CLK
        self.SigGen[CLK_NAME] = {'GPIB': 17}
        self.SigGenConnect['Input2'] = {'SigGen': CLK_NAME, 'Connect': list(['Frequency'])}
        
        # # self.Scope['Input1'] = {'GPIB': 24, 'Channel': 3, 'Average': 64, 'Skew': 5*10**-12} #16 means waiting for 0.5s
        self.Scope['Input1'] = {'GPIB': 16, 'Channel': 3, 'Average': 64, 'Skew': 0}  # 16 means waiting for 0.5s
        self.Scope['Input2'] = {'GPIB': 16, 'Channel': 4, 'Average': 64}
        
        # The first 'Input' refers to the Scope. It will be connected to the SigGen Input
        # Channel refers to the scope
        self.SigGenScopeConnect['Input1'] = {'Scope': 'Input1', 'AmplitudeScaleFactor': 2.1} 
        self.SigGenScopeConnect['Input2'] = {'Scope': 'Input2', 'AmplitudeScaleFactor': 2.1} 
        
        # Type: Differential means that the amplitudes of the siggen are adjusted in a way
        # to get them equal in size on the scope and that the sum of the amplitudes is equal
        # to the set FS amplitude (minus back-offs)
        self.ControlAmplitude['Input']  = { 'Scope': list(['Input1', 'Input2']),
                                           'SigGen': list(['Input1', 'Input2']), 
                                             'Type': 'Differential'}
        
        
        self.ControlSkew['Input']       = { 'Scope': list(['Input1', 'Input2']), 
                                           'SigGen': list(['Input1', 'Input2']), 
                                             'Type': 'Differential'}
        
        # Type: Differential means that the skew of the siggen is adjusted in order to make
        # sure the phase offset at the scope is 180deg.
        '''