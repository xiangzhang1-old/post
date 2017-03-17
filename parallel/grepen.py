#!/usr/bin/python
import os

class grepen(object):

 def __init__(self):
  self.energy=float(os.popen('grep "energy without" OUTCAR | tail -1 | awk \'{print $5}\'').read())
  self.efermi=float(os.popen('grep "E-fermi" OUTCAR | awk \'{print $3}\'').read())
  self.nbands=int(os.popen('grep NBANDS OUTCAR | awk \'{print $15}\'').read())
  self.nedos=int(os.popen('grep NEDOS OUTCAR | awk \'{print $6}\'').read())
  self.ispin=int(os.popen('grep ISPIN OUTCAR | awk \'{print $3}\'').read())
  self.lsorbit=os.popen('grep LSORBIT OUTCAR | awk \'{print $3}\'').read().strip('\n').strip('\t')
