# coding: utf-8
__doc__ = u"""
# hfd_in_out
набор функций для работы с hfd.inp и hfd.res
##список функций
- hfd_inp
- orbitals
## hfd_inp (hfd_inp_std)
преобразует шаблон для файла _hfd.inp_, сканируя его и подставляя
вместо !val! соответствующее значение. Так например вызов hfd_inp(ins, q="1.")
заменит все вхождения строки !q! ({q}) в потоке ins на 1.
(hfd_inp_std использует стандартный _.format()_ из python и обладает
большими возможностями)
*вызов*: hfd_inp(in_stream, \*\*kwargs)
- in_stream -- поток с шаблоном входного файла hfd.inp
- **kwargs -- список ключевых аргументов для подстановки в шаблон.
## orbitals
читает входной поток в формате hfd.res и возвращает кортеж из
словаря с информацией о
орбиталях и значением полной энергии атома.
*вызов*: orbs, en = orbitals(in_stream)
"""


def hfd_inp_std(in_stream, **kwargs):
    import re
    out = ""
    def aux(match):
        res = eval(match.group('expr'), {'__builtins__': None}, kwargs)
        return ("{:"+match.group('fmt')+'}').format(res)

    expr_fmt = re.compile(r'{(?P<expr>[^}:]*):(?P<fmt>[^}]*)}')
    with open('hfd.inp', 'w') as hfdinp:
        for line in in_stream:
            a = re.search(expr_fmt, line)
            if a is not None:
                out += expr_fmt.sub(aux, line)
            else:
                out += line
        hfdinp.write(out)

def hfd_inp(in_stream, **kwargs):
    with open('hfd.inp', 'w') as hfdinp:
        for line in in_stream:
            out = line
            for k in kwargs.keys():
                if ('!' + k + '!') in out:
                    out = out.replace('!' + k + '!', str(kwargs[k]))
            hfdinp.write(out)

def make_orbitals_parser(fmt):
    def orbitals(in_stream):
        st = 0
        etot_lookup = False
        res = []
        for line in in_stream:
            if '==========' in line:
                st = 1
            elif st == 1 and 'Etot =' in line:
                e_tot = float(line.split()[6])
                break
            elif st == 1 and 'ITER' not in line:  #  HFJ branch
                etot_lookup = True
                break
            else:
                st = 0

        if st == 0:
            raise TypeError
        st = 0
        for line in in_stream:  # to the end of header
            if st == 2 and '----' in line:
                break
            elif 'nl j' or 'nl  j' in line:
                st = 2

        if st < 2:
            raise TypeError
        # end of header
        for line in in_stream:
            if '==========' in line:
                break
            if 'kp' in line:
                st =3
                continue
            if st == 3:
                st = 2
                continue
            aux = line.split()
            aux[2] = aux[2][:-1]
            aux[3] = float(aux[3].replace(')',''))
            aux[4:] = [float(x) for x in aux[4:]]
            res += [dict(zip(fmt, aux))]

        if etot_lookup:
            e_tot = 0e0
            for line in in_stream:
                if 'Etot' in line:
                    e_tot = float(line.split('=')[1])
                    break
        return (res, e_tot)
    return orbitals

orbitals = make_orbitals_parser(fmt=['no', 'nl', 'j', 'occ', 'kp', 'en', 'd',
                                     'Rmax', 'Rav', 'Rm'])
