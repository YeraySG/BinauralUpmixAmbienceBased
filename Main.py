# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 18:29:47 2019

Main file used to call the functions to run the code

@author: u114293
"""

import matplotlib.pyplot as plt
from Functions import readwav, STFTcomputation,InverseSTFT, AutoCorr, CrossCorr, CrossCorrCoeff, AlphaCom, EqualRatios,AddNoise,CnstPwrPanning,Audiowrite
import numpy as np

#Xl,Xr,Samplerate= readwav('speech-female_Stereo_Lowered.wav')
Xl,Xr,Samplerate= readwav('Hi_Izuru_Style.wav')

'Check for zeros'

NewXl = AddNoise (Xl)
NewXr = AddNoise (Xr)

plt.figure()
plt.plot(NewXl, label='Left Chanel Signal')
plt.plot(NewXr, label='Right Chanel Signal')
plt.title('Input signal')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

'Panning'
#PAudio,PXl,PXr = CnstPwrPanning(NewXl,0)
#
#
#plt.figure()
#plt.plot(PXr, label='Panned Right Chanel Signal')
#plt.plot(PXl, label='Panned Left Chanel Signal')
#plt.title('Panned signal')
#plt.xlabel('Samples')
#plt.ylabel('Amplitude')
#plt.legend()
#plt.show()

#PannedAudio = Audiowrite(PXr,PXl,Samplerate,'PannedAudio_45.wav')

'STFT and Correlation'

#STFTXl, STFTXr = STFTcomputation(PXl,PXr,Samplerate)
STFTXl, STFTXr = STFTcomputation(NewXl,NewXr,Samplerate)

Rll = AutoCorr (STFTXl,0.7)
Rrr = AutoCorr (STFTXr,0.7)

CrossCorrLR = CrossCorr (STFTXl,STFTXr,0.7)
CCCoefficient = CrossCorrCoeff (CrossCorrLR,Rll,Rrr)


'Equal Ratios of Ambience'

AlphaC = AlphaCom (CCCoefficient)
#np.min(AlphaC)
#np.max(AlphaC)

AmbienceL,DirectL = EqualRatios(AlphaC,STFTXl)
AmbienceR,DirectR = EqualRatios(AlphaC,STFTXr)

#plt.figure(),plt.pcolormesh(np.power(np.abs(AmbienceL),2)),plt.colorbar(),plt.show()
#plt.figure(),plt.pcolormesh(np.power(np.abs(AmbienceR),2)),plt.colorbar(),plt.show()
#plt.figure(),plt.pcolormesh(np.power(np.abs(DirectL),2)),plt.colorbar(),plt.show()
#plt.figure(),plt.pcolormesh(np.power(np.abs(DirectR),2)),plt.colorbar(),plt.show()

IAmbienceL,IAmbienceR = InverseSTFT(AmbienceL,AmbienceR,Samplerate)
IDirectL,IDirectR = InverseSTFT(DirectL,DirectR,Samplerate)

Ambience = Audiowrite(IAmbienceL[1],IAmbienceR[1],Samplerate,'AmbienceHi_Izuru_Style.wav')
Direct = Audiowrite(IDirectL[1],IDirectR[1],Samplerate,'DirectHi_Izuru_Style.wav')

#DirectL = (1-AlphaC)*np.abs(STFTXl)
#DirectR = (1-AlphaC)*np.abs(STFTXr)

plt.figure(),plt.pcolormesh(np.power(np.abs(AmbienceL),2)),plt.colorbar(),plt.show()