import argparse
from algorithms import needleman_wunsch, smith_waterman

# Taken from biopython/FastaIO/SimpleFastaParser
def parse_fasta_file(file):
    for line in file:
        if line[0] == ">":
            title = line[1:].rstrip()
            break
    else:
        # no break encountered - probably an empty file
        return

    lines = []
    for line in file:
        if line[0] == ">":
            yield title, "".join(lines).replace(" ", "").replace("\r", "")
            lines = []
            title = line[1:].rstrip()
            continue
        lines.append(line.rstrip())

    yield title, "".join(lines).replace(" ", "").replace("\r", "")

def dump_array(text, keyword, array, filename):
    with open(filename, 'w') as file:
        file.write(f"{''.join([f'{s:5s}' for s in '  ' + text])}\n")
        file.write(f"{''.join([f'{str(s):5s}' for s in [' '] + array[0].tolist()])}\n")
        for i in range(1, array.shape[0]):
            file.write(f"{''.join([f'{str(s):5s}' for s in [keyword[i-1]] + array[i].tolist()])}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS583 HW2', formatter_class=argparse.RawTextHelpFormatter)
    # parser.add_argument('-g', '--global_align', default=False, action='store_true', help="Execute global alignment with Needle-Wunsch.")
    # parser.add_argument('-l', '--local_align', default=True,  action='store_true', help="Execute local alignment with Smith-Waterman.")
    parser.add_argument('-g', '--global_align', action='store_true', help="Execute global alignment with Needle-Wunsch.")
    parser.add_argument('-l', '--local_align', action='store_true', help="Execute local alignment with Smith-Waterman.")

    parser.add_argument('-p', '--keyword_file', default='./pattern.fasta', type=str, help="Path to file containing patterns.")
    parser.add_argument('-t', '--text_file', default='./text.fasta', type=str, help="Path to file containing text to be searched on.")
    parser.add_argument('-s', '--scores', default='+1|-1|-2', type=str, help="Path to output file containing search results.")
    parser.add_argument('-o', '--output_file', default='./output.txt', type=str, help="Path to output file containing search results.")

    args = parser.parse_args()  
    global_alignment = args.global_align
    local_align = args.local_align
    keyword_file = args.keyword_file
    text_file = args.text_file
    match_score, mismatch_penalty, indel_penalty = [abs(int(x)) for x in args.scores.strip().split('|')]
    output_file = args.output_file

    # Parse input
    keyword = None
    with open(keyword_file, 'r') as file:
        for name, seq in parse_fasta_file(file):
            keyword = seq
            break
    
    text = None
    with open(text_file, 'r') as file:
        for name, seq in parse_fasta_file(file):
            text = seq
            break

    # Run alignment
    if global_alignment:
        aligned_keyword, aligned_text, dp_table, backtrack_table = needleman_wunsch(keyword, text, match_score, mismatch_penalty, indel_penalty)
    else:
        aligned_keyword, aligned_text, dp_table, backtrack_table = smith_waterman(keyword, text, match_score, mismatch_penalty, indel_penalty)

    # Output results
    print(aligned_keyword)
    print(aligned_text)
    print(f'Score: {dp_table[-1,-1]}')
    dump_array(text, keyword, dp_table, output_file)
    dump_array(text, keyword, backtrack_table, f'{output_file}-backtrack')