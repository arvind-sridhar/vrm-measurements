#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Created on Apr 18, 2017

@author: rid
'''


class CONST():


    HAMMERHEAD_CONNECT_AND_INIT = "Init Hammerhead"
    HAMMERHEAD_DISCONNECT = "Disconnect"
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

    DUTY_BITS = 5
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
    # TODO: Confirm Load unit
    LOAD_BITS = 32
    LOAD_UNITS = u' × 13Ω'

    EQUIPMENT = "Equipment"
    EQ_VIN = "V<sub>in</sub>"
    EQ_INMAX = "I<sub>in,max</sub>"

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
    ONOFF = "On/Off"
    VINon = "VinOn"
    Vdon = "VdOn"
    FGon = "FGOn"
