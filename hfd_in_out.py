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