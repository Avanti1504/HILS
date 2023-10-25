import random
import subprocess
import numpy
import os

# Define thetarget outputs
desired_outputs= numpy.loadtxt("D:\Avanti\SSP\Parameter_tuning\ORION\output.txt", dtype=float)
# Reshape the array to have the desired shape of 100x4
desired_outputs= desired_outputs.reshape(100, 4)

# Print the array
#print(desired_outputs)
# Define thetarget outputs
outputs= numpy.loadtxt("D:\Avanti\SSP\Parameter_tuning\ORION\out_1.txt", dtype=float)
# Reshape the array to have the desired shape of 100x4
outputs= desired_outputs.reshape(100, 4)
# Print the array
#print(outputs)
mismatch=0
for i in range(0, 99):
    matched=True;
    for j in range(0,3):
        if desired_outputs[i][j]!=outputs[i][j]:
            matched=False
    if matched==False:
        mismatch=mismatch+1
        print("mismatch")
        

       


        
