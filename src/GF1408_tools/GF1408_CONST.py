#!/usr/bin/env python
# -*- coding: utf-8 -*- 


'''
Created on Apr 18, 2017

@author: rid
'''


class GF1408_CONST():
    
    
    HAMMERHEAD_CONNECT  = "Connect"
    HAMMERHEAD_DISCONNECT  = "Disconnect"
    HAMMERHEAD_INIT     = "Init"
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
    DT_STEP_N = 100 #ps
    DT_STEP_P = 100 #ps
    # TODO: Confirm deadtime
    
    LOADCTRL = "Load Control"
    EN_LOADCTRL = "Load clock enable"
    EN_LOADPROG = "Slow change"
    LOADCLK = "Load clock"
    LOADEN = "Set Load"
    # TODO: Confirm Load unit
    LOAD_BITS = 32
    LOAD_UNITS = u' × 13Ω'
    
    
