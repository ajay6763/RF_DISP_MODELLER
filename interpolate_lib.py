import numpy as np 
from scipy import interpolate
import matplotlib.pyplot as plt
#import interpolate_lib
def regularise(x,y,step):
	### Linear interpolation
	#f = interpolate.interp1d(x,y,kind='linear')
	#x_new = np.arange(min(x),max(x),step=step)
	#y_new = f(x_new)    
	### Nearest
    #f = interpolate.interp1d(x, y, kind='nearest')
    ### Cubic spline
    f = interpolate.InterpolatedUnivariateSpline(x, y)
    x_new = np.arange(min(x),max(x),step=step)
    y_new = f(x_new)
    return x_new,y_new
def interpolate_1D(x,y,step):
	f = interpolate.interp1d(x,y,kind='slinear')
	#f = interpolate.InterpolatedUnivariateSpline(-x, y)
	x_new = np.linspace(min(x),max(x),num=step)
	y_new = f(x_new)
	return x_new,y_new
def interpolate_1D_RF_DISP(x,y,step):
	f = interpolate.interp1d(x,y,kind='linear')
	x_new = np.arange(max(x),min(x),step=len(x))
	y_new = f(x_new)
	return x_new,y_new


def interpolate_2D(x,y,z,profile_len,reso,step):
	print('Model info \n')
	#reso=input('Enter resolution along the profile: \n')
	#reso=5
	#profile_len=input('Enter resolution the profile length: \n')
	#profile_len=625 
	x_=data[0:95,1]
	y_=range(0,profile_len,reso)
	Z=[]
	temp=0
	for i in range(len(x_)):
  		tmp = []
  		for j in range(len(y_)):
  			tmp.append(z[temp])
    		temp=temp+1
    		Z.append(tmp)
  	### making X,Y grid
	X,Y=np.meshgrid(y_,x_)

	#f = interpolate.interp2d(Y,X,Z,kind='linear')
	f = interpolate.interp2d(y,x,z,kind='linear')
	
	x_new = np.arange(min(x_),max(x_),step=step)
	y_new = np.arange(min(y_),max(y_),step=step)
	z_new = f(y_new,x_new)
	return x_new,y_new,z_new
'''
#data=np.loadtxt('vel.inp')
data=np.loadtxt('vp_vs.inp',usecols=(0,1))
r=interpolate_1D(data[:,0],data[:,1],5)
print r
np.savetxt('t',r)
#x,y,z=interpolate_2D(data[:,0],data[:,1],data[:,2],625,5,5)
#print z
#print np.shape(z)
#print x
#plt.contourf(y,x,z)
#plt.colorbar()
#plt.plot(x,y,label='orignal')
#plt.plot(x,y,label='interpolate')
#plt.legend()

#plt.show()
'''