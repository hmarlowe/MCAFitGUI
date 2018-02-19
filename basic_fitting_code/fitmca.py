import os
import numpy as np
import matplotlib.pyplot as plt
import GaussFit as gf
import curvefitting
import pdb
import inspect
import Tkinter, Tkconstants, tkFileDialog
from tkFileDialog import askopenfilename
plt.ion()

mcalen=1024 ##This should be changed to the number of mca channels in the file you're fitting i.e. 512, 1024...

def runfit(save=1):
	
	fname=selectmca()

	f=open(fname,'r')
	for i, l in enumerate(f): pass
	filelen=i+1
	

	spec=np.genfromtxt(fname, skip_header=filelen-(mcalen+1), skip_footer=1)
	chan=np.arange(0,len(spec))

	plt.figure(1)
	plt.clf()
	plt.plot(chan, spec)
	params, model, gerrs, chisq, chancut, speccut = auto_fit(spec, chan)
	pdb.set_trace()
	dof=len(chancut)-4
	rchisq=chisq/dof
	print params, gerrs, chisq, rchisq
	header='GaussFit params - Fit parameters: \nHeight of background, Amplitude, Shift, Width'

	params[3]=params[3]*2.35 #convert to FWHM from sigma
	H,A,X,W=params
	gerrs[3]=gerrs[3]*2.35
	data=np.array([params, gerrs, chisq])
	
	Her,Aer,Xer,Wer=gerrs # height, amp, centroid, width errors
	res=W/X # fwhm %
	reser= np.sqrt((Wer/X)**2 + ((W*Xer)/X**2)**2 )  #F=W/X dF/dw=1/X dF/dX = -W/X**2 sqrt((dw/X)**2+(W*dX/X**2)**2)
	plt.clf()
 	plt.plot(chancut, speccut)
   	plt.plot(chancut,model)
   	plt.title(fname)
   	plt.xlabel('MCA Channel')
   	plt.text(X+50,A, 'Cent: '+str(round(X,1))+' pm '+str(round(gerrs[2],2))+'\nWidth: '+str(round(W,1))+' pm '+str(round(gerrs[3],1))+'\nFWHM%: '+str(round(100*res,2)) )
   	if save:
		plt.savefig(fname+'.png')
		f=open(fname+'fit.txt', 'w')
		f.write(fname+'\n')
		f.write(header+'\n'+str(params)+'\n'+'Errors: '+str(gerrs)+'\n'+'Chisq = '+str(chisq)+'DoF = '+str(rchisq))
		f.close()



def selectmca():
	root = Tkinter.Tk()
	fname=askopenfilename(filetypes=[("MCA Files","*.mca")])
	root.destroy()
	print 'Read in file: ', fname
	return fname

def auto_fit(spec, chan):
   
    plt.figure(2, figsize=(10,10))
    plt.clf()
    plt.plot(chan, spec)

    #User selects data to be included in fit
    LLD=int(raw_input('Enter lower-level fit window: '))
    ULD=int(raw_input('Enter upper-level fit window: '))

    speccut=spec[LLD:ULD]
    chancut=chan[LLD:ULD]

    #Find initial guesses
    
    Ampg=int(raw_input('Amp guess? '))
    shiftg=int(raw_input('cent guess? '))
    widg=shiftg*0.3/2
    guess=[0,Ampg,shiftg,widg]
	
    """
    GaussFit
    params - Fit parameters: Height of background, Amplitude, Shift, Width

    """
    
    params, model, gerrs, chisq = gf.onedgaussfit(chancut, speccut, params=guess)
    print "~~~~~~~~~~~~~~~~\nFit parameters:\nBG height = ", round(params[0]), "\nCentroid = ", round(params[2],2), "\nAmp = ", round(params[1]), "\nFWHM = ", round(params[3]*2.35,2), "%\n~~~~~~~~~~~~~~~~"
   
    plt.plot(chancut, model)
    plt.xlim(LLD-100, ULD+100)

    while raw_input('ReFit? ') in ('Y', 'y'):
    	plt.clf()
    	plt.plot(chan, spec)
	LLD=int(raw_input('Enter guess for initial x '))
	ULD=int(raw_input('max x value? '))
	Ampg=int(raw_input('Amp guess? '))
	shiftg=int(raw_input('cent guess? '))
	#xb=[x0,xm]
    	speccut=spec[LLD:ULD]
    	chancut=chan[LLD:ULD]
    	errors=np.sqrt(speccut)
    	#plt.xlim(0,200)
    	#Ampg=np.max(speccut)
        #shiftg=int(np.average(chancut[np.where(spec==Ampg)]))
    	widg=shiftg*0.3/2
   	guess=[0,Ampg,shiftg,widg]
    	params, model, gerrs, chisq = gf.onedgaussfit(chancut, speccut, params=guess)
	print "~~~~~~~~~~~~~~~~\nFit parameters:\nBG height = ", round(params[0]), "\nCentroid = ", round(params[2],2), "\nAmp = ", round(params[1]), "\nFWHM = ", round(params[3]*2.35,2), "%\n~~~~~~~~~~~~~~~~"
    	print ('gausfits= ', params)
    	
    	plt.plot(chancut, model)
    	plt.xlim(LLD-100, ULD+100)


    return (params, model, gerrs, chisq, chancut, speccut)
def plot():
	fname=selectmca()

	f=open(fname,'r')
	print 'Opened ', fname
	for i, l in enumerate(f): pass
	filelen=i+1
	

	spec=np.genfromtxt(fname, skip_header=filelen-(mcalen+1), skip_footer=1)
	chan=np.arange(0,len(spec))
	plt.figure(1)
	plt.clf()
    	plt.plot(chan, spec)
	plt.title(fname)
	plt.xlabel('MCA Channel', fontsize=18)




	
	
	
	
	
	
