import numpy as np

def bitap_shift_and(t, p, sigma):
    def bitshift(arr):
        return np.hstack((np.asarray([True]), arr[:-1]))

    # O(m) since each position contains a unique character
    u = {sigma[i]:np.zeros((len(p))).astype(bool) for i in range(len(sigma))}
    for i in range(len(p)):
        u[p[i]][i] = True

    prev = np.zeros((len(p))).astype(bool)
    matches = []

    for i in range(len(t)):
        cur = bitshift(prev) & u[t[i]]

        if cur[-1] == True:
            matches += [i-len(p)+1] # start idx

        prev = cur

    print(matches)
    return matches
    _ = 1


if __name__ == "__main__":
    t0 = 'ABABAABABACBCABABACABABABACAABABACBABABACABABABACABABACCABABAC'
    t1 = 'ABABAABABACBCABABACABABABACAABABACBABABACABABABACABABACCABABACABABBABABBCBABCBCBCABABAABABABCBABCBACBB'

    t = t0
    p = 'ABABAC'
    sigma = 'ABC'

    bitap_shift_and(t,p,sigma)
    # [5, 13, 21, 28, 35, 43, 49, 56] 