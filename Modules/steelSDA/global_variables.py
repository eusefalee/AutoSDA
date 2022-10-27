# This file is used to declare all global constants.
# All user input parameters are summarized here.
# Developed by GUAN, XINGQUAN @ UCLA in Feb 2019
# Be cautious with line 19 - 25:
# If a batch of building designs would be generated, using sys.argv.
# Otherwise, simply using a string to define building_id is sufficient.

import os
import pandas as pd
import pathlib

from steel_material import SteelMaterial

##########################################################################
#                  User Defined Model Folder and Directory               #
##########################################################################

# Variables defined in this section is used in "seismic_design.py" file

# Define the current utilized steel type:
steel = SteelMaterial(yield_stress=50, ultimate_stress=65, elastic_modulus=29000, Ry_value=1.1)  # Unit: ksi

# Define path to where ElasticAnalysis tool base directory
base_directory = pathlib.Path(os.getcwd())

# Define path to OpenSees
OpenSeesPath = os.path.join(base_directory,"..","..","OpenSees","bin","OpenSees")

##########################################################################
#            User Defined Ratios Involved in Design                      #
##########################################################################

# Variables defined in this section are used in "building_information.py" file
# Those variables are used to facilitate performing the design

# Ix ratio between exterior column and interior column
# EXTERIOR_INTERIOR_COLUMN_RATIO = 1.0
EXTERIOR_INTERIOR_COLUMN_RATIO = 0.70

# Zx ratio between beam and interior column
BEAM_TO_COLUMN_RATIO = 0.60  # Used when SCWB = 1.0
# BEAM_TO_COLUMN_RATIO = 0.33  # Used when SCWB = 1.5
# BEAM_TO_COLUMN_RATIO = 0.33  # Try this when SCWB = 2.0

# Define the number of stories that have identical member sizes
# when considering constructability
IDENTICAL_SIZE_PER_STORY = 2

# Define a number that describes a ratio between upper column Zx and lower column Zx
# When SCWB is not satisfied, we need to use ratio to determine whether we should upscale upper column or lower column.
UPPER_LOWER_COLUMN_Zx = 0.5

# Define a coefficient that describes the accidental torsion
# Imagine two special moment frames are symmetrically placed at the building perimeter
# and the floor plan of the building is a regular shape (rectangle)
# If the accidental torsion is not considered -> each frame is taken 0.5 of total lateral force
# Then the ACCIDENTAL_TORSION = 1.0
# If the accidental torsion is considered -> one frame will take 0.55 of total lateral force
# since the center is assumed to be deviated from its actual location by 5% of the building dimension
# Then the ACCIDENTAL_TORSION = 0.55/0.50 = 1.1
ACCIDENTAL_TORSION = 0.50/0.50

# Define a boolean variable to determine whether the Section 12.8.6.2 is enforced or not
# Section 12.8.6.2:
# For determining the design story drifts, it is permitted to determine the elastic drifts using
# seismic design force based on the computed fundamental period without the upper limit (CuTa).
# True -> Bound by upper limit, i.e., don't impose Section 12.8.6.2
# False -> Not bound by upper limit, i.e., impose Section 12.8.6.2 requirement
# Please note this period is only for computing drift, not for computing required strength.
PERIOD_FOR_DRIFT_LIMIT = False

# Define a scalar to denote the drift limit which is based on ASCE 7-16 Table 12.12-1
DRIFT_LIMIT = 0.02

# Defining a boolean variable to determine whether a doubler plate is required or not.
# True -> Installing doubler plate is allowed
# False -> Not permit to use doubler plate (which may result in no design solution)
PERMIT_DOUBLER_PLATE = True

# Use RBS-connection or non-RBS connection
# True -> use RBS connection
# False -> use non-RBS connection: e.g., WUF-W connection
ADOPT_RBS_CONNECTION = True

# Use RSA design or ELF design:
DESIGN_METHOD = 'ELF'

# Boundary condition for the column base
# Options: "PIN" vs. "FIX"
COLUMN_BASE = 'FIX'

# Gravity constant
GRAVITY_CONSTANT = 386.4

##########################################################################
#        User Defined Ratios Involved in Check Design                    #
##########################################################################

# Variables defined in this section is used in "connection_part.py" file.

# Declare global variables of strong column weak beam ratio for checking
STRONG_COLUMN_WEAK_BEAM_RATIO = 1.0
# STRONG_COLUMN_WEAK_BEAM_RATIO = float(sys.argv[4])

#
RBS_STIFFNESS_FACTOR = 1.0

if ADOPT_RBS_CONNECTION:
    BEAM_STIFFNESS_REDUCTION = 0.9
else:
    BEAM_STIFFNESS_REDUCTION = 1.0

# ********************************************* May 5, 2021 ************************************************************
# if ADOPT_RBS_CONNECTION:
#     # The RBS dimension "c" is selected as the maximum cut -> drift amplification factor = 1.1
#     RBS_STIFFNESS_FACTOR = 1.10
# else:
#     # If non-RBS connection is used, the drift amplification factor = 1.0.
#     RBS_STIFFNESS_FACTOR = 1.0
# ********************************************* May 5, 2021 Ends *******************************************************

# #########################################################################
#           Open the section database and store it as a global variable   #
# #########################################################################

# Global constant: SECTION_DATABASE (a panda dataframe read from .csv file) (All sizes)
SECTION_DATABASE = pd.read_csv('AllSectionDatabase.csv', header=0)

# Global constant: COLUMN_DATABASE (only contains the sizes that are feasible for columns)
COLUMN_DATABASE = pd.read_csv('ColumnDatabase.csv', header=0)

# Global constant: BEAM_DATABASE (only contains the sizes that are feasible for beams)
if ADOPT_RBS_CONNECTION:
    BEAM_DATABASE = pd.read_csv('BeamDatabase.csv', header=0)
else:
    BEAM_DATABASE = pd.read_csv('WUF-W-BeamDatabase.csv', header=0)
# #########################################################################
#           Various Constants used for Running Dynamic Analysis           #
# #########################################################################

# Global constant: ACCELERATION_SPECTRUM: 5% spectral acceleration for a set of ground motions
ACCELERATION_SPECTRUM = pd.read_csv('AccelerationSpcetra5Percent.csv', header=0)

# Global constant: used for specifying the IDA scales in RunDynamicAnalysisUsingMP.tcl file
# IDA_SCALES = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250]
IDA_SCALES = [100, 150, 200, 250]

# Define the IDs used for label the ground motions
GM_IDs = range(1, 44+1)