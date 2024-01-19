# This file is used to define a function to call the OpenSeesMP for analysis
# Developed by GUAN, XINGQUAN @ UCLA in Sept. 2020.

import os
import shutil

from help_functions import convert_number_list_to_string

def run_dynamic_analysis_using_MP(base_directory, IDA_scales, building_id, SaMCE_factor, number_of_core):
    """
    This function is used to call the OpenSeesMP to run the nonlinear response history analysis
    :param base_directory: a string to specify the path to the folder where AutoSDA is stored
    :param IDA_scales: a list of numbers of specify the IDA scales in percent
    :param building_id: an integer to denote the building ID
    :param SaMCE_factor: a float to denote the factor that is used to anchor a set of ground motion to MCE level
    :param number_of_core: an integer to describe how many cores are used for OpenSeesMP
    :return: nothing is returned. Nonlinear analysis is performed
    """
    # Main .tcl file for dynamic analysis is located inside the base folder of BuildingNonlinearModels,
    # not in each building folder
    # Copy the main dynamic analysis .tcl file
    source_dir = base_directory / 'BaselineTclFiles' / 'NonlinearAnalysis'
    target_dir = base_directory / 'BuildingNonlinearModels'
    file_name = 'RunDynamicAnalysisUsingMP.tcl'
    shutil.copy(source_dir/file_name, target_dir/file_name)
    # Revise the IDA scales
    os.chdir(target_dir)
    with open('RunDynamicAnalysisUsingMP.tcl', 'r') as file:
        content = file.read()
    old_string = '**intensityScales**'
    new_string = convert_number_list_to_string(IDA_scales)
    new_content = content.replace(old_string, new_string)
    # Revise the model folder name for current building
    old_string = '**buildingID**'
    new_string = building_id
    new_content = new_content.replace(old_string, new_string)
    # Revise the SaMCE scaling factor
    old_string = '**SaMCEFactor**'
    new_string = str(SaMCE_factor)
    new_content = new_content.replace(old_string, new_string)

    #Revise Number of GMs
    countpath = target_dir / 'Histories'
    ngms = len([entry for entry in os.listdir(countpath) if os.path.isfile(os.path.join(countpath, entry))])
    old_string = '**nGMs**'
    new_string = str(ngms)
    new_content = new_content.replace(old_string,new_string)
    
    with open('RunDynamicAnalysisUsingMP.tcl', 'w') as file:
        file.write(new_content)
    # Run the dynamic analysis using OpenSeesMP (Change the number of cores that you need in the following line)
    command = '"C:\\Program Files\\MPICH2\\bin\\mpiexec" -n ' + str(number_of_core) \
              + ' OpenSeesMP.exe RunDynamicAnalysisUsingMP.tcl'
    os.system(command)