
def flattener(l):
    if hasattr(l, "__iter__"):
        r = []
        for ele in l:
            r.extend(flattener(ele))
        return r
    return [l]

if __name__ == "__main__":
    l = [[1, 2, 3], [[4, 5], 6]]
    print(flattener(l))
