This directory contains the implementation for CS481/583 HW3.

# General Info
Berat Biçer, 21503050
berat.bicer@bilkent.edu.tr
CS583, HW4

# Instructions
The code is implemented in Python3. The MAKEFILE contains recipes for compilation (Python, no compilation), execution, and cleanup.

Dependencies:
	For I/O, biopython's FASTA parsing features are used. Global alignment, phylogenetic tree construction including UPGMA, Neighbourhood Joining and their related functions are all implemented manually.
	For matrix operation, numpy library is used.
	For visualization of the constructed graphs, matplotlib is used.
		
In the implementation it is assumed that the penalties are all positive values and are substracted from the relevant score. Keep this in mind in case the outputs are inconsistent.
For example, the input scoring scheme '1:-1:-2' is accepted as '1:1:2'. 

For visualization' instead of the java package recommended, I opted for python's popular visualization tool matplotlib in coordination with biopython functionality. Note that both phylogenetic trees (using upgma and neighbourhood joining) are first constructed manually, converted to the requred Newick format, and then forwarded to biopython & mtaplotlib for visualization.

Another point of consideration is the way pairwise similarity scores from needleman_wunsch are converted to distance values. By default, similarities are first transformed such that highest similarity is assigned a distance of 1, and the rest scaled such that the worse the score is the greater the distance becomes, all positive quantities. These values are then scaled to [1,6] range for processing. Note that different distance transformations my yield various topographies.

Lastly, unlike the algorithm for neighbourhood joining given in class, since pairwise distances are floats, an approximate matching technique is applied such that if difference between 3-way pairwise distances is below this threshold after reduction by delta, a degenerate tuple is assumed to be found. This also means that when creating new nodes, the degenerate nodes loose some amount of distance due to FP arithmetics and this approximate matching. 

## Requirements
Make sure to install dependencies by executing the following commands, if necessary:
	pip install biopython
	pip install numpy
	pip install matplotlib

## Compilation
For compilation type to shell:
	make COMPILE

Note that since the implementation is done in Python, no compilation is necessary.

## Execution
For execution, since there's no need to compile the source code, and the fact that passing the relevant arguments from makefile to python interpreter is complicated, there's no execution recipe for this homework.

Instead, directly run a command similar to those shown below:
	python main.py -t upgma -i input.fasta -s '1:-1:-5' -o output
	python main.py -t nj -i input.fasta -s '1:-1:-5' -o output
	
Remember to wrap the scores with single or double quotation marks, otherwise parser will not accept the input. 

## Cleanup
For cleanup, type to shell:
	make CLEAN

Note that since the implementation is done in Python, no cleanup is necessary.
