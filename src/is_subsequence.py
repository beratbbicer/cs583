def isSubsequence(s: str, t: str) -> bool:
    if len(s) == 0:
        return True
    elif len(t) == 0:
        return False
    else:
        i = 0
        j = 0

        while True:
            if t[i] == s[j]:
                i += 1
                j += 1
            else:
                i += 1
                
            if i >= len(t) or j >= len(s):
                break
        
        if j >= len(s):
            return True
        else:
            return False

s = "a"
t = "a"
print(isSubsequence(s,t))