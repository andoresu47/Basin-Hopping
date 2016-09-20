import random
import sys
from input_parser import*
from AtomicStructure import AtomicStructure

# Necessary parameters are read from the execution of this program.
file = str(sys.argv[1])                                         # file to edit with newly generated coordinates
cluster_ntyp_list = get_atype_anumber(str(sys.argv[2]))         # atomic symbols and number of atoms per element
x_range = str(sys.argv[3])                                      # x range in the form "[0:10]"
y_range = str(sys.argv[4])                                      # y range in the form "[0:10]"
z_range = str(sys.argv[5])                                      # z range in the form "[0:10]"
vacuum_range = str(sys.argv[6])                                 # vacuum range in the form "[0:10]"
nAtoms = get_nAtoms_lst(cluster_ntyp_list)                      # total number of atoms

x_range_list = get_number_list(x_range)
y_range_list = get_number_list(y_range)
z_range_list = get_number_list(z_range)
vacuum_range_list = get_number_list(vacuum_range)

# Data types are extracted from input so that the program can manipulate them
xMin = x_range_list[0]
xMax = x_range_list[1]
yMin = y_range_list[0]
yMax = y_range_list[1]
zMin = z_range_list[0]  # 3
zMax = z_range_list[1]  # 3.7
vacuum_min = vacuum_range_list[0]
vacuum_max = vacuum_range_list[1]
sep_dist_l_b = "1.5"
sep_dist_u_b = "2.5"

# Check if the generated bulk can fit in the defined cell.
atomicStructure = None

cell_size_x = float(xMax) - float(xMin)
cell_size_y = float(yMax) - float(yMin)
cell_size_z = float(vacuum_max) - float(vacuum_min)

while True:
	atomicStructure = AtomicStructure(nAtoms, sep_dist_l_b, sep_dist_u_b)

	if atomicStructure.get_size_x() <= cell_size_x \
			and atomicStructure.get_size_y() <= cell_size_y \
			and atomicStructure.get_size_z() <= cell_size_z:
		break

# New lower boundaries are generated for the bulk
minimum_x = atomicStructure.get_min_x()
minimum_y = atomicStructure.get_min_y()
minimum_z = atomicStructure.get_min_z()

displacement_to_starting_point_x = float(xMin) - minimum_x
displacement_to_starting_point_y = float(yMin) - minimum_y
displacement_to_starting_point_z = float(zMin) - minimum_z

# Random ranges are defined for each axis, taking into
# account the total size of the bulk
x_random_top = cell_size_x - atomicStructure.get_size_x()
y_random_top = cell_size_y - atomicStructure.get_size_y()
# z_random_top = cell_size_z - atomicStructure.get_size_z()
z_random_top = float(zMax) - float(zMin)

random_displacement_x = random.uniform(0, x_random_top)
random_displacement_y = random.uniform(0, y_random_top)
random_displacement_z = random.uniform(0, z_random_top)

# This is for manipulating every line in the file
f = open(file, 'r')
lines = f.readlines()
f.close()

# Coordinates of the desired element are replaced with random generated ones
f = open(file, 'w')
for line in lines:
	if not line.startswith(tuple(cluster_ntyp_list[0::2])):
		f.write(line)

for i in range(len(atomicStructure.atoms)):
	if i < int(cluster_ntyp_list[1]):
		f.write(cluster_ntyp_list[0] + "\t" + str(
            round(atomicStructure.atoms[i].x_coordinate + displacement_to_starting_point_x + random_displacement_x,
                  9)) + "\t" + str(
            round(atomicStructure.atoms[i].y_coordinate + displacement_to_starting_point_y + random_displacement_y,
                  9)) + "\t" + str(
            round(atomicStructure.atoms[i].z_coordinate + displacement_to_starting_point_z + random_displacement_z,
                  9)) + "\n")
	else:
		f.write(cluster_ntyp_list[2] + "\t" + str(
            round(atomicStructure.atoms[i].x_coordinate + displacement_to_starting_point_x + random_displacement_x,
                  9)) + "\t" + str(
            round(atomicStructure.atoms[i].y_coordinate + displacement_to_starting_point_y + random_displacement_y,
                  9)) + "\t" + str(
            round(atomicStructure.atoms[i].z_coordinate + displacement_to_starting_point_z + random_displacement_z,
                  9)) + "\n")

f.close()

