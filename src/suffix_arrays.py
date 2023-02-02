def suffix_array_search(t, keywords, special_character):
    # create a suffix array for the text
    suffix_array = [t[i:] + special_character for i in range(len(t)+1)]
    suffix_array.sort()
    matches = {keyword:[] for keyword in keywords}

    # match the pattern with corresponding suffix array using binary search
    for kidx in range(len(keywords)):
        keyword = keywords[kidx]
        low, high = 0, len(t) - 1
        midpoint = int((low + high) * 0.5)
        j = 0
        flag = False

        while j < len(keyword):
            while low < high and len(suffix_array[midpoint]) > j: # keep searching
                if suffix_array[midpoint][j] > keyword[j]: # mid is greater than char
                    high = midpoint
                elif ((low == midpoint or high == midpoint) and suffix_array[midpoint][j] != keyword[j]): # mid is not char, but midptr is stuck here
                    flag = True
                    break
                elif suffix_array[midpoint][j] < keyword[j]: # mid is smaller than char
                    low = midpoint
                else:
                    break

                midpoint = int((low + high) * 0.5)

            if flag == False and low < high: # make low point to left-most, and high point to right-most occurrence of char
                while low < high and len(suffix_array[low]) > j and suffix_array[low][j] != keyword[j]:
                    low += 1

                while low < high and len(suffix_array[high]) > j and  suffix_array[high][j] != keyword[j]:
                    high -= 1

                j += 1
            else:
                break

        for i in range(low, high+1):
            if suffix_array[i][:len(keyword)] == keyword:
                matches[keyword] += [len(t) + 1 - len(suffix_array[i])]

    print(matches)
    return matches

if __name__ == "__main__":
    keywords0 = ['abab']
    t0 = 'ababbbbab'

    keywords1 = ['apple','apropos','banana','bandana','orange']
    t1 = 'abaproposbananacappleaappleapplebcorangedaproposbdhbabanananabandananaosnbandanamsmorangelkbanbanana'
    # Expected output: {'apple': [16, 22, 27], 'apropos': [2, 41], 'banana': [9, 53, 94], 'bandana': [61, 73], 'orange': [34, 83]}

    keywords2 = ['potato','tattoo','theater','other','recep', 'sex', 'excommunicate']
    t2 = 'sexcommunicatexcommunicatepotatotherecepotato'
    # Expected output: {'potato': [26, 39], 'tattoo': [], 'theater': [], 'other': [31], 'recep': [35], 'sex': [0], 'excommunicate': [1, 13]}

    t = t1
    keywords = keywords1
    special_characters = '$'
    suffix_array_search(t, keywords, special_characters)
    
