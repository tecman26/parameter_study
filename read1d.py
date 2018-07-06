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

    print(data_dir1D)
    radius_cutoff = 5*10**7
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
    #print(fn_1d)
    try:
        ds_1d = yt.load(fn_1d)
    except:
        return 0, 0, 0, 0, 0

    #ray1 = ds_1d.ray([0,0,0],[1.665e7,0,0])

    ad = ds_1d.all_data()
    shocked_region =  ad.cut_region(['(obj["dens"] < 1e11) & (obj["entr"] > 8)'])
    
    radius = np.array(ad["r"].in_units("cm").v)
    trunc_index_1d = (np.abs(radius - radius_cutoff)).argmin() + 1
    radius = radius[:trunc_index_1d]
    
    v_con = np.array(ad["vcon"].v)
    v_con = v_con[:trunc_index_1d]

    entr = np.array(ad["entr"].v)
    entr = entr[:trunc_index_1d]

    ye = np.array(ad["ye  "].v)
    ye = ye[:trunc_index_1d]

    radius_shocked = np.array(shocked_region["r"].in_units("cm").v)
    #v_con = np.array(shocked_region["vcon"].v)
    #entr = np.array(shocked_region["entr"].v)
    #ye = np.array(shocked_region["ye  "].v)

    #radius = np.array(ray1['r'].in_units("km").v)
    #v_con = np.array(ray1['vcon'].v)
    #entr = np.array(ray1['entr'].v)
    #ye = np.array(ray1['ye  '].v)

   
    trunc_index_3d = (np.abs(data_array[0,:] - radius_cutoff)).argmin()
    trunc_index_3d += 1 
    radius_3d = data_array[0,:trunc_index_3d]
    size_3d = len(radius_3d)
    # ---------------------------------------------------------------
    # BEGIN INTERPOLATION
    # Need this to have same size 3d, 1d data
    # ---------------------------------------------------------------

    x = np.linspace(0, size_3d, radius.shape[0])
    xvals = np.linspace(0, 5*10**7, size_3d)
    
    x_shocked = np.linspace(0, size_3d, radius_shocked.shape[0])
 
    v_con_interp = np.interp(radius_3d, radius, v_con)
    entr_interp = np.interp(radius_3d, radius, entr)
    ye_interp = np.interp(radius_3d, radius, ye)
     
    neg_values = v_con_interp < 0
    v_con_interp[neg_values] = 0


    return radius_3d, v_con_interp, ye_interp, entr_interp, max(radius_shocked)
