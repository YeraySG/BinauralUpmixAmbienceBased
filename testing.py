# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 18:54:07 2019

@author: u114293
"""
#import soundfile
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt


samplerate,data = wavfile.read('speech-female_Stereo_Lowered.wav')#read the data from the audio file

plt.plot(data)

Xl = data[:,0] # Left Channel
Xr = data[:,1] # Right Channel

plt.figure()
plt.plot(Xl)
plt.title('Left Channel')

plt.figure()
plt.plot(Xr)
plt.title('Right Channel')

AutoLeft = np.linalg.norm(Xl,ord=2)**2 #Squared Norm of the Vector Xl
#AutoLeft2 = np.sum(Xl.conj().T*Xl)
AutoLeft3 = np.sum(np.transpose(Xl)*Xl)

AutoRight = np.linalg.norm(Xr,ord=2)**2 #Squared Norm of the Vector Xr
#AutoRight2 = np.sum(Xr.conj().T*Xr)

Cross = Xl.conj().T*Xr  #conjugada traspuesta de Xl * Xr
CrossCoefficient = Cross/(np.linalg.norm(Xl)*np.linalg.norm(Xr)) #Cross Correlation Coefficient
#CrossCoefficient2 = Cross/np.sqrt(AutoLeft2*AutoRight2) 
Dif = sum (CrossCoefficient-CrossCoefficient2)