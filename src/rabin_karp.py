# Remember the following algebraic operations under modulo:
# 1. (a + b) mod x = ((a mod x) + (b mod x)) mod x
# 1. (a * b) mod x = ((a mod x) * (b mod x)) mod x

import numpy as np

def rabin_karp(t, p, sigma, prime):
    base = len(sigma)
    if len(t) < len(p):
        return None
    else:
        matches = []
        base_coeffs = base ** np.array([i for i in range (len(p)-1,-1,-1)])
        p_hash = (base_coeffs * np.array([ord(i) for i in p])).sum() % prime
        i = 0

        while True:
            t_hash = (base_coeffs * np.array([ord(i) for i in t[i:i+len(p)]])).sum() % prime
            if t_hash == p_hash:
                if t[i:i+len(p)] == p:
                    matches += [i]

            if i >= len(t) - len(p):
                break
            else:
                t_hash = ((t_hash - (base_coeffs[0] ** ord(t[i]))) * 10 + ord(t[i+len(p)])) % prime
                i += 1

        print(matches)
        return matches

if __name__ == "__main__":
    t0 = 'ABABAABABACBCABABACABABABACAABABACBABABACABABABACABABACCABABAC'
    t1 = 'ABABAABABACBCABABACABABABACAABABACBABABACABABABACABABACCABABACABABBABABBCBABCBCBCABABAABABABCBABCBACBB'

    t = t1
    p = 'ABABAC'
    sigma = ''.join(set(t))
    prime = 53

    rabin_karp(t,p,sigma,prime)

    '''
    X?Y____
    t[:i] -> x
    t[1:i+1] -> ((x - (X * base**(len(p-1))) % prime) * 10 + Y % prime) % prime
    '''
