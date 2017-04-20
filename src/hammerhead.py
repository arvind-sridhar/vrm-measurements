#!/usr/bin/python
import socket, warnings
from datetime import datetime

class Hammerhead():
    def __init__(self):
        # super(Hammerhead, self).__init__()
        
        self.initH()

    def initH(self):
#        self.ADDR = '192.168.1.200'

#       self.ADDR = '9.4.208.191' #hh2 
#       self.ADDR = '9.4.208.190' #hh1 -before

        self.ADDR = '9.4.208.196'  # hh3
        
        # TODO: Fix address
#        self.ADDR = 'hh3'
        self.CHANNEL = 0
        self.PORT = 55555
        self.DEBUGLEVEL = 2
        # minimum HHSPEED setting which is working: 2, very safe is 100
        self.MODE = 0  # 0x33 for old 13s behavior
        self.HHSPEED = 100
    
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isConnected = False
    
    def connect(self):
        try:
            self.s.settimeout(3)
            print('connecting...')
            self.s.connect((self.ADDR, self.PORT))
        except Exception as e:
            
            raise Exception('Something\'s wrong with %s:%d. Exception type is %s' % (self.ADDR, self.PORT, e))
            self.isConnected = False
        else:
            self.isConnected = True
            print('done.')
        return self.isConnected
    
    def disconnect(self):
        if(self.isConnected):
            print('disconnecting...')
            self.s.close()
            self.isConnected = False
            self.initH()
            print('done.')
    
    def write(self, addr, data):
#        print addr, data
        self.s.sendall(bytes('w ' + str(addr) + ' ' + str(data) + '\n'))  # , 'ascii'))

    def read(self, addr):
        self.s.sendall(bytes('r ' + str(addr) + '\n'))  # , 'ascii'))
        return int(self.s.recv(1024))

    def readRange(self, addr):
        # addr2=addr[0:100]
        # addr = addr2
        # sendString = ""
        for i in addr:
            self.s.sendall(bytes('r ' + str(i) + '\n'))  # , 'ascii'))
            # sendString = sendString + 'r '+str(i)+'\n'
        # self.s.sendall(bytes(sendString, 'ascii'))
        leftOver = ''
        readArr = list()
        self.s.setblocking(False)
        # self.s.settimeout(0.001)
        while (len(readArr) < len(addr)):
            try:
                bArr = self.s.recv(len(addr) * 10)
            except:
                bArr = []
            # print(bArr)
            if len(bArr) > 0:
                recStr = (leftOver + bArr.decode()).split('\n')
                leftOver = recStr[-1]
                readArr.extend(recStr[0:-1])
            # else:
            #    readArr.append(leftOver)
        
        readArrInt = list()
        for i in readArr:
            try:
                readArrInt.append(int(i))
            except:
                print('Error:' + i)
        # print(len(readArrInt))
        return readArrInt
    
    def writerd(self, addr, data):
        """Write reverse data"""
        self.write(addr, self.reverseBits(data, 12))    
  
    def writera(self, addr, data): 
        """Write reverse address"""
        self.write(self.reverseBits(addr, 11), data)

    def readra(self, addr):
        return self.read(self.reverseBits(addr, 11))

    def readraRange(self, addr):
        addrR = list()
        for i in addr:
            addrR.append(self.reverseBits(i, 11))
        return self.readRange(addrR)
    
    def init(self):
        print('Initializing...')
        self.s.sendall(bytes('debug ' + str(self.DEBUGLEVEL) + '\n'))  # , 'ascii'))
        self.s.sendall(bytes('c ' + str(self.CHANNEL) + '\n'))  # , 'ascii'))
        self.s.sendall(bytes('s ' + str(self.HHSPEED) + '\n'))  # , 'ascii'))
        self.s.sendall(bytes('m ' + str(self.MODE) + '\n'))  # , 'ascii'))
        self.s.sendall(bytes('i\n'))  # , 'ascii'))
        print('done.')

    def reverseBits(self, i, nbits):
        ibin = bin(i)[2:]
        ibin = '0' * (nbits - len(ibin)) + ibin
#        print ibin
        return int(ibin[::-1], 2)
    
