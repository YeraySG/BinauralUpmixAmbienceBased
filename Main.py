# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 18:29:47 2019

@author: u114293
Main
"""

from scipy.io import wavfile
import matplotlib.pyplot as plt

from STFTComputation import STFTComputation

samplerate,data = wavfile.read('speech-female_Stereo_Lowered.wav')#read the data from the audio file

plt.plot(data)

Left = data[:,0] # Left Channel
Right = data[:,1] # Right Channel

STFTComputation(Left,Right,samplerate)