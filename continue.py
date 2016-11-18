import glob
import os
import math
import random
import re
import sys
import datetime
from subprocess import*

# Variable declarations
programs_dir = ""
substrate_nat = ""
cluster_nat = ""
cluster_ntyp = ""
temperature_K = 0
step_width = ""
iterations = ""

time_initial = 0
time_final = 0

# Initial time
time_initial = datetime.datetime.now()

file = str(sys.argv[1])
i = int(sys.argv[2])

# Variable initialization with information from command line
f = open(file, 'r')
lines = f.readlines()
f.close()

for line in lines:
	l = line.strip()
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

sys.path.append(programs_dir)

from input_parser import*
# Cluster total number of atoms
cluster_nat = str(get_nAtoms_str(cluster_ntyp))

# Temperature
kBT = float(0.00008617 * temperature_K)

# Output folder name
output_dir_name = get_output_name(cluster_ntyp)

# Steps for the Basin hopping
# In case swap energy fails
swap_fail_flag = False
while i < iterations:

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
		# Swap failing
		if i%10 == 0:
			print("Swap failed to converge")
			swap_fail_flag = True

# Print elapsed time
time_final = datetime.datetime.now()
print("\nTiempo total de ejecucion: " + str(time_final - time_initial))
