import sys
import re
import random
from input_parser import*

coordinates_file = str(sys.argv[1])
input_file = str(sys.argv[2])

f = open(coordinates_file, 'r')
lines1 = f.readlines()
f.close()

f = open(input_file, 'r')
lines2 = f.readlines()
f.close()

f = open(input_file, 'w')

for line in lines2:
	if line.startswith("ATOMIC_POSITIONS"):
		f.write(line)
		break
	else:
		f.write(line)

for line in lines1:
	f.write(line)

f.close()
