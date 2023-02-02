def bruteforce_sm(t,p):
    idx = []
    for i in range(len(t)-len(p)+1):
        if t[i:i+len(p)] == p:
            idx.append(i)
    return idx

# Knuth-Morris-Pratt
# 'Is there a prefix p[:] that is also a suffix of p[1:]?' -> proper prefix
# Notice how recursion gives the next best partial prefix: f[i] is the longest, f[f[i]] is the next best, f[f[f[i]]] is the next, so on.
# https://www.topcoder.com/thrive/articles/Introduction%20to%20String%20Searching%20Algorithms

def failure_function(p):
        f = [0 for _ in range(len(p))]
        i,j = 1,0
        while i < len(p):
            if p[i] == p[j]: # match
                f[i] = j+1
                i += 1
                j += 1
            elif j > 0: # find the next longest prefix and try again.
                j = f[j-1] 
            else: # no prefix left, start over
                f[i] = 0
                i += 1
        return f

def kmp_sm(t,p):
    matches = []
    f = failure_function(p)
    i,j = 1,0
    while i < len(t):
        if t[i] == p[j]:
            if j == len(p) - 1: # match
                matches.append(i-j)
                i += 1
                j = 0
            else:
                i += 1
                j += 1
        else:
            if j > 0:
                j = f[j-1]
            else:
                i += 1
                j = 0
    return matches

# func1: given a string, find all its proper suffixes that are also prefixes of it
# recall that recursively you can find the next longest proper prefix 
def func1(t):
    f = failure_function(t)
    i = len(t) - 1
    arr = []

    while True:
        s = t[:f[i]]
        if len(s) > 0:
            arr.append(s)
            i = f[i-1]
        else:
            break

    print(t)
    print(arr)

# func2: given a string t find its shortest substring s such that the concatenation of one or more copies of it results in the original string
# s is such a string that t = ss..s
# find the shortest proper prefix s.t. its length divides length of t with no remainder
def func2(t):
    f = failure_function(t)
    i = len(t) - 1
    tmp = None
    
    s = t[:f[i]]
    while len(s) > 0:
        if len(t) % len(s) == 0:
            tmp = s
        
        i = f[i-1]
        s = t[:f[i]]
    
    print(t)
    print(tmp)

if __name__ == "__main__":
    func2('ABABAB')