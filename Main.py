# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 18:29:47 2019

Main file used to call the functions to run the code

@author: u114293
"""

import matplotlib.pyplot as plt
from Functions import readwav, STFTcomputation,InverseSTFT, AutoCorr, CrossCorr, CrossCorrCoeff, AlphaCom, EqualRatios,AddNoise,CnstPwrPanning,Audiowrite

Xl,Xr,Samplerate= readwav('speech-female_Stereo_Lowered.wav')

'Check for zeros'

NewXl = AddNoise (Xl)
NewXr = AddNoise (Xr)

#0 in NewXl
#0 in NewXr

plt.plot(NewXl, label='Left Chanel Signal')
plt.plot(NewXr, label='Right Chanel Signal')
plt.title('Input signal')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

'Panning'

PAudio,PXr,PXl = CnstPwrPanning(NewXl,45)

# IPXl,IPXr = InverseSTFT(PXl,PXr,Samplerate) # AQUI NO
PannedAudio = Audiowrite(PXr,PXl,Samplerate,'PannedAudio_45.wav')


'STFT and Correlation'

# STFTXl, STFTXr = STFTcomputation(NewXl,NewXr,Samplerate)
STFTXl, STFTXr = STFTcomputation(NewXl,NewXr,Samplerate)

Rll = AutoCorr (STFTXl,0.7)
Rrr = AutoCorr (STFTXr,0.7)

CrossCorrLR = CrossCorr (Rll,Rrr,0.7)
CCCoefficient = CrossCorrCoeff (CrossCorrLR,Rll,Rrr)


'Equal Ratios of Ambience'

AlphaC = AlphaCom (CCCoefficient)
#np.min(AlphaC)
#np.max(AlphaC)

AmbienceL = EqualRatios(AlphaC,STFTXl)
AmbienceR = EqualRatios(AlphaC,STFTXr)

# IAXl,IAXr = InverseSTFT(AmbienceL,AmbienceL,Samplerate) # AQUI SI
