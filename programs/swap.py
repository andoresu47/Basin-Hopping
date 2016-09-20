import sys
from Atom import Atom
import re
import random
from input_parser import*


atoms_set = []


def swap(to_swap, clstr_ntyp_lst):
    # Randomly chosen A-type atoms to swap
    typ_to_swp_1 = random.sample(range(0, int(clstr_ntyp_lst[1])), to_swap)

    # Randomly chosen B-type atoms to swap
    typ_to_swp_2 = random.sample(range(int(clstr_ntyp_lst[1]), len(atoms_set)), to_swap)

    # Coordinate swapping taking place for each of the chosen pairs
    for j in range(0, to_swap):
        a = typ_to_swp_1[j]
        b = typ_to_swp_2[j]
        temp_coord = atoms_set[a].get_coordinates()

        atoms_set[a].set_coordinates(atoms_set[b].get_coordinates())
        atoms_set[b].set_coordinates(temp_coord)

coordinates_file = str(sys.argv[1])
input_file = str(sys.argv[2])
cluster_ntyp_list = get_atype_anumber(str(sys.argv[3]))

# Minimum atomic quantity
minimum_natom_type = min(get_atoms_quantity_list(cluster_ntyp_list))

# Number of atoms to swap. Has to be between 1 and the minimum atomic quantity.
natoms_to_swp = random.randint(1, minimum_natom_type)

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
        coord_set = re.findall("[-+]?\d*\.\d+|\d+", lines1[i])

        if i < (int(cluster_ntyp_list[1]) + substrate + 4):
            atoms_set.append(Atom(cluster_ntyp_list[0], coord_set[0], coord_set[1], coord_set[2]))
        else:
            atoms_set.append(Atom(cluster_ntyp_list[2], coord_set[0], coord_set[1], coord_set[2]))

if int(cluster_ntyp_list[1]) != len(atoms_set):
	swap(natoms_to_swp, cluster_ntyp_list)

for atom in atoms_set:
    f.write(atom.to_string())

f.close()
