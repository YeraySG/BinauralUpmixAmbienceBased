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

def InverseSTFT (Xl,Xr,samplerate):
    IXl = sp.istft(Xl,samplerate,'hann',256)
    IXr = sp.istft(Xr,samplerate,'hann',256)
    
    
    return IXl, IXr

def CnstPwrPanning (Xl,Xr,angle): #Pan a stereo signal to a given angle using the Constant Power Panning formula
    """
    The angle value should be between -pi/2 and pi/2
    """
    if (angle > 45) or (angle < -45):
        print ('Insert a value of angle between +- 45º')
    else:
        rad = (angle*np.pi)/180
        
        PXl = Xl*np.cos(rad)
        PXr = Xr*np.sin(rad)
    
    return PXl,PXr

def Audiowrite(Xl,Xr,Fs):
    C=2
    S=np.size(Xl)
    data = np.zeros((S,C))
    for c in range (C):
        if c == 0:
            for s in range (S):
                data [c,s] = Xl[c,s]
        else:
            data[c,s] = Xr[c,s]
            
    return data
            

def CheckZeros (signal): #Checks for the value 0 and adds an unnoticeable value
    
    C = np.size(signal)
    for counter in range(C):
        if (signal[counter] == 0.0):
            signal[counter] = 10**-5
        else:
            signal[counter] = signal[counter]
    return signal

def AutoCorr (Xdata,FF): #Xl is STFTXL
    W,R =np.shape(Xdata) # Get the values of the time and frequency from the axis 
    AC = np.zeros( (W,R)) # Create a matrix of the same size as the STFT of the data
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
    Cc = np.zeros( (W,R)) # Create a matrix of the same size as the STFT of the data
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
    CCCoeff = np.zeros( (W,R)) # Create a matrix of the same size as the STFT of the data
    for t in range (1,R):
        for f in range(W):
            CCCoeff [f,t]= Cc[f,t]/(np.abs(AL[f,t])*np.abs(AR[f,t])) #Since the value is complex the abs is equal to the norm
#            CCCoeff_last = FF*CCCoeff[f,t-1]
#            CCCoeff_now = (1-FF)*CCCoeff[f,t] 
#            CCCoeff [f,t] = CCCoeff_last + CCCoeff_now
    for f in range(W): # Special case for t-1, which is non existing
            CCCoeff [f,0]= Cc[f,0]/(np.abs(AL[f,0])*np.abs(AR[f,0]))
#            CCCoeff_last = 0
#            CCCoeff_now = (1-FF)*CCCoeff[f,t]
#            CCCoeff [f,0] = CCCoeff_last + CCCoeff_now
    
    return CCCoeff

def AlphaCom (CCCoeff):
#    W,R = np.shape(CCCoeff)
#    AlphaCom = np.zeros((W,R))
#    #Ones = np.ones((W,R))
#    for t in range (R):
#        for f in range (W):
    AlphaCom = np.sqrt((1-CCCoeff))
            #AlphaCom [f,t] = np.sqrt((Ones[f,t]-CCCoeff[f,t]))
    return AlphaCom

def EqualRatios (AlphaCom,Xdata):
#    W,R = np.shape(Xdata)
#    Ambience = np.zeros((W,R))
#    for t in range (R):
#        for f in range (W):
    Ambience = np.abs(Xdata)*AlphaCom
    return Ambience

