def factor(x):
    j = []
    while True:
        try:
            if x<=0:
                print("\033[1;91mError!!!")
                exit()
            else:
                break
        except:
            print("\033[1;91mError!!!")
            exit()
    for i in range(x+1):
        if i >= 1:
            if x % i == 0:
                j.append(i)
    return j
def big(a, b):
    while True:
        try:
            if a == 0 or b == 0:
                print("\033[1;91mError!!!")
                exit()
            else:
                break
        except:
            print("\033[1;91mError!!!")
            exit()
    c = a % b
    while c != 0:
        a = b
        b = c
        c = a % b
    return b
def small(a, b):
    while True:
        try:
            if a == 0 or b == 0:
                print("\033[1;91mError!!!")
                exit()
            else:
                break
        except:
            print("\033[1;91mError!!!")
            exit()
    e = a
    f = b
    c = a % b
    while c != 0:
        a = b
        b = c
        c = a % b
    d = e*f/b
    return d