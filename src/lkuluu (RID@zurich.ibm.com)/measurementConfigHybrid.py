




class Config():
#------------------------------------------------------------------------------ 
    def __init__(self):
    
    
        self.Supply = {}
        # The entries GPIB, Type, Channel, allow4Point and MaxCurrent (in A) are mandatory
        # self.Supply['VDDA'] = {'GPIB': 7, 'Channel': 1, 'allow4Point': True, 'MaxCurrent': 0.1}
        # self.Supply['VDDB'] = {'GPIB': 7, 'Channel': 2, 'allow4Point': True, 'MaxCurrent': 0.35}
        self.Supply['VDDC'] = {'GPIB': 3, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.02}
        self.Supply['VDDD'] = {'GPIB': 5, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.02}
        self.Supply['VCM_P'] = {'GPIB': 2, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.02}
        self.Supply['VCM_N'] = {'GPIB': 4, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.02}
        self.Supply['VDDA'] = {'GPIB': 6, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.02}
        self.Supply['VREF'] = {'GPIB': 1, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.02}
        
        self.SigGen = {}
        # self.SigGen['TriggerScope'] = {'GPIB': 16, 'DefaultPowerDBm': -10, 'DefaultFrequency': 1e9}
        
        self.SigGen['Clock'] = {'GPIB': 19}
        self.SigGen['Input1'] = {'GPIB': 17}
        self.SigGen['Input2'] = {'GPIB': 18}

        #self.SigGen['Clock'] = {'GPIB': 20, 'Type': 'E8251A'}
#        self.SigGen['TriggerScope'] = {'GPIB': 18, 'Type': '8780A', 'DefaultPowerDBm': -10, 'DefaultFrequency': 1e9}
        
        # Locks two SigGens to the same signal. Here, sets the SigGen 'TriggerScope' to the same input as the SigGen 'Input'
        # Possible values for 'Connect' include Frequency and Amplitude
        self.SigGenConnect = {}
        # The max sampling scope frequency is 4G for the trigger input
        # self.SigGenConnect['TriggerScope'] = {'SigGen': 'Input1', 'Connect': list(['Frequency']), 'FrequencyScaleFactor': 1}
        # #self.SigGenConnect['Input2'] = {'SigGen': 'Input1', 'Connect': list(['Frequency', 'Amplitude'])}
        self.SigGenConnect['Input2'] = {'SigGen': 'Input1', 'Connect': list(['Frequency'])}
        
        self.Scope = {}
        # # self.Scope['Input1'] = {'GPIB': 24, 'Channel': 3, 'Average': 64, 'Skew': 5*10**-12} #16 means waiting for 0.5s
        self.Scope['Input1'] = {'GPIB': 16, 'Channel': 3, 'Average': 64, 'Skew': 0} #16 means waiting for 0.5s
        self.Scope['Input2'] = {'GPIB': 16, 'Channel': 4, 'Average': 64}
        
        self.SigGenScopeConnect = {}
        # The first 'Input' refers to the Scope. It will be connected to the SigGen Input
        # Channel refers to the scope
        # self.SigGenScopeConnect['Input1'] = {'Scope': ('Input1', 'Input2'), 'AmplitudeScaleFactor': 2.1} #hybrid, 0.9 if splitter used
        # #self.SigGenScopeConnect['Input'] = {'Scope': ('Input1','Input2','add'), 'AmplitudeScaleFactor': 1.8} #0.9 if splitter used
        self.SigGenScopeConnect['Input1'] = {'Scope': 'Input1', 'AmplitudeScaleFactor': 2.1} #diff, 0.9 if splitter used
        self.SigGenScopeConnect['Input2'] = {'Scope': 'Input2', 'AmplitudeScaleFactor': 2.1} #diff, 0.9 if splitter used
        
        self.ControlAmplitude = {}
        # Type: Differential means that the amplitudes of the siggen are adjusted in a way to get them equal in size
        # on the scope and that the sum of the amplitudes is equal to the set FS amplitude (minus back-offs)
        self.ControlAmplitude['Input'] = {'Scope': list(['Input1', 'Input2']), 'SigGen': list(['Input1', 'Input2']), 'Type': 'Differential'}
        # self.ControlAmplitude['Input'] = {'Scope': list(['Input1', 'Input2']), 'SigGen': list(['Input1']), 'Type': 'Hybrid'}
        
        self.ControlSkew = {}
        # Type: Differential means that the skew of the siggen is adjusted in order to make sure the phase offset at
        # the scope is 180deg.
        self.ControlSkew['Input'] = {'Scope': list(['Input1', 'Input2']), 'SigGen': list(['Input1', 'Input2']), 'Type': 'Differential'}

# Use this class, if the input signal is generated from a single PSG with a hybrid/balun
# attached.


class Config8G():
#------------------------------------------------------------------------------ 
    def __init__(self):
    
    
        self.Supply = {}
        # The entries GPIB, Type, Channel, allow4Point and MaxCurrent (in A) are mandatory
        self.Supply['VDA'] = {'GPIB': 7, 'Channel': 3, 'allow4Point': True, 'MaxCurrent': 0.5}
#        self.Supply['VDC'] = {'GPIB': 7, 'Channel': 1, 'allow4Point': False, 'MaxCurrent': 0.5}
#        self.Supply['VDI'] = {'GPIB': 7, 'Channel': 2, 'allow4Point': True, 'MaxCurrent': 0.5}
        self.Supply['VDD'] = {'GPIB': 7, 'Channel': 4, 'allow4Point': True, 'MaxCurrent': 0.5}
        self.Supply['VCMck'] = {'GPIB': 30, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.5}
        self.Supply['VCMinp'] = {'GPIB': 29, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.5}
        self.Supply['VCMinn'] = {'GPIB': 28, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.5}
        
        self.SigGen = {}
        self.SigGen['Clock'] = {'GPIB': 19}
        self.SigGen['Input1'] = {'GPIB': 17}
        self.SigGen['Input2'] = {'GPIB': 20}
        #self.SigGen['Clock'] = {'GPIB': 20, 'Type': 'E8251A'}
        self.SigGen['TriggerScope'] = {'GPIB': 18, 'Type': '8780A', 'DefaultPowerDBm': -10, 'DefaultFrequency': 1e9}
#        self.SigGen['TriggerScope'] = {'GPIB': 19, 'DefaultPowerDBm': -10, 'DefaultFrequency': 1e9}
        
        # Locks two SigGens to the same signal. Here, sets the SigGen 'TriggerScope' to the same input as the SigGen 'Input'
        # Possible values for 'Connect' include Frequency and Amplitude
        self.SigGenConnect = {}
        # The max sampling scope frequency is 4G for the trigger input
        self.SigGenConnect['TriggerScope'] = {'SigGen': 'Input1', 'Connect': list(['Frequency']), 'FrequencyScaleFactor': 0.1}
        #self.SigGenConnect['Input2'] = {'SigGen': 'Input1', 'Connect': list(['Frequency', 'Amplitude'])}
        self.SigGenConnect['Input2'] = {'SigGen': 'Input1', 'Connect': list(['Frequency'])}
        
        self.Scope = {}
        self.Scope['Input1'] = {'GPIB': 24, 'Channel': 3, 'Average': 64, 'Skew': 5*10**-12} #16 means waiting for 0.5s
        self.Scope['Input2'] = {'GPIB': 24, 'Channel': 4, 'Average': 64}
        
        self.SigGenScopeConnect = {}
        # The first 'Input' refers to the Scope. It will be connected to the SigGen Input
        # Channel refers to the scope
        #self.SigGenScopeConnect['Input'] = {'Scope': ('Input1','Input2','add'), 'AmplitudeScaleFactor': 1.8} #0.9 if splitter used
        self.SigGenScopeConnect['Input1'] = {'Scope': 'Input1', 'AmplitudeScaleFactor': 2.1} #0.9 if splitter used
        self.SigGenScopeConnect['Input2'] = {'Scope': 'Input2', 'AmplitudeScaleFactor': 2.1} #0.9 if splitter used
        
        self.ControlAmplitude = {}
        # Type: Differential means that the amplitudes of the siggen are adjusted in a way to get them equal in size
        # on the scope and that the sum of the amplitudes is equal to the set FS amplitude (minus back-offs)
        self.ControlAmplitude['Input'] = {'Scope': list(['Input1', 'Input2']), 'SigGen': list(['Input1', 'Input2']), 'Type': 'Differential'}
        
        self.ControlSkew = {}
        # Type: Differential means that the skew of the siggen is adjusted in order to make sure the phase offset at
        # the scope is 180deg.
        self.ControlSkew['Input'] = {'Scope': list(['Input1', 'Input2']), 'SigGen': list(['Input1', 'Input2']), 'Type': 'Differential'}

# Use this class, if the input signal is generated from a single PSD with a hybrid/balun
# attached.


class ConfigHybrid():
#------------------------------------------------------------------------------ 
    def __init__(self):
    
    
        self.Supply = {}
        # The entries GPIB, Type, Channel, allow4Point and MaxCurrent (in A) are mandatory
        self.Supply['VDA'] = {'GPIB': 7, 'Channel': 3, 'allow4Point': True, 'MaxCurrent': 0.5}
        self.Supply['VDC'] = {'GPIB': 7, 'Channel': 1, 'allow4Point': False, 'MaxCurrent': 0.5}
        self.Supply['VDI'] = {'GPIB': 7, 'Channel': 2, 'allow4Point': True, 'MaxCurrent': 0.5}
        self.Supply['VDD'] = {'GPIB': 7, 'Channel': 4, 'allow4Point': True, 'MaxCurrent': 0.5}
        self.Supply['VCMck'] = {'GPIB': 30, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.5}
        self.Supply['VCMinp'] = {'GPIB': 29, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.5}
        self.Supply['VCMinn'] = {'GPIB': 28, 'Channel': 0, 'allow4Point': False, 'MaxCurrent': 0.5}
        
        self.SigGen = {}
        self.SigGen['Clock'] = {'GPIB': 16}
        self.SigGen['Input1'] = {'GPIB': 17}
#        self.SigGen['Input2'] = {'GPIB': 20}
        #self.SigGen['Clock'] = {'GPIB': 20, 'Type': 'E8251A'}
#        self.SigGen['TriggerScope'] = {'GPIB': 18, 'Type': '8780A', 'DefaultPowerDBm': -10, 'DefaultFrequency': 1e9}
        self.SigGen['TriggerScope'] = {'GPIB': 19, 'DefaultPowerDBm': -10, 'DefaultFrequency': 1e9}
        
        # Locks two SigGens to the same signal. Here, sets the SigGen 'TriggerScope' to the same input as the SigGen 'Input'
        # Possible values for 'Connect' include Frequency and Amplitude
        self.SigGenConnect = {}
        # The max sampling scope frequency is 4G for the trigger input
        self.SigGenConnect['TriggerScope'] = {'SigGen': 'Input1', 'Connect': list(['Frequency']), 'FrequencyScaleFactor': 0.1}
        #self.SigGenConnect['Input2'] = {'SigGen': 'Input1', 'Connect': list(['Frequency', 'Amplitude'])}
#        self.SigGenConnect['Input2'] = {'SigGen': 'Input1', 'Connect': list(['Frequency'])}
        
        self.Scope = {}
        self.Scope['Input1'] = {'GPIB': 24, 'Channel': 3, 'Average': 64, 'Skew': 5*10**-12} #16 means waiting for 0.5s
        self.Scope['Input2'] = {'GPIB': 24, 'Channel': 4, 'Average': 64}
        
        self.SigGenScopeConnect = {}
        # The first 'Input' refers to the Scope. It will be connected to the SigGen Input
        # Channel refers to the scope
        #self.SigGenScopeConnect['Input'] = {'Scope': ('Input1','Input2','add'), 'AmplitudeScaleFactor': 1.8} #0.9 if splitter used
        self.SigGenScopeConnect['Input1'] = {'Scope': ('Input1', 'Input2'), 'AmplitudeScaleFactor': 2.1} #0.9 if splitter used

        self.ControlAmplitude = {}
        # Type: Differential means that the amplitudes of the siggen are adjusted in a way to get them equal in size
        # on the scope and that the sum of the amplitudes is equal to the set FS amplitude (minus back-offs)
        self.ControlAmplitude['Input'] = {'Scope': list(['Input1', 'Input2']), 'SigGen': list(['Input1']), 'Type': 'Hybrid'}

        self.ControlSkew = {}
        # Type: Differential means that the skew of the siggen is adjusted in order to make sure the phase offset at
        # the scope is 180deg.
        # self.ControlSkew['Input'] = {'Scope': list(['Input1', 'Input2']), 'SigGen': list(['Input1', 'Input2']), 'Type': 'Differential'}
        
