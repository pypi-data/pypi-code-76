#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import raisin

def solve_commente(f, *symbols, **flags):
    """
    Algebraically solves equations and systems of equations.

    Currently supported are:
        - polynomial,
        - transcendental
        - piecewise combinations of the above
        - systems of linear and polynomial equations
        - systems containing relational expressions.

    Input is formed as:
    
    * f
        - a single Expr or Poly that must be zero,
        - an Equality
        - a Relational expression
        - a Boolean
        - iterable of one or more of the above

    * symbols (object(s) to solve for) specified as
        - none given (other non-numeric objects will be used)
        - single symbol
        - denested list of symbols
          e.g. solve(f, x, y)
        - ordered iterable of symbols
          e.g. solve(f, [x, y])

    * flags
        'dict'=True (default is False)
            return list (perhaps empty) of solution mappings
        'set'=True (default is False)
            return list of symbols and set of tuple(s) of solution(s)
        'exclude=[] (default)'
            don't try to solve for any of the free symbols in exclude;
            if expressions are given, the free symbols in them will
            be extracted automatically.
        'check=True (default)'
            If False, don't do any testing of solutions. This can be
            useful if one wants to include solutions that make any
            denominator zero.
        'numerical=True (default)'
            do a fast numerical check if ``f`` has only one symbol.
        'minimal=True (default is False)'
            a very fast, minimal testing.
        'warn=True (default is False)'
            show a warning if checksol() could not conclude.
        'simplify=True (default)'
            simplify all but polynomials of order 3 or greater before
            returning them and (if check is not False) use the
            general simplify function on the solutions and the
            expression obtained when they are substituted into the
            function which should be zero
        'force=True (default is False)'
            make positive all symbols without assumptions regarding sign.
        'rational=True (default)'
            recast Floats as Rational; if this option is not used, the
            system containing floats may fail to solve because of issues
            with polys. If rational=None, Floats will be recast as
            rationals but the answer will be recast as Floats. If the
            flag is False then nothing will be done to the Floats.
        'manual=True (default is False)'
            do not use the polys/matrix method to solve a system of
            equations, solve them one at a time as you might "manually"
        'implicit=True (default is False)'
            allows solve to return a solution for a pattern in terms of
            other functions that contain that pattern; this is only
            needed if the pattern is inside of some invertible function
            like cos, exp, ....
        'particular=True (default is False)'
            instructs solve to try to find a particular solution to a linear
            system with as many zeros as possible; this is very expensive
        'quick=True (default is False)'
            when using particular=True, use a fast heuristic instead to find a
            solution with many zeros (instead of using the very slow method
            guaranteed to find the largest number of zeros possible)
        'cubics=True (default)'
            return explicit solutions when cubic expressions are encountered
        'quartics=True (default)'
            return explicit solutions when quartic expressions are encountered
        'quintics=True (default)'
            return explicit solutions (if possible) when quintic expressions
            are encountered
        """
    return solver.solve(f, *symbols, **flags)


def solve(f, *symbols, **flags):
    """
    Algebraically solves equations and systems of equations.

    Input is formed as:
    
    * f
        - a single Expr or Poly that must be zero,
        - an Equality
        - a Relational expression
        - a Boolean
        - iterable of one or more of the above

    * symbols (object(s) to solve for) specified as
        - none given (other non-numeric objects will be used)
        - single symbol
        - denested list of symbols
          e.g. solve(f, x, y)
        - ordered iterable of symbols
          e.g. solve(f, [x, y])
    * flags
        'dict'=True (default is False)
            return list (perhaps empty) of solution mappings
        'set'=True (default is False)
            return into maybe a list of dictionary, the solution like a raisin.sympy interval
        'exclude=[] (default)'
            don't try to solve for any of the free symbols in exclude;
            if expressions are given, the free symbols in them will
            be extracted automatically.
        'check=True (default)'
            If False, don't do any testing of solutions. This can be
            useful if one wants to include solutions that make any
            denominator zero.
        'numerical=True (default)'
            do a fast numerical check if ``f`` has only one symbol.
        'minimal=True (default is False)'
            a very fast, minimal testing.
        'warn=True (default is False)'
            show a warning if checksol() could not conclude.
        'simplify=True (default)'
            simplify all but polynomials of order 3 or greater before
            returning them and (if check is not False) use the
            general simplify function on the solutions and the
            expression obtained when they are substituted into the
            function which should be zero
        'force=True (default is False)'
            make positive all symbols without assumptions regarding sign.
        'rational=True (default)'
            recast Floats as Rational; if this option is not used, the
            system containing floats may fail to solve because of issues
            with polys. If rational=None, Floats will be recast as
            rationals but the answer will be recast as Floats. If the
            flag is False then nothing will be done to the Floats.
        'manual=True (default is False)'
            do not use the polys/matrix method to solve a system of
            equations, solve them one at a time as you might "manually"
        'implicit=True (default is False)'
            allows solve to return a solution for a pattern in terms of
            other functions that contain that pattern; this is only
            needed if the pattern is inside of some invertible function
            like cos, exp, ....
        'particular=True (default is False)'
            instructs solve to try to find a particular solution to a linear
            system with as many zeros as possible; this is very expensive
        'quick=True (default is False)'
            when using particular=True, use a fast heuristic instead to find a
            solution with many zeros (instead of using the very slow method
            guaranteed to find the largest number of zeros possible)
        'cubics=True (default)'
            return explicit solutions when cubic expressions are encountered
        'quartics=True (default)'
            return explicit solutions when quartic expressions are encountered
        'quintics=True (default)'
            return explicit solutions (if possible) when quintic expressions
            are encountered
    """
    if flags.get("set", False):
        return raisin.geometry.to_set(raisin.sympy.solve(f, *symbols, **flags))
    return raisin.sympy.solve(f, *symbols, **flags)



