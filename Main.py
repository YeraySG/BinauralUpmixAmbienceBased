# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 18:29:47 2019

Main file used to call the functions to run the code

@author: u114293
"""

import matplotlib.pyplot as plt
from Functions import readwav, STFTcomputation,InverseSTFT, AutoCorr, CrossCorr, CrossCorrCoeff, AlphaCom, EqualRatios,AddNoise,Audiowrite,AmbienceEqualLevels,EqLevelMask,EqualLevels
import numpy as np
import scipy.signal as sp
import time
start = time.time()

AmbiencePath = 'Specify a path where the Ambience of the Equal Ratios results will be stored, and the name of the file itself'#'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\AudioResults\\EqualRatios\\Ambience\\AmbienceFull - SeenRain.wav'
DirectPath = 'Specify a path where the Direct of the Equal Ratios results will be stored, and the name of the file itself' #'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\AudioResults\\EqualRatios\\Direct\\DirectFull - SeenRain.wav'
AmbienceElPath = 'Specify a path where the Ambience of the Equal Levels results will be stored, and the name of the file itself' #'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\AudioResults\\EqualLevels\\Ambience\\AmbienceELFull - SeenRain.wav'
DirectElPath = 'Specify a path where the Direct of the Equal Levels results will be stored, and the name of the file itself' #'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\AudioResults\\EqualLevels\\Direct\\DirectELFull - SeenRain.wav'
SongPath =  'Path to the audio file we will be using to test the algorithm '#'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\Music\\Boney M. - Have You Ever Seen The Rain.wav'
MusicPath = 'If we only use a small fraction of the original audio, this has to contain the path to the audio sample'#'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\Music\\SeenRainFull.wav'

#Xl,Xr,Samplerate= readwav('speech-female_Stereo_Lowered.wav')
# Xl,Xr,Samplerate= readwav('R&T.wav')
Xl,Xr,Samplerate= readwav(SongPath)
Xl = Xl[:40*Samplerate]
Xr = Xr[:40*Samplerate]

'Check for zeros' #Prevents us to encounter NaN problems along the way

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


'STFT and Correlation'

STFTXl, STFTXr = STFTcomputation(NewXl,NewXr,Samplerate) #Compute the STFT of both channels from the original file

Rll = AutoCorr (STFTXl,0.7) #Autocorrelation from the Left channel
Rrr = AutoCorr (STFTXr,0.7) #Autocorrelation from the Right channel

CrossCorrLR = CrossCorr (STFTXl,STFTXr,0.7) #Crosscorrelation from the channels
CCCoefficient = CrossCorrCoeff (CrossCorrLR,Rll,Rrr) #Crosscorrelation Coefficient


'Equal Ratios of Ambience'

AlphaC = AlphaCom (CCCoefficient) #Common mask
#np.min(AlphaC)
#np.max(AlphaC)

AmbienceL,DirectL = EqualRatios(AlphaC,STFTXl) #Results from the Left channel
AmbienceR,DirectR = EqualRatios(AlphaC,STFTXr) #Results from the Right channel

#plt.figure(),plt.pcolormesh(np.power(np.abs(AmbienceL),2)),plt.colorbar(),plt.show()
#plt.figure(),plt.pcolormesh(np.power(np.abs(AmbienceR),2)),plt.colorbar(),plt.show()
#plt.figure(),plt.pcolormesh(np.power(np.abs(DirectL),2)),plt.colorbar(),plt.show()
#plt.figure(),plt.pcolormesh(np.power(np.abs(DirectR),2)),plt.colorbar(),plt.show()

IAmbienceL,IAmbienceR = InverseSTFT(AmbienceL,AmbienceR,Samplerate) #Revert to time-domain
IDirectL,IDirectR = InverseSTFT(DirectL,DirectR,Samplerate)

Ambience = Audiowrite(IAmbienceL[1],IAmbienceR[1],Samplerate,AmbiencePath) #Store the final Ambience in one file
Direct = Audiowrite(IDirectL[1],IDirectR[1],Samplerate,DirectPath) #Store the final Direct in one file


#plt.figure(),plt.pcolormesh(np.power(np.abs(AmbienceL),2)),plt.colorbar(),plt.show()

'Equal Levels of Ambience'

Ia = AmbienceEqualLevels(Rll,Rrr,CrossCorrLR) #Compute the Ia value
MaskL = EqLevelMask(Ia,Rll) #Compute the mask value for the Left channel
MaskR = EqLevelMask(Ia,Rrr) #Compute the mask value for the Right channel

plt.figure(),plt.pcolormesh(np.power(np.abs(MaskL),2)),plt.colorbar(),plt.show()
plt.figure(),plt.pcolormesh(np.power(np.abs(MaskR),2)),plt.colorbar(),plt.show()


AmbienceElL, PrimaryElL = EqualLevels(MaskL,STFTXl) #Results from the Left channel
AmbienceElR, PrimaryElR = EqualLevels(MaskR,STFTXr) #Results from the Right channel

IAmbienceElL,IAmbienceElR = InverseSTFT(AmbienceElL,AmbienceElR,Samplerate) #Revert to time-domain
IPrimaryElL,IPrimaryElR = InverseSTFT(PrimaryElL,PrimaryElR,Samplerate)

AmbienceEl = Audiowrite(IAmbienceElL[1],IAmbienceElR[1],Samplerate,AmbienceElPath) #Store the final Ambience in one file
PrimaryEl = Audiowrite(IPrimaryElL[1],IPrimaryElR[1],Samplerate,DirectElPath) #Store the final Direct in one file

SongCut = Audiowrite(NewXl,NewXr,Samplerate,MusicPath) #If we use a fragment of the audio, store it so we can later use it
