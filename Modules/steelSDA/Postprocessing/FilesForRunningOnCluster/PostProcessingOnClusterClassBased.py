# This file is used to extract EDPs from OpenSees dynamic results
# It will be executed on Hoffman cluster directly
# This file should be put at the directory where a bunch of building models are stored.

# Import necessary packages
import os
import numpy as np
import pandas as pd
import pathlib

from ExtractEDPsOnCluster import PostprocessNonlinearAnalysis

prefix = 'ABuilding_'

# Define the directory where the program starts
base_directory = pathlib.Path(os.getcwd())

# Define GM information
number_GM = 44
GM_IDs = range(1, number_GM+1)
IDA_scales = [50, 100, 150, 200, 250]

# Read the environmental variables
seed = int(os.getenv('SGE_TASK_ID'))

# Read the building IDs for current batch of buildings
os.chdir(base_directory)
IDs = list(np.loadtxt('BuildingIDs.txt'))
STORY_LIST = list(np.loadtxt('Stories.txt'))
SaMCE_LIST = list(np.loadtxt('SaMCEs.txt'))

# Define building ID based on environmental variables
building_ID = int(IDs[seed-1])

# Define number of story based on environmental variables
number_story = int(STORY_LIST[seed-1])

# Define SaMCE based on environmental variables
SaMCE = SaMCE_LIST[seed-1]

# Define the building directory for each building model
building_directory = base_directory / (prefix + str(building_ID))

# Define the target directory where all EDPs are stored
data_directory = pathlib.Path('/u/flashscratch/g/guanxing/GUANResultsForR8')

# Call the defined class to perform the postprocessing task
postprocess_results = PostprocessNonlinearAnalysis(building_directory, data_directory, building_ID, number_story, GM_IDs, IDA_scales, SaMCE)