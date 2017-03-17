#!/usr/bin/python
# dos related utility
import numpy as np
import os
from __main__ import *
# parameter: min_dos. is dos considered 0 if it's 0.002? 
min_dos=1E-3
# initialize dos file. all dos -> np.float64::tdos
doscar_file=open("DOSCAR","r")
tmplines=doscar_file.readlines()
doscar_lines=[tmplines[i].split() for i in range(6,6+grepen.nedos)]
dos=np.float64(doscar_lines)
index_fermi=abs(dos[:,0]-grepen.efermi).argmin()+1
#ispin=1 or 2?
if grepen.lsorbit!='F':
 print "dos.py: we don't support lsorbit=true yet. exiting..."
 exit(1)
if grepen.ispin==1: 
 ##ispin=1
 if abs(dos[index_fermi][1])>min_dos:
  print 'dos.py: conductor.'
 else: 
  VB=dos[index_fermi:0:-1]
  CB=dos[index_fermi:len(dos)]
  VB1=[VB[x][0] for x in range(0,len(VB)) if abs(VB[x][1])>min_dos]
  CB1=[CB[x][0] for x in range(0,len(CB)) if abs(CB[x][1])>min_dos]
  if len(VB1)==0 or len(CB1)==0:
   print 'dos.py: weird. len(VB1/CB1) is 0'
   exit(1)
  VBM1=VB1[0]
  CBM1=CB1[0]
  print 'dos.py: insulator. bandgap: ',CBM1-VBM1,' eV'
elif grepen.ispin==2:
 ##ispin=2
 if abs(dos[index_fermi][1])>min_dos and abs(dos[index_fermi][2])>min_dos:
  print 'dos.py: conductor. quite probably. but check dos anyway.'
 elif abs(dos[index_fermi][1])<min_dos and abs(dos[index_fermi][2])<min_dos: 
  VB=dos[index_fermi:0:-1]
  CB=dos[index_fermi:len(dos)]
  VB1=[VB[x][0] for x in range(0,len(VB)) if abs(VB[x][1])>min_dos]
  VB2=[VB[x][0] for x in range(0,len(VB)) if abs(VB[x][2])>min_dos]
  CB1=[CB[x][0] for x in range(0,len(CB)) if abs(CB[x][1])>min_dos]
  CB2=[CB[x][0] for x in range(0,len(CB)) if abs(CB[x][2])>min_dos]
  if len(VB1)==0 or len(VB2)==0 or len(CB1)==0 or len(CB2)==0:
   print 'dos.py: weird. len(VB1) is ',len(VB1),'. len(VB2) is ',len(VB2),'. len(CB1) is ',len(CB1),'. len(CB2) is ',len(CB2)
   exit(1)
  VBM1=VB1[0] ; CBM1=CB1[0] ; VBM2=VB2[0] ; CBM2=CB2[0]
  if abs(VBM1-VBM2)<min_dos or abs(CBM1-CBM2)<min_dos:
   print 'dos.py: insulator. bandgap: ',CBM1-VBM1,' eV'
  else:
   print 'BMS ',min(abs(VBM1-VBM2),min(VBM1,VBM2)-max(CBM1,CBM2),abs(CBM1-CBM2))
 elif abs(dos[index_fermi][1])<min_dos and abs(dos[index_fermi][2])>min_dos:
  VB=dos[index_fermi:0:-1]
  CB=dos[index_fermi:len(dos)]
  VBM1=next(VB[x][0] for x in range(0,len(VB)) if abs(VB[x][1])>min_dos or abs(VB[x][2])<min_dos)
  CBM1=next(CB[x][0] for x in range(0,len(CB)) if abs(CB[x][1])>min_dos or abs(CB[x][2])<min_dos)
  print 'HM ',CBM1-VBM1
 elif abs(dos[index_fermi][1])>min_dos and abs(dos[index_fermi][2])<min_dos:
  VB=dos[index_fermi:0:-1]
  CB=dos[index_fermi:len(dos)]
  VBM1=next(VB[x][0] for x in range(0,len(VB)) if abs(VB[x][2])>min_dos or abs(VB[x][1])<min_dos)
  CBM1=next(CB[x][0] for x in range(0,len(CB)) if abs(CB[x][2])>min_dos or abs(CB[x][1])<min_dos)
  print 'HM ',CBM1-VBM1
else:
  print 'dos.py: we only support ispin=1 and 2.'
