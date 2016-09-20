#!/bin/sh
cd $(dirname "$0")
mpirun -np 64 pw.x < input.in > output.out

