# -*- coding: utf-8 -*-
"""
Created on Mon May 13 20:19:02 2019

@author: Yeray
"""

from pysofaconventions import SOFAFile
import matplotlib.pyplot as plt
import scipy.signal as sp
import soundfile as sf
import numpy as np
from Functions import readwav

#path = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\SCUT_KEMAR_radius_1.sofa'
#path = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\subject_003.sofa'
#path = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\HRIR_CIRC360_NF100.sofa'
#HRIRpath = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\HRIR\\HRIR_CIRC360_NF025.sofa'
#HRIRpath = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\HRIR\\SCUT_KEMAR_radius_0.2.sofa'
HRIRpath = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\HRIR\\dtf b_nh821.sofa'

DirectPath = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\AudioResults\\EqualRatios\\Direct\\Direct - Dreams.wav'
AmbiencePath = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\AudioResults\\EqualRatios\\Ambience\\Ambience - Dreams.wav'
MusicPath = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\Music\\Fleetwood Mac - Dreams.wav'
ConvPath = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\Convolution\\RealHead\\5Sources\\5-Dreams-binaural.wav'

sofa = SOFAFile(HRIRpath,'r')

# File is actually not valid, but we can forgive them
print ("\n")
print ("File is valid:", sofa.isValid())

# Convention is SimpleFreeFieldHRIR
print ("\n")
print ("SOFA Convention:", sofa.getGlobalAttributeValue('SOFAConventions'))

# Let's see the dimensions:
#   - M: 1250 (different measurement positions)
#   - R: 2 (the two ears)
#   - E: 1 (one loudspeaker)
#   - N: 200 (lenght of the HRTFs in samples)
print ("\n")
print ("Dimensions:")
sofa.printSOFADimensions()

# Let's see the variables as well
print ("\n")
print ("Variables")
sofa.printSOFAVariables()

# Let's check the position of the measurementa (Source position)
sourcePositions = sofa.getVariableValue('SourcePosition')
print ("\n")
print ("Source Positions")
print (sourcePositions)
# and the info (units, coordinates)
print (sofa.getPositionVariableInfo('SourcePosition'))

# Let's inspect the first measurement
m = 0
print ("\n")
print ("Source Position of measurement " + str(m))
print (sourcePositions[m])
# which is at 82 degrees azimuth, -7 degrees elevation

# Read the data
data = sofa.getDataIR()
# and get the HRTF associated with m=0
hrtf = data[m,:,:]

# Let's check the dimensions of the hrtf
print ("\n")
print ("HRTF dimensions")
print (hrtf.shape)

'We use the variable sourcePositions to find the values of Elevation and Azimuth that we want'

#'Circ360'
#HRTF0 = data[0,:,:]
#
#HRTFMin30 = data[30,:,:]
#
#HRTFMin110 = data[110,:,:]
#
#HRTFPlus30 = data[330,:,:]
#
#HRTFPlus110 = data[250,:,:]

'KEMAR'
HRTF0 = data[144,:,:]

HRTFMin30 = data[150,:,:]

HRTFMin110 = data[194,:,:]

HRTFPlus30 = data[210,:,:]

HRTFPlus110 = data[166,:,:]

dataxl,dataxr,samplerate = readwav(MusicPath)

directxl,directxr,sampleratedirect = readwav(DirectPath)

'0'
plt.plot(HRTF0[0], label="left", linewidth=0.5,  marker='o', markersize=1)
plt.plot(HRTF0[1], label="right", linewidth=0.5,  marker='o', markersize=1)
plt.grid()
plt.legend()
plt.show()

binaural_left0 = sp.convolve(directxl,HRTF0[0], mode='full', method='auto')[:len(directxl)]
binaural_right0 = sp.convolve(directxr,HRTF0[1], mode='full', method='auto')[:len(directxr)]

binaural0 = np.asarray([binaural_left0, binaural_right0]).swapaxes(-1,0)

'30'
plt.plot(HRTFPlus30[0], label="left", linewidth=0.5,  marker='o', markersize=1)
plt.plot(HRTFPlus30[1], label="right", linewidth=0.5,  marker='o', markersize=1)
plt.grid()
plt.legend()
plt.show()

binaural_leftPlus30 = sp.convolve(dataxl,HRTFPlus30[0], mode='full', method='auto')[:len(dataxl)]
binaural_rightPlus30 = sp.convolve(dataxr,HRTFPlus30[1], mode='full', method='auto')[:len(dataxr)]

binauralPlus30 = np.asarray([binaural_leftPlus30, binaural_rightPlus30]).swapaxes(-1,0)
# Write to a file, and enjoy!

#sf.write('binauralPlus30.wav',binauralPlus30, samplerate)

'-30'
plt.plot(HRTFMin30[0], label="left", linewidth=0.5,  marker='o', markersize=1)
plt.plot(HRTFMin30[1], label="right", linewidth=0.5,  marker='o', markersize=1)
plt.grid()
plt.legend()
plt.show()

binaural_leftMin30 = sp.convolve(dataxl,HRTFMin30[0], mode='full', method='auto')[:len(dataxl)]
binaural_rightMin30 = sp.convolve(dataxr,HRTFMin30[1], mode='full', method='auto')[:len(dataxr)]

binauralMin30 = np.asarray([binaural_leftMin30, binaural_rightMin30]).swapaxes(-1,0)

#sf.write('binauralMin30.wav',binauralMin30, samplerate)

ambiencexl,ambiencexr,samplerateambience = readwav(AmbiencePath)

'110'
plt.plot(HRTFPlus110[0], label="left", linewidth=0.5,  marker='o', markersize=1)
plt.plot(HRTFPlus110[1], label="right", linewidth=0.5,  marker='o', markersize=1)
plt.grid()
plt.legend()
plt.show()

binaural_leftPlus110 = sp.convolve(ambiencexl,HRTFPlus110[0], mode='full', method='auto')[:len(ambiencexl)]
binaural_rightPlus110 = sp.convolve(ambiencexr,HRTFPlus110[1], mode='full', method='auto')[:len(ambiencexr)]

binauralPlus110 = np.asarray([binaural_leftPlus110, binaural_rightPlus110]).swapaxes(-1,0)

#sf.write('binauralPlus110.wav',binauralPlus110, samplerateambience)

'-110'
plt.plot(HRTFMin110[0], label="left", linewidth=0.5,  marker='o', markersize=1)
plt.plot(HRTFMin110[1], label="right", linewidth=0.5,  marker='o', markersize=1)
plt.grid()
plt.legend()
plt.show()

binaural_leftMin110 = sp.convolve(ambiencexl,HRTFMin110[0], mode='full', method='auto')[:len(ambiencexl)]
binaural_rightMin110 = sp.convolve(ambiencexr,HRTFMin110[1], mode='full', method='auto')[:len(ambiencexr)]

binauralMin110 = np.asarray([binaural_leftMin110, binaural_rightMin110]).swapaxes(-1,0)

#sf.write('binauralMin110.wav',binauralMin110, samplerateambience)

binaural = binaural0+binauralPlus30+binauralMin30+binauralPlus110+binauralMin110 /5
sf.write(ConvPath,binaural,samplerate)