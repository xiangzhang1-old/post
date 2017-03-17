#!/usr/bin/python 

# initialize
eigenval_file=open("EIGENVAL","r")
tmplines=eigenval_file.readlines()
eigenval_lines=[tmplines[i].split() for i in range(6,len(tmplines))]
nkpts=len(eigenval_lines)/(NBANDS+2)
listOfBandOfKptE=[]
## all bands [kx,ky,kz,e] -> np.float64::bands
for i_band in range(0,NBANDS):
 BandOfKptE=[]
 for i_kpt in range(0,nkpts):
  KptE=eigenval_lines[i_kpt*(NBANDS+2)+1][0:3]
  KptE.append(eigenval_lines[i_kpt*(NBANDS+2)+i_band+2][1])
  BandOfKptE.append(KptE)
 listOfBandOfKptE.append(BandOfKptE)
BANDS=np.float64(listOfBandOfKptE)
# select bands that cross CBM1+0.5 and VBM-0.5
neargap_bands=[]
for band in BANDS:
 if any([(KptE[3]<VBM1 and KptE[3]>VBM1-0.5) for KptE in band]) or any([(KptE[3]>CBM1 and KptE[3]<CBM1+0.5) for KptE in band]):   
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
### this function returns average_min_kpoint_deltae for each i_band.
def parallelDeltaE(i_band_local):
 average_min_kpoint_deltae_entireband=0
 average_min_kpoint_deltae_01=0
 average_min_kpoint_deltae_03=0
 counter_entireband=0
 counter_01=0
 counter_03=0
 band=neargap_bands[i_band_local]
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
  if VBM1-0.3<band[i_kpoint_1][3]<VBM1 or CBM1<band[i_kpoint_1][3]<CBM1+0.3:
   average_min_kpoint_deltae_03+=min_kpoint_deltae
   counter_03+=1
  if VBM1-0.1<band[i_kpoint_1][3]<VBM1 or CBM1<band[i_kpoint_1][3]<CBM1+0.1:
   average_min_kpoint_deltae_01+=min_kpoint_deltae
   counter_01+=1
   #for debug purposes:
   print "0.1-neargap kpoint, band ", i_band_local, ": ", band[i_kpoint_1]
 average_min_kpoint_deltae_entireband/=counter_entireband
 average_min_kpoint_deltae_03/=counter_03
 average_min_kpoint_deltae_01/=counter_01
 return [average_min_kpoint_deltae_entireband,average_min_kpoint_deltae_03,average_min_kpoint_deltae_01,counter_entireband,counter_03,counter_01]
### parallelized version. 
parallelDeltaE_results = Parallel(n_jobs=20)(delayed(parallelDeltaE)(i_band) for i_band in range(0,len(neargap_bands)))
l=np.float64(parallelDeltaE_results) ####a shorthand
average_min_kpoint_deltae_entireband=sum(l[:,0])/float(len(l[:,0]))
average_min_kpoint_deltae_03=sum(l[:,1])/float(len(l[:,1]))
average_min_kpoint_deltae_01=sum(l[:,2])/float(len(l[:,2]))
counter_entireband=int(sum(l[:,3]))
counter_03=int(sum(l[:,4]))
counter_01=int(sum(l[:,5]))
### output result
print "bandstructure.py: DeltaE_KPOINTS by visual inspection: entireband value %.5f eV based on %d points, 0.3eV-neargap value %.5f eV based on %d points, 0.1eV-neargap value %.5f eV based on %d points" % (average_min_kpoint_deltae_entireband, counter_entireband, average_min_kpoint_deltae_03, counter_03, average_min_kpoint_deltae_01, counter_01)
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
