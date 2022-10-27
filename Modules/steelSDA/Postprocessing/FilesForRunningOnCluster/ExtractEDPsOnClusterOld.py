# This file defines a function to extract required EDPs from OpenSees dynamic analysis results
# Developed by GUAN, XINGQUAN @ UCLA, 05/27/2019
# This file shall be put at the same folder with a bunch of building model folders

import os
import numpy as np

def extract_peak_story_drift(building_directory, building_ID, scale, number_story, number_GM):
    """
    This function returns a M*N numpy array of peak story drifts for a certain building subjected to different GMs.
    M is the number of stories for the building and N is the number of ground motions (GMs).
    :param building_directory: a string specifies the current building OpenSees model is.
    :param building_ID: an integer specifies the current building ID
    :param number_story: an integer specifies the number of stories for the building
    :param number_GM: an integer specifies the number of ground motion records
    :return: M*N numpy array
    """
    # Initialize a numpy array to store results
    peak_drift_array = np.zeros([number_story, number_GM])
    # Loop over all ground motion records
    for GM in range(1, number_GM+1):
        # Change the current working directory to the folder of drift output files
        drift_directory = building_directory + '/DynamicAnalysis/IDAOutput/EQ_' + str(GM) + '/Scale_' + str(scale) + '/StoryDrifts'
        os.chdir(drift_directory)
        # Loop over all stories of current building
        for story in range(1, number_story+1):
            # Load story drift
            file = ('Story%i.out' % story)
            drift = np.abs(np.loadtxt(file)[:, -1])
            peak_drift_array[story-1, GM-1] = np.max(drift)
    # Display the information to output files on cluster
    print("********** Peak Story Drifts *************")
    print("Current ModelIndex: %i" % building_ID)
    print("******************************************")
    # Return the desired results
    return peak_drift_array


def extract_residual_story_drift(building_directory, building_ID, number_story, number_GM):
    """
    This function returns a M*N numpy array of residual story drifts for a certain building subjected to different GMs.
    M is the number of stories for the building and N is the number of ground motions (GMs).
    :param building_directory: a string specifies the current building OpenSees model is.
    :param building_ID: an integer specifies the current building ID
    :param number_story: an integer specifies the number of stories for the building
    :param number_GM: an integer specifies the number of ground motion records
    :return: M*N numpy array
    """
    # Initialize a numpy array to store results
    residual_drift_array = np.zeros([number_story, number_GM])
    # Loop over all ground motion records
    for GM in range(1, number_GM+1):
        # Change the current working directory to the folder of drift output files
        drift_directory = building_directory + '/DynamicAnalysis/IDAOutput/EQ_' + str(GM) + '/Scale_100/StoryDrifts'
        os.chdir(drift_directory)
        # Loop over all stories of current building
        for story in range(1, number_story+1):
            # Load story drift
            file = ('Story%i.out' % story)
            drift = np.abs(np.loadtxt(file)[:, -1])
            residual_drift_array[story-1, GM-1] = drift[-1]
    # Display the information to output files on cluster
    print("********** Residual Story Drifts *********")
    print("Current ModelIndex: %i" % building_ID)
    print("******************************************")
    # Return the desired results
    return residual_drift_array


def extract_peak_acceleration(building_directory, building_ID, number_story, number_GM):
    """
    This function returns a (M+1)*N numpy array of residual story drifts for a certain building subjected to different GMs.
    M+1 is the number of floor levels for the building and N is the number of ground motions (GMs).
    :param building_directory: a string specifies the current building OpenSees model is.
    :param building_ID: an integer specifies the current building ID
    :param number_story: an integer specifies the number of stories for the building
    :param number_GM: an integer specifies the number of ground motion records
    :return: (M+1)*N numpy array
    """
    # Initialize a numpy array to store results
    peak_acceleration_array = np.zeros([number_story+1, number_GM])
    # Loop over all ground motion records
    for GM in range(1, number_GM+1):
        # Change the current working directory to the folder of drift output files
        acceleration_directory = building_directory + '/DynamicAnalysis/IDAOutput/EQ_' + str(GM) + '/Scale_100/NodeAccelerations'
        os.chdir(acceleration_directory)
        # Loop over all stories of current building
        for level in range(1, number_story+2):
            # Load story drift
            file = ('NodeAccLevel%i.out' % level)
            acceleration = np.abs(np.loadtxt(file)[:, 1:])
            peak_acceleration_array[level - 1, GM - 1] = np.max(acceleration)
    # Display the information to output files on cluster
    print("******* Peak Floor Accelerations *********")
    print("Current ModelIndex: %i" % building_ID)
    print("******************************************")
    # Return the peak floor acceleration
    return peak_acceleration_array