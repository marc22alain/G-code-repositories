#!/usr/bin/env python

from Polar_Holes_class import PolarHolesBorer
from Setup_class import Setup

setup = Setup()
app = PolarHolesBorer(None, setup)
app.master.title("Polar Holes 0.9")
app.mainloop()
