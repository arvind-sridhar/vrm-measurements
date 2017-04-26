import visa, vxi11
import time

# old Box
GPIBADDR = "9.4.68.123"
# New box
GPIBADDR = "9.4.68.124"
GPIBNAME = 'hpib'
# GPIBADDR = "0.4.68.123"
MODE = 'visa'

rm = visa.ResourceManager()


# import visa
# rm = visa.ResourceManager('@py')
# rm.list_resources()
# inst = rm.open_resource("GPIB::%i::INSTR" % 5)
# inst = rm.open_resource("TCPIP::9.4.68.124::GPIB::%i::INSTR" % 5)
# print(inst.query("*IDN?"))

pwrsuppTest = True

for i in range(3, 5):
    if MODE is 'vx11':
        instr = vxi11.Instrument(GPIBADDR, GPIBNAME+","+str(i))
    else:
        instr = rm.open_resource("GPIB::%i::INSTR" % i)

    try:
        print('ID ' + str(i) + ': ' + instr.ask("*IDN?"))
    except Exception as e:
        print('ID ' + str(i) + ':')
        #print(e)

         
# listInstruments(GPIBADDR)
# E8251A
siggenTest = False
if (siggenTest):
    siggen = vxi11.Instrument(GPIBADDR, "hpib,20")
    siggen.write("*RST")
    siggen.write("*CLS")
    siggen.write("SYST:LANG SCPI")
    print('siggen outp stat:' + siggen.ask('OUTP:STAT?'))
    siggen.write("OUTP ON")
    print('siggen outp stat:' + siggen.ask('OUTP:STAT?'))
    siggen.write("FREQ 0.45GHZ")
    print('siggen freq:' + siggen.ask('FREQ?'))
    siggen.write("FREQ 12GHZ")
    print('siggen freq:' + siggen.ask('FREQ?'))
    siggen.write("POW -5DBM")
    print('siggen pow:' + siggen.ask('POW?'))
    siggen.write("POW 50mV")
    print('siggen pow:' + siggen.ask('POW?'))

# HP8780A
siggenTestV2 = False
if (siggenTestV2):
    siggen = vxi11.Instrument(GPIBADDR, "hpib,18")
#    siggen.write("*RST")
#    siggen.write("*CLS")
    siggen.write("PR")
    siggen.write("SP0")
    siggen.write("FR 1 GZ")
    siggen.write("LV 1 DBM")
    
    siggen.write("RF0")
    siggen.write("REN")
#    siggen.write("SYST:LANG SCPI")
#    print('siggen outp stat:'+siggen.ask('OUTP:STAT?'))
#    siggen.write("OUTP ON")
#    print('siggen outp stat:'+siggen.ask('OUTP:STAT?'))
#    siggen.write("FREQ 0.45GHZ")
#    print('siggen freq:'+siggen.ask('FREQ?'))
#    siggen.write("FREQ 12GHZ")
#    print('siggen freq:'+siggen.ask('FREQ?'))
#    siggen.write("POW -5DBM")
#    print('siggen pow:'+siggen.ask('POW?'))
#    siggen.write("POW 50mV")
#    print('siggen pow:'+siggen.ask('POW?'))

# E3644A

if (pwrsuppTest):
    pwrsupp = vxi11.Instrument(GPIBADDR, "hpib,3")
    
    
    
    pwrsupp.write("*RST")
    pwrsupp.write("*CLS")
    pwrsupp.write("*VOLT:PROT:LEV 1.4V")
    print('pwrsupp volt?:' + pwrsupp.ask("VOLT?"))
    pwrsupp.write("VOLT 1.2V")
    print('pwrsupp volt?:' + pwrsupp.ask("VOLT?"))
    print('pwrsupp curr?:' + pwrsupp.ask("CURR?"))
    pwrsupp.write("VOLT:PROT:LEV 1.4V")
    print('pwrsupp volt lim?:' + pwrsupp.ask("VOLT:PROT:LEV?"))
    pwrsupp.write("VOLT 1.6V")
    print('pwrsupp volt?:' + pwrsupp.ask("VOLT?"))
    print('pwrsupp volt prot trip?:' + pwrsupp.ask("VOLT:PROT:TRIP?"))
    print('pwrsupp volt state?:' + pwrsupp.ask("VOLT:PROT:STAT?"))
    print('pwrsupp meas volt?:' + pwrsupp.ask("MEAS:VOLT?"))
    print('pwrsupp meas curr?:' + pwrsupp.ask("MEAS:CURR?"))
    pwrsupp.write("VOLT:RANG P20V")
    print('pwrsupp volt rang?:' + pwrsupp.ask("VOLT:RANG?"))
    pwrsupp.write("VOLT:RANG P8V")
    print('pwrsupp volt rang?:' + pwrsupp.ask("VOLT:RANG?"))

# N6705A
pwrsupp2Test = False
if (pwrsupp2Test):
    pwrsupp2 = vxi11.Instrument(GPIBADDR, "hpib,7")
    pwrsupp2.write("*RST")
    pwrsupp2.write("*CLS")
    print('pwrsupp2 volt?:' + pwrsupp2.ask("VOLT? (@1:4)"))
    pwrsupp2.write("VOLT 1.2V,(@1)")
    print('pwrsupp2 volt?:' + pwrsupp2.ask("VOLT? (@1:4)"))
    print('pwrsupp2 volt prot?:' + pwrsupp2.ask("VOLT:PROT:LEV? (@1:4)"))
    pwrsupp2.write("VOLT:PROT:LEV 1.4V,(@1:4)")
    print('pwrsupp2 volt prot?:' + pwrsupp2.ask("VOLT:PROT:LEV? (@1:4)"))
    pwrsupp2.write("OUTP ON,(@1:4)")
    print('pwrsupp2 outp?:' + pwrsupp2.ask("OUTP? (@1:4)"))
    pwrsupp2.write("VOLT:PROT:LEV 1.5V,(@1:4)")
    print('pwrsupp2 prot?:' + pwrsupp2.ask("VOLT:PROT:LEV? (@1:4)"))
    pwrsupp2.write("CURR:LEV 0.5A,(@1:4)")
    print('pwrsupp2 curr lev?:' + pwrsupp2.ask("CURR:LEV? (@1:4)"))
    print('pwrsupp2 meas volt?:' + pwrsupp2.ask("MEAS:VOLT? (@1:4)"))
    print('pwrsupp2 meas curr?:' + pwrsupp2.ask("MEAS:CURR? (@1:4)"))
    print('pwrsupp2 volt rang?:' + pwrsupp2.ask("VOLT:RANG? (@1:4)"))
    pwrsupp2.write("VOLT:RANG 5,(@1:4)")
    print('pwrsupp2 volt rang?:' + pwrsupp2.ask("VOLT:RANG? (@1:4)"))
    pwrsupp2.write("VOLT:SENS:SOUR INT,(@1:4)")
    print('pwrsupp2 volt sens sour?:' + pwrsupp2.ask("VOLT:SENS:SOUR? (@1:4)"))
    pwrsupp2.write("VOLT:SENS:SOUR EXT,(@1:2)")
    print('pwrsupp2 volt sens sour?:' + pwrsupp2.ask("VOLT:SENS:SOUR? (@1:4)"))
    # Allow local access to device
    pwrsupp2.write("SYST:COMM:RLST LOC")


# Infinium 86100C
scopeTest = False
if (scopeTest):
    scope = vxi11.Instrument(GPIBADDR, "hpib,7")
#    siggen = vxi11.Instrument(GPIBADDR, "hpib,20")
    print('ID ' + str(24) + ': ' + scope.ask("*IDN?"))
#    scope.write("*RST")
#    scope.write("*CLS")
#    scope.write("ACQUIRE:COUNT 1")
    scope.write("ACQUIRE:COUNT 64")
    scope.write(":ACQuire:AVERage ON")
    scope.write(":ACQuire:AVERage ON")
    scope.write("CDISPLAY")
    scope.write("TIMEBASE:RANGE 201ns")
#    scope.write("MEAS:DEF DELT,RIS,1,MIDD,FALL,1,MIDD")
#    print(scope.ask("MEAS:DELT? CHANNEL3,CHANNEL4"))
#    siggen.write("PHAS:REF")
#    siggen.write("PHAS 60DEG")
    # scope.write("CAL:SKEW CHANNEL3,5PS")
    scope.write("CHANNEL1:RANGE 900mV")
    scope.write("MEAS:SOUR CHANNEL1")
    print('scope meas vamp?:' + scope.ask("MEAS:VPP?"))
    time.sleep(2)
    print('scope meas vamp?:' + scope.ask("MEAS:VPP?"))
    time.sleep(2)
    print('scope meas vamp?:' + scope.ask("MEAS:VAMP?"))
    time.sleep(2)
    print('scope meas vamp?:' + scope.ask("MEAS:VAMP?"))
    time.sleep(2)
    print('scope meas vamp?:' + scope.ask("MEAS:VAMP?"))


#    print('scope meas freq?:'+scope.ask("MEAS:FREQ?"))
    # y-range in V
#    print('scope channel3 range?:'+scope.ask("CHANNEL3:RANGE?"))
#    scope.write("TIMEBASE:RANGE 1E-9")
#    print('scope channel3 hor range?:'+scope.ask("TIMEBASE:RANGE?"))
#    scope.write("FUNCTION1:SUBT CHANNEL3,CHANNEL4")
#    scope.write("MEAS:SOUR FUNCTION1")
#    print('scope meas vamp?:'+scope.ask("MEAS:VAMP?"))
#    print('scope meas freq?:'+scope.ask("MEAS:FREQ?"))
