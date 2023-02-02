from string import punctuation
import random

class Node():
    def __init__(self, parent, index):
        self.parent = parent
        self.index = index # start idx of the pattern
        self.children = {}

class SuffixTree():
    def __init__(self, keywords) -> None:
        self.keywords = keywords
        self.all_special_characters = punctuation.replace('\\','').replace('"','').replace("'",'') + ''.join(['£','€','ß'])
        self.special_characters = random.SystemRandom().sample(self.all_special_characters,  len(keywords))
        self.create_suffix_tree_naive()

    def create_suffix_tree_naive(self):
        root = Node(None, -1)

        for kidx in range(len(self.keywords)):
            keyword = self.keywords[kidx]
            suffixes = [keyword[i:] + self.special_characters[kidx] for i in range(len(keyword)+1)]

            for i in range(len(suffixes)):
                head = root
                suffix = suffixes[i]
                while True:
                    if len(head.children) < 1 and head is root: # empty root, insert
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
        self.root = root                     

    # Improvement over keyword trees:
    # Reduced space requirement due to compact tree hierarchy
    # One potential limitation is having to address associating a unique character for each keyword
    # Also, having to compare each edge during search is costly
    def query(self, text):
        print('---> Suffix Tree')
        root = self.root
        head = root
        matches = {k:[] for k in self.keywords}
        i = 0
        comparisons = 0

        while i < len(text):
            j = i
            while True:
                flag = False
                match = False
                print(f'\t{head} ->')

                for child in head.children:
                    if child in self.special_characters:
                        if j < len(text):
                            comparisons += 1
                            print(f'\t\ttarget = {text[j]}, edge = {child}, comparisons = {comparisons}.')
                        continue

                    clean_child = child[:-1] if child[-1] in self.special_characters else child
                    comparisons += 1

                    if text[j:j+len(clean_child)] == clean_child:
                        if len(head.children[child].children) < 1 and text[i:i+head.children[child].index-1] in self.keywords:
                            match = True
                            matches[text[i:i+head.children[child].index-1]] += [i]
                            print(f'\t*** Pattern {text[i:i+head.children[child].index-1]} found at i = {i}, continue from i = {i+1}\n')
                        else:
                            print(f'\t\tPartial match at j={j} for edge={child}, comparisons = {comparisons}.')
                            head = head.children[child]
                            j += len(clean_child)
                            flag = True
                        break
                    else:
                        if j < len(text):
                            print(f'\t\ttarget = {text[j:j+len(clean_child)]}, edge = {child}, comparisons = {comparisons}.')

                if flag == False:
                    head = root
                    i += 1
                    if match == False:
                        print(f'\t*** No matching edge found for i = {i-1}, comparisons = {comparisons}, restart at i = {i}.\n')
                    break
        
        print(f'\tSearch complete. Total comparisons = {comparisons}.')
        return matches

    def output_tree(self, path):
        queue = [self.root]
        nodes = {self.root:0}
        edges = []
        nidx = 1
        
        while len(queue) > 0:
            head = queue.pop(0)

            for child in head.children:
                edges += [(head, head.children[child], child)]
                nodes[head.children[child]] = nidx
                nidx += 1
                queue += [head.children[child]]

        with open(path, 'w') as file:
            file.write('digraph MySuffixTree {\n')
            for _, (node, idx) in enumerate(nodes.items()):
                file.write(f'\tn{idx}\t[label="{node.index}"]\n')

            file.write('\n')

            for (source, dest, label) in edges:
                file.write(f'\tn{nodes[source]} -> n{nodes[dest]}\t[label="{label}"]\n')

            file.write('}')