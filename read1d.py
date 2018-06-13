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
from read3d import *
import yt

def read1d(dataDir):


    # ---------------------
    # Read 3D Data
    # ---------------------
    data_array, r_sh = read3d(dataDir)
    r_shock = r_sh[:,1]



    fn_1d = "stir_may10_s13.3_alpha0.9_hdf5_chk_0100"
    ds_1d = yt.load(fn_1d)

    #ray1 = ds_1d.ray([0,0,0],[1.665e7,0,0])

    ad = ds_1d.all_data()
    shocked_region =  ad.cut_region(['(obj["dens"] < 1e11) & (obj["entr"] > 8)'])
    radius = np.array(shocked_region["r"].in_units("cm").v)
    v_con = np.array(shocked_region["vcon"].v)
    entr = np.array(shocked_region["entr"].v)
    ye = np.array(shocked_region["ye  "].v)

    #radius = np.array(ray1['r'].in_units("km").v)
    #v_con = np.array(ray1['vcon'].v)
    #entr = np.array(ray1['entr'].v)
    #ye = np.array(ray1['ye  '].v)

    size_3d = data_array[:,1].shape[0]

    # ---------------------------------------------------------------
    # BEGIN INTERPOLATION
    # Need this to have same size 3d, 1d data
    # ---------------------------------------------------------------

    x = np.linspace(0, size_3d, radius.shape[0])
    xvals = np.linspace(0, size_3d, size_3d)

    radius_interp = np.interp(xvals, x, radius)
    v_con_interp = np.interp(xvals, x, v_con)
    entr_interp = np.interp(xvals, x, entr)
    ye_interp = np.interp(xvals, x, ye)

    return radius_interp, v_con_interp, entr_interp, ye_interp
