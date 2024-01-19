# This file is the main file that calls function to perform seismic design
# Users need to specify the system argument in this file.
# Users also need to specify the variables in "global_variables.py"

# The reason why I create this "redundant" file is to perform seismic
# design for a bunch of buildings (not a single one)

##########################################################################
#                       Relevant Publications                            #
##########################################################################

# Add relevant publications below

##########################################################################
#                       Load Necessary Packages                          #
##########################################################################

import time
import numpy as np
import os

from seismic_design import seismic_design
from global_variables import base_directory
from global_variables import ACCELERATION_SPECTRUM

from help_functions import compute_SaMCE_scaling_factor

# Count the starting time of the main program
start_time = time.time()

# ********************* Revised for Using System Argument ****************
# start_id = sys.argv[1]
# end_id = sys.argv[2]
# step_id = sys.argv[3]
# for id in range(int(start_id), int(end_id), int(step_id)):
#     building_id = 'Building_' + str(id)
#     print("Design for building ID = ", building_id)
#     seismic_design(building_id, base_directory)
# ********************* Revision Ends Here *******************************

# ********************* Single Building Case Ends Here *******************
IDs = [1]
for id in IDs:
    building_id = 'Test' + str(id)
    print("Design for Building ID = ", building_id)
    opt_building, con_building_ = seismic_design(building_id, base_directory)

    # Save some necessary results for later analysis
    SaMCE_factor_opt = compute_SaMCE_scaling_factor(opt_building.elf_parameters['SaMCE'],
                                                    opt_building.elf_parameters['approximate period'], ACCELERATION_SPECTRUM)
    SaMCE_factor_con = compute_SaMCE_scaling_factor(con_building_.elf_parameters['SaMCE'],
                                                    con_building_.elf_parameters['approximate period'], ACCELERATION_SPECTRUM)
    # Store this SaMCE factor into building data folder
    os.chdir(base_directory / 'BuildingData' / building_id)
    np.savetxt('OptimalSaMCEFactor.txt', np.array([SaMCE_factor_opt]), fmt='%.5f')
    np.savetxt('ConstructionSaMCEFactor.txt', np.array([SaMCE_factor_con]), fmt='%.5f')

    steel_weight_opt = opt_building.compute_steel_weight()
    steel_weight_con = con_building_.compute_steel_weight()
    # Store the results into building data folder
    os.chdir(opt_building.directory['building data'])
    np.savetxt('OptimalSteelWeight.txt', np.array([steel_weight_opt]))
    np.savetxt('ConstructionSteelWeight.txt', np.array([steel_weight_con]))

# ********************* Single Building Case Ends Here *******************

end_time = time.time()

print("Running time is: %s seconds" % round(end_time - start_time, 2))