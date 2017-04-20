'''
Created on Apr 13, 2017

@author: rid
'''

import numpy
#from hammerhead import Hammerhead# the serial interface board

class BIDI_REGISTERS(object):
    '''
    classdocs
    '''
    WORD_LENGTH = 12
    HAMMERHEAD=None

    def __init__(self, _registerCount,_hammerhead, _RegisterListClass):
        '''
        Constructor
        '''
        self.registerCount = _registerCount;
        self.bitCount = _registerCount*self.WORD_LENGTH
        
        self.registers_Used = numpy.zeros(shape=(_registerCount, self.WORD_LENGTH), dtype=numpy.int)
        self.registers_Bits = numpy.zeros(shape=(_registerCount, self.WORD_LENGTH), dtype=numpy.int)
        self.register_Names = [None]*self.bitCount
        
        self.HAMMERHEAD = _hammerhead;
        self.RegisterListClass = _RegisterListClass
    
        self.initRegisters()
        
    def allBits(self):
        return self.registers_Bits.reshape(self.bitCount)
    
    def allRegistersUsage(self):
        return self.registers_Used.reshape(self.bitCount)
        
    def setRegisterParamter(self, _bitrangeArray, _registerName ):
        
        # 1. Check if defined range is available
        
        if (self.allRegistersUsage()[_bitrangeArray]!=0).any():
            
            overlapIDs_local = (self.allRegistersUsage()[_bitrangeArray]!=0)
            overlapIDs_global = _bitrangeArray[overlapIDs_local]
            oneOverlap = overlapIDs_global[0]
            
            raise IndexError("Registers are already used for {}".format( self.register_Names[oneOverlap]))
        
        for name in self.register_Names:
            if(name == _registerName):
                raise NameError("Name is already in use: {}".format( _registerName ))
        
        # 2. Register Range
        self.allRegistersUsage()[_bitrangeArray] = 1
        for i in _bitrangeArray:
            self.register_Names[i] = _registerName
        print(self.register_Names)

    def updateRegister(self,bidi_parameter,value_array):
        
        # 0. Ensure bitrange is valid
        
        assert bidi_parameter.bitrange_array.shape == value_array.shape
        
        # 1. Overwrite mentioned registers
        self.allBits()[bidi_parameter.bitrange_array] = value_array
        
        # 2. Prepare addresses and bit list
        AlteredAdresses = bidi_parameter.bitrange_array/self.WORD_LENGTH 
        UpdatedRegisters=numpy.unique( AlteredAdresses.astype(numpy.int) )
        
        # 3. Iterate over updated registers and write to Bidi
        for address in numpy.nditer(UpdatedRegisters):
            
            content = self.registers_Bits[address]
            bitstring = numpy.array2string(content,separator='')[1:-1]
            
            print(bitstring)
            #TODO: Write the stuff
            #self.HAMMERHEAD.writerd(address, int(bitstring,2))
        return True

    def initRegisters( self ):
        
        RegisterClass = self.RegisterListClass
        Registers = self.RegisterListClass.__dict__.items()
        
        for name, liste in  Registers:
            
            if not ("__") in name and not ("static") in name:
                BIDIParameter = BIDI_PARAMETER.fromListe(name,liste,self,RegisterClass)
                setattr(self, name, BIDIParameter)
            

class BIDI_PARAMETER():
    
    VAL_ISLINEAR = 0
    VAL_BITRANGE = 1
    VAL_MAPFUN = 3
            
    @staticmethod
    def linear(name, startBit,Length, BIDI):
        return BIDI_PARAMETER(name, numpy.arange(startBit,startBit+Length), BIDI)
    
    @staticmethod
    def fromListe(name,liste,BIDI,Registers):
        self = BIDI_PARAMETER
        
        if( liste[self.VAL_ISLINEAR] ):
            startBit = liste[self.VAL_BITRANGE]
            Length = liste[self.VAL_BITRANGE+1]
            bitrange = numpy.arange(startBit,startBit+Length)
        else:
            bitrange = liste[self.VAL_BITRANGE]
        
        
        if len(liste)>3:
            #print liste[self.VAL_MAPFUN]
            fun = getattr(Registers,liste[self.VAL_MAPFUN])
        else:
            fun = None    
        
        return  BIDI_PARAMETER( name, bitrange, BIDI,fun)
    
    def __init__(self,name, bitrange_array, BIDI,mapFun = None):    
        
        assert len(bitrange_array.shape) == 1
        assert bitrange_array.size>0
        
        self.BIDI = BIDI
        self.name = name
        self.bitrange_array = bitrange_array
        
        self.mapFun = mapFun
        
        BIDI.setRegisterParamter(bitrange_array,name)
        
    def set(self, newValue):
        
        if self.mapFun != None:
            newValue = self.mapFun(newValue)
        
        Length = len(self.bitrange_array)
        
        # Convert to binary
        newValue_bin = ("{0:0"+str(Length)+"b}").format(newValue)
        
        assert(len(newValue_bin)<=Length)
        
        newValue_bin_array  = numpy.zeros(shape=(Length), dtype=numpy.int)
        
        i = 0
        for char in newValue_bin:
            newValue_bin_array[i] = int(char)
            i=i+1
        
        print(newValue_bin_array)
        self.BIDI.updateRegister(self,newValue_bin_array)
    