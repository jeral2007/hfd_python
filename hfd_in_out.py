# coding: utf-8
__doc__ = u"""
# hfd_in_out
набор функций для работы с hfd.inp и hfd.res
##список функций
- hfd_inp
- orbitals
## hfd_inp
преобразует шаблон для файла _hfd.inp_, сканируя его и подставляя
вместо !val! соответствующее значение. Так например вызов hfd_inp(ins, q="1.")
заменит все вхождения строки !q! в потоке ins на 1.

*вызов*: hfd_inp(in_stream, \*\*kwargs)
- in_stream -- поток с шаблоном входного файла hfd.inp
- **kwargs -- список ключевых аргументов для подстановки в шаблон.
## orbitals
читает входной поток в формате hfd.res и возвращает кортеж из
словаря с информацией о
орбиталях и значением полной энергии атома.
*вызов*: orbs, en = orbitals(in_stream)
"""


def hfd_inp(in_stream, **kwargs):
    with open('hfd.inp', 'w') as hfdinp:
        for line in in_stream:
            out = line
            for k in kwargs.keys():
                if ('!' + k + '!') in out:
                    out = out.replace('!' + k + '!', str(kwargs[k]))
            hfdinp.write(out)


def orbitals(in_stream):
    fmt = ['no', 'nl', 'j', 'occ', 'kp', 'en',
           'd', 'Rmax', 'Rav', 'Rm']
    st = 0
    res = []
    for line in in_stream:
        if '==========' in line:
            st = 1
        elif st == 1 and 'Etot =' in line:
            e_tot = float(line.split()[6])
            break
        else:
            st = 0
    if st == 0:
        raise TypeError
    st = 0
    for line in in_stream:  # count 3 lines
        if st == 2:
            break
        st += 1
    if st < 2:
        raise TypeError
    # end of header
    for line in in_stream:
        if '===========' in line:
            break
        aux = line.split()
        aux[2] = aux[2][:-1]
        aux[3] = float(aux[3][:-1])
        aux[4:] = [float(x) for x in aux[4:]]
        res += [dict(zip(fmt, aux))]
    return (res, e_tot)
