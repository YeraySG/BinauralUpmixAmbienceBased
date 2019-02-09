# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 11:39:17 2019

@author: u114293
"""
import scipy.signal as sp
import numpy as np
from scipy.io import wavfile

def readwav (name): 
    samplerate,data = wavfile.read(name)#read the data from the audio file and extracts the samplerate
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