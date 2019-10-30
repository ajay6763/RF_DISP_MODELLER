###########33
## Tkinter
import tkinter
from tkinter import Menu, filedialog, PhotoImage 
import tkFileDialog
import tkMessageBox
import tkSimpleDialog

##################
## OS stuff
import os
from shutil import copyfile

################
## Matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as  NavigationToolbar2Tk
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

#####################
### user defined liberaries
import Modify_model
#import Modify_model 
import Make_CPS_model 
import interpolate_lib
#### for file operations


import numpy as np
#### clear up
## setting up the input file
path=os.getcwd()
#os.system("rm -f updated_model ")
#os.system("rm -f temp* tmp* ")
rf='./PS49_stack.xy'
#import prep_model


vel='./vel.inp'

data=np.loadtxt(vel)
step=len(data)
#X,Y = interpolate_lib.interpolate_1D(data[:,1],data[:,0],20)
#X=np.flip(X,axis=0)
#Y=np.flip(Y,axis=0)
#to_save = np.column_stack((Y,X))
np.savetxt('updated_model_vs', data) 
step=len(data)

'''
temp[:,0]=data[:,0]
y=np.append(temp[:,0],0.0)
y=np.append(y,0.0)
#y.append(y[0])
temp[:,1]=data[:,1]
x=np.append(temp[:,1],temp[-1,1])
x=np.append(x,temp[0,1])
tmp=np.zeros((len(x),2))
tmp[:,0]=y
tmp[:,1]=x
np.savetxt('updated_model_vs', tmp) 
'''

vp_vs='./vp_vs.inp'
data=np.loadtxt(vp_vs)
X,Y = interpolate_lib.interpolate_1D(data[:,1],data[:,0],step)
X=np.flip(X,axis=0)
Y=np.flip(Y,axis=0)
to_save = np.column_stack((Y,X))
np.savetxt('updated_model_vp_vs', to_save) 
'''
#### setting vpvs
temp=np.zeros((len(data),2))
temp[:,0]=data[:,0]
y=np.append(temp[:,0],0.0)
y=np.append(y,0.0)
#y.append(y[0])
temp[:,1]=data[:,1]
x=np.append(temp[:,1],temp[-1,1])
x=np.append(x,temp[0,1])
tmp=np.zeros((len(x),2))
tmp[:,0]=y
tmp[:,1]=x
np.savetxt('updated_model_vp_vs', tmp) 
'''

disp='./200_SURF96.inp'
vp_vs = './updated_model_vp_vs'
vel = './updated_model_vs'
#copyfile(path+vel,path+'/updated_model')
#vel = './updated_model'



################3
## Tkinter Functions
def hello():
    print "hello!"

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def _modify_model():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
def load_rf():
    global rf
    root.filename =  filedialog.askopenfilename(initialdir = path,title = "Select file",filetypes = (("all files","*.*"),("text files","*.txt")))
    rf = root.filename
    return rf
def load_vel():
    global vel
    os.system('rm -f updated_model')
    root.filename =  filedialog.askopenfilename(initialdir = path,title = "Select file",filetypes = (("all files","*.*"),("text files","*.txt")))
    vel = root.filename
    return vel

def load_disp():
    global disp
    root.filename =  filedialog.askopenfilename(initialdir = path,title = "Select file",filetypes = (("all files","*.*"),("text files","*.txt")))
    dis = root.filename
    return disp

def save():
    os.system("cp vel.inp vel-`date +%F_time-%T`.inp.bak ")
    os.system("cp updated_model vel.inp")
def save_as(): ### This is not working
    #f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".inp")
    f = tkSimpleDialog.askstring
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    command='cp updated_model_vs '+ str(f)
    os.system(command)

def plot(vel,vp_vs,rf,disp,fig):
    #fig.cla()
    #fig.clf() 
    fig.clear()
    ################Vs
    data=np.loadtxt(vel)
    y=list(data[:,1])
    x=list(data[:,0])
    y.append(y[-1])
    y.append(y[0])
    x.append(0)
    x.append(0)
    poly = Polygon(np.column_stack([x, y]), animated=True)
    ax_vel=fig.add_subplot(141)
    ax_vel.add_patch(poly)
    ax_vel.set_xlim([min(x),4.0])
    ax_vel.set_ylim([min(y),max(y)])
    ax_vel.set_xlabel('Vs ($km/s$)')
    ax_vel.set_ylabel('Depth ($km$)')
    plt.grid()
    p1 = Modify_model.PolygonInteractor(ax_vel, poly,'updated_model_vs',20)
    #canvas.draw()
    ######## interpolating vs and vp_vs to have same dimension
    vs=np.loadtxt('updated_model_vs')


    
    ################Vs
    ax_vp_vs = fig.add_subplot(142)
    data_vp_vs=np.loadtxt(vp_vs)
    #print data
    y=list(data_vp_vs[:,1])
    x=list(data_vp_vs[:,0])
    y.append(y[-1])
    y.append(y[0])
    x.append(0)
    x.append(0)

    poly_vp_vs = Polygon(np.column_stack([x, y]), animated=False)
    #ax_vp_vs.add_patch(poly_vp_vs)
    ax_vp_vs.plot(data_vp_vs[:,0],data_vp_vs[:,1],color='r',label='Synthetic')
    ax_vp_vs.add_patch(poly_vp_vs)#plot(data_vp_vs[:,0],data_vp_vs[:,1],color='r',label='Synthetic')
    p2 = Modify_model.PolygonInteractor(ax_vp_vs, poly_vp_vs,'updated_model_vp_vs',20)
    '''
    ax_vp_vs.set_xlim([0,2.0])
    ax_vp_vs.set_ylim([min(y),max(y)])
    ax_vp_vs.set_xlabel('Vp$_$Vs ')
    ax_vp_vs.set_ylabel('Depth ($km$)')
    '''
    #plt.legend(loc='best')
    #plt.grid()
    #p2 = Modify_model_Vp_Vs.PolygonInteractor(ax_vp_vs, poly_vp_vs,'updated_model_vp_vs')
    #canvas.draw()
    ######## make CPS input file
    #Make_CPS_model
    Make_CPS_model.make()
    
# fig.add_subplot(131).plot(data[:,1],data[:,5])

    #############RF
    # plot observed RF
    ax_rf = fig.add_subplot(143)
    data=np.loadtxt(rf) 
    ax_rf.plot(data[:,1],data[:,0],color='k',label='Observed')
    ##### run and plot RF forward
    os.system("hrftn96 -P -ALP 2.5 -DT 0.1 -D 5. -RAYP 0.07 -M temp_mod  -2 hr  -NSAMP 1500")
    os.system("mv hrftn96.sac temp_mod.2.5.eqr")
    os.system("sac2xy temp_mod.2.5.eqr rf.out")
    data=np.loadtxt('rf.out') 
    ax_rf.plot(data[:,1],data[:,0],color='r',label='Synthetic')
    ax_rf.invert_yaxis()
    ax_rf.set_ylim((20,-5))
    plt.legend(loc='best')
    plt.grid()
    ax_rf.set_xlabel('Amplitude ')
    ax_rf.set_ylabel('Time ($s$)')

    #fig.add_subplot(132).stackplot(data[:,1],data[:,0],color='k')
    ######### Disp
    ### Plot observed disp
    data=np.loadtxt(disp,usecols=(5,6,7))
    ax_disp = fig.add_subplot(144)
    #ax2.errorbar(profile_in,topo_in,yerr=topo_error,fmt='o-',markersize=marker_size,ecolor='b',label='Observed')    
    ax_disp.errorbar(data[:,1],data[:,0],xerr=data[:,2],fmt='o',label='Observed')
    ### run and plot disp forward
    os.system("surf96 39")
    os.system("surf96 1 2 6")
    os.system("surf96 27 disp.out")
    data=np.loadtxt('disp.out',usecols=(5,6,7))
    #ax2.errorbar(profile_in,topo_in,yerr=topo_error,fmt='o-',markersize=marker_size,ecolor='b',label='Observed')    
    ax_disp.errorbar(data[:,1],data[:,0],xerr=data[:,2],fmt='o',color='r',label='Synthetic')
    

    #ax_disp.errplot(data[:,1],data[:,0],'o',label='Obs')
    plt.legend(loc='best')
    plt.grid()
    ax_disp.invert_yaxis()
    ax_disp.set_ylim(   ( max(data[:,0]) , min(data[:,0])  ) )
    ax_disp.set_xlabel('Velocity ($km/s$)')
    ax_disp.set_ylabel('Period ($s$)')

    #fig.add_subplot(133).plot(data[:,1],data[:,0],'r')
    #canvas.draw()
    canvas.draw()
    #fig.canvas.flush_events()
    canvas.mpl_connect("key_press_event", on_key_press)
    #fig.clear()



######################################
### Main App
##### Starting TKinter
root = tkinter.Tk()
root.wm_title("RF DISP Modeller")
#### Embedding matplotib fig in TKiner canvas
#fig = Figure(figsize=(5, 4), dpi=100)
fig= plt.figure()

#### Getting the Cavas for the matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#### Addig the matplotlib toolbar
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
canvas.draw()

canvas.mpl_connect("key_press_event", on_key_press)





menubar = Menu(root)
## create a pulldown menu to load vel,RF,disp
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open Velocity file", command=lambda:load_vel())
print(rf)
filemenu.add_command(label="Open RF file", command=lambda:load_rf())
filemenu.add_command(label="Open Disp file", command=lambda:load_disp())
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Open", menu=filemenu)

menubar.add_command(label="Save Model", command=lambda:save())
menubar.add_command(label="Run Model", command=lambda:plot(vel,vp_vs,rf,disp,fig))
menubar.add_command(label="Quit", command=_quit)



helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
helpmenu.add_command(label="Help", command=hello)
menubar.add_cascade(label="Help", menu=helpmenu)




# display the menu
root.config(menu=menubar)


####################################################
### This connects the key press events in the matpplotlib


#button1 = tkinter.Button(master=root, text="Quit", command=_quit)
#button2 = tkinter.Button(master=root, text="Modify", command=_modify_model)
#button3 = tkinter.Button(master=root, text="Refresh", command=lambda:plot(vel,rf,disp,fig))



'''
# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
'''
#menubar.add_cascade(label="Help", menu=helpmenu)


#button1 = tkinter.Button(master=root, text="Quit", command=_quit)
#button2 = tkinter.Button(master=root, text="Modify", command=_modify_model)
#button3 = tkinter.Button(master=root, text="Refresh", command=lambda:plot(vel,rf,disp,fig))

#button1.pack(side=tkinter.LEFT)
#button2.pack(side=tkinter.RIGHT)
#button3.pack(side=tkinter.RIGHT)

tkinter.mainloop()


# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
