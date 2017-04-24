'''
Created on Apr 13, 2017

@author: rid
'''

from xlrd.formula import num2strg
import numpy

from BIDI_PARAMETER import BIDI_PARAMETER


class BIDI_REGISTERS(object):
    '''
    classdocs
    '''
    WORD_LENGTH = 12
    HAMMERHEAD = None

    def __init__(self, _registerCount:int, _hammerhead, _RegisterListClass):
        '''
        Constructor
        '''
        self.registerCount = _registerCount;
        self.bitCount = _registerCount * self.WORD_LENGTH
        
        self.registers_Used = numpy.zeros(shape=(_registerCount, self.WORD_LENGTH), dtype=numpy.int)
        self.registers_Bits = numpy.zeros(shape=(_registerCount, self.WORD_LENGTH), dtype=numpy.int)
        self.register_Names = [None] * self.bitCount
        
        self.HAMMERHEAD = _hammerhead;
        self.RegisterListClass = _RegisterListClass
    
        self.initRegisters()
        
    def allBits(self):
        return self.registers_Bits.reshape(self.bitCount)
    
    def allRegistersUsage(self)->numpy.ndarray:
        
        return self.registers_Used.reshape(self.bitCount)
        
    def setRegisterParamter(self, _bitrangeArray, _registerName:str):
        
        # 1. Check if defined range is available 
        if (self.allRegistersUsage()[_bitrangeArray] != 0).any():
            
            overlapIDs_local = (self.allRegistersUsage()[_bitrangeArray] != 0)
            overlapIDs_global = _bitrangeArray[overlapIDs_local]
            oneOverlap = overlapIDs_global[0]
            
            raise IndexError("Registers are already used for {}".format(self.register_Names[oneOverlap]))
        
        for name in self.register_Names:
            if(name == _registerName):
                raise NameError("Name is already in use: {}".format(_registerName))
        
        # 2. Register Range
        self.allRegistersUsage()[_bitrangeArray] = 1
        for i in _bitrangeArray:
            self.register_Names[i] = _registerName
        print(self.register_Names)

    def updateRegister(self, bidi_parameter:BIDI_PARAMETER, value_array:numpy.ndarray) -> bool:
        
        # 0. Ensure bitrange is valid
        
        assert bidi_parameter.bitrange_array.shape == value_array.shape
        
        # 1. Overwrite mentioned registers
        self.allBits()[bidi_parameter.bitrange_array] = value_array
        
        # 2. Prepare addresses and bit list
        AlteredAdresses = bidi_parameter.bitrange_array / self.WORD_LENGTH 
        UpdatedRegisters = numpy.unique(AlteredAdresses.astype(numpy.int))
        
        # 3. Iterate over updated registers and write to Bidi
        success = True
        for address in numpy.nditer(UpdatedRegisters):
            
            content = self.registers_Bits[address]
            bitstring = numpy.array2string(content, separator='')[1:-1]
            
            print("Write to " + num2strg(address) + " : " +bitstring)
            
            # TODO: Write the stuff
            #success = success and self.HAMMERHEAD.writerd(address, int(bitstring,2))
        return success

    def initRegisters(self):
        
        RegisterClass = self.RegisterListClass
        Registers = self.RegisterListClass.__dict__.items()
        
        for name, liste in  Registers:
            
            if not ("__") in name and not ("static") in name:
                BIDIParameter = BIDI_PARAMETER.fromListe(name, liste, self, RegisterClass)
                setattr(self, name, BIDIParameter)
            
