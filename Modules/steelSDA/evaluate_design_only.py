"""
This file is used to evaluate a given design.

Developed by GUAN, XINGQUAN @ UCLA, April 29 2021
"""

# Please add all the imported modules in the part below
import copy
import numpy as np
import os
import sys
import pandas as pd
import pathlib
import matplotlib.pyplot as plt

from building_information import Building
from elastic_analysis import ElasticAnalysis
from elastic_output import ElasticOutput
from response_spectrum_analysis import ResponseSpectrumAnalysis
from global_variables import steel
from global_variables import DESIGN_METHOD
from global_variables import PERMIT_DOUBLER_PLATE

from design_helper import create_column_set
from design_helper import create_beam_set
from design_helper import create_connection_set
from design_helper import save_all_design_results
from design_helper import store_miscellaneous_design_results
from design_helper import save_scaling_factor

##########################################################################
#                         Miscellaneous Input                            #
##########################################################################

building_id = 'C1-08-RCIV-5Bay-RSA'
base_directory = pathlib.Path('C:\\Users\\henry\\Desktop\\AutoSDA-ConventionalSMF')
PASS_ALL_CHECK = True
drift_limit = 0.015


##########################################################################
#                         Prepare the Evaluation                         #
##########################################################################

# Create an instance using "Building" class
building = Building(building_id, base_directory)

# Assign the member sizes from given files
os.chdir(building.directory['building data'])
member_sizes = pd.read_csv('TrialMemberSize.csv', header=0)
building.member_size['exterior column'] = list(member_sizes['exterior column'])
building.member_size['interior column'] = list(member_sizes['interior column'])
building.member_size['beam'] = list(member_sizes['beam'])
building.construction_size = copy.deepcopy(building.member_size)

# Perform the EigenValue Analysis only to obtain the period
_ = ElasticAnalysis(building, DESIGN_METHOD, analysis_load_type='EigenValue')
building.read_modal_period()

# Compute the seismic story forces based on modal period and CuTa
building.compute_seismic_force()

# Perform RSA-based design
if DESIGN_METHOD == 'RSA':
    RSA = ResponseSpectrumAnalysis(building)
if DESIGN_METHOD != 'RSA' and DESIGN_METHOD != 'ELF':
    sys.stderr.write("Wrong value for DESIGN_METHOD!")
    sys.stderr.write("Only 'RSA' or 'ELF' is allowed")
    sys.exit(10)

# Create an elastic analysis model for building instance above using "ElasticAnalysis" class
_ = ElasticAnalysis(building, DESIGN_METHOD, analysis_load_type='All')

# Read elastic analysis drift and force demands
if DESIGN_METHOD == 'ELF':
    building.read_story_drift()
    building.read_floor_displacement()
elastic_demand = ElasticOutput(building)

##########################################################################
#                         Check Story Drift                              #
##########################################################################

# Check story drift
if DESIGN_METHOD == 'ELF':
    # The ELF-based drift is stored in building class.
    drift_check = \
        (np.max(building.elastic_response['story drift']) * building.elf_parameters['Cd']
        > drift_limit / building.elf_parameters['rho'])
else:
    # The RSA-based drift is stored in RSA class.
    drift_check = np.max(RSA.final_RSA_responses['story drift']) > drift_limit / building.elf_parameters['rho']
    # Assign the RSA-based drift to building class
    building.elastic_response['story drift'] = RSA.final_RSA_responses['story drift']
    building.elastic_response['floor displacement'] = RSA.final_RSA_responses['floor displacement']

##########################################################################
#                         Check Column Strength                          #
##########################################################################

column_set, not_feasible_column = create_column_set(building, elastic_demand, steel)

##########################################################################
#                         Check Beam Strength                            #
##########################################################################

beam_set, not_feasible_beam = create_beam_set(building, elastic_demand, steel)

##########################################################################
#                         Check Connection Requirements                  #
##########################################################################

connection_set, not_feasible_connection = create_connection_set(building, column_set, beam_set, steel)

##########################################################################
#                         Compute Stability Coefficient                  #
##########################################################################
stability_coefficient = np.zeros([building.geometry['number of story'], 1])
for story in range(building.geometry['number of story']):
    if DESIGN_METHOD == 'ELF':
        drift = building.elastic_response['story drift'] * building.elf_parameters['Cd'] / building.elf_parameters['Ie']
    else:
        drift = RSA.final_RSA_responses['story drift']
    if story == 0:
        hsx = building.geometry['first story height']
        delta = drift[story] * building.geometry['first story height']
    else:
        hsx = building.geometry['typical story height']
        delta = drift[story] * building.geometry['typical story height']
    floor_area = building.geometry['number of X bay'] * building.geometry['X bay width'] \
                 * building.geometry['number of Z bay'] * building.geometry['Z bay width']
    dead_load = np.array(building.gravity_loads['floor dead load']) * floor_area / 1000  # unit: kips
    live_load = np.array(building.gravity_loads['floor live load']) * floor_area / 1000  # unit: kips
    Px = 1.0 * np.sum(dead_load[story:]) + 0.5 * np.sum(live_load[story:])
    if DESIGN_METHOD == 'ELF':
        Vx = building.seismic_force_for_strength['story shear'][story]
    else:
        Vx = RSA.final_RSA_responses['story shear'][story]
    stability_coefficient[story] = Px * delta * building.elf_parameters['Ie'] / Vx / hsx / building.elf_parameters['Cd']

stability_limit = np.ones([building.geometry['number of story'], 1]) * 0.5 / 1.0 / building.elf_parameters['Cd']

##########################################################################
#                         Display Evaluation Results                     #
##########################################################################

# Display the drift check results
print('-----------------------------------------')
if drift_check:
    PASS_ALL_CHECK = False
    print('Story drift is not satisfied:')
    if DESIGN_METHOD == 'ELF':
        print(building.elastic_response['story drift']*building.elf_parameters['Cd']*100)
    else:
        print(RSA.final_RSA_responses['story drift'])

# Display the column strength results
print('//////////////////////////////////////////')
for story, connection_no in not_feasible_column:
    PASS_ALL_CHECK = False
    print('Column in Story %i on Line %i has insufficient strength' % (story+1, connection_no))

# Display the beam strength results
print('******************************************')
for story, bay in not_feasible_beam:
    PASS_ALL_CHECK = False
    print('Beam in Floor %i on Bay %i has insufficient strength' % (story+1, bay))

# Display the connection results
print('++++++++++++++++++++++++++++++++++++++++++')
for story in range(building.geometry['number of story']):
    for connection_no in range(building.geometry['number of X bay']+1):
        if (not connection_set[story][connection_no].is_feasible['shear strength']) \
                or (not connection_set[story][connection_no].is_feasible['flexural strength']):
            PASS_ALL_CHECK = False
            print('Connection in Floor %i on Line %i is not OK because of beam' % (story+1, connection_no))
        if not connection_set[story][connection_no].is_feasible['SCWB']:
            PASS_ALL_CHECK = False
            print('Connection in Floor %i on Line %i is not OK because of SCWB: %f'
                  % (story+1, connection_no, connection_set[story][connection_no].moment['Mpc']
                     / connection_set[story][connection_no].moment['Mpb']))

# Display the constructability
for story in range(0, building.geometry['number of story']):
    for col_no in range(0, building.geometry['number of X bay']+1):
        if column_set[story][col_no].section['bf'] < beam_set[story][0].section['bf']:
            PASS_ALL_CHECK = False
            print('Column width in Story %i on Line %i is less than the corresponding beam' % (story+1, col_no))

if PASS_ALL_CHECK and (not PERMIT_DOUBLER_PLATE):
    # Display the doubler plate thickness
    for story in range(0, building.geometry['number of story']):
        for conn_no in range(0, building.geometry['number of X bay'] + 1):
            if connection_set[story][conn_no].doubler_plate_thickness > 0:
                print('Connection in Story %i on Line %i requires doubler plate' % (story+1, conn_no))
                print(connection_set[story][conn_no].shear_force['Ru'], connection_set[story][conn_no].shear_force['Rn'])


print('##############################################')
print('All evaluation results are displayed')


##########################################################################
#                         Store the Design Results                       #
##########################################################################

building_weight, _ = building.compute_steel_weight()

if PASS_ALL_CHECK or not PASS_ALL_CHECK:
    # Change the working directory to building data
    os.chdir(building.directory['building data'])

    # Save the steel weight
    np.savetxt('SteelWeight.txt', X=np.array([building_weight]), fmt='%.2f')


    # Save all design results.
    save_all_design_results(building, column_set, beam_set, connection_set, True)

    # Save all the rest results
    if DESIGN_METHOD == 'ELF':
        store_miscellaneous_design_results(stability_coefficient, list([building.elf_parameters['modal period']]),
                                           building.seismic_force_for_strength['story shear'],
                                           building.seismic_force_for_drift['story shear'],
                                           pd.DataFrame.from_dict(building.elf_parameters, orient='index'), DESIGN_METHOD)
    else:
        store_miscellaneous_design_results(stability_coefficient, RSA.modal_periods,
                                           building.seismic_force_for_strength['story shear'],
                                           building.seismic_force_for_drift['story shear'],
                                           pd.DataFrame.from_dict(building.elf_parameters, orient='index'), DESIGN_METHOD,
                                           RSA.final_RSA_responses['story shear'],
                                           RSA.final_RSA_responses['story shear'] / RSA.scaling_factors['force']
                                           * RSA.scaling_factors['drift'],
                                           RSA.modal_shapes)
        save_scaling_factor(RSA.scaling_factors['force'], RSA.scaling_factors['drift'])

    # Display the design drifts
    plt.figure(1)
    if DESIGN_METHOD == 'ELF':
        plt.plot(building.elastic_response['story drift'] * building.elf_parameters['Cd']*100,
                range(1, building.geometry['number of story']+1))
    else:
        plt.plot(RSA.final_RSA_responses['story drift']*100, range(1, building.geometry['number of story']+1))
        plt.xlim([0, 2.0])
    plt.ylim([1, building.geometry['number of story']])
    plt.xlabel('Design story drift (%)')
    plt.ylabel('Story level')
    plt.show()
    plt.savefig(DESIGN_METHOD + 'DesignDriftProfile.png')

    # Display the stability check results
    plt.figure(2)
    plt.plot(stability_coefficient, range(1, building.geometry['number of story']+1))
    plt.plot(stability_limit, range(1, building.geometry['number of story']+1))
    plt.xlabel('Stability coefficient')
    plt.ylabel('Story level')
    plt.show()
    plt.savefig(DESIGN_METHOD + 'StabilityCoefficientProfile.png')

# Go back to base directory
os.chdir(base_directory)

# Display the finalized results
if PASS_ALL_CHECK:
    print("Design Passed All Checks.")
else:
    print("Design Failed to Meet Codes!!!")