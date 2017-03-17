#!/usr/bin/python
import numpy as np
import os
energy=float(os.popen('grep "energy without" OUTCAR | tail -1 | awk \'{print $5}\'').read())
efermi=float(os.popen('grep "E-fermi" OUTCAR | awk \'{print $3}\'').read())
nbands=int(os.popen('grep NBANDS OUTCAR | awk \'{print $15}\'').read())
nedos=int(os.popen('grep NEDOS OUTCAR | awk \'{print $6}\'').read())
ispin=int(os.popen('grep ISPIN OUTCAR | awk \'{print $3}\'').read())
lsorbit=os.popen('grep LSORBIT OUTCAR | awk \'{print $3}\'').read().strip('\n').strip('\t')
