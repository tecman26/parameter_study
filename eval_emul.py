######################################################
# Compares emulator predictions to simulation results
######################################################

import numpy as np
from scipy.stats import chisquare
import matplotlib.pyplot as plt
from helper_functions import *
from emulators import *

test_dir = "/mnt/research/SNAPhU/STIR/parameter_study/emul_test"
pos_filename = os.path.join(test_dir, "positions.txt")
pos_list, pos_arr = readPositions(pos_filename)
test_sim_id = 2

data_pathname = glob.glob(os.path.join(test_dir,"run_mcmcPS_"+str(test_sim_id)+"*")) #Choose results from first simulation
data_pathname = data_pathname[0]

r_sim, v_con_sim, y_e_sim, s_sim, r_sh_sim = read1d(data_pathname)


params = pos_arr[test_sim_id] #should be a two-element list
params = np.array(params)
params = np.reshape(params,(1,-1))

loadEmulators()
r_sh_emul, r_sh_std = emulRShock(params)
v_con_emul, v_con_std = emulVCon(params)
y_e_emul, y_e_std = emulYE(params)
s_emul, s_std = emulS(params)

def rShockCompare():
    print("r_sh_sim = "+str(r_sh_sim))
    print("r_sh_emul = "+str(r_sh_emul))
    
def vConCompare():
    norm = l2_norm(v_con_emul, v_con_sim)
    print("Convective velocity L2 norm = "+str(norm))

def yECompare():
    norm = l2_norm(y_e_emul, y_e_sim)
    print("Electron Fraction L2 norm = "+str(norm))

def SCompare():
    norm = l2_norm(s_emul, s_sim)
    print("Entropy L2 norm = "+str(norm))

def plot():
    plt.figure("Convective Velocity")
    plt.plot(r_sim, v_con_sim, color = 'b')
    plt.plot(r_sim, v_con_emul, color = 'g')
    
    plt.figure("Electron Fraction")
    plt.plot(r_sim, y_e_sim, color = 'b')
    plt.plot(r_sim, y_e_emul, color = 'g')
    
    plt.figure("Entropy")
    plt.plot(r_sim, s_sim, color = 'b')
    plt.plot(r_sim, s_emul, color = 'g')
    
    plt.show()

if __name__ == "__main__":
    rShockCompare()
    vConCompare()
    yECompare()
    SCompare()
    plot()   
