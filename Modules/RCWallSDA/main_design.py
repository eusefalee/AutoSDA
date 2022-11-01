"""
Created by: Muneera Aladsani - UCLA

Last edit: Oct 24 2022

"""

import pandas as pd
import os
from designWall import designWall14, designWall19
from createNonlinearfiles import createNLRHAfiles

# Define base directory
baseDirectory = os.getcwd()

#Read input file
inputfile = pd.read_excel(r"Input.xlsx") 

#Choose ACI 318 version (14 or 19)
aciVersion = 19

#Design the walls
if aciVersion == 14:
    designWall14(inputfile)
elif aciVersion == 19:
    designWall19(inputfile)

#Read design results file
designfile = pd.read_csv(r"Design Results.csv") 

#Create nonlinear analysis tcl files
createNLRHAfiles(inputfile,designfile)

