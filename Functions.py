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

def AutoCorr (Xl,FF): #Xl is STFTXL
    W,R =np.shape(Xl) # Get the values of the time and frequency from the axis 
    AL = np.zeros( (W,R)) # Create a matrix of the same size as the STFT of the data
    for t in range (1,R):
        for f in range(W):
            AL [f,t]= np.power(np.abs(Xl[f,t]),2) #Since the value is complex the abs is equal to the norm
            AL_last = FF*AL[f,t-1]
            AL_now = (1-FF)*AL[f,t]
            AL [f,t] = AL_last + AL_now
    for f in range(W): # Special case for t-1, which is non existing
            AL [f,0]= np.power(np.abs(Xl[f,0]),2) 
            AL_last = 0
            AL_now = (1-FF)*AL[f,t]
            AL [f,0] = AL_last + AL_now
    return AL