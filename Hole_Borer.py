#!/usr/bin/env python

from Hole_Borer_class import HoleBorer
from Setup_class import Setup

setup = Setup()
app = HoleBorer(None, setup)
app.master.title("Hole Borer 0.9")
app.mainloop() 
