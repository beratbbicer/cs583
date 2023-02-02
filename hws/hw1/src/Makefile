SHELL = '/bin/sh'
OUTDOT = '$(o).dot'
OUTIMG = '$(o).jpg'

COMPILE:
	printf '%s\n' "Python, no compilation."

RUN: main.py keyword_tree.py suffix_tree.py
	python main.py -p $(p) -t $(t) -o $(o)
	dot $(OUTDOT) -Tpng > $(OUTIMG)

CLEAN: $(OUTDOT) $(OUTIMG)
	printf '%s\n' "Python, no cleanup necessary."