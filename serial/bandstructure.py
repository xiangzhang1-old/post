#!/usr/bin/python 
import os
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from __main__ import *
import time
import progressbar
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer
# initialize
eigenval_file=open("EIGENVAL","r")
tmplines=eigenval_file.readlines()
eigenval_lines=[tmplines[i].split() for i in range(6,len(tmplines))]
nkpts=len(eigenval_lines)/(grepen.nbands+2)
listOfBandOfKptE=[]
## all bands [kx,ky,kz,e] -> np.float64::bands
for i_band in range(0,grepen.nbands):
 BandOfKptE=[]
 for i_kpt in range(0,nkpts):
  KptE=eigenval_lines[i_kpt*(grepen.nbands+2)+1][0:3]
  KptE.append(eigenval_lines[i_kpt*(grepen.nbands+2)+i_band+2][1])
  BandOfKptE.append(KptE)
 listOfBandOfKptE.append(BandOfKptE)
bands=np.float64(listOfBandOfKptE)
# select bands that cross CBM1+0.5 and VBM-0.5
neargap_bands=[]
for band in bands:
 if any([(KptE[3]<dos.VBM1 and KptE[3]>dos.VBM1-0.5) for KptE in band]) or any([(KptE[3]>dos.CBM1 and KptE[3]<dos.CBM1+0.5) for KptE in band]):   
  neargap_bands.append(band)
print 'bandstructure.py: the number of near-gap bands are', len(neargap_bands)
print 'bandstructure.py: warning. this program has not been adapted for magnetic systems. ispin=2 is fine, but only spin channel 1 is considered.'
# -------------------precision check------------------------- 
## geometry of k-mesh
kpoints=[KptE[0:3] for KptE in neargap_bands[0]]
min_kpoint_dist=1
for i_kpoint_1 in range(0,len(kpoints)):
 for i_kpoint_2 in range(0,len(kpoints)):
  kpoint_dist=np.linalg.norm(kpoints[i_kpoint_1]-kpoints[i_kpoint_2])
  if kpoint_dist<min_kpoint_dist and i_kpoint_1!=i_kpoint_2 and kpoint_dist>1E-9:
   min_kpoint_dist=kpoint_dist
## calculate DeltaE_KPOINTS by grabbing average E diff / average E diff near bandgap from EIGENVAL.
average_min_kpoint_deltae_entireband=0
average_min_kpoint_deltae_01=0
average_min_kpoint_deltae_03=0
counter_entireband=0
counter_01=0
counter_03=0
widgets = ['precision check bands: ', Percentage(), ' ', Bar(), ' ', ETA()] #pretty print
pbar = ProgressBar(widgets=widgets, maxval=len(neargap_bands)).start()
for i_band,band in enumerate(neargap_bands):
 pbar.update(i_band+1) #pretty print
 for i_kpoint_1 in range(0,len(kpoints)):
  #find the deltae for this kpoint
  min_kpoint_deltae=1
  for i_kpoint_2 in range(0,len(kpoints)):
   kpoint_dist=np.linalg.norm(kpoints[i_kpoint_1]-kpoints[i_kpoint_2])
   kpoint_deltae=abs(band[i_kpoint_1][3]-band[i_kpoint_2][3])
   if kpoint_dist<min_kpoint_dist*2 and kpoint_dist>min_kpoint_dist*0.5 and kpoint_deltae<min_kpoint_deltae:
    min_kpoint_deltae=kpoint_deltae
  #if this kpoint energy is near bandgap (kpoint is valid) then add this point to average
  if 1==1:
   average_min_kpoint_deltae_entireband+=min_kpoint_deltae
   counter_entireband+=1
  if dos.VBM1-0.3<band[i_kpoint_1][3]<dos.VBM1 or dos.CBM1<band[i_kpoint_1][3]<dos.CBM1+0.3:
   average_min_kpoint_deltae_03+=min_kpoint_deltae
   counter_03+=1
  if dos.VBM1-0.1<band[i_kpoint_1][3]<dos.VBM1 or dos.CBM1<band[i_kpoint_1][3]<dos.CBM1+0.1:
   average_min_kpoint_deltae_01+=min_kpoint_deltae
   counter_01+=1
pbar.finish() #pretty print
average_min_kpoint_deltae_entireband/=counter_entireband
average_min_kpoint_deltae_03/=counter_03
average_min_kpoint_deltae_01/=counter_01
print "bandstructure.py: DeltaE_KPOINTS by visual inspection: entireband value ",average_min_kpoint_deltae_entireband,"eV based on",counter_entireband, " points, 0.3eV-neargap value ",average_min_kpoint_deltae_03,"eV based on",counter_03, " points, 0.1eV-neargap value ",average_min_kpoint_deltae_01, "eV based on ", counter_01," points"
## calculate DeltaE_KPOINTS by Delta_K x NablaE

# -------------------end precision check---------------------
# --------------------plot E(KPOINT)-----------------
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#xs = bands[0][:,0]
#ys = bands[0][:,1]
#zs = bands[0][:,2]
#cs = bands[0][:,3]
#p = ax.scatter(xs, ys, zs, s=15, c=cs)
#
#ax.set_xlabel('KX')
#ax.set_ylabel('KY')
#ax.set_zlabel('KZ')
#
#fig.colorbar(p)
#
#plt.show()
# -------------------end plot--------------
