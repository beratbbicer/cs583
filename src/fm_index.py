from xxlimited import new
import numpy as np
import math

class FMIndex():
    def __init__(self, t, tally_step, suffix_step) -> None:
        self.t = t
        self.tally_step = tally_step
        self.suffix_step = suffix_step
        self.sigma = sorted(list(set(t + '$')))
        self.f, self.bwt = self.burrows_wheeler_transform(t)
        self.tally_lookup = self.get_tally_lookup(self.bwt, self.sigma, tally_step)
        self.suffix_array = self.get_suffix_array(t, suffix_step)
        self.ranks = self.get_rank_array(self.f, self.sigma)
        self.counts = self.get_count_array(t, self.sigma)

    def nearest_int(self, i, d):
        x, y = i - (i % d), (i+d) - (i%d)

        if i - x > y - i:
            return y
        else:
            return x

    def burrows_wheeler_transform(self, t):
        t = t + '$'
        rotations = []
        for i in range(len(t)):
            rotations += [t[i] + t[i+1:len(t)] + t[0:i]]

        rotations = sorted(rotations, reverse=False)
        f, l = [s[0] for s in rotations], [s[-1] for s in rotations]
        return f, l

    def get_tally_lookup(self, bwt, sigma, tally_step):
        lookup = {x:[0 for _ in range(len(bwt))] for x in sigma}
        for i in range(len(bwt)):
            if i != 0:
                lookup[bwt[i]][i] = lookup[bwt[i]][i-1] + 1
                for c in sigma:
                    if c != bwt[i]:
                        lookup[c][i] = lookup[c][i-1]
                    else:
                        continue
            else:
                lookup[bwt[i]][i] = 1

        for i in range(len(bwt)):
            if i % tally_step != 0:
                for s in sigma:
                    lookup[s][i] = None

        return lookup
    
    def do_tally_lookup(self, char, bwt, idx, tally_lookup, tally_step):   
        if tally_lookup[char][idx] != None:
            return tally_lookup[char][idx]
        else:
            target = max(0, self.nearest_int(idx, tally_step))      
            while target >= len(tally_lookup[char]):
                target -= tally_step 

            cur_tally = tally_lookup[char][target]

            if target > idx:
                i = target - 1
                while True:
                    if bwt[i + 1] == char:
                        cur_tally -= 1

                    if i <= idx:
                        break
                    else:
                        i -= 1
            elif target < idx:
                i = target + 1
                while True:
                    if bwt[i] == char:
                        cur_tally += 1
                    
                    if i >= idx:
                        break
                    else:
                        i += 1
            else:
                raise Exception('Error in logic.')
            return cur_tally

    def get_suffix_array(self, t, suffix_step):
        suffix_array = [(t[len(t)-i:] + '$',len(t)-i) for i in range(0,len(t)+1)]
        suffix_array = sorted(suffix_array, key= lambda v: v[0])
        for i in range(len(suffix_array)):
            if suffix_array[i][1] % suffix_step != 0:
                suffix_array[i] = None
        return suffix_array

    def get_rank_array(self, f, sigma):
        ranks = {i: -1 for i in sigma}
        for i in range(len(f)):
            if ranks[f[i]] == -1:
                ranks[f[i]] = i

            if -1 not in ranks.values():
                break
        return ranks

    def get_count_array(self, t, sigma):
        counts = {i: 0 for i in sigma}
        for i in range(len(t)):
            counts[t[i]] += 1

        counts['$'] = 1
        return counts

    def f_to_l_map(self, idx, bwt, sigma, counts, tally_lookup, tally_step):
        char = bwt[idx]
        new_idx = 0
        for i in range(len(sigma)):
            if sigma[i] != char:
                new_idx += counts[sigma[i]]
            else:
                break
        
        occ = self.do_tally_lookup(char, bwt, idx, tally_lookup, tally_step)
        new_idx += occ
        return new_idx

    def resolve_search_offset(self, idx, bwt, suffix_array, tally_lookup, tally_step, sigma, counts):
        if suffix_array[idx] is not None:
            return suffix_array[idx][1]
        else:
            f_idx = idx
            count = 0
            while f_idx not in suffix_array and (0 <= f_idx and f_idx < len(bwt)) and bwt[f_idx] != '$':
                f_idx = self.f_to_l_map(f_idx, bwt, sigma, counts, tally_lookup, tally_step) - 1
                count += 1
            
            return suffix_array[f_idx][1] + count

    def query(self, p):
        i, j = 1, len(self.bwt) - 1
        for idx in range(len(p)-1, -1, -1):
            occ_i = self.do_tally_lookup(p[idx], self.bwt, i-1, self.tally_lookup, tally_step)
            occ_j = self.do_tally_lookup(p[idx], self.bwt, j, self.tally_lookup, tally_step)

            if idx == len(p)-1 and occ_i != 0:
                i_new = self.ranks[p[idx]] + occ_i - 1
            else:
                i_new = self.ranks[p[idx]] + occ_i

            j_new = self.ranks[p[idx]] + occ_j - 1

            _ = 1

            i = i_new
            j = j_new
        
        if i <= j:
            matches = []
            for idx in range(i, j+1): 
                t_idx = self.resolve_search_offset(idx, self.bwt, self.suffix_array, self.tally_lookup, tally_step, self.sigma, self.counts)
                matches += [t_idx]

            print(matches)
            return matches
        else:
            print('No matches.')
            return None

if __name__ == "__main__":
    t0 = 'AGCCTAGCTAGTACCATGATCCAGAACAAAAGGGATCAGTCCATAAAGCCTAGCAACAAAGTCCATCAAAGCCTAGCAACACCTAGCCTGCCGAAAATAGCCTAAAAAAAGTCCATAAAGCCTAGCAACATAGCCTAAAAGTCCATAAAGCCTAGCAACATAGCCTAAAAAAA'
    t1 = 'ABCDE'
    t2 = 'AABBCCDDEE'
    t3 = 'abaaba'
    t4 = 'agcagcagact'
    t5 = 'aaabbbcccdddbbbeee'
    t6 = 'mississippi'

    p0 = 'TAGCC'
    p1 = 'gca'
    p2 = 'bba'
    p3 = 'aa'
    p4 = 'aba'
    p5 = 'bbb'
    p6 = 'iss'

    tally_step = 3
    suffix_step = 3
    
    fm_index = FMIndex(t3, tally_step, suffix_step)
    # fm_index.query(p4)
    # fm_index.query('baa')
    fm_index.query('abb')

    '''fm_index = FMIndex(t4, tally_step, suffix_step)
    fm_index.query(p1)'''

    '''fm_index = FMIndex(t6, tally_step, suffix_step)
    fm_index.query(p6)'''

    '''fm_index = FMIndex(t5, tally_step, suffix_step)
    fm_index.query(p5)'''
    