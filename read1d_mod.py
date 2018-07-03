#!/usr/bin/env python

# ---------------------------------------
#
#  A very bad function for reading in
#  our 3D data.
#
# ---------------------------------------

import numpy as np
import os
import matplotlib.pyplot as plt

def read1d_mod():

    scalarFile = "/mnt/research/SNAPhU/STIR/parameter_study/calib2/run_mcmcPS_20_a0.343333_b0.22/output/run_mcmcPS_20_a0.343333_b0.2.dat"

    data = np.genfromtxt(scalarFile)
    time = data[:,0]
    E_expl = data[:,9]
    shock_radius = data[:,11]
    rho_c = data[:,16]
    heat_gain = data[:,17]
    entr_gain = data[:,19]
    lum_nue = data[:,33]
    lum_anue = data[:,34]
    lum_nux = data[:,35]
    
    plt.figure("Explosion energy/shock radius")
    ax1 = plt.subplot()
    plt.plot(time, E_expl, label="explosion energy", color='r')
    plt.legend()
    ax2 = plt.twinx()
    plt.plot(time, shock_radius, label="shock radius", color='b')
    plt.legend()  
 
    plt.figure("Central density")
    plt.plot(time, rho_c, label="central density", color='g')
    plt.legend()

    plt.figure("Supernova attributes plot 2")
    ax3 = plt.subplot()
    plt.plot(time, heat_gain, label="net heating rate in gain region", color='r')
    plt.legend()
    ax4 = ax3.twinx()
    plt.plot(time, entr_gain, label="average entropy in gain region", color='b')
    plt.legend()

    plt.figure("Supernova attributes plot 3")
    plt.plot(time, lum_nue, label="electron neutrino luminosity", color='b')
    plt.plot(time, lum_anue, label="electron antineutrino luminosity", color='g')
    plt.plot(time, lum_nux, label="other neutrino luminosity", color='r')
    plt.legend()

    plt.show()
read1d_mod()
