# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 11:39:17 2019

File to create and define all the functions used for the implementation of the paper

@author: u114293
"""
import scipy.signal as sp
import numpy as np
import soundfile as sf

def readwav (name): 
    
    data,samplerate = sf.read(name)#read the data from the audio file and extracts the samplerate
    Xl = data[:,0] # Left Channel
    Xr = data[:,1] # Right Channel
    return Xl,Xr,samplerate

def STFTcomputation (Xl,Xr,samplerate):

    STFTdataXl  = sp.stft(Xl,samplerate,'hann',256)
    STFTdataXr  = sp.stft(Xr,samplerate,'hann',256)

    timesXl = STFTdataXl[1]
    timesXr = STFTdataXr[1]
    
    STFTXl = STFTdataXl[2]
    STFTXr = STFTdataXr[2]
    
    return STFTXl,STFTXr

def InverseSTFT (Xl,Xr,Fs):
    
    IXl = sp.istft(Xl,Fs,'hann',256)
    IXr = sp.istft(Xr,Fs,'hann',256)
    
    return IXl, IXr

def CnstPwrPanning (signal,angle): #Pan a stereo signal to a given angle using the Constant Power Panning formula
    """
    The angle value should be between -pi/2 and pi/2
    """
#    if (angle > 45) or (angle < -45):
#        print ('Insert a value between +- 45º')
    if angle ==-45:
        PXl = signal*1.0
        PXr = signal*6.123233995736766e-17
        
        PAudio = np.zeros((np.size(signal),2))
        PAudio [:,0] = PXl
        PAudio [:,1] = PXr
    
        return PAudio,PXl,PXr
    else:
        rad = ((45+angle)*np.pi)/180
        
        PXl = signal*np.cos(rad)
        PXr = signal*np.sin(rad)
        
        PAudio = np.zeros((np.size(signal),2))
        PAudio [:,0] = PXl
        PAudio [:,1] = PXr
    
        return PAudio,PXl,PXr

def Audiowrite(Xl,Xr,Fs,name):
    
    C=2
    S=np.size(Xl)
    data = np.zeros((S,C))
    data [:,0] = Xl[:]
    data [:,1] = Xr[:]    
    sf.write(name,data,Fs)        
    return data
            

def AddNoise (signal): #Checks for the value 0 and adds an unnoticeable value
    
    noise = np.random.normal(1e-100,1e-50,np.size(signal)) # 0 is the mean of the normal distribution, 1 is the std. deviation of the normal distribution, np.size() is the number of elements in the noise
    data = signal+noise 
    return data

def AutoCorr (Xdata,FF): #Xl is STFTXL
    
    W,R =np.shape(Xdata) # Get the values of the time and frequency from the axis 
    AC = np.zeros( (W,R),dtype='complex') # Create a matrix of the same size as the STFT of the data
    for t in range (1,R):
        for f in range(W):
            AC [f,t]= np.power(np.abs(Xdata[f,t]),2) #Since the value is complex the abs is equal to the norm
            AC_last = FF*AC[f,t-1]
            AC_now = (1-FF)*AC[f,t]
            AC [f,t] = AC_last + AC_now
    for f in range(W): # Special case for t-1, which is non existing
            AC [f,0]= np.power(np.abs(Xdata[f,0]),2) 
            AC_last = 0
            AC_now = (1-FF)*AC[f,t]
            AC [f,0] = AC_last + AC_now
    return AC

def CrossCorr (Xl,Xr,FF): #Xl is STFTXL
    
    W,R =np.shape(Xl) # Get the values of the time and frequency from the axis 
    Cc = np.zeros( (W,R), dtype='complex') # Create a matrix of the same size as the STFT of the data
    for t in range (1,R):
        for f in range(W):
            Cc [f,t]= Xl[f,t]*np.conj(Xr[f,t]) #Since the value is complex the abs is equal to the norm
            Cc_last = FF*Cc[f,t-1]
            Cc_now = (1-FF)*Cc[f,t] #Is the same as-> Cc_now = (1-FF)*Xl[f,t]*np.conj(Xr[f,t]), as seen in the eq. 34
            Cc [f,t] = Cc_last + Cc_now
    for f in range(W): # Special case for t-1, which is non existing
            Cc [f,0]= Xl[f,0]*np.conj(Xr[f,0]) 
            Cc_last = 0
            Cc_now = (1-FF)*Cc[f,t]
            Cc [f,0] = Cc_last + Cc_now
    return Cc

def CrossCorrCoeff (Cc,AL,AR):
   
    W,R =np.shape(Cc) # Get the values of the time and frequency from the axis 
    CCCoeff = np.zeros( (W,R), dtype='complex') # Create a matrix of the same size as the STFT of the data
    for t in range (R):
        for f in range(W):
            CCCoeff [f,t]= Cc[f,t]/np.sqrt((AL[f,t])*(AR[f,t])) #Since the value is complex the abs is equal to the norm
    return CCCoeff

def AlphaCom (CCCoeff):
    
    AlphaCom = np.sqrt((1-np.abs(CCCoeff)))
    return AlphaCom

def EqualRatios (AlphaCom,Xdata):
    
    AmbienceER = Xdata*AlphaCom
    InvMask = 1-AlphaCom
    PrimaryER = Xdata*InvMask
    return AmbienceER,PrimaryER

def AmbienceEqualLevels (Rll,Rrr,Rlr):
    
    Squared = np.sqrt(np.power(Rll-Rrr,2)+(4*(np.power(np.abs(Rlr),2))))
    Plus = Rll+Rrr
    Iaa = 0.5*(Plus-Squared)
    Ia = np.sqrt(Iaa)
    return Ia

def EqLevelMask(Ia, Rxx):
    Mask = Ia / np.sqrt(Rxx)
    return Mask

def EqualLevels(Mask,Xdata):
    
    AmbienceEL = Xdata*Mask
    InverseMask = 1 - Mask
    PrimaryEL = Xdata*InverseMask
    return AmbienceEL,PrimaryEL