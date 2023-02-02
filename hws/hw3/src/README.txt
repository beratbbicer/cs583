This directory contains the implementation for CS481/583 HW3.

# General Info
Berat Biçer, 21503050
berat.bicer@bilkent.edu.tr
CS583, HW3

# Instructions
The code is implemented in Python3. The MAKEFILE contains recipes for compilation (Python, no compilation), execution, and cleanup.

Dependencies:
	For I/O, biopython's FASTA and PHYLYP parsing features are used. Global alignment and MSA, including related functions, are implemented manually.
	For matrix operation, numpy library is used.
	
In the implementation it is assumed that the penalties are all positive values and are substracted from the relevant score. Keep this in mind in case the outputs are inconsistent.
For example, the input scoring scheme '1:-1:-2' is accepted as '1:1:2'. 

## Requirements
Make sure to install dependencies by executing the following commands, if necessary:
	pip install biopython
	pip install numpy

## Compilation
For compilation type to shell:
	make COMPILE

Note that since the implementation is done in Python, no compilation is necessary.

## Execution
For execution, since there's no need to compile the source code, and the fact that passing the relevant arguments from makefile to python interpreter is complicated, there's no execution recipe for this homework.

Instead, directly run a command similar to what's shown below:
	python main.py -i "input.fasta" -s "1:-1:-5" -o "output.phy"
	
Remember to wrap the scores with single or double quotation marks, otherwise parser will not accept the input. 

## Cleanup
For cleanup, type to shell:
	make CLEAN

Note that since the implementation is done in Python, no cleanup is necessary.
