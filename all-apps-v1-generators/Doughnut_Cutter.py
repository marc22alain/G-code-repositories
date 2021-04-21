#!/usr/bin/env python

from Doughnut_Cutter_class import DoughnutCutter
from Setup_class import Setup

setup = Setup()
app = DoughnutCutter(None, 	setup)
app.master.title("Doughnut Cutter 0.9")
app.mainloop()
