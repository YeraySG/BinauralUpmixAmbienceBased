# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 11:39:17 2019

@author: u114293
"""
def STFTcomputation (Xl,Xr,samplerate)

STFTdataXl  = sp.stft(Xl,samplerate,'hann',256)
STFTdataXr  = sp.stft(Xr,samplerate,'hann',256)

test = STFTdataXl[2]

timesXl = STFTdataXl[1]
timesXr = STFTdataXr[1]

STFTXl = STFTdataXl[2]
STFTXr = STFTdataXr[2]


ForgettingFactor = 0.7

for t in timesXl:
    rLL = np.empty( len(STFTXl[1]))
    xl = STFTXl[129,t]
    rLL = ForgettingFactor*rLL(t-1) + (1-ForgettingFactor)*(STFTXl(t).conj()*STFTXl(t))