# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:53:51 2019

@author: Yeray
"""

from pysofaconventions import SOFAFile
import matplotlib.pyplot as plt
import scipy.signal as sp
import soundfile as sf
from Functions import readwav

path = 'C:\\Users\\Yeray\\Documents\\GitHub\\TFG\\SCUT_KEMAR_radius_1.sofa'
sofa = SOFAFile(path,'r')

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

HRTFMin30 = data[150,:,:]

HRTFMin110 = data[166,:,:]

HRTFPlus30 = data[210,:,:]

HRTFPlus110 = data[194,:,:]

plt.plot(HRTFMin30[0], label="left", linewidth=0.5,  marker='o', markersize=1)
plt.plot(HRTFMin30[1], label="right", linewidth=0.5,  marker='o', markersize=1)
plt.grid()
plt.legend()
plt.show()

dataxlMin30,dataxrMin30,samplerate = readwav('JungleFire-Jambú.wav')


binaural_leftMin30 = sp.convolve(dataxlMin30,HRTFMin30[0], mode='full', method='auto')[:len(dataxlMin30)]
binaural_rightMin30 = sp.convolve(dataxrMin30,HRTFMin30[1], mode='full', method='auto')[:len(dataxrMin30)]