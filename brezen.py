#!/usr/bin/env python2.7
#coding: utf8
__doc__ = """

содержит функцию для генерации максимально равномерных распределений k  единиц,
а диапазоне от 0 до N"""


def max_even_distrib(N, k):
    """ функция для генерации максимально равномерных распределений k единиц,
в  диапазоне от 0 до N
См, код, массив seq используется в двух значениях - с одной стороны seq[k]
указывает на то, брать маленький или большой интервал для k-той единицы,
с другой это бинарный номер распределения,
увеличивая его на единицу на каждом шаге, мы автомагически генерируем
новое распределение
"""
    from math import floor
    alpha = (N+1)*1e0/k
    precomp = [int(floor(alpha*i)) - 1 for i in xrange(1, k)]
    seq = [0] * (k-1)
    while(True):  # repeat at least once
        yield [0] + [precomp[i] + s for i, s in enumerate(seq)] + [N+1]
        # add 1
        ind = 0
        while (True):
            if seq[ind] == 0:
                seq[ind] = 1
                seq[0:ind] = [0]*ind
                break  # to outer loop
            else:
                ind += 1 # carry 1
                if ind == k-1:
                    return  # last sequence reached


def display_seq(seq):
    symb = {True: "X", False: "."}
    print("".join([symb[i in seq] for i in range(seq[-1]-1)])+"|X")


for seq in max_even_distrib(8, 3):
    display_seq(seq)
print "-"*12
for seq in max_even_distrib(8, 5):
    display_seq(seq)
print "-"*12
for seq in max_even_distrib(16, 3):
    display_seq(seq)
print("!!!!!!!!!!!!!!!!!!!!!! ")
for seq in max_even_distrib(16, 6):
    display_seq(seq)
print("!!!!!!!!!!!!!!!!!!!!!! ")
for seq in max_even_distrib(16, 7):
    display_seq(seq)
