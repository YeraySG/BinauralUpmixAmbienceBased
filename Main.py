# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 18:29:47 2019

Main file used to call the functions to run the code

@author: u114293
"""

import matplotlib.pyplot as plt
from Functions import readwav, STFTcomputation,InverseSTFT, AutoCorr, CrossCorr, CrossCorrCoeff, AlphaCom, EqualRatios,CheckZeros,CnstPwrPanning,Audiowrite

Xl,Xr,Samplerate= readwav('speech-female_Stereo_Lowered.wav')

# Check for zeroes

NewXl=CheckZeros (Xl)
NewXr=CheckZeros (Xr)

#0 in NewXl
#0 in NewXr

plt.plot(NewXl, label='Left Chanel Signal')
plt.plot(NewXr, label='Right Chanel Signal')
plt.title('Input signal')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

#Panning

PXl,PXr = CnstPwrPanning(NewXl,NewXr,45)
IPXl,IPXr = InverseSTFT(PXl,PXr,Samplerate)
Paudio = Audiowrite(PXl,PXr,Samplerate)

#Pannedaudio =sf.write()

#STFT and Correlation

STFTXl, STFTXr = STFTcomputation(NewXl,NewXr,Samplerate)

Rll = AutoCorr (STFTXl,0.7)
Rrr = AutoCorr (STFTXr,0.7)

CrossCorrLR = CrossCorr (Rll,Rrr,0.7)
CCCoefficient = CrossCorrCoeff (CrossCorrLR,Rll,Rrr)


#Equal Ratios of Ambience

AlphaC = AlphaCom (CCCoefficient)

AmbienceL = EqualRatios(AlphaC,STFTXl)
AmbienceR = EqualRatios(AlphaC,STFTXr)

