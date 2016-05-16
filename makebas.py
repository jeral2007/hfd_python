#coding: utf8
import atom_strings as ats
import scipy as sc
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

Модуль содержит следующие функции
-ljblocks(basis)


### Basis(hfd)
производит инициализацию, считывает значения сетки в Basis.grid  и
инициализирует пустой словарь ljblock (экземпляр класса Hfd[hfd_dat]).

### Basis.add_orbital(self, hfd, orb)
добавляет одну орбиталь, заданную в строковом формате('1s1/2', '2p1/2' и т.д.)
orb -- строка орбитали

### Basis.remove_orbital(self, orb_name)
удаляет орбиталь заданную строкой orb_name из базиса

### Basis.save_bas(self, bas_file), Basis.load_bas(bas_file)
сериализация орбиталей с использованием Pickle.

*save_bas* производит запись словаря орбиталей, являющегося результатом
работы *load*, в файл bas_file.

*load_bas* считывает словарь орбиталей из файла bas_file

Обе функции используют модуль cPickle из стандартной библиотеки python

### ljblocks(basis)

Генератор, предназначенный для осуществления итерации по словарю basis.ljblock
На каждом шаге итерации возвращает кортеж (lj, orb_names, orb_val, smat).

- lj = (l, j) -- кортеж из значений орбитального и полного моментов блока
- orb_names - список имен орбиталей ('1s1/2', '2p1/2' и т.д)
- orb_val -- аналогичен *list_orb_data*[list_orb_data]
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
        self._eigen  = None
    def remove_orbital(self, orb_name):
        n, l, j
    def __init__(self, hfd=None):
        if hfd is not None:
            self.grid = (hfd.grid, hfd.weights, hfd.h)
        self.ljblock = {}
        self._eigen = None
        self._rc= 1e15

    @classmethod
    def load_bas(cls, bas_file):
        import cPickle
        with open(bas_file, 'r') as basin:
            grid, ljblock = cPickle.load(basin)
        res = cls()
        res.grid = grid
        res.ljblock = ljblock
        res._eigen = None
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

    def eigen(self, rc=1e15):
        import scipy.linalg as lg
        from hfd_dat import gr_trapz
        if self._eigen is None or abs(rc - self._rc)<1e-10:
            self._eigen = {}
            self._rc = rc
            #dirty hack for attributes
            aux = lambda: None
            aux. grid, aux.weights, aux.h = self.grid
            for lj in self.ljblock:
                data = self.ljblock[lj][1]
                smat = sc.array([[gr_trapz(p1*p2 + q1*q2, aux, rc)
                                 for p1, q1, l1, j1 in data]
                                 for p2, q2, l2, j2 in data])
                ex, ev = lg.eig(smat)
                perm = sc.argsort(sc.real(ex))
                self._ex, self._eigen[lj] = ex[perm], ev[perm]
        return self._ex, self._eigen


def ljblocks(basis, nc=-1):
    import scipy as sc
    for lj, data in basis.ljblock.items():
        N = len(data[0])
        smat = sc.zeros((N, N))
        for i in xrange(N):
            pi, qi, li, ji = data[1][i]
            for j in xrange(i+1):
                pj, qj, llj, jj = data[1][j]
                smat[i, j] = sc.trapz((pi[:nc]*pj[:nc] +
                                       qi[:nc]*qj[:nc]) *
                                      basis.grid[1][:nc])*basis.grid[2]
                smat[j, i] = smat[i, j]
        yield lj, data[0], data[1], smat
