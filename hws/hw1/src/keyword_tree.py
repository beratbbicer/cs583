class Node():
    def __init__(self, parent, index):
        self.parent = parent
        self.index = index # start idx of the pattern
        self.children = {}

class KeywordTree():
    def __init__(self, keywords) -> None:
        self.keywords = keywords
        self.create_tree_naivethreading()
    
    # O(N) where N -> total size of the patterns
    def create_tree_naivethreading(self):
        root = Node(None, -1)
        for keyword in self.keywords:
            head = root
            for i in range(len(keyword)):
                s = keyword[i]
                if s not in head.children:
                    head.children[s] = Node(head, head.index+1)
                
                head = head.children[s]
        self.root = root

    # O(N + nm), N: total length of patterns, n: length of t, m: length of a pattern
    def query(self, text):
        print('---> Keyword Tree')
        root = self.root
        matches = {k:[] for k in self.keywords}
        head = root
        i = 0
        comparisons = 0

        while i < len(text):
            j = i
            x = text[i]
            while j < len(text):
                y = text[j]
                
                print(f'\t{head} ->')
                for child in head.children:
                    if child != text[j]:
                        comparisons += 1
                        print(f'\t\ttarget_char = {y}, candidate = {child}, comparisons = {comparisons}')

                if text[j] in head.children: # match
                    child = head.children[text[j]]
                    idx = j - child.index
                    keyword = text[idx:j+1]

                    if len(child.children) < 1: # exact match at a leaf
                        matches[keyword] += [idx]
                        head = root
                        i += 1
                        print(f'\t*** Pattern {keyword} found at i = {idx}, continue from i = {i}\n')
                        break
                    else: # Continue until you get a mismatch
                        comparisons += 1
                        head = head.children[text[j]]
                        print(f'\t\tCharacter match at j={j}, comparisons = {comparisons}.')
                        j += 1

                else: # no match
                    head = root
                    i += 1
                    print(f'\t*** Character mismatch at j = {j}, comparisons = {comparisons}, restart at i = {i}.\n')
                    break
        
        print(f'\tSearch complete. Total comparisons = {comparisons}.')
        return matches