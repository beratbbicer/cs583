import numpy as np

def affine_gap_alignment(t1,t2,match_points,mismatch_penalty,gap_opening_penalty,gap_extension_penalty):
    m, n = len(t1), len(t2)
    t1_gap_table = np.zeros((m+1,n+1)).astype(np.int64)
    t2_gap_table = np.zeros((m+1,n+1)).astype(np.int64)
    match_table = np.zeros((m+1,n+1)).astype(np.int64)
    score_table = np.zeros((m+1,n+1)).astype(np.int64)
    backtrack_table = np.zeros((m+1,n+1)).astype(np.int64)

    t1_gap_table[0,0] = -1e4
    t1_gap_table[0,1:] = 0
    t1_gap_table[1:,0] = -gap_opening_penalty - np.arange(1,m+1,1) * gap_extension_penalty

    t2_gap_table[0,0] = -1e4
    t2_gap_table[1:,0] = 0
    t2_gap_table[0,1:] = -gap_opening_penalty - np.arange(1,n+1,1) * gap_extension_penalty

    match_table[0,0] = -1e4

    score_table[0,0] = 0
    score_table[1:,0] = -gap_opening_penalty - np.arange(1,m+1,1) * gap_extension_penalty
    score_table[0,1:] = -gap_opening_penalty - np.arange(1,n+1,1) * gap_extension_penalty

    backtrack_table[0,0] = 0
    backtrack_table[1:,0] = 2
    backtrack_table[0,1:] = 3

    for i in range(1,m+1):
        for j in range(1,n+1):
            t1_gap_table[i,j] = max(t1_gap_table[i-1,j] - gap_extension_penalty, match_table[i-1,j] - gap_opening_penalty - gap_extension_penalty)
            t2_gap_table[i,j] = max(t1_gap_table[i,j-1] - gap_extension_penalty, match_table[i,j-1] - gap_opening_penalty - gap_extension_penalty)

            if t1[i-1] == t2[j-1]:
                match_table[i,j] = max(match_table[i-1,j-1] + match_points, t1_gap_table[i,j], t2_gap_table[i,j])
                # match_table[i,j] = match_table[i-1,j-1] + match_points
            else:
                match_table[i,j] = max(match_table[i-1,j-1] - mismatch_penalty, t1_gap_table[i,j], t2_gap_table[i,j])
                # match_table[i,j] = match_table[i-1,j-1] - mismatch_penalty

            values = [match_table[i,j], t2_gap_table[i,j], t1_gap_table[i,j]]
            max_val = max(values)
            if max_val == values[1]:
                score_table[i,j] = t2_gap_table[i,j]
                backtrack_table[i,j] = 2 # up
            elif max_val == values[2]:
                score_table[i,j] = t1_gap_table[i,j]
                backtrack_table[i,j] = 3 # left
            else:
                score_table[i,j] = match_table[i,j]
                backtrack_table[i,j] = 1 # diagonal

    
    with np.printoptions(threshold=np.inf, linewidth=100000):
        print(backtrack_table)
        print(score_table)
    

    # reconstruct / backtrack
    t1_new, t2_new = [],[]
    i,j = m,n
    while i > 0 and j > 0:
        if backtrack_table[i,j] == 1: # diagonal
            t1_new = [t1[i-1]] + t1_new
            t2_new = [t2[j-1]] + t2_new
            i -= 1
            j -= 1
        elif backtrack_table[i,j] == 2: # up
            t1_new = ['_'] + t1_new
            t2_new = [t2[j-1]] + t2_new
            j -= 1
        elif backtrack_table[i,j] == 3: # left
            t1_new = [t1[i-1]] + t1_new
            t2_new = ['_'] + t2_new
            i -= 1
        else: # error
            break

    t1_new = ''.join(t1_new)
    t2_new = ''.join(t2_new)
    print(t1_new)
    print(t2_new)
    return t1_new, t2_new
    _ = 1
    
if __name__ == "__main__":
    t1 = 'AGCCTAGCTAGCCATGATCCAGAACAAAA'
    t2 = 'AAAGTCCATAAAGCCTAGCAACATAGCCTAAAA'

    match_points = 1
    mismatch_penalty = 2
    gap_opening_penalty = 16
    gap_extension_penalty = 1
    t1_new, t2_new = affine_gap_alignment(t1,t2,match_points,mismatch_penalty,gap_opening_penalty,gap_extension_penalty)