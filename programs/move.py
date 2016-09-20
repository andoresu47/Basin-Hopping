import sys
import re
import random
from input_parser import*


def move(l, step):
	coord_set = re.findall("[-+]?\d*\.\d+|\d+", l)
	new_coord_set = []

	for coord in coord_set:
		new_coord = round(float(coord) + (2 * step * random.uniform(-1, 1)), 9)

		new_coord_set.append(new_coord)

	return new_coord_set

coordinates_file = str(sys.argv[1])
input_file = str(sys.argv[2])
step_width = float(sys.argv[3])
cluster_ntyp_list = get_atype_anumber(str(sys.argv[4]))

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

substrate = 0
for i in range(4, len(lines1)):
	if not lines1[i].startswith(tuple(cluster_ntyp_list[0::2])):
		f.write(lines1[i])
		substrate += 1
	else:
		moved = move(lines1[i], step_width)
		if i < (int(cluster_ntyp_list[1]) + substrate + 4):
			f.write(cluster_ntyp_list[0] + "\t" + str(moved[0]) + "\t" + str(moved[1]) + "\t" + str(moved[2]) + "\n")
		else:
			f.write(cluster_ntyp_list[2] + "\t" + str(moved[0]) + "\t" + str(moved[1]) + "\t" + str(moved[2]) + "\n")

f.close()
