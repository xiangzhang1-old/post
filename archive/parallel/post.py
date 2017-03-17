#!/usr/bin/python
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import multiprocessing

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
execfile(dname+'/grepen.py')
execfile(dname+'/dos.py')
execfile(dname+'/bandstructure.py')
