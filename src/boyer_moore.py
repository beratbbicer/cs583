import copy
import time

# This is supposed to be O(m + sigma), but I don't see how?
# Best I can do atm is O(m*sigma)
def bad_character_lookup(p, sigma):
    table = [{a:-1 for a in sigma} for _ in range(len(p))]

    for i in range(0,len(p)-1):
        for letter in sigma:
            if p[i] == letter:
                table[i+1][letter] = i
            else:
                table[i+1][letter] = table[i][letter]

    return table

'''
# To do this w/o loops, we can modify a running update rule
# Since default copy behavior of python is shallow copy, deep copy is required, which is expensive
# But, assuming assignment is O(1), this is O(m)
def bad_character_lookup2(p, sigma):
    counter = {a:-1 for a in sigma}
    counter[p[0]] = 0
    table = [counter]
    
    for i in range(1,len(p)):
        counter2 = copy.deepcopy(counter)
        counter2[p[i]] = i
        table.append(counter2)
        counter = counter2

    return table
'''

# Good Suffix Rule 1:
# Start iterating from j':j-1,0 which points to the candidate head
# And the candidate suffix becomes j'+1:j'+1+len(suffix)
# Save j' and iterate j, if heads do not match but the suffixes do
# WOrst case O(mxm), doesn't affect the worst-case scenario of the algorithm
def goodsuffix1_lookup(p):
    gs1 = [-1 for _ in range(len(p))]
    for j in range(len(p)):
        head, suffix = p[j], p[j+1:]
        if suffix == '':
            continue
        else:
            for idx in range(j-1,-1,-1):
                new_head, new_suffix = p[idx], p[idx+1:idx+1+len(suffix)]
                if suffix == new_suffix and head != new_head:
                    gs1[j] = idx + len(suffix)
                    break
    return gs1

# Good Suffix Rule 2:
# Find the largest k in range 0 <= k <= m-j s.t.
#   p[:k+1] is a suffix of p[j+1:]
def goodsuffix2_lookup(p):
    gs2 = [-1 for _ in range(len(p))]
    for j in range(len(p)):
        for k in range(len(p)-j-1,-1,-1):
            suffix = p[:k+1]
            if p[j+1:][-len(suffix):] == suffix:
                gs2[j] = k
                break
    return gs2

'''
What changed?
    1. Index i points to the start of the string
    2. When there's a match, we iterate i by one to continue from the next character
    3. Since BC table is filled with indices, the jump quantity is calculated with null = -1 instead of 0 (contrary to the slides)
    4. Good Suffix jump is 1 if j = len(p) - 1, ie., when the last characters mismatch / the first comparison failes
    5. Otherwise, maximum of GS1 & GS2 skips is selected, but jump is still calculated based on index values, i.e., len(p) - 1 instead.

    Not mentioning the fact that this code finds all matches in the given string, 
    So preprocessing might be worse, in terms of complexity, than what's been shown in the slides.
    Mine is, I think, worst-case O(m * Sigma) whereas the slides claim it should be O(m + Sigma).
    Overall, still worst-case O(n*m).
'''
def boyer_moore_sm(t, p):
    sigma = ''.join(set(t))
    bc_lookup = bad_character_lookup(p, sigma)
    gs1_lookup = goodsuffix1_lookup(p)
    gs2_lookup = goodsuffix2_lookup(p)
    i = 0
    matches = []

    while i <= len(t)-len(p):
        j = len(p) - 1
        while j >= 0 and p[j] is t[i+j]:
            j -= 1

        if j < 0: 
            matches.append(i)
            i += len(p)
        else:
            bc_jump = j - bc_lookup[j][t[i+j]]
            if j == len(p) - 1:
                gs_jump = 1
            else:
                gs_jump = len(p) - 1 - max(gs1_lookup[j], gs2_lookup[j], 0)
            i += max(bc_jump, gs_jump)

    print(matches)
    return matches

if __name__ == "__main__":
    t1 = 'AAAAAAGCCTAGCAACAAAA'
    p1 = 'ATCACATCATCA'

    t2 = 'ABABABCABABABCABABAC'
    p2 = 'ABABAC'

    t21 = 'ABABAABABACBCABABABCABABAC'
    #           |----|
    #           5----10
    p21 = 'ABABAC'
    
    #            9          19         29         39         49         59
    # 'ABABAABAB ACBCABABAC ABABABACAA BABACBABAB ACABABABAC ABABACCABA BAC'
    t22 = 'ABABAABABACBCABABACABABABACAABABACBABABACABABABACABABACCABABAC'
    p22 = 'ABABAC'

    # Works for this:
    t23 = 'ABABACABABACCABABAC'
    p23 = 'ABABAC'

    # gs1 = [-1,-1,-1,-1,-1,-1]

    t3 = 'ABABABCABABABCABCBAB'
    p3 = 'ABCBAB'

    '''
    t1 = time.time()
    bad_character_lookup(p,sigma)
    t2 = time.time()
    print(f'Runtime of bad_character_lookup (nano-seconds): {(t2-t1) * 1e6}')

    t1 = time.time()
    bad_character_lookup2(p,sigma)
    t2 = time.time()
    print(f'Runtime of bad_character_lookup (nano-seconds): {(t2-t1) * 1e6}')
    '''

    # gs1_lookup(p1)

    boyer_moore_sm(t22,p22)

    '''
    gs:
          0   1   2   3   4   5
          A   B   A   B   A   C
    gs1  -1  -1  -1  -1  -1  -1
    gs2  -1  -1  -1  -1  -1  -1
    gs    6   6   6   6   6   1


    bc:
        0   1   2   3   4   5
        A   B   A   B   A   C
    A   0   0   2   2   4   4
    B  -1   1   1   3   3   3
    C  -1  -1  -1  -1  -1   5
    '''