import sys

file = str(sys.argv[1])
pattern = str(sys.argv[2])
replace_with = str(sys.argv[3])

f = open(file, 'r')
lines = f.readlines()
f.close()

f = open(file, 'w')
for line in lines:
	f.write(line.replace(pattern, replace_with))

f.close()
