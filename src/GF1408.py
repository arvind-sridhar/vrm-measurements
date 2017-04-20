#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Apr 12, 2017

@author: rid
'''

import sys
from PyQt5 import QtWidgets
from GF1408_tools.GF1408_GUI import GF1408_GUI



def main():
    app = QtWidgets.QApplication(sys.argv)
    a = GF1408_GUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()