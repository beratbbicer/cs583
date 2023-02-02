class Node():
    def __init__(self, parent, index):
        self.parent = parent
        self.index = index # start idx of the pattern
        self.children = {}

# O(N) in theory where N -> total size of the patterns
# For implementation-related reasons this isn't the case
def create_suffix_tree_naive(keywords, special_characters):
    root = Node(None, -1)

    for kidx in range(len(keywords)):
        keyword = keywords[kidx]
        suffixes = [keyword[i:] + special_characters[kidx] for i in range(len(keyword)+1)]

        for i in range(len(suffixes)):
            head = root
            suffix = suffixes[i]
            while True:
                if len(head.children) < 1 and head is root: # empty root
                    head.children[suffix] = Node(head, len(suffixes[i]))
                    break
                else: # check for overlaps
                    longest_overlapping_child, longest_overlap = None, 0
                    for child in head.children:
                        j = 0
                        while j < len(child) and j < len(suffix) and child[j] == suffix[j]:
                            j += 1

                        if j > longest_overlap:
                            longest_overlapping_child = child
                            longest_overlap = j

                    if suffix == longest_overlapping_child: # there's an exact item, skip
                        break
                    elif longest_overlap > 0 and suffix[:longest_overlap] == longest_overlapping_child: # an edge already exists within the suffix
                        head = head.children[longest_overlapping_child]
                        suffix = suffix[longest_overlap:]
                    elif longest_overlapping_child == None and suffix != '': # Create a new leaf node at head
                        head.children[suffix] = Node(head, len(suffixes[i]))
                        break
                    elif longest_overlap > 0 and suffix[:longest_overlap] not in head.children: # Overlap isn't an edge but it's nonzero - split                        
                        child_node = head.children[longest_overlapping_child]
                        head.children.pop(longest_overlapping_child, None)
                        
                        new_child = Node(head, -1)
                        head.children[suffix[:longest_overlap]] = new_child

                        new_child.children[longest_overlapping_child[longest_overlap:]] = child_node
                        child_node.parent = new_child

                        # Continue traversing here
                        head = new_child
                        suffix = suffix[longest_overlap:]
                    else:
                        raise Exception('Error in logic.')
    return root                     

# Improvement over keyword trees:
# Reduced space requirement due to compact tree hierarchy
# One potential limitation is having to address associating a unique character for each keyword
# Also, having to compare each edge during search is costly
def suffix_tree_search(t, keywords, special_characters):
    root = create_suffix_tree_naive(keywords, special_characters)
    head = root
    matches = {k:[] for k in keywords}
    i = 0

    while i < len(t):
        j1 = i
        while True:
            flag = False
            for child in head.children:
                if child in special_characters:
                    continue

                clean_child = child[:-1] if child[-1] in special_characters else child

                if t[j1:j1+len(clean_child)] == clean_child:
                    if len(head.children[child].children) < 1 and t[i:i+head.children[child].index-1] in keywords:
                        matches[t[i:i+head.children[child].index-1]] += [i]
                    else:
                        head = head.children[child]
                        j1 += len(clean_child)
                        flag = True
                    break

            if flag == False:
                head = root
                i += 1
                break

    print(matches)
    return root, matches

if __name__ == "__main__":
    keywords0 = ['abab']
    special_characters0 = ['$']
    t0 = 'ababbbbab'

    keywords1 = ['apple','apropos','banana','bandana','orange']
    special_characters1 = ['#','$','%','&','é']
    t1 = 'abaproposbananacappleaappleapplebcorangedaproposbdhbabanananabandananaosnbandanamsmorangelkbanbanana'
    # Expected output: {'apple': [16, 22, 27], 'apropos': [2, 41], 'banana': [9, 53, 94], 'bandana': [61, 73], 'orange': [34, 83]}

    keywords2 = ['potato','tattoo','theater','other','recep', 'sex', 'excommunicate']
    special_characters2 = ['#','$','%','&','é','@','|']
    t2 = 'sexcommunicatexcommunicatepotatotherecepotato'
    # Expected output: {'potato': [26, 39], 'tattoo': [], 'theater': [], 'other': [31], 'recep': [35], 'sex': [0], 'excommunicate': [1, 13]}

    t = t2
    keywords = keywords2
    special_characters = special_characters2
    suffix_tree_search(t, keywords, special_characters)
