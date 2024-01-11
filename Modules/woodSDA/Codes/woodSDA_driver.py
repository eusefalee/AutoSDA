import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os 
import re 
import sys
from distutils.dir_util import copy_tree

import subprocess
import json

import subprocess
import time
from pathlib import Path

cd = os.getcwd()
cwd = Path(cd,'..')

sys.path.append(os.path.join(cwd, *['Codes','DesignTool']))
sys.path.append(os.path.join(cwd, *['Codes','ModelingTool']))
sys.path.append(os.path.join(cwd, *['Codes', 'PostProcessing']))

####################### Modules required for Design Tool ##################
from FinalShearWallDesign_allFloors import FinalShearWallDesign
from StiffnessBasedDesign import RDADesignIterationClass

####################### Modules required for OpenSees Modeling ##################
# os.chdir(os.path.join(cwd, *['Codes','ModelingTool']))
from BuildingModelClass import BuildingModel
from utils import *

####################### Modules required for Post-Processing ##################
import ExtractMaxEDP as extractedps
import ExtractPushoverData as epd
import csv
import math

####################### Modules required for Loss Assessment ##################
# and import pelicun classes and methods
# from pelicun.base import set_options, convert_to_MultiIndex
# from pelicun.assessment import Assessment

# pd.set_option('display.max_colwidth', 100)



def run_woodSDA(ID):


    # Utility function directory 
    UtilDirectory = os.path.join(cwd, *['Codes','ModelingTool'])
    # Base directory is the main directory that models, model inputs and utility directory stores
    BaseDirectory = cwd
    # Model directory is where you want to store your model
    ModelDirectory = os.path.join(cwd, 'BuildingModels')
    # DB directory is where you store Database.csv (for steel section)
    DBDirecctory = UtilDirectory

    # If there is no model directory, create one
    if os.path.isdir(ModelDirectory) != True:
        os.chdir(BaseDirectory)
        os.mkdir('BuildingModels')

    ## create a directory to story results
    resultDirectory = os.path.join(cwd, 'Results')
    if os.path.isdir(resultDirectory) != True:
        os.chdir(cwd)
        os.mkdir('Results')
        
    # Read in building name(s) 
    # Make sure the building name is consistent with the input folders
    os.chdir(os.path.join(cwd, 'Codes'))
    # with open('BuildingNames_woodSDATest.txt', 'r') as f:
    #     BuildingList = f.read() 
    

    
    caseID = 'Building_' + str(ID[0])
    BuildingList = [caseID]
    start = time.time()

    basedirectory = os.path.join(cwd, *['BuildingInfo', caseID])

    # read in building parameters
    numstorpath = Path(basedirectory,'Geometry','numberOfStories.txt')
    direction = Path(basedirectory,'Geometry','direction.txt')
    wallnamepath = Path(basedirectory,'Geometry','wallLineName.txt')
    numwallpath = Path(basedirectory,'Geometry','numberOfWallsPerLine.txt')

    with open(numstorpath) as n, open(wallnamepath) as w, open(numwallpath) as nw, open(direction) as d:
        numFloors = n.read()
        direction = d.read().split("\n")
        wall_line_name = w.read().split("\n")
        nwPerLine = nw.read().split("\n")
        numWallsPerLine = [eval(i) for i in nwPerLine]
    
    # direction = ['X', 'X', 'X', 
    #             'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']
    # wall_line_name = ['gridA', 'gridB', 'gridC',
    #                 'grid1', 'grid2','grid3','grid4','grid5','grid6', 'grid7']
    # numWallsPerLine = [4, 4, 4,
    #                 2, 2, 4, 2, 4, 2, 2]
    counter = 0

    rda = RDADesignIterationClass(caseID, basedirectory, direction,numWallsPerLine, counter, wall_line_name,
                                weight_factor=1, seismic_design_level='Extreme', mat_ext_int='HWS_GWB')

    # rda.maindf
    # rda.maindf.to_csv(os.path.join(resultDirectory, "FinalDesignOutput.csv"))
    stop = time.time()
    print( stop - start, 'seconds')

#################### Modeling Module ##########################
    start = time.time()

    ModelDirectory = str(Path(BaseDirectory,'BuildingModels'))
# Generate eigen analysis, pushover analysis and dynamic analysis models for each one in the building list
    for i in range(0, len(BuildingList)):
        design_level = 'Extreme'
            
        InfoDirectory = os.path.join(BaseDirectory, *['BuildingInfo', '%s'%BuildingList[i]])
        ModelClass = BuildingModel(BuildingList[i], InfoDirectory, seismic_design_level = design_level)

        # alternatively, one can choose to read inputs from json 
        ModelClass.read_in_txt_inputs(BuildingList[i], InfoDirectory)

        if os.path.isdir(ModelDirectory+'/%s'%BuildingList[i]) != True:
            os.chdir(ModelDirectory)
            os.mkdir('%s'%BuildingList[i])
            
        os.chdir(ModelDirectory+'/%s'%BuildingList[i])

        period = generateModalAnalysisModel(ModelClass.ID, ModelClass, str(BaseDirectory).replace("\\","/"), DBDirecctory)
        # Turn off RunPushoverSwitch to speed up the model creation 
        generatePushoverAnalysisModel(ModelClass.ID, ModelClass, str(BaseDirectory).replace("\\","/"), DBDirecctory,
                                GenerateModelSwitch = True, RunPushoverSwitch = True)
        generateDynamicAnalysisModel(ModelClass.ID, ModelClass, str(BaseDirectory).replace("\\","/"), DBDirecctory, period,
                                GenerateModelSwitch = True)
        print(period)
        print(BuildingList[i])

    finish = time.time()
    print((finish - start)/60, 'Minutes')

################## Dynamic Analysis ############################
    ### MSA using selected GM records for 5 hazard levels. Location: Boelter Hall
    Scale_Sa_GM = '0.403 0.975 1.307 1.676 2.237'
    GM_Num = '50 47 47 48 47'

    # GM_ID = 1 # GM pair
    GM_folder = r'GM_sets/BoelterHall'

    Model_Name = caseID

    # start_ID is tarting index which starts from 1 instead of 0
    # finish_ID is the total number of GMs in multiple stripe or incremental dynamic analysis
    # for eg: if you have 10 hazard levels with 22 GM pairs, finish_id should be 10*22 + 1
    start_ID, finish_ID = 1, 3 # for demonstration I'm running dynamic analysis for 2 ground motion pairs
    acc_time = 0
    start_time = time.time()

    # ModelDirectory = str(Path(BaseDirectory,'BuildingModels'))

    ## following chucks of codes run dynamic analysis for each ground motion pair iteratively
    # Pairing ID == 1 i.e. apply H1 motion in X and H2 motion in Z

    for GM_ID in range(start_ID, finish_ID):
        s = time.time()
        SetupDyamaicAnalysis(ModelDirectory, Scale_Sa_GM, GM_Num, GM_ID, GM_folder, Model_Name, 1)
        os.chdir(ModelDirectory)

        r = os.system('C:\\OpenSees\\bin\\OpenSees RunDynamic_Single.tcl')
        f = time.time()
        if not r: 
            print('Hazard Level %i GM Pair %s with Pairing ID %i has finished successfully in %.3fs!'%(int(GM_ID/50)+1, str(GM_ID-int(GM_ID/50)), 1, f-s))
            os.remove('RunDynamic_Single.tcl')
            acc_time += (f-s)
            #print('Estimate remaining time %.3fs!'%(acc_time/(GM_ID - start_ID)*(finish_ID - GM_ID)))
        else: 
            print('GM Pair %s has failed'%str(GM_ID))
            break

    # Pairing ID == 2 i.e. apply H2 motion in X and H1 motion in Z
    for GM_ID in range(start_ID, finish_ID):
        s = time.time()
        SetupDyamaicAnalysis(ModelDirectory, Scale_Sa_GM, GM_Num, GM_ID, GM_folder, Model_Name, 2)
        os.chdir(ModelDirectory)
        r = os.system('C:\\OpenSees\\bin\\OpenSees RunDynamic_Single.tcl')
        f = time.time()
        if not r: 
    #         print('Hazard Level %i GM Pair %s with Pairing ID %i has finished successfully in %.3fs!'%(int(GM_ID/22)+1, str(GM_ID-int(GM_ID/22)), 2, f-s))
            os.remove('RunDynamic_Single.tcl')
            acc_time += (f-s)
            #print('Estimate remaining time %.3fs!'%(acc_time/(GM_ID - start_ID)*(finish_ID - GM_ID)))
        else: 
            print('GM Pair %s has failed'%str(GM_ID))
            break

    finish_time = time.time()
    print('The total runtime is %.3f minutes' %(int(finish_time-start_time)/60))

    ############### Post-Process Dynamic Analysis ###################
    # NumGM = np.array([50, 47, 47, 48, 47])

    # CollapseCriteria = 0.1
    # DemolitionCriteria = 0.01

    # HazardLevel = np.array([0.403, 0.975, 1.307, 1.676, 2.237])

    # dynamicDirectory = os.path.join(cwd, *['BuildingModels',BuildingList[0],'DynamicAnalysis'])

    # sdr = extractedps.ExtractSDR(dynamicDirectory, HazardLevel, NumGM, numFloors)
    # rdr = extractedps.ExtractRDR(dynamicDirectory, HazardLevel, NumGM, NumStory)
    # gmDirectory = r'C:\Users\Laxman\Desktop\Python Tool\BuildingModels\GM_sets\BoelterHall'
    # PGA = extractedps.ExtractPGA(gmDirectory, HazardLevel, NumGM)
    # pfa = extractedps.ExtractPFA(dynamicDirectory, HazardLevel, NumGM, NumStory, PGA, g = 386.4)


if __name__ == "__main__":
    import sys
    id = int(sys.argv[1])
    print("Id is ",id)
    run_woodSDA([id])