This directory contains the implementation for CS481/583 HW1.

# General Info
Berat Biçer, 21503050
berat.bicer@bilkent.edu.tr
CS583, HW1

# Instructions
The code is implemented in Python3. The MAKEFILE contains recipes for compilation (Python, no compilation), execution, and cleanup.

Note that the program will create multiple outputs: 
	1. Search result will be written inside the designated file output file.
	2. The graph will be dumped to a file having the same name but with extension '.dot'.
	3. Graphviz output image will be dumped to a file having the same name but with extension '.jpg'.
For example, if output path is './output', the program will create two output files:
	1. './output' will contain the search results,
	2. './output.dot' will contain the graph,
	3. './output.jpg' will contain the visualization of the graph.

In addition, the program prints the outputs of both searches instead of a single method's. This is done to further validate the implementations. 
Based on the previous example, './output' will contain two sections: 
	1., marked with line '---> Keyword Tree' contains the output of the keyword-tree based search. 
	2., marked with line '---> Suffix Tree' contains the output of the suffix-tree based search.

Note that output is formatted hierarchically using tab(\t) characters. Look for no-tabs or '#'-lines to find the start of the previous methods' trace. 
1 tab gives you node location or pattern match/mismatch while 2 tabs give you the intermediate comparisons, etc.

Lastly, special characters attached to the strings are limited in size. Due to trivial nature of this assignment, no additional effort spent on creating these characters.
Thus, a maximum 32 unique patterns can be searched simultaneously for the scope of this homework. To address this we'd simply select random unicode bytes instead.
However, this is out of the scope of this homework, so it's not implemented / included in the source code.

## Requirements
Make sure the system has Graphviz installed.
For Python 3, installations contain 'argparse, random, string' libraries by default, hence, no additional action is necessary. 

## Compilation
For compilation type to shell:
	make COMPILE

Note that since the implementation is done in Python, no compilation is necessary.

## Execution
For execution, type to shell:
	make RUN p=arg1 t=arg2 o=arg3
	
where arg1 is the path to file containing keywords/patterns (p), and arg2 is path to file containing the text body (t) and arg3 is the path to output file (o). 
Since arguments are expected to be string-typed, enclose them using quotations as shown below:

Example run:
	make RUN p='./patterns1.txt' t='./text1.txt' o='./output'
	
This fills a patterns array from './patterns1.txt', sets the text to be the content of file './text1.txt' and outputs the search result into './output'.
The suffix tree will be placed into './output.dot' and the graph visualization will be placed into './output.jpg'.

## Cleanup
For cleanup, type to shell:
	make CLEAN

Note that since the implementation is done in Python, no cleanup is necessary.