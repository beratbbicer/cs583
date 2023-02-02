import numpy as np

# local alignment with weighted mismatch/indel penalty
# in backtrack table, 1 -> diagonal, 2 -> up, 3 -> left.
def smith_waterman(t1, t2, match_points, mismatch_penalty, indel_penalty):
    # initialization
    m, n = len(t1), len(t2)
    dp_table = np.zeros((m+1,n+1)).astype(np.int64)
    backtrack_table = np.zeros((m+1,n+1)).astype(np.int64)
    
    # fill dp tables
    for i in range(1,m+1):
        for j in range(1,n+1):
            match_score = dp_table[i-1,j-1] + match_points
            mismatch_score = dp_table[i-1,j-1] - mismatch_penalty
            indel_score_up = dp_table[i-1,j] - indel_penalty
            indel_score_left = dp_table[i,j-1] - indel_penalty
            
            if t1[i-1] == t2[j-1]: # match
                scores = [0, match_score, indel_score_up, indel_score_left]
            else:
                scores = [0, mismatch_score, indel_score_up, indel_score_left]

            max_idx = np.argmax(scores)

            dp_table[i,j] = scores[max_idx]

            if max_idx == 1:
                backtrack_table[i,j] = 1 # diagonal
            elif max_idx == 2:
                backtrack_table[i,j] = 2 # up
            elif max_idx == 3: 
                backtrack_table[i,j] = 3 # left
            else:
                backtrack_table[i,j] = 0 # free ride - restart alignment

    # reconstruct / backtrack
    t1_new, t2_new = [],[]
    i,j = np.unravel_index([np.argmax(dp_table)], (m+1,n+1))
    i,j = i[0], j[0]
    while dp_table[i,j] != 0:
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
        else: # stop
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
    mismatch_penalty = 1
    indel_penalty = 2
    t1_new, t2_new = smith_waterman(t1,t2,match_points,mismatch_penalty,indel_penalty)