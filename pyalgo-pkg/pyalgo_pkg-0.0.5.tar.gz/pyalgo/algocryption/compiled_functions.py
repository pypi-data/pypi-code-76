from numba import njit


# // faster RSA function to find the private key faster \\
@njit
def find_private_key(e, Phi):
    k = 1
    d = 5.5

    #while not (d.is_integer()):
    while not (int(d) == d):
        d = ((k*Phi) + 1) / e

        #if d >= Phi:
        #    raise ValueError("'d' cannot exceed phi({self.Phi})")

        if k % 1000000 == 0:
            print(k, d)

        k += 1

    print("final d =", int(d))
    return int(d)