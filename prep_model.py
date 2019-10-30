import numpy as np 
import math

def prep_model_litmod(litmod_post_process_file,dist):
	data=np.loadtxt(litmod_post_process_file,usecols=(0,1,2,3,4,5,6))
	vp_vs=1.73 #input('Enter Vp/Vs value:  ')
	#########################################################
	#### Anelastic attenuation model from Jackson et al., 2010
	########################################################
	AA1=816
	alfa3=0.36
	energi=293.0E03
	volexp=1.20E-05
	rgas=8.314472
	pi=3.1415926
	Qp=[]
	Qs=[]
	dsize=10
	oscill=50
	### data format
	#  X	Z	T 	P 	Vp 	Vs 	density 	Material mk??
	## caluclating Vp in crust according to Brocher 2005
	f=0
	ind_dist=np.where(data[:,0]==dist)
	ind_crust=np.where( (data[:,4]==0) & (data[:,0]==dist) )
	ind_mantle=np.where( (data[:,4]!=0) & (data[:,0]==dist) )

	for i in range(len(data)):
		if data[i,5]==0 and data[i,0]== dist:
			dens=data[i,6]/1000
			# From emprical relations		
			data[i,4]= 39.128*dens - 63.064*dens**2 + 37.083*dens**3 - 9.1819*dens**4 + 0.8215*dens**5
			#f=vp_vs -  data[i,1]/1000
			data[i,5]=data[i,4]/vp_vs
			### Accroding to equation 6 Brocher BSSA 2005
			#data[i,5]= 0.7858 -1.2344*data[i,4] + 0.7949*data[i,4]**2 - 0.1238*data[i,4]**3 + 0.0064*data[i,4]**4
			
			### Accroding to equation 7 Brocher BSSA 2005
			#data[i,5]= (data[i,4]-1.36)/1.16 # does not work

			### Accroding to equation 8 Brocher BSSA 2005
			#data[i,5]= 2.88 + 0.52*(data[i,4]-5.25)  # works but not perfect
			## Constant values
			#data[i,4]=6.52
			#data[i,5]=3.0
			Qp.append(1000)
			Qs.append(200)
		else:
			parexp=math.exp((-(energi+(volexp*data[i,3])))/(rgas*(data[i,2]+273.0E0)))
			sqatt50=AA1*(((oscill*(1.0E0/(dsize*1000.0E0)))*parexp))**alfa3	
			Qp.append((1/sqatt50)*(9/4))
			Qs.append(1/sqatt50)

	is_first_line = True
	f=open("crust","w")
	l=list(ind_crust[0])
	for i in l[:-1]:
		f.writelines(" %f  %f  %f  %f  %f %f %f %f %f  \n " % (data[i,0],data[i,1],data[i,2],data[i,3],data[i,4],data[i,5],data[i,6]/1000,Qp[i],Qs[i]))
	f.writelines(" %f  %f  %f  %f  %f %f %f %f %f" % (data[l[-1],0],data[l[-1],1],data[l[-1],2],data[l[-1],3],data[l[-1],4],data[l[-1],5],data[l[-1],6]/1000,Qp[l[-1]],Qs[l[-1]]))
	f.close()

	f=open("vel.inp","w")
	l=list(ind_crust[0])
	for i in l[:-1]:
		f.writelines(" %f  %f  \n " % (data[i,5],data[i,1]))
	f.writelines(" %f  %f  " % (data[l[-1],5],data[l[-1],1]))
	f.close()

	f=open("vp_vs.inp","w")
	l=list(ind_crust[0])
	for i in l[:-1]:
		f.writelines(" %f  %f  \n " % (data[i,4]/data[i,5],data[i,1]))
	f.writelines(" %f  %f  " % (data[l[-1],4]/data[l[-1],5],data[l[-1],1]))
	f.close()



	l=list(ind_mantle[0])
	f=open("mantle","w")
	for i in l[:-1]:
		f.writelines(" %f  %f  %f  %f  %f %f %f %f %f  \n " % (data[i,0],data[i,1],data[i,2],data[i,3],data[i,4],data[i,5],data[i,6]/1000,Qp[i],Qs[i]))
	f.writelines(" %f  %f  %f  %f  %f %f %f %f %f" % (data[l[-1],0],data[l[-1],1],data[l[-1],2],data[l[-1],3],data[l[-1],4],data[l[-1],5],data[l[-1],6]/1000,Qp[l[-1]],Qs[l[-1]]))
	f.close()
