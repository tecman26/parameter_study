#!/usr/bin/env python

# ---------------------------------------
#
#  A very bad function for reading in
#  our 3D data.
#
# ---------------------------------------

import numpy as np
import os

def read3d(dataDir):

    shockRadiusFile = os.path.join(dataDir,"mesa20_v_LR.dat")
    data = np.genfromtxt(shockRadiusFile)
    mean_shock_radius = data[:,11]
    time = data[:,0]
    mean_rs = np.array( [time, mean_shock_radius] )

    vconDir = os.path.join(dataDir,"vconData")
    profileDir = os.path.join(dataDir,"profileData")

    vconFile = os.path.join(vconDir,"mesa20_v_LR_hdf5_plt_cnt_0120.dat")
    profileFile = os.path.join(profileDir,"mesa20_v_LR_hdf5_plt_cnt_0120.dat")

    data_vcon = np.genfromtxt(vconFile)
    data_profile = np.loadtxt(profileFile)

    rey_stress = data_vcon[:,6]
    neg_values = rey_stress < 0
    rey_stress[neg_values] = 0

    vcon_radius = data_vcon[:,0]
    vcon = np.sqrt( rey_stress / 2 )
    prof_radius = data_profile[:,0]
    entropy = data_profile[:,8]
    ye = data_profile[:,10]

    vcon_interp = np.interp(prof_radius, vcon_radius, vcon)


    trunc = (np.abs(prof_radius - 5*10**7)).argmin()
    #print(trunc)
    #print(len(prof_radius))
    #print(prof_radius)
    #print(" -- TRUNCATE AT INDEX %f ---" % trunc)

    data = np.array([prof_radius[:(trunc+1)], vcon_interp[:(trunc+1)], \
      entropy[:(trunc+1)], ye[:(trunc+1)]])

    return data, np.transpose( mean_rs )
