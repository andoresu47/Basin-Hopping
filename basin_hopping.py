############################################################
# Implementation of the Basin Hopping (BH) algorithm for
# structure optimization.
#
# BH algorithm has been implemented using Python3.4;
# coupled to Quantum Espresso 5.2 (DFT code as calculator)
#
# Author  : Andres Lopez Martinez
# Advisor : Dr. Oliver Paz Borbon (IF-UNAM)
#
# Financial Support (PAPIIT-UNAM: Project  IA102716
# Computational resources (Miztli-UNAM):   SC15-1-IG-82
# SC16-1-IG-78
#
#
# Note: Output folders will be generated in current
# directory.
############################################################

import glob
import os
import math
import random
import re
import sys
import datetime
from subprocess import*

# Variable declarations
init = ""
input_dir = ""
programs_dir = ""
substrate_nat = ""
cluster_nat = ""
cluster_ntyp = ""
temperature_K = 0
step_width = ""
iterations = ""
x_range = ""
y_range = ""
z_range = ""
z_vacuum = ""

time_initial = 0
time_final = 0

# Initial time
time_initial = datetime.datetime.now()

file = str(sys.argv[1])

# Variable initialization with information from command line
f = open(file, 'r')
lines = f.readlines()
f.close()

for line in lines:
	l = line.strip()
	if l.startswith("initialization_file"):
		init = l.split("initialization_file = ", 1)[1]
	if l.startswith("input_dir"):
		input_dir = l.split("input_dir = ", 1)[1]
	if l.startswith("programs_dir"):
		programs_dir = l.split("programs_dir = ", 1)[1]
	if l.startswith("substrate_nat"):
		substrate_nat = l.split("substrate_nat = ", 1)[1]
	if l.startswith("cluster_ntyp"):
		cluster_ntyp = l.split("cluster_ntyp = ", 1)[1]
	if l.startswith("temperature_K"):
		temperature_K = float(l.split("temperature_K = ", 1)[1])
	if l.startswith("step_width"):
		step_width = l.split("step_width = ", 1)[1]
	if l.startswith("iterations"):
		iterations = int(l.split("iterations = ", 1)[1])
	if l.startswith("x_range"):
		x_range = l.split("x_range = ", 1)[1]
	if l.startswith("y_range"):
		y_range = l.split("y_range = ", 1)[1]
	if l.startswith("z_range"):
		z_range = l.split("z_range = ", 1)[1]
	if l.startswith("z_vacuum"):
		z_vacuum = l.split("z_vacuum = ", 1)[1]

sys.path.append(programs_dir)

from input_parser import*
# Cluster total number of atoms
cluster_nat = str(get_nAtoms_str(cluster_ntyp))

# Temperature
kBT = float(0.00008617 * temperature_K)

# Output folder name
output_dir_name = get_output_name(cluster_ntyp)

# Output folder is created
call(['cp', '-r', input_dir, './' + output_dir_name])
# The input file gets edited to remain consistent with the number of atoms
call(['python3.4', programs_dir + '/replace_line.py', output_dir_name + '/input.in', 'nat=n,', 'nat=' + str(int(cluster_nat) + int(substrate_nat))  + ','])
# The cluster gets randomly generated only if there is no initialization file
if init == "False" or init == "false":
	call(['python3.4', programs_dir + '/RandomGenerator.py', output_dir_name + '/input.in', cluster_ntyp, x_range, y_range, z_range, z_vacuum])
else:
	call(['python3.4', programs_dir + '/initializer.py', init, output_dir_name + '/input.in'])

print("Comienza la iteracion 1  de " + output_dir_name)
	
# The "run" script gets executed, with particular emphasis on its completion before continuing with 
# the subsequent commands in the script
subproc = Popen([output_dir_name + '/run.sh'], stdout = PIPE, stderr = PIPE)
(out, err) = subproc.communicate()

while call('grep -q \"Begin final coordinates\" ' + output_dir_name + '/output.out', shell = True) == 1:
	print("Fallo en la convergencia. Comienza nuevamente la iteracion 1  de " + output_dir_name)
	# The cluster gets randomly generated again; ie, the original input gets tossed out
	call(['python3.4', programs_dir + '/RandomGenerator.py', output_dir_name + '/input.in', cluster_ntyp, x_range, y_range, z_range, z_vacuum])
	# The failing output file gets deleted, for the next one to take its place
	call(['rm', output_dir_name + '/output.out'])
	
	subproc = Popen([output_dir_name + '/run.sh'], stdout = PIPE, stderr = PIPE)
	(out, err) = subproc.communicate()

# Naming of corresponding input and output
call(['cp', output_dir_name + '/input.in', output_dir_name + '/input1.in'])
call(['cp', output_dir_name + '/output.out', output_dir_name + '/output1.out'])
#Naming of final coordinates and energy file
call('grep \"! \" ' +  output_dir_name + '/output1.out | tail -1 > ' + output_dir_name + '/coord1.xyz', shell = True)
# -A to take the necessary subsequent lines, head -n to take only the first ocurrence of the argument
# grep -A 5 "Begin final coordinates" coord.xyz | head -n 5
call('grep -A ' + str(int(substrate_nat) + 2 + int(cluster_nat)) + ' \"Begin final coordinates\" ' + output_dir_name + '/output1.out | head -n ' + str(int(substrate_nat) + 3 + int(cluster_nat)) + ' >> ' + output_dir_name + '/coord1.xyz', shell = True)
	
# Deletion of unnecessary files
call(['rm', '-r', output_dir_name + '/pwscf.save', output_dir_name + '/output.out'])

for fl in glob.glob(output_dir_name + '/pwscf.*'):
	os.remove(fl)
	
print("Concluida la iteracion 1")
	
# Steps for the Basin hopping
i = 1
# In case swap energy fails
swap_fail_flag = False
while i < iterations:
	# Every 10th iteration a swap routine gets executed
	if i%10 == 0 and swap_fail_flag == False:
		call(['python3.4', programs_dir + '/swap.py', output_dir_name + '/coord' + str(i) + '.xyz', output_dir_name + '/input.in', cluster_ntyp])
	else:
		swap_fail_flag = False
		call(['python3.4', programs_dir + '/move.py', output_dir_name + '/coord' + str(i) + '.xyz', output_dir_name + '/input.in', step_width, cluster_ntyp])	
	
	print("Comienza la iteracion " + str(i + 1)+ " de " + output_dir_name)

	# The "run" script gets executed, with particular emphasis on its completion before continuing with
   	# the subsequent commands in the script
	subproc = Popen([output_dir_name + '/run.sh'], stdout = PIPE, stderr = PIPE)
	(out, err) = subproc.communicate()

	while call('grep -q \"Begin final coordinates\" ' +  output_dir_name + '/output.out', shell = True) == 1:
		print("Fallo en la convergencia. Comienza nuevamente la iteracion " + str(i + 1) + " de " + output_dir_name)
		# The Pt coordinates get moved again; ie, the original input gets tossed out
		call(['python3.4', programs_dir + '/move.py', output_dir_name + '/coord' + str(i) + '.xyz', output_dir_name + '/input.in', step_width, cluster_ntyp])	
		# The failing output file gets deleted, for the next one to take its place
		call(['rm', output_dir_name + '/output.out'])

		subproc = Popen([output_dir_name + '/run.sh'], stdout = PIPE, stderr = PIPE)
		(out, err) = subproc.communicate()

	# Naming of corresponding input and output
	call(['cp', output_dir_name + '/input.in', output_dir_name + '/input' + str(i + 1) + '.in'])
	call(['cp', output_dir_name + '/output.out', output_dir_name + '/output' + str(i + 1) + '.out'])
	# Creation of final energy and coordinates file
	call('grep \"! \" ' + output_dir_name + '/output' + str(i + 1) + '.out | tail -1 > ' + output_dir_name + '/coord' + str(i + 1) + '.xyz', shell = True)
	call('grep -A ' + str(int(substrate_nat) + 2 + int(cluster_nat)) + ' \"Begin final coordinates\" ' + output_dir_name + '/output' + str(i + 1) + '.out | head -n ' + str(int(substrate_nat) + 3 + int(cluster_nat)) + ' >> ' + output_dir_name + '/coord' + str(i + 1) + '.xyz', shell = True)
		
	# Deletion of unnecessary files
	call(['rm', '-r', output_dir_name + '/pwscf.save', output_dir_name + '/output.out'])
	
	for fl in glob.glob(output_dir_name + '/pwscf.*'):
		os.remove(fl)

	# Metropolis condition for accepting
	f = open(output_dir_name + '/coord' + str(i) + '.xyz', 'r')
	E0 = float(re.findall("\d+\.\d+", f.readline())[0]) * -13.6
	f.close()
	f = open(output_dir_name + '/coord' + str(i + 1) + '.xyz', 'r')
	En = float(re.findall("\d+\.\d+", f.readline())[0]) * -13.6
	f.close()

	if math.exp((E0 - En)/kBT) > random.uniform(0,1):
		print("Energia aceptada.")
		print("Concluida la iteracion " + str(i + 1))
		i = i + 1
		continue
	else:
		print("Energia rechazada.")
		call(['rm', '-r', output_dir_name + '/input' + str(i + 1) + '.in', output_dir_name + '/output' + str(i + 1) + '.out', output_dir_name + '/coord' + str(i + 1) + '.xyz'])
		print("Iteracion " + str(i + 1) + " fallida. Comienza de nuevo.")
		# Every 10th iteration swap gets involved
		if i%10 == 0:
			print("Swap failed to converge.")
			swap_fail_flag = True

# Print elapsed time
time_final = datetime.datetime.now()
print("\nTiempo total de ejecucion: " + str(time_final - time_initial))
