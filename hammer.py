import numpy as np
from helper_functions import *
from read1d import *
from read3d import *
from emulators import *
import emcee

loadEmulators()

runs_directory = os.path.join(trial_directory,"runs")
if os.path.isdir(runs_directory) == False:
    os.makedirs(runs_directory)
run_num = 1
runs = glob.glob(os.path.join(runs_directory,"run*"))
    
if len(runs) == 0:
    pass
else: 
    runs = [os.path.basename(x) for x in runs]
    run_nums = [int(x.split("_")[1]) for x in runs]
    run_nums.sort()
    run_num = run_nums[-1]
    run_num += 1
output_directory = os.path.join(trial_directory,"runs/run_"+str(run_num))
os.makedirs(output_directory)

r_sh_3D, r_3D, v_con_3D, y_e_3D, s_3D = readOutput(data_dir3D)

def lnprob(params):

    r_sh, r_sh_std = emulRShock(params)
    v_con, v_con_std = emulVCon(params)
    y_e, y_e_std = emulYE(params)
    s, s_std = emulS(params)

    chi2 = (r_sh - r_sh_3D)**2/r_sh_3D + chi2(v_con, v_con_3D) + chi2(y_e, y_e_3D) + chi2(s, s_3D)
    
    return -chi2/2

# Generate starting positions
init_pos = []
for i in range(n_walkers):
    l = (lmax-lmin)*np.random.random_sample() + lmin
    dneut = (dmax-dmin)*np.random.random_sample() + dmin
    dye = (dmax-dmin)*np.random.random_sample() + dmin
    deint = (dmax-dmin)*np.random.random_sample() + dmin
    detrb = (dmax-dmin)*np.random.random_sample() + dmin

    init_pos.append([l, dneut, dye, deint, detrb])

sampler = emcee.EnsembleSampler(n_walkers, 5, lnprob, args=params)
sampler.run_mcmc(init_pos, n_steps)
writePositions(output_directory, sampler.flatchain)

