# This file is the main file that calls function to perform seismic design, nonlinear model generation and analysis

##########################################################################
#                       Relevant Publications                            #
##########################################################################

# Add relevant publications below
# [1]. Guan, X., Burton, H., and Thomas, S. (2020).
# “Python-based computational platform to automate seismic design,
# nonlinear structural model construction and analysis of steel moment
# resisting frames.” Engineering Structures.

import time
import os
import pandas as pd
import numpy as np
import pickle

from seismic_design import seismic_design

from global_variables import base_directory
from global_variables import OpenSeesPath
from global_variables import ACCELERATION_SPECTRUM
from global_variables import IDA_SCALES
from global_variables import GM_IDs
from model_generation import model_generation

from run_dynamic_analysis import run_dynamic_analysis_using_MP

from postprocess_nonlinear_analysis import PostprocessNonlinearAnalysis

from help_functions import compute_SaMCE_scaling_factor


def run_AutoSDA(IDs):
    # Count the starting time of the main program
    start_time = time.time()

    # IDs = [570]
    # IDs = [1]
    for id in IDs:
        # *********************** Design Starts Here *************************
        building_id = 'Building_' + str(id)
        print("Design for Building ID = ", id)
        seismic_design(building_id, base_directory)

        # ******************* Nonlinear Model Generation Starts Here ******
        print("Model generation for Building ID = ", id)
        model_generation(building_id, base_directory)

        # ******************* Perform Eigen Value Analysis ****************
        print('Eigen Value Analysis for Building ID = : ', id)
        analysis_type = 'EigenValueAnalysis'
        target_model = base_directory / 'BuildingNonlinearModels' / building_id / analysis_type
        os.chdir(target_model)
        # os.system('C:\\OpenSees\\bin\\OpenSees Model.tcl')
        os.system(OpenSeesPath + ' Model.tcl')

        # # ******************* Perform Nonlinear Pushover Analysis *********
        print('Pushover Analysis for Building ID = : ', id)
        analysis_type = 'PushoverAnalysis'
        target_model = base_directory / 'BuildingNonlinearModels' / building_id / analysis_type
        os.chdir(target_model)
        os.system(OpenSeesPath + ' Model.tcl')

        # # *************** Perform Dynamic Analysis using OpenSeesMP *********
        # SaMCE_factor = compute_SaMCE_scaling_factor(building.elf_parameters['SaMCE'],
        #                                             building.elf_parameters['period'], ACCELERATION_SPECTRUM)
        # # Store this SaMCE factor into building data folder
        # os.chdir(base_directory / 'BuildingData' / building_id)
        # np.savetxt('SaMCEFactor.txt', np.array([SaMCE_factor]), fmt='%.5f')
        # # Run dynamic analysis using OpenSeesMP
        # run_dynamic_analysis_using_MP(base_directory, IDA_SCALES, building_id, SaMCE_factor, number_of_core=14)

        # # *************** Postprocess Dynamic Analysis Results (EDPs) *********
        # SaMCE_factor = compute_SaMCE_scaling_factor(building.elf_parameters['SaMCE'],
        #                                             building.elf_parameters['period'], ACCELERATION_SPECTRUM)
        # postprocess_results = PostprocessNonlinearAnalysis(building.directory['building nonlinear model'],
        #                                                     building.directory['building data'],
        #                                                     building.geometry['number of story'],
        #                                                     GM_IDs, IDA_SCALES, building.elf_parameters['SaMCE'],
        #                                                     SaMCE_factor, building.elf_parameters['approximate period'])
        # steel_weight = building.compute_steel_weight()
        # # Store the results into building data folder
        # os.chdir(building.directory['building data'])
        # np.savetxt('SteelWeight.txt', np.array([steel_weight]))
        # np.savetxt('ACMR.txt', np.array([postprocess_results.performance_metrics['ACMR']]))
        # with open('nonlinear_analysis_results.pkl', 'wb') as output_file:
        #     pickle.dump(postprocess_results, output_file)

    print("The design, model construction, and analysis for Building ID = %i at has been accomplished." % id)

    end_time = time.time()
    print("Running time is: %s seconds" % round(end_time - start_time, 2))
