import scipy as sc


def read_prop(fil):
    START, RPROP, TITLE, DENS, SIZE, MAT = 0, 1, 2, 3, 4, 5
    state = START
    while(state == START):
        line = fil.readline()
        if "RpropertyJML" in line:
            state = RPROP
            break
        if line == '':
            return None
    title_line = fil.readline()
    if "title=" not in title_line:
        raise ValueError(
            "This line should contain \"title=\" -- {}".format(title_line))
    state = TITLE
    title = title_line[1+title_line.find('='):]
    dens_line = fil.readline()
    if "dens=" not in dens_line:
        raise ValueError(
            "This line should contain \"dens=\" -- {}".format(title_line))
    dens = dens_line[1+title_line.find('='):]
    state = DENS
    size_line = fil.readline()
    try:
        size = int(size_line)
    except Exception:
        raise ValueError(
            "This line should contain integer number -- {}".format(size_line))
    state = SIZE
    mat = sc.zeros((size, size))
    for i in xrange(size):
        row_line = fil.readline()
        try:
            row = sc.array(map(float, row_line.split()))
            mat[i, :] = row
        except Exception:
            raise ValueError(
                "This line should contain {} tab/space separated\
                float numbers -- {}".format(size, row_line))
    state = MAT
    return {title: (size, dens, mat)}

def __test__():
    props = {}
    prop = {}
    with open('prop.txt', 'r') as props_file:
        while (True):
            prop = read_prop(props_file)
            try:
                props.update(prop)
            except TypeError:
                break

    for prop_name in props:
        print(prop_name)
        print(" ".join(['{:3.5f}'] * props[prop_name][0]).format(
            *props[prop_name][2].diagonal()))
        print("---------------")

if __name__ == "__main__":
    __test__()
