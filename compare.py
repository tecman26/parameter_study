from emulators import *
import matplotlib.pyplot as plt
from settings import *
from read1d import *
from read3d import *

loadEmulators()
#lcomp = 0.343
#dcomp = 0.843
lcomp = 0.8
dcomp = 0.33333
params = np.reshape(np.array([[lcomp,dcomp]]),(1,-1))
#plot1_v, plot1_v_std = emulVCon(params)
#plot1_y, plot1_y_std = emulYE(params)
#plot1_s, plot1_s_std = emulS(params)

pathname = "/mnt/research/SNAPhU/STIR/parameter_study/calib2/run_mcmcPS_171_a0.733333_b0.616667"
r, plot1_v, plot1_y, plot1_s, r_sh_1D = read1d(pathname, data_dir3D)


r_sh_3D, r_3D, v_con_3D, y_e_3D, s_3D = readOutput(data_dir3D, 3)
plot2 = v_con_3D

#print("Shock radius (1D) = "+str(emulRShock(params)[0]))
print("Shock radius (1D) = "+str(r_sh_1D))
print("Shock radius (3D) = "+str(r_sh_3D))

plt.figure("Convective Velocity")
#print(r.shape)
#print(r)
#print(len(r_3D))
#print(r_3D)

#print(plot1_v)
#print(plot1_y)
#print(plot1_s)
plt.plot(r,np.transpose(plot1_v), color = 'b') 
plt.plot(r,v_con_3D, color = 'g')

plt.figure("Electron Fraction")
plt.plot(r,np.transpose(plot1_y), color = 'b') 
plt.plot(r,y_e_3D, color = 'g')

plt.figure("Entropy")
plt.plot(r,np.transpose(plot1_s), color = 'b') 
plt.plot(r,s_3D, color = 'g')

plt.show() 
