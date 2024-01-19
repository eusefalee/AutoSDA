"""
Created by: Muneera Aladsani - UCLA

Last edit: Oct 24 2022

"""

import pandas as pd
import os
from designWall import designWall14, designWall19
from createNonlinearfiles import createNLRHAfiles
from pathlib import Path

# Define base directory
baseDirectory = os.getcwd()

def run_rcwallsda(IDs):

    for id in IDs:
        
        print("Design for Building ID = ", id)

        #Read input file
        inputfile = pd.read_excel(r"Input.xlsx") 

        # Overwrite building IDs text file?
        with open(Path(baseDirectory,'Nonlinear analysis','BuildingIDs.txt'),'w') as f:
            f.write(str(id))
            f.close()
        
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

        # Run Nonlinear Analysis
        os.chdir(baseDirectory + '\\Nonlinear analysis')
        os.system('OpenSees RunAnalysis.tcl')

if __name__ == "__main__":
    import sys
    id = int(sys.argv[1])
    print("Id is ",id)
    run_rcwallsda([id])