from post_processor import *

f = open('./files/linear-dist-two-pecks.ngc', 'r')
# f = open('./files/one-peck-optimized.ngc', 'r')
# f = open('./files/one-peck-optimized-multiple-safe-z.ngc', 'r')
program = f.read()

print(program)

pp = PostProcessor()
pp.setProgram(program)
pp.parseProgram()

print(pp.getProgramData()['processed_gcode'])
