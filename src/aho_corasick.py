from keyword_trees import keyword_tree_naivethreading, keyword_tree_search
import time
# Dependency on a prebuilt keyword tree

# Exploit BFS to successfully compute failure links
# Results in an NFA where failure links are epsilon transitions
def create_failure_links(kt_root):
    assert len(kt_root.children) > 0, 'Error -- faulty tree.'
    queue = [kt_root]
    while len(queue) > 0:
        head = queue.pop(0)
        
        if head == kt_root or head.parent == kt_root:
            head.failure_link = kt_root
        else:
            for child in head.parent.children:
                if head.parent.children[child] is head:
                    break

            address = head.parent.failure_link
            while child not in address.children and address is not kt_root:
                address = address.failure_link

            if child in address.children:
                head.failure_link = address.children[child]
            else:
                head.failure_link = kt_root

        for child in head.children:
            queue += [head.children[child]]

# Improvement over keyword trees:
# More space requirement due to failure links
# But, more efficient at search time in O(n) instead of O(n*m) due to 'remembering' past inputs
# Similar to finite automaton search algorithm (check 'finite_automaton_search.py')
def aho_corasick(t, p, root):
    create_failure_links(root)
    matches = {k:[] for k in p}
    head = root
    i = 0
    j = i

    while j < len(t):
        x = t[i]
        y = t[j]

        if t[j] in head.children: # match
            child = head.children[t[j]]
            idx = j - child.index
            keyword = t[idx:j+1]

            if len(child.children) < 1: # this is a leaf
                matches[keyword] += [idx]
                i = j - child.failure_link.index
                head = child.failure_link
                j += 1
            else:
                head = head.children[t[j]]
                j += 1

        else: # no match
            if head.failure_link is root and t[j] not in root.children: # A character that is nonexistent in given patterns observed.
                j += 1
                i = j
                head = root
            else: # character observed previously, follow the failure links
                i = j - head.failure_link.index
                head = head.failure_link

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
    
    t1 = time.time()
    root, matches = keyword_tree_search(t, keywords)
    t2 = time.time()
    print(f'Elapsed time: {t2 - t1}')

    t1 = time.time()
    root, matches = aho_corasick(t, keywords, root)
    t2 = time.time()
    print(f'Elapsed time: {t2 - t1}')

    t1 = time.time()
    kt_root = keyword_tree_naivethreading(keywords)
    kt_root, matches = aho_corasick(t, keywords, kt_root)
    t2 = time.time()
    print(f'Elapsed time: {t2 - t1}')