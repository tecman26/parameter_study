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

    radius = data_vcon[:,0]
    vcon = np.sqrt( abs( data_vcon[:,6] ) / 2 )
    entropy = data_profile[:,8]
    ye = data_profile[:,10]

    trunc = (np.abs(radius - 5*10**7)).argmin()
    print(" -- TRUNCATE AT INDEX %f ---" % trunc[0][0])

    data = np.array([radius[:trunc[0][0]], vcon[:trunc[0][0]], \
      entropy[:trunc[0][0]], ye[:trunc[0][0]]])

    return np.transpose(data), np.transpose( mean_rs )
