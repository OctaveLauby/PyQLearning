def are_same(l):
    base = l[0]
    for elem in l:
        if elem != base:
            return False
    return True
