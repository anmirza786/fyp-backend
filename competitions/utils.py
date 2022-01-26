def char_Count(alphabets):
    alphabets = alphabets.upper()
    S_range, E_range = alphabets.split("-")
    range_list = list(map(chr, range(ord(S_range), ord(E_range) + 1)))
    return range_list
