#coding: utf8
import atom_strings as ats
__doc__ = """##makebas.py
Модуль для загрузки радиальных компонент из hfd.dat
Класс Basis содержит следующие методы
- __init__(self, hfd_dat, orbs)
- add_orbital(self, hfd, orb)
- save_bas(self, bas_file)
- load_bas(bas_file)

данные хранятся в следующих членах класса:
- Basis.grid -- кортеж задающий сетку в формате из
    electron_integrals.py[elintpy]
- Basis.ljblock -- кортеж (list_orb_name, list_orb_data) из
    списка названий загруженных орбиталей, соответствующего orbs;
    list_orb_data -- список со значениями орбиталей в узлах сетки, их
    орбитальным и полными моментами, заданными в виде кортежа из
    electron_integrals.py [elint.py]

### Basis(hfd)
производит инициализацию, считывает значения сетки в Basis.grid  и
инициализирует пустой словарь ljblock (экземпляр класса Hfd[hfd_dat]).

### add_orbital(self, hfd, orb)
добавляет одну орбиталь, заданную в строковом формате('1s1/2', '2p1/2' и т.д.)
orb -- строка орбитали

### save_bas(bas_file, bas), load_bas(bas_file)
сериализация орбиталей с использованием Pickle.

*save_bas* производит запись словаря орбиталей, являющегося результатом
работы *load*, в файл bas_file.

*load_bas* считывает словарь орбиталей из файла bas_file

Обе функции используют модуль cPickle из стандартной библиотеки python
"""


class Basis(object):
    def add_orbital(self, hfd, orb):
        n, l, j = ats.str2nlj(orb)
        if (l, j) not in self.ljblock.keys():
            self.ljblock[(l, j)] = [[], []]
        p, q, en = hfd[orb]
        if orb in self.ljblock[(l, j)][0]:
            raise ValueError("orbital {} already in basis".format(orb))
        self.ljblock[(l, j)][0] += [orb]
        self.ljblock[(l, j)][1] += [(p.copy(), q.copy(), l, j)]

    def __init__(self, hfd=None):
        if hfd is not None:
            self.grid = (hfd.grid, hfd.weights, hfd.h)
        self.ljblock = {}

    @classmethod
    def load_bas(cls, bas_file):
        import cPickle
        with open(bas_file, 'r') as basin:
            grid, ljblock = cPickle.load(basin)
        res = Basis()
        res.grid = grid
        res.ljblock = ljblock
        return res

    def save_bas(self, bas_file):
        import cPickle
        with open(bas_file, 'w') as basout:
            cPickle.dump((self.grid, self.ljblock), basout)

    def __str__(self):
        res = "Basis(rmax grid = {}, number of lj blocks {}, ".format(
            self.grid[-1], len(self.ljblock.keys()))
        for k, v in self.ljblock.iteritems():
            res += ("there are {} orbitals in {}{}/2 block: ".format(len(v[0]),
                                                                     ats.lsymb[k[0]],
                                                                     int(2*k[1])))
            res += " ".join(v[0])+", "
        return res
