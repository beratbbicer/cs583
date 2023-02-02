import numpy as np

def create_deterministic_finite_automata(p, sigma):
    suffixes = [p[:i] for i in range(len(p), -1, -1)]
    deterministic_finite_automata = np.zeros((len(p)+1,len(sigma))).astype(np.int64)
    for i in range(len(p)+1):
        for j in range(len(sigma)):
            # delta(i,sigma[j]) -> p[:i] . sigma[j]
            # Find largest suffix of this in suffixes array
            word = f'{p[:i]}{sigma[j]}'
            flag = False

            for k in range(len(word), -1, -1):
                if suffixes[len(suffixes) - 1 - k] == word[len(word) - k:]:
                    deterministic_finite_automata[i,j] = k
                    flag = True
                    break

            if flag == False:
                deterministic_finite_automata[i,j] = 0

    return deterministic_finite_automata

def finite_automaton_search(t, p, sigma):
    dfa = create_deterministic_finite_automata(p, sigma)
    sigma_lookup = {sigma[i]:i for i in range(len(sigma))}
    matches = []
    state = 0
    for i in range(len(t)):
        if dfa[state, sigma_lookup[t[i]]] == len(p):
            matches.append(i-len(p)+1)
            
        state = dfa[state, sigma_lookup[t[i]]]

    print(matches)
    return matches

if __name__ == "__main__":
    t0 = 'ABABAABABACBCABABACABABABACAABABACBABABACABABABACABABACCABABAC'
    t1 = 'ABABAABABACBCABABACABABABACAABABACBABABACABABABACABABACCABABACABABBABABBCBABCBCBCABABAABABABCBABCBACBB'

    t = t0
    p = 'ABABAC'
    sigma = 'ABC'
    finite_automaton_search(t,p,sigma)
    # [5, 13, 21, 28, 35, 43, 49, 56] 