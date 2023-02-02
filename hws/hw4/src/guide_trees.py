import numpy as np
from typing import Union
from copy import deepcopy
import collections
import itertools
import math

# In UPGMA, node depths must the the same, current visualization doesn't do that.

class GuideTree():
    def __init__(self, scoring_function:str) -> None:
        self.match_score, self.mismatch_penalty, self.gap_penalty = scoring_function

    def needleman_wunsch(self, t1:str, t2:str) -> Union[str, str, np.ndarray, np.ndarray]:
        match_points, mismatch_penalty, indel_penalty = self.match_score, self.mismatch_penalty, self.gap_penalty

        # initialization
        m, n = len(t1), len(t2)
        dp_table = np.zeros((m+1,n+1)).astype(np.int64)
        dp_table[0,:] = np.asarray([-indel_penalty * i for i in range(n+1)])
        dp_table[:,0] = np.asarray([-indel_penalty * i for i in range(m+1)])
        backtrack_table = np.zeros((m+1,n+1)).astype(np.int64)
        
        # fill dp tables
        for i in range(1,m+1):
            for j in range(1,n+1):
                match_score = dp_table[i-1,j-1] + match_points
                mismatch_score = dp_table[i-1,j-1] - mismatch_penalty
                indel_score_up = dp_table[i-1,j] - indel_penalty
                indel_score_left = dp_table[i,j-1] - indel_penalty
                
                if t1[i-1] == t2[j-1]: # match
                    scores = [match_score, indel_score_up, indel_score_left]
                else:
                    scores = [mismatch_score, indel_score_up, indel_score_left]

                max_idx = np.argmax(scores)
                dp_table[i,j] = scores[max_idx]

                if max_idx == 0:
                    backtrack_table[i,j] = 1 # diagonal
                elif max_idx == 1:
                    backtrack_table[i,j] = 2 # up
                elif max_idx == 2: 
                    backtrack_table[i,j] = 3 # left
                else:
                    backtrack_table[i,j] = 0 # error

        # reconstruct / backtrack
        t1_new, t2_new = [],[]
        i,j = m,n
        while i > 0 and j >0:
            if backtrack_table[i,j] == 1: # diagonal
                t1_new = [t1[i-1]] + t1_new
                t2_new = [t2[j-1]] + t2_new
                i -= 1
                j -= 1
            elif backtrack_table[i,j] == 2: # up
                t1_new = [t1[i-1]] + t1_new
                t2_new = ['_'] + t2_new
                i -= 1
            elif backtrack_table[i,j] == 3: # left
                t1_new = ['_'] + t1_new
                t2_new = [t2[j-1]] + t2_new
                j -= 1
            else: # error
                continue

        t1_new = ''.join(t1_new)
        t2_new = ''.join(t2_new)
        # print(t1_new)
        # print(t2_new)
        return t1_new, t2_new, dp_table, backtrack_table

    def get_pairs(self, size:int) -> list:
        pairs = []
        for i in range(size):
            for j in range(i+1,size):
                pairs += [[i,j]]
        return pairs
    
    '''def score_to_distance(self, alignments:dict) -> dict:
        max_score = next(iter(alignments.items()))[1][0]
        distances = {k: 2 - alignments[k][0] / (max_score + 1e-8) for k in alignments} # Set min to 1
        # distances = {k: int((((alignments[k][0] - min_score) / (max_score - min_score + 1e-8))* 2 - 1)*100) for k in alignments} # -100'100
        return distances'''

    # val - min / (max - mmin)
    def score_to_distance(self, alignments:dict) -> dict:
        # Revert signs
        max_score = next(iter(alignments.items()))[1][0]
        distances = {k: 2 - alignments[k][0] / (max_score + 1e-8) for k in alignments}

        # Scale to [0,1] and then to [1,6]
        min_distance = next(iter(distances.items()))[1]
        for k in distances:
            max_distance = distances[k]
        
        distances_scaled = {k: ((distances[k] - min_distance) / (max_distance - min_distance + 1e-8)) * 5 + 1 for k in distances}
        return distances_scaled

    def compute_pairwise_distances(self, sequences:list) -> Union[list,list]:
        pairwise_alignments = {}
        for index in self.get_pairs(len(sequences)):
            alignment_0, alignment_1, dp_table, _ = self.needleman_wunsch(sequences[index[0]][0], sequences[index[1]][0])
            pairwise_alignments[(index[0],index[1])] = [dp_table[-1,-1], alignment_0, alignment_1]
        pairwise_alignments = {k: v for k, v in sorted(pairwise_alignments.items(), key=lambda item: item[1][0], reverse=True)}
        pairwise_distances = self.score_to_distance(pairwise_alignments)
        return pairwise_alignments, pairwise_distances

class UPGMA_HierachicalTree():
    def __init__(self):
        self.children = []
        self.string = ''
        self.depth = 0

    def is_empty(self):
        return bool(self.children) == False

    def update_string(self):
        string = '('
        for idx in range(len(self.children)):
            child = self.children[idx]
            
            if idx == len(self.children) - 1:
                string = f'{string}{child[2]}:{self.depth:.3f}'
            else:
                string = f'{string}{child[2]}:{self.depth:.3f},'
        string = f'{string})'
        self.string = string

    def find_in_children(self, item):
        for idx in range(len(self.children)):
            if self.children[idx][0] == item:
                return idx

class GuideTree_UPGMA(GuideTree):
    def __init__(self, scoring_function:str) -> None:
        super(GuideTree_UPGMA, self).__init__(scoring_function)
    
    def flatten(self, xs):
        for x in xs:
            if isinstance(x, collections.Iterable) and not isinstance(x, (str, bytes)):
                yield from self.flatten(x)
            else:
                yield x

    def update_distances(self, clusters:dict, pairwise_distances:dict) -> dict:
        new_distances = {}
        keys = list(clusters.keys())
        for index in self.get_pairs(len(keys)):
            c0, c1 = keys[index[0]], keys[index[1]]
            if not isinstance(c0, tuple) and not isinstance(c1, tuple):
                new_distances[(c0,c1)] = pairwise_distances[(c0,c1)]
            elif isinstance(c0, tuple) and not isinstance(c1, tuple):
                dist = 0
                counter = 0
                for c in self.flatten(c0):
                    if (c,c1) in pairwise_distances:
                        dist += pairwise_distances[(c,c1)]
                    else:
                        dist += pairwise_distances[(c1,c)]
                    counter += 1
                new_distances[(c0,c1)] = dist / float(counter)
            elif isinstance(c1, tuple) and not isinstance(c0, tuple):
                dist = 0
                counter = 0
                for c in self.flatten(c1):
                    if (c,c0) in pairwise_distances:
                        dist += pairwise_distances[(c,c0)]
                    else:
                        dist += pairwise_distances[(c0,c)]
                    counter += 1
                new_distances[(c0,c1)] = dist / float(counter)
            else: # both tuple
                dist = 0
                counter = 0
                for x in self.flatten(c0):
                    for y in self.flatten(c1):
                        if (x,y) in pairwise_distances:
                            dist += pairwise_distances[(x,y)]
                        else:
                            dist += pairwise_distances[(y,x)]
                        counter += 1
                new_distances[(c0,c1)] = dist / float(counter)
        new_distances = {k: v for k, v in sorted(new_distances.items(), key=lambda item: item[1])}
        return new_distances

    def reformat_tree(self, sequences:list, hierarchy:list) -> str:
        tree = UPGMA_HierachicalTree()

        for step in hierarchy:
            if tree.is_empty():
                string = f'({sequences[step[0][0]][1]}:{step[1]:.3f},{sequences[step[0][1]][1]}:{step[1]:.3f})'
                tree.children += [step + [string]]
                tree.depth = step[1]
                tree.string = string
                pass
            else:
                is_left_tuple, is_right_tuple = isinstance(step[0][0], tuple), isinstance(step[0][1], tuple)

                if is_left_tuple == False and is_right_tuple == False:
                    string = f'({sequences[step[0][0]][1]}:{step[1]:.3f},{sequences[step[0][1]][1]}:{step[1]:.3f})'
                    tree.depth = max(tree.depth,step[1])
                    tree.children += [step + [string]]
                    tree.update_string()
                    pass
                elif ((is_left_tuple and is_right_tuple) == False) and ((is_left_tuple or is_right_tuple) == True):
                    if is_left_tuple:
                        child = step[0][0]
                    else:
                        child = step[0][1]

                    idx = tree.find_in_children(child)

                    # update child
                    tree.children[idx][0] = step[0]
                    tree.children[idx][1] = step[1]
                    string = f'({tree.children[idx][2]}:{tree.children[idx][1]:.3f},{sequences[step[0][0]][1]}:{tree.children[idx][1]:.3f})'
                    tree.children[idx][2] = string

                    # Update tree
                    tree.depth = max(tree.depth, tree.children[idx][1])
                    tree.update_string()
                    pass
                elif (is_left_tuple and is_right_tuple) == True:
                    idx1, idx2 = tree.find_in_children(step[0][0]), tree.find_in_children(step[0][1])
                    child1, child2 = tree.children[idx1], tree.children[idx2]
                    tree.children = [tree.children[i] for i in range(len(tree.children)) if i != idx1 and i != idx2]
                    depth = max(child1[1], child2[1], step[1])
                    string = f'({child1[2]}:{depth:.3f},{child2[2]}:{depth:.3f})'
                    tree.children += [step + [string]]
                    tree.depth = max(tree.depth, depth)
                    tree.update_string()
                    pass
                else:
                    raise Exception('Logic Error in Tree Reformatting.')
        return tree.string

    def construct(self, sequences:list) -> str:
        pairwise_alignments, pairwise_distances = self.compute_pairwise_distances(sequences)
        clusters = {i:0 for i in range(len(sequences))}
        hierarchy = []
        cluster_distances = deepcopy(pairwise_distances)

        while len(clusters) > 1:
            c0, c1 = next(iter(cluster_distances))
            clusters = {c:clusters[c] for c in clusters if c != c0 and c!= c1}
            clusters[(c0,c1)] = cluster_distances[(c0,c1)] / 2.0
            hierarchy += [[(c0,c1), cluster_distances[(c0,c1)] / 2.0]]
            cluster_distances = self.update_distances(clusters, pairwise_distances)        

        # return f'{next(iter(clusters))}' # raw output
        max_depth = next(iter(pairwise_distances.items()))[0][1]
        string = self.reformat_tree(sequences, hierarchy) # editted output
        return string
        
class NJ_NonheadedTreeEdge():
    def __init__(self, vertex1, vertex2, weight):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = weight

class NJ_NonheadTreeNode():
    def __init__(self, id):
        self.edges = []
        self.id = id

class NJ_NonheadedTree():
    def __init__(self):
        self.leaves = {}

    def update_leaf_weights(self, amount:float) -> None:
        for id, leaf in self.leaves.items():
            for vertex in leaf.edges: # O(1) since leaves have 1 edge only
                vertex.weight += amount

    def locate_pathway(self, addr:NJ_NonheadTreeNode, dst:NJ_NonheadTreeNode) -> Union[bool, list]:
        def locate_pathway_worker(addr, dst, hist):
            for edge in addr.edges:
                if edge in hist:
                    continue
                else:
                    hist.append(edge)

                if edge.vertex1 == dst or edge.vertex2 == dst: # base, hit
                    return True, [edge]
                elif (edge.vertex1 == addr and edge.vertex2.id != None and edge.vertex2 == dst) or \
                    (edge.vertex2 == addr and edge.vertex1.id != None and edge.vertex1 == dst): # This is a leaf that isn't dst
                    pass
                else:
                    if edge.vertex1 == addr and edge.vertex2.id == None: # Noneleaf, keep traversing from edge
                        flag, path = locate_pathway_worker(edge.vertex2, dst, hist)
                    elif edge.vertex2 == addr and edge.vertex1.id == None:
                        flag, path = locate_pathway_worker(edge.vertex1, dst, hist)
                    else:
                        flag, path = False, []
                        
                    if flag == False:
                        pass
                    else:
                        return flag, [edge] + path
            return False, [] # Not found in this branch
        return locate_pathway_worker(addr, dst, [])

    def remove_edge(self, src:NJ_NonheadTreeNode, dst:NJ_NonheadTreeNode) -> None:
        for edge in src.edges:
            if (edge.vertex1 == src and edge.vertex2 == dst) or \
                (edge.vertex2 == src and edge.vertex1 == dst):
                src.edges.remove(edge)
                dst.edges.remove(edge)
                del edge        
                return    

    def reformat_tree(self, sequences:list, pairwise_distances:dict) -> str:
        # Format: (A:0.1,B:0.2,(C:0.3,D:0.4):0.5);
        # https://en.wikipedia.org/wiki/Newick_format
        
        def reformat_tree_worker(sequences, addr, hist):
            if len(addr.edges) == 1:
                return f'{sequences[addr.id][1]}:{addr.edges[0].weight:.3f}'
            else:
                substrings = []

                for edge in addr.edges:
                    if edge in hist:
                        continue
                    else:
                        hist.append(edge)

                    other_vertex = edge.vertex1 if edge.vertex1 != addr else edge.vertex2
                    substrings.append(reformat_tree_worker(sequences, other_vertex, hist))

                intermediary_edge = None
                for edge in addr.edges:
                    other_vertex = edge.vertex1 if edge.vertex1 != addr else edge.vertex2
                    if other_vertex.id == None:
                        intermediary_edge = edge
                        break

                string = '('
                for s in substrings:
                    string = f'{string}{s},'
                return f'{string[:-1]}):{intermediary_edge.weight:.3f}'

        # Find the closest pair & the first intermediary node connected to them
        c0, _ = next(iter(pairwise_distances))
        start_node = self.leaves[c0]
        start_edge = start_node.edges[0]
        addr = start_edge.vertex1 if start_edge.vertex1 != start_node else start_edge.vertex2
        string = reformat_tree_worker(sequences, addr, [])
        return string

class GuideTree_NJ(GuideTree):
    def __init__(self, scoring_function:str) -> None:
        super(GuideTree_NJ, self).__init__(scoring_function)

    def find_degenerate(self, elements:list, distances:dict, sigma:float) -> tuple:
        l2dist = lambda x,y: math.sqrt((x-y)**2)

        for t in itertools.combinations(elements, 3):
            d01 = distances[(t[0],t[1])] if (t[0],t[1]) in distances else distances[(t[1],t[0])]
            d02 = distances[(t[0],t[2])] if (t[0],t[2]) in distances else distances[(t[2],t[0])]
            d12 = distances[(t[1],t[2])] if (t[1],t[2]) in distances else distances[(t[2],t[1])]

            if l2dist(d01 + d02, d12) < sigma: # 10 02 12
                return (t[1], t[0], t[2])
            elif l2dist(d01 + d12, d02) < sigma: # 01 12 02
                return (t[0], t[1], t[2])
            elif l2dist(d02 + d12, d01) < sigma: # 02 21 01
                return (t[0], t[2], t[1])
            else:
                pass
        return ()

    def additive_phylogeny(self, sequences: list, distances:dict, delta:float) -> tuple:
        def fix_reductions(tree, distances, delta):
            # extend all edges by delta / 2, 
            tree.update_leaf_weights(delta * 0.5)

            # Update pairwise distances by delta
            for k in distances:
                distances[k] += delta

        def worker(leaves, distances, tree, delta):
            t, count = self.find_degenerate(leaves, distances, delta), 0
            
            if t == ():
                count = 1
                while True:
                    for k in distances:
                        distances[k] -= delta

                    t = self.find_degenerate(leaves, distances, delta)
                    count += 1

                    if t != ():
                        break

            j = t[1]

            if len(leaves) > 3:
                worker([l for l in leaves if l != j], {k:v for k,v in distances.items() if j not in k}, tree, delta)

                # Find the pathway from t[0] to t[2]                    
                _, pathway = tree.locate_pathway(tree.leaves[t[0]], tree.leaves[t[2]])

                # Find insertion point on this pathway at the midpoint of the pathway between t[0] and t[2]
                addr, edge_idx = tree.leaves[t[0]], 0
                fuel = distances[(t[0],t[1])] if (t[0],t[1]) in distances else distances[(t[1],t[0])]
                while True:
                    edge = pathway[edge_idx]
                    addr = edge.vertex1 if edge.vertex2 == addr else edge.vertex2
                    fuel -= edge.weight
                    edge_idx += 1

                    if edge_idx >= len(pathway) or fuel < pathway[edge_idx].weight:
                        break

                if edge_idx >= len(pathway):
                    addr, edge_idx = tree.leaves[t[2]], len(pathway) - 1
                    fuel = distances[(t[2],t[1])] if (t[2],t[1]) in distances else distances[(t[1],t[2])]
                    while True:
                        edge = pathway[edge_idx]
                        addr = edge.vertex1 if edge.vertex2 == addr else edge.vertex2
                        fuel -= edge.weight
                        edge_idx -= 1

                        if fuel < pathway[edge_idx].weight:
                            break

                # Create a new vertex 'anchor' at the midpoint & handle its connections
                anchor = NJ_NonheadTreeNode(None)
                node_opposite = pathway[edge_idx].vertex1 if pathway[edge_idx].vertex2 == addr else pathway[edge_idx].vertex2

                # -----Create edges
                edge_anchor_addr = NJ_NonheadedTreeEdge(anchor, addr, pathway[edge_idx].weight * 0.5)
                edge_anchor_node_opposite = NJ_NonheadedTreeEdge(anchor, node_opposite, pathway[edge_idx].weight * 0.5)

                # -----Remove old connections
                tree.remove_edge(addr, node_opposite)

                # -----Connect the new edge to vertices
                anchor.edges += [edge_anchor_addr, edge_anchor_node_opposite]
                addr.edges += [edge_anchor_addr]
                node_opposite.edges += [edge_anchor_node_opposite]

                # Create new node for t[1] & handle its connections
                new_node = NJ_NonheadTreeNode(t[1])
                # -----Insert to leaves-lookup
                tree.leaves[t[1]] = new_node
                # -----Create and edge between anchor & this node
                new_edge = NJ_NonheadedTreeEdge(new_node, anchor, 0)
                # -----Connect the new edge to the anchor & the new node
                new_node.edges += [new_edge]
                anchor.edges += [new_edge]
                _ = 1
            else:
                d = distances[(t[0],t[2])] if (t[0],t[2]) in distances else distances[(t[2],t[0])]

                child0 = NJ_NonheadTreeNode(t[0])
                child1 = NJ_NonheadTreeNode(t[1])
                child2 = NJ_NonheadTreeNode(t[2])
                anchor = NJ_NonheadTreeNode(None)

                edge0_a = NJ_NonheadedTreeEdge(child0, anchor, d * 0.5)
                edge1_a = NJ_NonheadedTreeEdge(child1, anchor, 0)
                edge2_a = NJ_NonheadedTreeEdge(child2, anchor, d * 0.5)

                child0.edges += [edge0_a]
                child1.edges += [edge1_a]
                child2.edges += [edge2_a]
                anchor.edges += [edge0_a, edge1_a, edge2_a]

                tree.leaves[t[0]] = child0
                tree.leaves[t[1]] = child1
                tree.leaves[t[2]] = child2

            fix_reductions(tree, distances, delta)

            # Fix the previous reductions
            while count > 0:
                fix_reductions(tree, distances, delta)
                count -= 1

        tree = NJ_NonheadedTree()
        worker([i for i in range(len(sequences))], distances, tree, delta)
        return tree

    def construct(self, sequences:list) -> str:
        pairwise_alignments, pairwise_distances = self.compute_pairwise_distances(sequences)
        tree = self.additive_phylogeny(sequences, pairwise_distances, 0.25)
        string = tree.reformat_tree(sequences, pairwise_distances)
        return string