from itertools import izip

def drop_blank(stream):
    for line in stream:
        if '----------------' in line:
            continue
        aux = line.split()
        if len(aux) == 0:
            continue
        yield line


def readnmos(stream):
    line = stream.next()
    if '! Total energy' in line:
        raise StopIteration
    elif 'MO' in line:
        aux = [a for a in line.split() if a == '>>']
        return len(aux)
    else:
        raise ValueError("Incorrect line: " + line)


def readrow(stream, numc, header):
    line = stream.next()
    aux = line.split()
    if aux[0] != header:
        raise ValueError("Expected '{}' in the beginning of '{}'".format(header,
                                                                         line))
    if len(aux) != numc:
        raise ValueError("Expected {} columns in '{}'".format(numc, line))

    return map(float, aux[1:])


def parse_eigen(stream):
    fstream = drop_blank(stream)
    st = 0
    eigh = []
    eigev = []
    occ_n = []
    for line in fstream:
        if 'Energy eigenvalues of twocomp' in line:
            st = 1
            break
    if st != 1:
        raise ValueError("No eigenvalues in file")
    while(True):
        nmos = readnmos(fstream)+1
        eigh += readrow(fstream, nmos, 'Eig[Eh]')
        eigev += readrow(fstream, nmos, 'Eig[eV]')
        occ_n += readrow(fstream, nmos, 'OccNum')

    if any(abs(au*27.211 - ev) for au, ev in izip(eigh, eigev)):
        raise ValueError("Something wrong")
    return eigh, occ_n


