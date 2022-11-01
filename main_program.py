import pandas as pd
from help_functions import *

# Read building inputs
inputs = pd.read_csv('input.csv')

# Iterate over the buildings, calculating the parameters and writing
# into the corresponding ELF Parameters csv file
for id in inputs.BuildingID:
    
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

    # Combine seismic parameters and export to csv file
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


# Clean BuildingInfo directories in submodules
