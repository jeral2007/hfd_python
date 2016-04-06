global __prop_db__
import sqlite3 as lite


def initdb(filename):
    global __prop_db__
    __prop_db__ = filename


def get_comps():
    global __prop_db__
    con = lite.connect(__prop_db__)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM comps")
        comps = cur.fetchall()
    return comps


def add_comp(name, time):
    global __prop_db__
    con = lite.connect(__prop_db__)
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO comps(name,date) VALUES (?, ?);",
                    (name.upper(), time))
        comp_id = cur.lastrowid
    return comp_id


def add_prop(name):
    global __prop_db__
    con = lite.connect(__prop_db__)
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO props(name) VALUES (?);",
                    (name.upper(),))
        prop_id = cur.lastrowid
    return prop_id


def add_propval(prop_id, comp_id, val):
    global __prop_db__
    con = lite.connect(__prop_db__)
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO propvals(prop,comp,val) VALUES (?,?,?);",
                    (prop_id, comp_id, val))


def get_prop_id(name):
    global __prop_db__
    con = lite.connect(__prop_db__)
    with con:
        cur = con.cursor()
        cur.execute("SELECT propid FROM props WHERE name=?", (name.upper(),))
        res = cur.fetchone()
    if res is not None:
        return res[0]


def get_props_for_given_comp_pattern(comp_pattern):
    global __prop_db__
    con = lite.connect(__prop_db__)
    with con:
        cur = con.cursor()
        cur.execute(
                    """SELECT comps.name,props.name,propvals.val
                       FROM comps,props,propvals
                       WHERE comps.name LIKE ? AND
                       propvals.prop = props.propid AND
                       propvals.comp = comps.compid""", (comp_pattern,))
        res = cur.fetchall()
    if res is not None:
        return res


def add_orb(orbnum, energy, orbtype, comp_id):
    global __prop_db__
    con = lite.connect(__prop_db__)
    with con:
        cur = con.cursor()
        cur.execute("""
                    INSERT INTO orbitals(comp,orbnum,energy,orbtype)
                    VALUES (?, ?, ?, ?);""",
                    (comp_id, orbnum, energy, orbtype))
        orb_id = cur.lastrowid
    return orb_id


def get_orbs_for_given_comp_pattern(comp_pattern):
    global __prop_db__
    con = lite.connect(__prop_db__)
    with con:
        cur = con.cursor()
        cur.execute(
                    """SELECT name,orbnum,energy,orbtype
                       FROM orbitals INNER JOIN comps
                            ON orbitals.comp = comps.compid
                       WHERE comps.name LIKE ?""", (comp_pattern,))
        res = cur.fetchall()
    return res
