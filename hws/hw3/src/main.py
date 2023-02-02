import argparse
from Bio import SeqIO
from msa import MSA_CenterStar

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS583 HW3', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input_file', default='./input.fasta', help="Multiline, multisequence FASTA file containing input sequences.")
    parser.add_argument('-s', '--scoring_function', default='1:-1:-5', type=str, help="Scoring function for the alignment. match score, mismatch penalty, gap penalty, separated by :")
    parser.add_argument('-o', '--output_file', default='./output.phy', type=str, help="Path to output file in PHYLIP format containing the alignment.")

    args = parser.parse_args()  
    input_file = args.input_file
    scoring_function = [abs(int(x)) for x in args.scoring_function.strip().split(':')]
    output_file = args.output_file

    sequences = []
    for record in SeqIO.parse(input_file, 'fasta'):
        sequences.append([str(record.seq), record.description])

    # compute alignment
    msa = MSA_CenterStar(scoring_function)
    aligned_sequences = msa.align(sequences)

    with open(output_file, "w") as output_handle:
        SeqIO.write(aligned_sequences, output_handle, "phylip")