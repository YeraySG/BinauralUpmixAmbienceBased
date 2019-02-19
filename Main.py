# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 18:29:47 2019

Main file used to call the functions to run the code

@author: u114293
"""

import matplotlib.pyplot as plt
from Functions import readwav, STFTcomputation, AutoCorr, CrossCorr, CrossCorrCoeff, AlphaCom, EqualRatios,CheckZeroes,CnstPwrPanning

Xl,Xr,Samplerate= readwav('speech-female_Stereo_Lowered.wav')

# Check for zeroes

NewXl=CheckZeroes (Xl)
NewXr=CheckZeroes (Xr)

#0 in NewXl
#0 in NewXr


plt.plot(Xl, label='Left Chanel Signal')
plt.plot(Xr, label='Right Chanel Signal')
plt.title('Input signal')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

#Panning

PXl,PXr = CnstPwrPanning(NewXl,NewXr,45)


#STFT and Correlation

STFTXl, STFTXr = STFTcomputation(Xl,Xr,Samplerate)

Rll = AutoCorr (STFTXl,0.7)
Rrr = AutoCorr (STFTXr,0.7)

CrossCorrLR = CrossCorr (Rll,Rrr,0.7)
CCCoefficient = CrossCorrCoeff (CrossCorrLR,Rll,Rrr)




#Equal Ratios of Ambience

AlphaC = AlphaCom (CCCoefficient)

AmbienceL = EqualRatios(AlphaC,STFTXl)
AmbienceR = EqualRatios(AlphaC,STFTXr)

