#coding: utf8

__doc__ = """##dirac_parse.py
Функции для работы с out файлами dirac

Содержит следующие функции
- dirac_total_energies(dirac_out)
- dirac_orbital_energies(dirac_out, orbenmax=1e15)

Пользовательское исключение

- InvalidDiracOutput()

### dirac_orbital_energies(dirac_out,orbenmax=1e15)

Считывает из потока dirac_out, строки задания орбиталей
соответствующие орбитальным энергиям и возвращает словарь res,
в котором сопоставлены номера орбиталей и их энергии.

### dirac_total_energies(dirac_out)

Возвращает кортеж из списка полных энергий на каждой итерации для потока
dirac_out и приращений энергии на каждой итерации.

### subst_ind(dirac_out, inv_end_string):

Возвращает лист подстановок для каждой орбитали, все строки до
inv_end_string остаются неизменными, дальше упорядочивает по номеру атома.
"""


class InvalidDiracOutput(Exception):
    pass


def _wait_for_str(dirac_out, wait_str):
    """считывает из потока dirac_out строки пока не наткнется на строку, в
    которой содержится wait_str, если такой нет, то производит исключение
    InvalidDiracOutput"""
    for line in dirac_out:
        if wait_str in line:
            return
    raise InvalidDiracOutput("no {} in {}".format(wait_str, dirac_out))


def dirac_total_energies(dirac_out):
    """Возвращает кортеж из списка полных энергий на каждой итерации для потока
    dirac_out и списка приращений энергии на каждой итерации"""
    _wait_for_str(dirac_out, "START ITERATION NO.")
    ens = []
    for line in dirac_out:
        if "It." in line:
            ens += [float(line.split()[2])]
        elif "** Exit" in line:
            return ens, [0] + [ens[i] - ens[i-1] for i in xrange(1, len(ens))]

    raise InvalidDiracOutput()


def dirac_orbital_energies(dirac_out, orbenmax=1e15):
    """Считывает из потока dirac_out, строки задания орбиталей
    соответствующие орбитальным энергиям и возвращает словарь res,
    в котором сопоставлены номера орбиталей и их энергии."""
    try:
        _wait_for_str(dirac_out, "* Vector print *")
        _wait_for_str(dirac_out, "***")
    except InvalidDiracOutput:
        _wait_for_str(dirac_out, "population analysis *")
        _wait_for_str(dirac_out, "***")
    res = {}
    for line in dirac_out:
        if "eigenvalue" in line:
            aux = line.split(':')
            aux[1] = aux[1].replace('D', 'e')
            num, en = int(aux[0].split('.')[-1]), float(aux[1])
            print("eig parsing")
            print(num, en)
            if (en < orbenmax):
                res[num] = en
            else:
                return res
        elif "*******************************" in line:
            return res
    raise InvalidDiracOutput()


def subst_ind(dirac_out, inv_end_string):
    """возвращает лист подстановок для каждой орбитали, все строки до
    inv_end_string остаются неизменными, дальше упорядочивает по номеру атома.
    """
    _wait_for_str(dirac_out, "* Vector print *")
    _wait_for_str(dirac_out, "---")
    _wait_for_str(dirac_out, "---")
    skip_line = False
    invariant = True
    res = {}
    inv_res = []
    first = True
    for line in dirac_out:
        if skip_line:
            skip_line = False
            continue
        elif "eigenvalue" in line:
            aux = line.split(':')
            orb_num = int(aux[0].split('.')[-1])
            skip_line = True
            invariant = True
            first = False
            atoms = {}
            continue
        elif len(line.strip()) == 0:
            if first:
                continue
            res[orb_num] = [set(inv_res)] + [set(atoms[atom]) for atom in
                                      sorted(atoms.keys())]
            inv_res = []
            continue
        elif "*****************" in line:
            return res

        aux = line.split()
        bas_num = int(aux[0])
        atom = aux[2], int(aux[3])
        if invariant:
            inv_res += [bas_num]
        else:
            atoms[atom] = atoms.get(atom, []) + [bas_num]

        invariant = invariant and inv_end_string not in line

    raise InvalidDiracOutput()
