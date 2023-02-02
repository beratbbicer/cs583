This directory contains the implementation for CS481/583 HW0.

# General Info
Berat Biçer, 21503050
berat.bicer@bilkent.edu.tr
CS583, HW0

# Instructions
The code is implemented in Python3. The MAKEFILE contains recipes for compilation (Python, no compilation), execution, and cleanup.
Make sure you install the requirements before running the code.

## Requirements
Install python 3, and pip. Then, install numpy using the following command:
	pip install numpy

## Compilation
For compilation type to shell:
	make COMPILE

Note that since the implementation is done in Python, no compilation is necessary.

## Execution
For execution, type to shell:
	make RUN n=arg1 s=arg2
	
where arg1 is the value for the size of the matrices (n), and arg2 is the scalar value. 

Example run:
	make RUN n=5 s=10
	
This sets the matrices to have a size of 5x5, while applying scalar multiplication with 10.

## Cleanup
For cleanup, type to shell:
	make CLEAN

Note that since the implementation is done in Python, no cleanup is necessary.
