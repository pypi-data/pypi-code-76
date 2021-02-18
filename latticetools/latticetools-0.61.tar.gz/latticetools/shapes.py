import numpy as np
from functools import reduce

def hyperellipse(centres, radii, theta, axis):
    def func2(R):
        Rd = tuple(Ri - ci for Ri, ci in zip(R, centres, ) ) 
        newcoords = rotatedcoords([Ri for i,Ri in enumerate(Rd) if i is not axis], theta)
        return reduce(lambda squaresum, cr:
                      squaresum + (cr[0]/cr[1])**2.,
                      zip([Ri if i is axis else newcoords[
                          i - (i > axis)] for i,Ri in enumerate(Rd)],
                          radii),
                      np.zeros_like(reduce(np.add,Rd,0.)))**.5 < 1.
    return func2

# +
rectfunc = lambda x: (-0.5 <= x) * (x < 0.5) * 1

box = lambda widths, centre: lambda R: reduce(
    np.multiply,
    (
        rectfunc((Ri - ci) / wi)
        for Ri, ci, wi 
        in zip(R, centre, widths)
    ),
    1,
)

# +
rotatedcoords = lambda R, theta: tuple(
    [
        [getattr(i,part) for part in ('real','imag',)] 
        for i 
        in [(R[0]+1j*R[1])*np.exp(1j*-theta),]
    ][0])

shepp_params = [
    [   1,   .69,   .92,    0,      0,   0],
    [-.80, .6624, .8740,    0, -.0184,   0],
    [-.20, .1100, .3100,  .22,      0, -18],
    [-.20, .1600, .4100, -.22,      0,  18],
    [ .10, .2100, .2500,    0,    .35,   0],
    [ .10, .0460, .0460,    0,     .1,   0],
    [ .10, .0460, .0460,    0,    -.1,   0],
    [ .10, .0460, .0230, -.08,  -.605,   0],
    [ .10, .0230, .0230,    0,  -.606,   0],
    [ .10, .0230, .0460, .06, -.605, 0]]

shepp_logan = lambda radius, centre: lambda R: sum(
    hyperellipse(
        (
            x0 * radius + centre[0],
            centre[1],
            z0 * radius + centre[2],
        ), 
        (
            a * radius,
            a * radius,
            b * radius,
        ), 
        np.pi * phi / 180, 
        1, 
    )(R) * A
    for A, a, b, x0, z0, phi in shepp_params
)
