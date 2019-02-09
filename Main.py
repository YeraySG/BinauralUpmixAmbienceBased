# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 18:29:47 2019

Main file used to call the functions to run the code

@author: u114293
"""

import matplotlib.pyplot as plt
from Functions import readwav, STFTcomputation, AutoCorr, CrossCorr, CrossCorrCoeff

Xl,Xr,Samplerate= readwav('speech-female_Stereo_Lowered.wav')

#plt.plot(Xl)
#plt.plot(Xr)
#plt.show()

STFTXl, STFTXr = STFTcomputation(Xl,Xr,Samplerate)

Rll = AutoCorr (STFTXl,0.7)
Rrr = AutoCorr (STFTXr,0.7)

CrossCorrLR = CrossCorr (Rll,Rrr,0.7)
CCCoefficient = CrossCorrCoeff (CrossCorrLR,Rll,Rrr,0.7)