# Basin-Hopping
Implementation of a Basin Hopping Monte Carlo (BH) global optimization algorithm for supported metal nanoalloys. 
BH algorithm has been implemented with Python3.4, coupled to Quantum Espresso 5.2 (DFT code as calculator).

## Requirements

Quantum Espresso needs to be installed before running the BH programs. Quantum Espresso 5.2 and later are supported. 
To download and install, please refer to the following links:

[Download Quantum Espresso](http://www.quantum-espresso.org/download/)

[User guide for Quantum Espresso](http://www.quantum-espresso.org/wp-content/uploads/Doc/user_guide.pdf)

In addition, [Python 3.4](https://www.python.org/download/releases/3.4.0/) or later must be installed to run this project.

## Installation

To "install" this project simply download the files and put them in a prefered directory. 

It is highly recommended to preserve the project file structure as it is, since it makes things much easier. 

## Usage

For simplicity, the usage of this project has been simplified to adding specifications into an input file "input.bh". This file has 
different categories for the user to fill in with data regarding the problem to solve. These are:

1. Control: This category deals with specifying the paths to both the QE input directory and the auxiliary Python programs directory.

        &control
          input_dir = /home/path/to/input
          programs_dir = /home/path/to/programs

2. Basin Hopping: This category deals with specifics of the problem to solve. 

        &basin_hopping
          substrate_nat = //number of atoms of the substrate (in case there is any). Eg. 40
          cluster_ntyp = //Monometallic: "[AtomicSymbol:NumberOfAtoms]". Eg. [Pt:5]
                         //Bimetallic: "[AtomicSymbol_1st:NumberOfAtoms_1st], [AtomicSymbol_2nd:NumberOfAtoms_2nd]". Eg. [Pt:5], [Au:2]
          temperature_K = //Temperature in Kelvin. Eg. 500
          step_width = //Step width tu use for the basin hopping algorithm. Eg. 0.6
          iterations = //Total number of iterations, or steps in the basin hopping execution. Eg. 100

3. Random range: This category deals with specifying the 3D space available for generating the initial randomized cluster.

        &random_range
          x_range = //[xMin:xMax]
          y_range = //[yMin:yMax]
          z_range = //[zMin:zMax]
          z_vacuum = //[VaccumStart:VaccumEnd]

  The penultimate option has to do with anchoring the generated structure within a certain distance from the substrate. 
  The other three define space constraints of the cell. Note: the value of "zMax" has to coincide with "VaccumStart" in most cases.  

To run the project, execute the main program as: `python 3.4 basin_hopping.py input.bh`

Other than the `input.bh` file, the other files that need specification are the QE input file `input.in` and the QE run script
`run.sh` (within the `input` directory). These are the usual QE run files. 

## Credits

Author  : Andres Lopez Martinez

Advisor : Dr. Oliver Paz Borbon (IF-UNAM)

Financial Support (PAPIIT-UNAM): Project  IA102716

Computational resources (Miztli-UNAM):   SC15-1-IG-82

SC16-1-IG-78

Project Contact: Dr. Oliver Paz Borbon oliver_paz@fisica.unam.mx

## License

Unless otherwise noted, this work is released under: http://www.apache.org/licenses/LICENSE-2.0
