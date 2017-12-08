from __future__ import print_function
import sys
import subprocess as sp

def nlj(hinp_line):
    """  1     1S (1/2)   2.0000    0    1
        0      1   2       3       4    5"""
    aux = hinp_line.lower().split()
    return aux[1]+aux[2][1:4]


def change_q(shell_raw, dq):
    shell = shell_raw.lower()
    fmt = "   {}     {} {}   {:.4f}    {}    {}\n"
    hfd_inp = open('hfd.inp', 'r')
    hinp_ls = hfd_inp.readlines()
    hinp_ls_gen = (line for line in hinp_ls)
    hfd_inp = open('hfd.inp', 'w')
#  process header of hfd.inp
    for line in hinp_ls_gen:
        hfd_inp.write(line)
        if "NL   J       QQ     NC   KP" in line:
            break
    hfd_inp.write(hinp_ls_gen.next())
#  process shells section
    for line in hinp_ls_gen:
        if '=====' in line:
            hfd_inp.write(line)
            break
        if nlj(line) != shell:
            hfd_inp.write(line)
            continue
        aux = line.split()
        aux[3] = float(aux[3]) + dq
        hfd_inp.write(fmt.format(*aux))
#  process rest of the hfd.inp
    for line in hinp_ls_gen:
        hfd_inp.write(line)


def relat_en():
    sp.call("./relat.exe >/dev/null", shell=True)
    for line in open('relat.res'):
        if 'Ehfd' in line:
            en = float(line.split('=')[1].split()[0])
            break
    return en


def tran_en(in_sh, fin_sh):
    change_q(in_sh, -1)
    en = relat_en()
    change_q(in_sh, 1)
    change_q(fin_sh, -1)
    en -= relat_en()
    change_q(fin_sh, 1)
    return en


def switch_context(context):
    sp.call('tar -xzf {}'.format(context), shell=True)

contexts = sys.argv[1:3]
tran_shell = sys.argv[3:]
in_shell = []
fin_shell = []
while (len(tran_shell) > 0):
    in_shell += [tran_shell.pop(0)]
    fin_shell += [tran_shell.pop(0)]

tran_ens = {}
switch_context(contexts[0])
for in_sh, fin_sh in zip(in_shell, fin_shell):
    tran_ens[in_sh+' -- '+fin_sh] = tran_en(in_sh, fin_sh)*27.211
print(tran_ens)

switch_context(contexts[1])
for in_sh, fin_sh in zip(in_shell, fin_shell):
    tran_ens[in_sh+' -- '+fin_sh] -= tran_en(in_sh, fin_sh)*27.211
    tran_ens[in_sh+' -- '+fin_sh] *= 1000

print(tran_ens)
