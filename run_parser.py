from gcode_parser import *

g = GCodeParser()

p = 'F1000\nG17\n'

g.resetProgram(p.split('\n'))
g.parseProgram()

print g.getProgramData()
