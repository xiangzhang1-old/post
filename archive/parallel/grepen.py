#!/usr/bin/python
import numpy as np
import os
ENERGY=float(os.popen('grep "energy without" OUTCAR | tail -1 | awk \'{print $5}\'').read())
EFERMI=float(os.popen('grep "E-fermi" OUTCAR | awk \'{print $3}\'').read())
NBANDS=int(os.popen('grep NBANDS OUTCAR | awk \'{print $15}\'').read())
NEDOS=int(os.popen('grep NEDOS OUTCAR | awk \'{print $6}\'').read())
ISPIN=int(os.popen('grep ISPIN OUTCAR | awk \'{print $3}\'').read())
LSORBIT=os.popen('grep LSORBIT OUTCAR | awk \'{print $3}\'').read().strip('\n').strip('\t')
