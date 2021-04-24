from post_processor import *

f = open('./files/linear-dist-two-pecks.ngc', 'r')
program = f.read()

print(program)

pp = PostProcessor()
pp.setProgram(program)
pp.parseProgram()

