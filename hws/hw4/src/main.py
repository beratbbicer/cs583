import argparse
from Bio import SeqIO, Phylo
from guide_trees import GuideTree_UPGMA, GuideTree_NJ
from io import StringIO
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS583 HW3', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--tree_type', default='upgma', type=str, help="Type of guide tree algorithm to be used. Default: upgma")
    parser.add_argument('-i', '--input_file', default='./input.fasta', type=str, help="Multiline, multisequence FASTA file containing input sequences.")
    parser.add_argument('-s', '--scoring_function', default='1:-1:-5', type=str, help="Scoring function for the alignment. match score, mismatch penalty, gap penalty, separated by :")
    parser.add_argument('-o', '--output_file', default='./output.tree', type=str, help="Path to output file in Newick Tree format.")

    args = parser.parse_args()  

    assert args.tree_type in ['nj', 'upgma'], 'Error -- invalid Guide Tree type.'
    tree_type = args.tree_type

    input_file = args.input_file
    scoring_function = [abs(int(x)) for x in args.scoring_function.strip().split(':')]
    output_file = args.output_file

    sequences = []
    for record in SeqIO.parse(input_file, 'fasta'):
        sequences.append([str(record.seq), record.description])

    if tree_type == 'upgma':
        gt = GuideTree_UPGMA(scoring_function)
    else:
        gt = GuideTree_NJ(scoring_function)

    tree_string = gt.construct(sequences)

    # output guide tree
    with open(f'{output_file}-{tree_type}.tree', 'w') as file:
        file.write(f'{tree_string};\n')

    # Output visualization
    tree = Phylo.read(StringIO(tree_string), 'newick')
    tree.ladderize(reverse=True)
    Phylo.draw(tree, do_show=False)
    plt.savefig(f'{output_file}-{tree_type}.png')