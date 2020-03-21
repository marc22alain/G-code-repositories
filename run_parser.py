from gcode_parser import *

v = GCodeValidator()
g = GCodeParser([v])

p = 'F1000\nG17\n'
p2 = 'F1000.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X5.0 Y15.0 \nG90 \nG0 Z10.0 \nG91 \nG1 Z-5.0 \nG4 P0.5 \nG90 \nG0 Z80.0 \nG91 \nG0 X-5.0 Y-15.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X25.0 Y50.0 \nG90 \nG0 Z10.0 \nG91 \nG1 Z-5.0 \nG4 P0.5 \nG90 \nG0 Z80.0 \nG91 \nG0 X-25.0 Y-50.0 \nG90 \nG0 Z80.0 \nG91 \nG0 X35.0 Y75.0 \nG90 \nG0 Z10.0 \nG91 \nG1 Z-5.0 \nG4 P0.5 \nG90 \nG0 Z80.0 \nG91 \nG0 X-35.0 Y-75.0 \nG90 \nM2 \n'
p3 = 'F1000.0 G90 G0 Z80.0 G91 G0 X5.0 Y15.0 G90 G0 Z10.0 G91 G1 Z-5.0 G4 P0.5 G90 G0 Z80.0 G91 G0 X-5.0 Y-15.0 G90 G0 Z80.0 G91 G0 X25.0 Y50.0 G90 G0 Z10.0 G91 G1 Z-5.0 G4 P0.5 G90 G0 Z80.0 G91 G0 X-25.0 Y-50.0 G90 G0 Z80.0 G91 G0 X35.0 Y75.0 G90 G0 Z10.0 G91 G1 Z-5.0 G4 P0.5 G90 G0 Z80.0 G91 G0 X-35.0 Y-75.0 G90 M2 '

g.resetProgram(p2.split('\n'))
g.parseProgram()

print g.getProgramData()
# print v.getProgramData()
