# This file is used to extract EDPs from OpenSees dynamic results
# It will be executed on Hoffman cluster directly
# This file should be put at the directory where a bunch of building models are stored.

# Import necessary packages
import os
import numpy as np
import pandas as pd

from ExtractEDPsOnCluster import extract_peak_story_drift
from ExtractEDPsOnCluster import extract_residual_story_drift
from ExtractEDPsOnCluster import extract_peak_acceleration

from ExtractEDPsOnCluster import extract_peak_roof_drift

# Define the directory where the program starts
base_directory = os.getcwd()

# Define building and GM information
number_GM = 40

# Read the environmental variables
seed = int(os.getenv('SGE_TASK_ID'))

# Read the building IDs for current batch of buildings
os.chdir(base_directory)
IDs = list(np.loadtxt('BuildingIDs.txt'))
STORY = list(np.loadtxt('BuildingStories.txt'))

# Define building ID based on environmental variables
building_ID = int(IDs[seed-1])
number_story = int(STORY[seed-1])

# Define the building directory for each building model
building_directory = base_directory + '/Building_' + str(building_ID)

# Define the target directory where all EDPs are stored
target_directory = '/u/flashscratch/g/guanxing/GUANResults'

# Run the user-defined functions to obtain the PSDR, PFA, RSD.
os.chdir(base_directory)
peak_story_drift = extract_peak_story_drift(building_directory, building_ID, number_story, number_GM)
os.chdir(base_directory)
residual_drift = extract_residual_story_drift(building_directory, building_ID, number_story, number_GM)
os.chdir(base_directory)
peak_floor_acceleration = extract_peak_acceleration(building_directory, building_ID, number_story, number_GM)

# ******************************* Added by GUAN in Version 2 ***************************************
# Run the user-defined functions to obtain the PRDR.
os.chdir(base_directory)
peak_roof_drift = extract_peak_roof_drift(building_directory, building_ID, number_GM)
# ******************************* Revision End*****************************************************

# Define the headers for pandas dataframe
headers = []
for GM in range(1, number_GM + 1):
    name = 'GM' + str(GM)
    headers.append(name)
peak_story_drift_dataframe = pd.DataFrame(peak_story_drift, columns=headers)
residual_drift_dataframe = pd.DataFrame(residual_drift, columns=headers)
peak_floor_acceleration_dataframe = pd.DataFrame(peak_floor_acceleration, columns=headers)

# ******************************** Added by GUAN in Version 2 ************************************
peak_roof_drift_dataframe = pd.DataFrame(peak_roof_drift, columns=headers)
# ******************************** Revision End **************************************************

# Store postprocessing resutls in target directory
file_name1 = 'Building_' + str(building_ID) + '_PSDR.csv' 
file_name2 = 'Building_' + str(building_ID) + '_RSDR.csv'
file_name3 = 'Building_' + str(building_ID) + '_PFA.csv'

# ******************************** Added by GUAN in Version 2 ************************************
file_name4 = 'Building_' + str(building_ID) + '_PRDR.csv'
# ******************************** Revision End **************************************************

os.chdir(target_directory + '/PeakStoryDrift')
peak_story_drift_dataframe.to_csv(file_name1, sep=',', index=False)
os.chdir(target_directory + '/ResidualStoryDrift')
residual_drift_dataframe.to_csv(file_name2, sep=',', index=False)
os.chdir(target_directory + '/PeakFloorAcceleration')
peak_floor_acceleration_dataframe.to_csv(file_name3, sep=',', index=False)
os.chdir(target_directory + '/PeakRoofDrift')
peak_roof_drift_dataframe.to_csv(file_name4, sep=',', index=False)