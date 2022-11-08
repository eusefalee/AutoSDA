"""
Automated Seismic Deisgn and Analysis Platform (AutoSDA)

Developed as an interface between steelSDA (previously AutoSDA), woodSDA, and RCWall-SDA

Written By: Eusef Abdelmalek-Lee

Date Modified: 11/08/2022
"""


import pandas as pd
from help_functions import *
import multiprocessing as mp


########## OPTIONAL USER INPUTS #############

# Specify numer of processors to use
# To use the total number of processors on your machine use numProcessors = mp.cpu_count()
numProcessors = mp.cpu_count()

# Clean the module subdirectories after running a building. The output files
# for each building are copied to the "Outputs" folder in the top-level, so the subdirectory 
# files are usually not necessary. 
cleanSubdirectories = "yes" # "yes" or "no"

############ END USER INPUTS ################


# Read building list
inputs = pd.read_csv('runList.csv')

# Function to execute the program for the buildings specified in the runList file
def AutoSDA_main(id):

    # Make sure working in the top level directory
    os.chdir(topLevelDirectory)
    
    # Get current building
    currentBuilding = inputs.loc[inputs['BuildingID'] == id]

    print(currentBuilding)

    # Lookup location based parameters SS,S1, and TL
    seismsicLocParams = onlineParamLookup(
        currentBuilding['Latitude'].item(),
        currentBuilding['Longitude'].item(),
        currentBuilding['Site Class'].item(),
        currentBuilding['Risk Category'].item()
    )

    # Lookup non-location based parameters Cd, rho, Ct, R, Ie, and x
    seismicNonlocParams = nonLocParamLookup(
        currentBuilding['LFRS'].item(),
        currentBuilding['Risk Category'].item()
    )

    # Combine seismic parameters
    seismicParams = pd.concat(
        [seismsicLocParams, seismicNonlocParams],
        ignore_index=True
        )
    # Create necessary building files and subdirectories
    writeFiles(currentBuilding,seismicParams)

    # Run design and analysis for current building
    runSDA(currentBuilding['LFRS'].item(),id)

    # Get current building results and add to Outputs folder
    getOutputs(currentBuilding['LFRS'].item(),id)

    print("Building_",id," Completed!")


if __name__ == "__main__":

    # Create multiprocessing pool
    pool = mp.Pool(numProcessors)
    for building in inputs.BuildingID.values:

        # Runs the building design/analysis in parallel, outputting the results
        # for the buildings as they are performed
        pool.apply_async(AutoSDA_main,args=(building,))
    
    pool.close()
    pool.join()


# Clean BuildingInfo directories in submodules
