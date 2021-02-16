#!/usr/bin/pypy3
from time import time
from math import log, ceil
from . import number as num_baseX

def baseXto10(number, base = 10):
    '''
    subprocessor for baseXtoY
    '''
    number = number.upper()
    result = 0
    l = int(base**(len(number) - 1))
    for n in number:
        if '0' <= n <= '9':
            result += l*(ord(n) - ord('0'))
        else:
            result += l*(ord(n) - 55)
            # ord('A') - 10 = 55
        l = round(l/base)
    return result

def base10toX(number: int, base=10):
    '''
    subprocessor for baseXtoY
    '''
    start = ''.join(['0' for _ in range(ceil(log(number, base)))])
    start = '0'
    result = num_baseX(start, base)
    def _wrapper(number: int, base = 10):
        nonlocal result
        log_num = int(log(number, base))
        for i in range(base**log_num):
            result.next()
        number = number - base**log_num
        if number > 0:
            _wrapper(number, base)
    _wrapper(number, base)
    return result

def baseXtoY(num, **kwargs):
    """
    Usage:
    baseXtoY(number, X, Y)
    X = base of num
    Y = base to convert to


    This product includes software developed by L. Pham-Trong, and this guy rocks.
    """

    integer_num = baseXto10(num, kwargs['X'])
    return base10toX(integer_num, kwargs['Y'])

def license():
    print("""Copyright (c) 2021, Luca PHAM-TRONG
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. All advertising materials mentioning features or use of this software must
   display the following acknowledgement:
     This product includes software developed by L. Pham-Trong, and this guy rocks.

4. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY COPYRIGHT HOLDER "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.""")
