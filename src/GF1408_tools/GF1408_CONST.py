#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Created on Apr 18, 2017

@author: rid
'''


class CONST():


    HAMMERHEAD_CONNECT_AND_INIT = "Init Hammerhead"
    HAMMERHEAD_DISCONNECT = "Disconnect Hammerhead"
    SET_ALL_REGISTERS = "Set all registers"
    HAMMERHEAD_INIT = "Init"
    EXIT = "Exit"
    DPWM = "DPWM Control"
    EN_DPWM = "Enable DPWM"
    RST_DPWM = "Reset DPWM"
    DUTY = "Duty Cycle"
    DT_N = "D-Time(N)"
    DT_P = "D-Time(P)"
    PHASE = "Phase"
    SHIFT = "Shift"
    EN_ALLPHASES = "Enable all phases"
    CONNECTING = "Connecting..."
    
    DUTY_BITS = 4
    DT_BITS_N = 3
    DT_BITS_P = 3
    DT_STEP_N = 100  # ps
    DT_STEP_P = 100  # ps
    # TODO: Confirm deadtime

    LOADCTRL = "Load Control"
    EN_LOADCTRL = "Load clock enable"
    EN_LOADPROG = "Slow change"
    LOADCLK = "Load clock"
    LOADEN = "Set Load"
    LOAD_BITS = 32
    LOAD_UNITS = u' × 17Ω'
    LOAD_CK_ARR = ["CK2", "CK4" , "CK8" , "CK16"];

    EQUIPMENT = "Equipment"
    EQ_VIN = "V<sub>in</sub>"
    EQ_INMAX = "I<sub>in,max</sub>"
    EQ_VOUT = "V<sub>out</sub>"
    EQ_Vd = "V<sub>d</sub>"
    EQ_IdMAX = "I<sub>d,max</sub>"

    EQ_FREQ_AC = "V<sub>clk</sub>"
    EQ_FREQ_DC = "V<sub>clk,DC</sub>"
    EQ_FREQ_F = "f<sub>clk</sub>"

    UNIT_MV = " mV"
    UNIT_MA = " mA"
    UNIT_MHZ = " MHz"

    SYNC = "Sync"
    VALUE = "Value"
    NAME = "Name"
    REFERENCE = "Reference"
    INSTRUMENTS_CONNECT_AND_INIT = "Init instruments"
    INSTRUMENTS_DISCONNECT = "Disconnect instruments"
    ONOFF = "On/Off"
    VINon = "VinOn"
    Vdon = "VdOn"
    FGon = "FGOn"
    VOuton = "VOuton"
    
    DEG_STR = [u"0°", u"90°" , u"180°" , u"270°"]
    
        
