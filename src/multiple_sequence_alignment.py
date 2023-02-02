from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import numpy as np

class MSA_CenterStar():
    def __init__(self, scoring_function) -> None:
        self.match_score, self.mismatch_penalty, self.gap_penalty = scoring_function
    
    def needleman_wunsch(self, t1, t2):
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

    def get_alignment_pairs(self, size):
        pairs = []
        for i in range(size):
            for j in range(i+1,size):
                pairs += [[i,j]]
        return pairs

    def create_profile(self, alignment):
        alphabet = {'_'}
        for sequence in alignment:
            alphabet = alphabet | set(sequence)
        alphabet = list(alphabet)

        alphabet_lookup = {alphabet[i]:i for i in range(len(alphabet))}
        profile = np.zeros((len(alphabet), len(alignment[0])))
        
        for i in range(len(alignment)):
            for j in range(len(alignment[0])):
                profile[alphabet_lookup[alignment[i][j]],j] += 1

        return alphabet_lookup, profile

    def column_alignment_score(self, i, j, alphabet_lookup, profile, sequence):
        if i == '_':
            x = '_'
        else:
            x = sequence[i]
        score = 0

        for y in alphabet_lookup.keys():
            frequency = profile[:,j][alphabet_lookup[y]] / profile[:,j].sum()

            if (y == '_' and x != '_')  or (y != '_' and x == '_'):
                score -= self.gap_penalty * frequency
            elif x == y:
                score += self.match_score * frequency
            elif x != y:
                score -= self.mismatch_penalty * frequency
            else:
                raise Exception('Error in logic -- column alignment score.')
        return score

    def sequence_profile_alignment(self, alphabet_lookup, profile, alignments, next_sequence):
        # Update the alphabet
        new_letters = list(set(next_sequence[0]) - set(alphabet_lookup.keys()))
        if len(new_letters) != 0:
            for i in range(len(new_letters)):
                alphabet_lookup[new_letters[i]] = len(alphabet_lookup)

            profile = np.vstack((profile, np.zeros((len(new_letters), profile.shape[1]))))

        # Initialize DP table
        sequence = next_sequence[0]
        dp_table, backtrack_table = np.zeros((len(sequence) + 1, profile.shape[1] + 1)), np.zeros((len(sequence) + 1, profile.shape[1] + 1))

        for j in range(1, profile.shape[1]+1):
            dp_table[0,j] = dp_table[0,j-1] + self.column_alignment_score('_', j-1, alphabet_lookup, profile, sequence)
            backtrack_table[0,j] = 3 # left, profile

        for i in range(1, len(sequence)+1):
            dp_table[i,0] = dp_table[i-1,0] - self.gap_penalty
            backtrack_table[i,0] = 2 # up, sequence

        # Fill DP table
        for i in range(1,len(sequence)+1):
            for j in range(1,profile.shape[1]+1):
                diagonal = dp_table[i-1,j-1] + self.column_alignment_score(i-1, j-1, alphabet_lookup, profile, sequence)

                if sequence[i-1] == '_':
                    up = dp_table[i-1,j] + self.match_score
                else:
                    up = dp_table[i-1,j] - self.gap_penalty

                left = dp_table[i,j-1] + self.column_alignment_score('_', j-1, alphabet_lookup, profile, sequence)

                max_value = max([diagonal, up, left])
                dp_table[i,j] = max_value

                if max_value == diagonal:
                    backtrack_table[i,j] = 1 # diagonal
                elif max_value == up:
                    backtrack_table[i,j] = 2 # up
                elif max_value == left:
                    backtrack_table[i,j] = 3 # left
                else:
                    raise Exception('Error in logic -- DP loop.')

                _ = 1
        _ = 1

        new_alignments, new_sequence = {e:[] for e in alignments}, []
        i,j = len(sequence), profile.shape[1]
        while i > 0 and j > 0:
            if backtrack_table[i,j] == 1: # diagonal
                new_sequence = [sequence[i-1]] + new_sequence

                for e in new_alignments:
                    new_alignments[e] = [alignments[e][j-1]] + new_alignments[e]

                i -= 1
                j -= 1
            elif backtrack_table[i,j] == 2: # up
                new_sequence = [sequence[i-1]] + new_sequence

                for e in new_alignments:
                    new_alignments[e] = ['_'] + new_alignments[e]

                i -= 1
            elif backtrack_table[i,j] == 3: # left
                new_sequence = ['_'] + new_sequence

                for e in new_alignments:
                    new_alignments[e] = [alignments[e][j-1]] + new_alignments[e]

                j -= 1
            else: # error
                raise Exception('Error in logic -- backtrack.')

        new_sequence = ''.join(new_sequence)
        for e in new_alignments:
            new_alignments[e] = ''.join(new_alignments[e])

        return new_alignments, new_sequence

    def align(self, sequences):
        # Pairwise Alignments
        pairwise_alignments = []
        for index in self.get_alignment_pairs(len(sequences)):
            alignment_0, alignment_1, dp_table, _ = self.needleman_wunsch(sequences[index[0]][0], sequences[index[1]][0])
            pairwise_alignments.append([index, dp_table[-1,-1], alignment_0, alignment_1])
        
        # Star Scores
        max_score, center_star = -10**8, -1
        for i in range(len(sequences)):
            score = 0
            for j in range(len(pairwise_alignments)):
                if i in pairwise_alignments[j][0]:
                    score += pairwise_alignments[j][1]

            if score >= max_score:
                max_score = score
                center_star = i 

        # Compute initial profile and alignments
        center_star_neighbourhood = sorted([x for x in pairwise_alignments if center_star in x[0]], key=lambda x: x[1], reverse=True)
        alphabet_lookup, profile = self.create_profile([center_star_neighbourhood[0][2], center_star_neighbourhood[0][3]])
        current_alignments = {center_star_neighbourhood[0][0][0]:center_star_neighbourhood[0][2],\
            center_star_neighbourhood[0][0][1]:center_star_neighbourhood[0][3]}

        # Iteratively add new sequences to the alignment
        if len(center_star_neighbourhood) > 1:
            for j in range(1,len(center_star_neighbourhood)):
                next_sequence = [x for x in center_star_neighbourhood[j][0] if x != center_star][0]
                new_alignments, new_sequence = self.sequence_profile_alignment(alphabet_lookup, profile, current_alignments, sequences[next_sequence])
                new_alignments[next_sequence] = new_sequence
                current_alignments = new_alignments
                alphabet_lookup, profile = self.create_profile(list(current_alignments.values()))
                _ = 1
        
        return [SeqRecord(Seq(current_alignments[i]), id=sequences[i][1], name=sequences[i][1])\
            for i in range(len(sequences)) if i in current_alignments]