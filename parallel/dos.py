#!/usr/bin/python
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import multiprocessing

# dos related objects
class dos(object):

 def __init__(self,grepen):
  # parameter: min_dos. is dos considered 0 if it's 0.002? 
  min_dos=1E-3
  # initialize dos file. all dos -> np.float64::tdos
  doscar_file=open("DOSCAR","r")
  tmplines=doscar_file.readlines()
  doscar_lines=[tmplines[i].split() for i in range(6,6+grepen.nedos)]
  self.dos=np.float64(doscar_lines)
  index_fermi=abs(self.dos[:,0]-grepen.efermi).argmin()+1
  #ispin=1 or 2?
  if grepen.lsorbit!='F':
   print "dos.py: we don't support lsorbit=true yet. exiting..."
   exit(1)
  if grepen.ispin==1: 
   ##ispin=1
   if abs(self.dos[index_fermi][1])>min_dos:
    print 'dos.py: conductor.'
   else: 
    self.vb=self.dos[index_fermi:0:-1]
    self.cb=self.dos[index_fermi:len(self.dos)]
    self.vb1=[self.vb[x][0] for x in range(0,len(self.vb)) if abs(self.vb[x][1])>min_dos]
    self.cb1=[self.cb[x][0] for x in range(0,len(self.cb)) if abs(self.cb[x][1])>min_dos]
    if len(self.vb1)==0 or len(self.cb1)==0:
     print 'dos.py: weird. len(self.vb1/self.cb1) is 0'
     exit(1)
    self.vbm1=self.vb1[0]
    self.cbm1=self.cb1[0]
    print 'dos.py: insulator. bandgap: ',self.cbm1-self.vbm1,' eV'
  elif grepen.ispin==2:
   ##ispin=2
   if abs(self.dos[index_fermi][1])>min_dos and abs(self.dos[index_fermi][2])>min_dos:
    print 'dos.py: conductor. quite probably. but check dos anyway.'
   elif abs(self.dos[index_fermi][1])<min_dos and abs(self.dos[index_fermi][2])<min_dos: 
    self.vb=self.dos[index_fermi:0:-1]
    self.cb=self.dos[index_fermi:len(self.dos)]
    self.vb1=[self.vb[x][0] for x in range(0,len(self.vb)) if abs(self.vb[x][1])>min_dos]
    self.vb2=[self.vb[x][0] for x in range(0,len(self.vb)) if abs(self.vb[x][2])>min_dos]
    self.cb1=[self.cb[x][0] for x in range(0,len(self.cb)) if abs(self.cb[x][1])>min_dos]
    self.cb2=[self.cb[x][0] for x in range(0,len(self.cb)) if abs(self.cb[x][2])>min_dos]
    if len(self.vb1)==0 or len(self.vb2)==0 or len(self.cb1)==0 or len(self.cb2)==0:
     print 'dos.py: weird. len(self.vb1) is ',len(self.vb1),'. len(self.vb2) is ',len(self.vb2),'. len(self.cb1) is ',len(self.cb1),'. len(self.cb2) is ',len(self.cb2)
     exit(1)
    self.vbm1=self.vb1[0] ; self.cbm1=self.cb1[0] ; self.vbm2=self.vb2[0] ; self.cbm2=self.cb2[0]
    if abs(self.vbm1-self.vbm2)<min_dos or abs(self.cbm1-self.cbm2)<min_dos:
     print "dos.py: insulator. bandgap: %.5f. e-fermi: %.5f. self.vbm: %.5f. self.cbm: %.5f." % (self.cbm1-self.vbm1, grepen.efermi, self.vbm1, self.cbm1)
    else:
     print 'BMS ',min(abs(self.vbm1-self.vbm2),min(self.vbm1,self.vbm2)-max(self.cbm1,self.cbm2),abs(self.cbm1-self.cbm2))
   elif abs(self.dos[index_fermi][1])<min_dos and abs(self.dos[index_fermi][2])>min_dos:
    self.vb=self.dos[index_fermi:0:-1]
    self.cb=self.dos[index_fermi:len(self.dos)]
    self.vbm1=next(self.vb[x][0] for x in range(0,len(self.vb)) if abs(self.vb[x][1])>min_dos or abs(self.vb[x][2])<min_dos)
    self.cbm1=next(self.cb[x][0] for x in range(0,len(self.cb)) if abs(self.cb[x][1])>min_dos or abs(self.cb[x][2])<min_dos)
    print 'HM ',self.cbm1-self.vbm1
   elif abs(self.dos[index_fermi][1])>min_dos and abs(self.dos[index_fermi][2])<min_dos:
    self.vb=self.dos[index_fermi:0:-1]
    self.cb=self.dos[index_fermi:len(self.dos)]
    self.vbm1=next(self.vb[x][0] for x in range(0,len(self.vb)) if abs(self.vb[x][2])>min_dos or abs(self.vb[x][1])<min_dos)
    self.cbm1=next(self.cb[x][0] for x in range(0,len(self.cb)) if abs(self.cb[x][2])>min_dos or abs(self.cb[x][1])<min_dos)
    print 'HM ',self.cbm1-self.vbm1
  else:
    print 'dos.py: we only support ispin=1 and 2.'


