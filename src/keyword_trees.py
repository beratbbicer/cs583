class Node():
    def __init__(self, parent, index):
        self.parent = parent
        self.index = index # start idx of the pattern
        self.children = {}

# O(N) where N -> total size of the patterns
def keyword_tree_naivethreading(keywords):
    root = Node(None, -1)
    for keyword in keywords:
        head = root
        for i in range(len(keyword)):
            s = keyword[i]
            if s not in head.children:
                    head.children[s] = Node(head, head.index+1)
            
            head = head.children[s]
    return root

# Keep a pointer to the start
# Slowly try and push the strings you see from the head downwards
# If you get a mismatch, increment the start ptr & keep pushing
# mplementation is O(N + nm), N: total length of patterns, n: length of t, m: length of a pattern
def keyword_tree_search(t, p):
    root = keyword_tree_naivethreading(p)
    matches = {k:[] for k in p}
    head = root
    i = 0

    while i < len(t):
        j = i
        x = t[i]
        while j < len(t):
            y = t[j]
            if t[j] in head.children: # match
                child = head.children[t[j]]
                idx = j - child.index
                keyword = t[idx:j+1]

                if len(child.children) < 1: # match, this is a leaf
                    matches[keyword] += [idx]
                    head = root
                    i += 1
                    break
                else:
                    '''
                    # a keyword that is also a prefix of another exists, but we don't need to search explicitly for this.
                    # searching for the shorter string & then extending to match the longer string suffices. 
                    if keyword in p: 
                        matches[keyword] += [idx]
                    '''
                    head = head.children[t[j]]
                    j += 1

            else: # no match
                head = root
                i += 1
                break

    print(matches)
    return root, matches

if __name__ == "__main__":
    keywords1 = ['apple','apropos','banana','bandana','orange']
    t1 = 'abaproposbananacappleaappleapplebcorangedaproposbdhbabanananabandananaosnbandanamsmorangelkbanbanana'
    # Expected output: {'apple': [16, 22, 27], 'apropos': [2, 41], 'banana': [9, 53, 94], 'bandana': [61, 73], 'orange': [34, 83]}

    keywords2 = ['potato','tattoo','theater','other','recep', 'sex', 'excommunicate']
    t2 = 'sexcommunicatexcommunicatepotatotherecepotato'
    # Expected output: {'potato': [26, 39], 'tattoo': [], 'theater': [], 'other': [31], 'recep': [35], 'sex': [0], 'excommunicate': [1, 13]}

    t = t2
    keywords = keywords2
    keyword_tree_search(t, keywords)