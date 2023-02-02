This directory contains the implementation for CS481/583 HW2.

# General Info
Berat Biçer, 21503050
berat.bicer@bilkent.edu.tr
CS583, HW2

# Instructions
The code is implemented in Python3. The MAKEFILE contains recipes for compilation (Python, no compilation), execution, and cleanup.

Note that the program will create multiple outputs: 
	1. DP table will be outputted into the designated output switch where the first row contains the letters of the text, and the first column contains the letters of the pattern.
	2. Backtrack table will be outputted into the designed switch + '-backtrack' extension.
For example, if output path is './output', the program will create two output files:
	1. './output' will contain DP table,
	2. './output-backtrack' will contain the backtraking table.

Backtrack table is printed for your convenience, to make tracing easier.

The aligned strings, as well as the alignment score, is printed to stdout. No additional file is created to store this output.

A code snippet from biopython library for parsing FASTA files is included in my implementation. 
This snippet is placed inside a function named parse_fasta_file, which is explicitly stated in the source code as well.

Lastly, in my implementation I assume that the penalties are all positive values and are substracted from the relevant score. Please keep this in mind in case the outputs are inconsistent.
For example, the input scoring scheme '1|-1|-2' is accepted as '1|1|2'. 

## Requirements
Make sure the system has numpy installed, which I have in my dijkstra root.
For Python 3, installations contain 'argparse' libraries by default, hence, no additional action is necessary. 

## Compilation
For compilation type to shell:
	make COMPILE

Note that since the implementation is done in Python, no compilation is necessary.

## Execution
For execution, since there's no need to compile the source code, and the fact that passing the relevant arguments from makefile to python interpreter is complicated, there's no execution recipe for this homework.

Instead, directly run a command similar to what's shown below:
	python main.py -g -p ./pattern.fasta -t ./text.fasta -s "+1|-1|-2" -o ./output.txt
for global alignment, or:
	python main.py -l -p ./pattern.fasta -t ./text.fasta -s "+1|-1|-2" -o ./output.txt
for local alignment.

Remember to wrap the scores with single or double quotation marks, otherwise parser will not accept the input. 

## Cleanup
For cleanup, type to shell:
	make CLEAN

Note that since the implementation is done in Python, no cleanup is necessary.