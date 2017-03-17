#!/usr/bin/python
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
import multiprocessing

from grepen import *
from dos import *
from bands import *

Agrepen=grepen()
Ados=dos(Agrepen)
Abands=bands(Agrepen,Ados)
