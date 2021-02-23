#!/usr/bin/env python
# coding: utf-8

import csv


fname = input('Enter File: ')
if len(fname) < 1 : fname = 'Read_conversione.csv'
lines = open(fname)

lis = list()
for row in lines:
    lin = row.rstrip()      # cancella gli spazi a destra
    wds = lin.split(';')
    li = lis.append(wds)

di = dict(lis)

key = di.keys()

um = list(key)


def menu(um):
    i = 0
    while i < len(um):
        ums = um[i]
        print(i, ums)
        i = i + 1
    scegli = int(input(''))
    return (scegli)


scelta_da = menu(um)
scelta_a = menu(um)


def conversione(val, da, a):
    conda = float(di.get(da, 'Misura non trovata!'))
    cona = float(di.get(a, 'Misura non trovata!'))
    num = val
    ug = (num*conda)/cona
    return num, da, ug, a


val = float(input(''))
da = um[scelta_da]
a = um[scelta_a]

sol = conversione(val, da, a)

print(str(sol))

lines.close()
