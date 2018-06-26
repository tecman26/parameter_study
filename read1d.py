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

def read1d(data_dir1D, data_dir3D=data_dir3D):

    # ---------------------
    # Read 3D Data
    # ---------------------
    data_array, r_sh = read3d(data_dir3D)
    r_shock = r_sh[:,1]

    #data_dir1d is run directory
    pathname = os.path.join(data_dir1D,"output/sim_output") #Should start in output directory!
    #pathname = "/mnt/home/f0004519/parameter_study/trial_test/step"+step+"/"+runname+"/output/sim_output"
    runname = os.path.basename(data_dir1D)
    fn_1d = os.path.join(pathname,runname+"hdf5_chk_0013")
    print(fn_1d)
    try:
        ds_1d = yt.load(fn_1d)
    except:
        return 0, 0, 0, 0, 0

    #ray1 = ds_1d.ray([0,0,0],[1.665e7,0,0])

    ad = ds_1d.all_data()
    shocked_region =  ad.cut_region(['(obj["dens"] < 1e11) & (obj["entr"] > 8)'])
    
    radius = np.array(ad["r"].in_units("cm").v)
    v_con = np.array(ad["vcon"].v)
    entr = np.array(ad["entr"].v)
    ye = np.array(ad["ye  "].v)

    radius_shocked = np.array(shocked_region["r"].in_units("cm").v)
    #v_con = np.array(shocked_region["vcon"].v)
    #entr = np.array(shocked_region["entr"].v)
    #ye = np.array(shocked_region["ye  "].v)

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

    radius_shocked_interp = np.interp(xvals, x, radius_shocked)
    radius_interp = np.interp(xvals, x, radius)
    v_con_interp = np.interp(xvals, x, v_con)
    entr_interp = np.interp(xvals, x, entr)
    ye_interp = np.interp(xvals, x, ye)
    

    return radius_interp, v_con_interp, ye_interp, entr_interp, max(radius_shocked_interp)
