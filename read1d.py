#!/usr/bin/env python

# ---------------------------------------
#
#  A very bad function for reading in
#  our 1D data.
#
# ---------------------------------------

import numpy as np
import os
from settings import *
import yt

def read1d(dataDir):

    # Will have to update the filename appropriately
    shockRadiusFile = os.path.join(dataDir,"mesa20_v_LR.dat")
    data = np.genfromtxt(shockRadiusFile)
    mean_shock_radius = data[:,11]
    time = data[:,0]
    mean_rs = np.array( [time, mean_shock_radius] )

    path = os.path.join(dataDir, "output/output") # May need to update.
    fn_1d = "stir_may10_s13.3_alpha0.9_hdf5_chk_0100" #Edit
    ds_1d = yt.load(fn_1d)

    ray1 = ds_1d.ray([0,0,0],[2e7,0,0])

    radius = np.array(ray1['r'].in_units("km").v)
    v_con = np.array(ray1['vcon'].v)
    entr = np.array(ray1['entr'].v)
    ye = np.array(ray1['ye  '].v)

    return radius, v_con, entr, ye
