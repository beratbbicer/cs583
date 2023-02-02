def maximal_palindrome(s: str) -> str:
    if len(s) == 1:
        return s
    elif len(s) == 2:
        if s[0] == s[1]:
            return s
        else:
            return s[0]
    else:
        m = len(s)
        dp = [[False for i in range(m+1)] for j in range(m+1)]

        for start in range(m):
            dp[0][start] = False

        for start in range(m):
            dp[1][start] = True

        for start in range(m-1):
            if s[start] == s[start+1]:
                dp[2][start] = True
            else:
                dp[2][start] = False

        for extend in range(3, m+1):
            for start in range(m+1-extend):                
                if s[start] == s[start+extend-1] and dp[extend-2][start+1]:
                    dp[extend][start] = True
                else:
                    dp[extend][start] = False

        max_len, max_loc = 0, 0
        for extend in range(1,m+1):
            for start in range(m+1-extend):
                if dp[extend][start] and extend > max_len:
                    max_loc = start
                    max_len = extend
        return s[max_loc:max_loc+max_len]

s = 'cbbd'
print(maximal_palindrome(s))