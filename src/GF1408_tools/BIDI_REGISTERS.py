'''
Created on Apr 13, 2017

@author: rid
'''

import numpy
import hammerhead # the serial interface board

class BIDI_REGISTERS(object):
    '''
    classdocs
    '''
    WORD_LENGTH = 12
    HAMMERHEAD=None

    def __init__(self, registerCount,hammerhead):
        '''
        Constructor
        '''
        self.registerCount = registerCount;
        self.bitCount = self.WORD_LENGTH*self.WORD_LENGTH
        self.registers_Used = numpy.zeros(shape=(registerCount, self.WORD_LENGTH))
        self.registers_Bits = numpy.zeros(shape=(registerCount, self.WORD_LENGTH))
        self.HAMMERHEAD = hammerhead;
    
    def allBits(self):
        return self.registers_Bits.reshape(self.bitCount)
    
    def allRegistersUsage(self):
        return self.registers_Used.reshape(self.bitCount)
        
    def setRegisterParamter(self, bitrange_array ):
        
        # 1. Check if defined range is available
        if (self.allRegistersUsage(self)[bitrange_array]!=0).all():
            raise IndexError()
        
        # 2. Register Range
        self.allRegistersUsage(self)[bitrange_array] = 1
        
    def updateRegister(self,bidi_parameter,value_array):
        
        # 0. Ensure bitrange is valid
        assert bidi_parameter.bitrange_array.shape == value_array.shape
        
        # 1. Overwrite mentioned registers
        self.allBits(self)[bidi_parameter.bitrange_array] = value_array
        
        # 2. Prepare addresses and bit list
        UpdatedRegisters=numpy.unique(bidi_parameter.bitrange_array/self.WORD_LENGTH)
        
        # 3. Iterate over updated registers and write to Bidi
        for address in numpy.nditer(UpdatedRegisters):
            
            content = self.registers_Bits[address]
            bitstring = numpy.array2string(content,separator='')[1:-1]
            self.HAMMERHEAD.writerd(address, int(bitstring,2))
            
        return True
    
class BIDI_PARAMETER():
    
    @classmethod
    def linear(name, startBit,Length, BIDI):
        return BIDI_PARAMETER(name, numpy.arange(startBit,startBit+1+Length), numpy.arange(0,2**Length), BIDI)
        
    def __init__(self,name, bitrange_array,allowedValues, BIDI):    
        
        assert len(bitrange_array.shape) == 1
        assert bitrange_array.size>0
        
        self.BIDI = BIDI
        self.name = name
        self.bitrange_array = bitrange_array
        self.allowedValues = allowedValues
        
    def set(self, newValue):
        
        assert newValue in self.allowedValues
        
        self.BIDI.updateRegister(self,newValue)


        