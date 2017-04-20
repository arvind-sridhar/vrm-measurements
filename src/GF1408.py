#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on Apr 12, 2017

@author: rid
'''

import sys

from PyQt5.QtWidgets import QApplication


from GF1408_tools.GF1408_GUI import GF1408_GUI
from warnings import catch_warnings



def main():

    app = QApplication(sys.argv)
    GF1408_GUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()