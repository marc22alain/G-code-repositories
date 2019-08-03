#!/usr/bin/env python
import os
from Tkinter import *
from utilities import log

IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")

class AxisPrintButton(object):

    def __init__(self, master, row_num, gen_code, keep_alive=False):
        self.print_button = self.makePrintButton(master, row_num)
        self.gen_code = gen_code
        self.keep_alive = keep_alive

    def makePrintButton(self, master, row_num):
        print_button = None
        if IN_AXIS:
            print_button = Button(master, text='Write to AXIS and Quit',\
                command=self.writeToAxis)
        else:
            print_button = Button(master, text='Print', command=self.printToConsole)
        print_button.grid(row=row_num, column=0, columnspan=2)
        return print_button

    def printToConsole(self):
        log(self.gen_code())
        if not self.keep_alive:
            # since self.quit() does not work on OSX
            os._exit(0)


    def writeToAxis(self):
        sys.stdout.write(self.gen_code())
        if not self.keep_alive:
            self.quit()

    def getPrintButton(self):
        return self.print_button
