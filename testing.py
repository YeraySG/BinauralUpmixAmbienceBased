# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 18:54:07 2019

@author: u114293
"""

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
AutoRight = np.linalg.norm(Xr,ord=2)**2 #Squared Norm of the Vector Xr  
#Cross = """"