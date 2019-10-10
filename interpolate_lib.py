import numpy as np 
from scipy import interpolate
import matplotlib.pyplot as plt

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
	f = interpolate.interp1d(x,y,kind='linear')
	x_new = np.arange(min(x),max(x),step=step)
	y_new = f(x_new)
	return x_new,y_new

def interpolate_2D(x,y,step):
	f = interpolate.interp1d(x,y,kind='linear')
	x_new = np.arange(min(x),max(x),step=step)
	y_new = f(x_new)
	return x_new,y_new

data=np.loadtxt('vel.inp')
x,y=interpolate_cubic(-data[:,1],data[:,0],0.5)

plt.plot(-data[:,1],data[:,0],label='orignal')
plt.plot(x,y,label='interpolate')
plt.legend()

plt.show()