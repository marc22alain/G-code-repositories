#!/usr/bin/env python

from Doughnut_Cutter_class import DoughnutCutter
from Setup_class import Setup

setup = Setup()
app = DoughnutCutter(None, 	setup)

app.setup.feed_rate_var.set("1000")
app.setup.Z_safe_var.set("100")
app.setup.cut_per_pass_var.set(3)
app.setup.bit_diameter_var.set(6.35)
app.setup.stock_thickness_var.set(25)

app.tab_thickness_var.set(1.5)
app.tab_width_var.set("6.35")
app.doughnut_OD_var.set(120)
app.doughnut_ID_var.set(75)

code = app.generateCode()

print code