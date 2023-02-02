import argparse
from keyword_tree import KeywordTree
from suffix_tree import SuffixTree

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CS583 HW1', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', '--keywords_file', default='./patterns1.txt', type=str, help="Path to file containing patterns.")
    parser.add_argument('-t', '--text_file', default='./text1.txt', type=str, help="Path to file containing text to be searched on.")
    parser.add_argument('-o', '--output_file', default='./output.txt', type=str, help="Path to output file containing search results.")
    args = parser.parse_args()  
    keywords_file = args.keywords_file
    text_file = args.text_file
    output_file = args.output_file

    # Parse input files
    keywords = []
    with open(keywords_file, 'r') as file:
        for line in file:
            keywords += [line.strip()]

    text = []
    with open(text_file, 'r') as file:
        for line in file:
            text = line.strip()

    # Create Search Trees
    keyword_tree = KeywordTree(keywords)
    suffix_tree = SuffixTree(keywords)

    # Query
    keyword_matches = keyword_tree.query(text)
    print('\n########################################################################################################################\n')
    suffix_matches = suffix_tree.query(text)

    # Output
    with open(output_file, 'w') as file:
        file.write('---> Keyword Tree\n')
        for idx in range(len(keywords)):
            file.write(f'{keywords[idx]}: {" ".join([str(x) for x in keyword_matches[keywords[idx]]])}\n')

        file.write('\n---> Suffix Tree\n')
        for idx in range(len(keywords)):
            file.write(f'{keywords[idx]}: {" ".join([str(x) for x in suffix_matches[keywords[idx]]])}\n')

    suffix_tree.output_tree(f'{output_file}.dot')
    print('\nExecution complete.')