# This file is used to define a class to postprocessing nonlinear analysis results.
# Developed by GUAN, XINGQUAN @ UCLA in Sept. 2020
# Adapted for running on Hoffman2

import os
import numpy as np
import pandas as pd

from scipy.optimize import minimize
from scipy.stats import norm
from scipy.stats import binom

PREFIX = 'ABuilding_'

# #########################################################################
#    Define a class to postprocess nonlinear static and dynamic results   #
# #########################################################################


class PostprocessNonlinearAnalysis(object):
    """
    This class is used to do the following assignments:
    (1) Extract the peak story drift for each ground motion at each intensity
    (2) Extract the maximum peak story drift (one value for one building) for each ground motion at each intensity
    (3) Count the number of collapse cases at each intensity level
    (4) Compute the actual hazard level using Sa value
    (5) Determine the collapse margin ratio (CMR) and adjusted collapse margin ratio (ACMR)
    (11) Compute the total steel weight
    """

    def __init__(self, building_directory, data_directory, building_ID, number_story, GM_IDs, IDA_scales, SaMCE):
        # Initialize some variables to store the class member data
        self.peak_story_drift = dict()
        self.peak_floor_acceleration = dict()
        self.residual_drift = dict()
        self.maximum_drift = None
        self.collapse_cases = list()
        self.intensity_levels = SaMCE * np.array(IDA_scales) / 100
        self.lognorm_parameters = dict()
        self.performance_metrics = dict()

        # Call the following methods to compute the member data
        self.extract_peak_story_drift(building_directory, number_story, GM_IDs, IDA_scales)
        self.extract_peak_floor_acceleration(building_directory, number_story, GM_IDs, IDA_scales)
        self.extract_residual_story_drift(building_directory, number_story, GM_IDs, IDA_scales)
        self.save_EDPs(data_directory, building_ID)
        self.process_peak_story_drift(IDA_scales, GM_IDs)
        self.save_IDA_results(data_directory, IDA_scales, building_ID)
        self.count_collapse_case()
        self.lognormfit(len(GM_IDs), building_ID, 'MLE')
        self.compute_performance_metrics(SaMCE, building_ID)

    def extract_peak_story_drift(self, building_directory, number_story, GM_IDs, IDA_scales):
        """
        This method extract  peak story drift profile for  building subjected to each ground motion at each intensity.
        :param building_directory: a string to specify the path where the nonlinear model is stored
        :param number_story: an integer to denote the number of stories
        :param GM_IDs: a list of integers to denote the ground motion IDs
        :param IDA_scales: a list of integers specifies the IDA scales in the unit of percent
        :return: a dictionary: the key is the intensity scale and each value is a M*N numpy array
        """
        # Initialize a dictionary to store results
        number_GM = len(GM_IDs)
        peak_story_drift_profile = dict()
        # Loop over all scales
        for scale in IDA_scales:
            peak_drift_array = np.zeros([number_story, number_GM])
            # Loop over all ground motion records
            count = 1
            for GM in GM_IDs:
                # Change the current working directory to the folder of drift output files
                # Use windows path rather than hard coding
                drift_directory = building_directory / 'DynamicAnalysis' / 'IDAOutput' / ('EQ_' + str(GM)) \
                                  / ('Scale_' + str(scale)) / 'StoryDrifts'
                try:
                    os.chdir(drift_directory)
                    # Loop over all stories of current building
                    for story in range(1, number_story+1):
                        # Load story drift
                        file = ('Story%i.out' % story)
                        drift = np.abs(np.loadtxt(file)[:, -1])
                        peak_drift_array[story-1, count-1] = np.max(drift)
                except FileNotFoundError:
                    for story in range(1, number_story+1):
                        peak_drift_array[story-1, count-1] = 0.10
                except ValueError:
                    for story in range(1, number_story+1):
                        peak_drift_array[story-1, count-1] = 0.10
                count += 1
            peak_story_drift_profile[scale] = peak_drift_array
        # Store the results into the class member data
        self.peak_story_drift = peak_story_drift_profile

    def extract_peak_floor_acceleration(self, building_directory, number_story, GM_IDs, IDA_scales):
        """
        This method extract peak floor acceleration for building subjected to each ground motion at each intensity.
        :param building_directory: a string to specify the path where the nonlinear model is stored
        :param number_story: an integer to denote the number of stories
        :param GM_IDs: a list of integers to denote the ground motion IDs
        :param IDA_scales: a list of integers specifies the IDA scales in the unit of percent
        :return: a dictionary: the key is the intensity scale and each value is a M*N numpy array
        """
        # Initialize a dictionary to store results
        number_GM = len(GM_IDs)
        peak_floor_acceleration_profile = dict()
        # Loop over all scales
        for scale in IDA_scales:
            peak_acceleration_array = np.zeros([number_story+1, number_GM])
            # Loop over all ground motion records
            count = 1
            for GM in GM_IDs:
                # Change the current working directory to the folder of acceleration output files
                # Use windows path rather than hard coding
                acceleration_directory = building_directory / 'DynamicAnalysis' / 'IDAOutput' / ('EQ_' + str(GM)) \
                                         / ('Scale_' + str(scale)) / 'NodeAccelerations'
                try:
                    os.chdir(acceleration_directory)
                    # Loop over all stories of current building
                    for level in range(1, number_story+2):
                        # Load floor accelerations
                        file = ('NodeAccLevel%i.out' % level)
                        # Since EqualDOF is used: all nodes at same floor level have identical acceleration
                        # thus only the last column is selected
                        acceleration = np.abs(np.loadtxt(file)[:, -1])
                        peak_acceleration_array[level - 1, count- 1] = np.max(acceleration)
                except FileNotFoundError:
                    for level in range(1, number_story+2):
                        peak_acceleration_array[level - 1, count- 1] = 10*386.4
                except ValueError:
                    for level in range(1, number_story+2):
                        peak_acceleration_array[level-1, count-1] = 10*386.4
                count += 1
            peak_floor_acceleration_profile[scale] = peak_acceleration_array
        # Store the results into the class member data
        self.peak_floor_acceleration = peak_floor_acceleration_profile

    def extract_residual_story_drift(self, building_directory, number_story, GM_IDs, IDA_scales):
        """
        This method extract residual story drift for building subjected to each ground motion at each intensity.
        :param building_directory: a string to specify the path where the nonlinear model is stored
        :param number_story: an integer to denote the number of stories
        :param GM_IDs: a list of integers to denote the ground motion IDs
        :param IDA_scales: a list of integers specifies the IDA scales in the unit of percent
        :return: a dictionary: the key is the intensity scale and each value is a M*N numpy array
        """
        # Initialize a dictionary to store results
        number_GM = len(GM_IDs)
        residual_drift_profile = dict()
        # Loop over all scales
        for scale in IDA_scales:
            residual_drift_array = np.zeros([number_story, number_GM])
            # Loop over all ground motion records
            count = 1
            for GM in GM_IDs:
                # Change the current working directory to the folder of drift output files
                # Use windows path rather than hard coding
                drift_directory = building_directory / 'DynamicAnalysis' / 'IDAOutput' / ('EQ_' + str(GM)) \
                                  / ('Scale_' + str(scale)) / 'StoryDrifts'
                try:
                    os.chdir(drift_directory)
                    # Loop over all stories of current building
                    for story in range(1, number_story+1):
                        # Load story drift
                        file = ('Story%i.out' % story)
                        drift = np.abs(np.loadtxt(file)[:, -1])
                        residual_drift_array[story-1, count-1] = drift[-1]
                except FileNotFoundError:
                    for story in range(1, number_story+1):
                        residual_drift_array[story-1, count-1] = 0.10
                except ValueError:
                    for story in range(1, number_story+1):
                        residual_drift_array[story-1, count-1] = 0.10
                count += 1
            residual_drift_profile[scale] = residual_drift_array
        # Store the results into the class member data
        self.residual_drift = residual_drift_profile

    def save_EDPs(self, data_directory, building_ID):
        """
        This function is used to save the EDP (engineering demand parameters) into the data folder
        :param data_directory: a string to specify the path to where the building data is stored
        :return: save the all EDPs results into a JSON format
        """
        # Save peak story drifts
        os.chdir(data_directory / 'PeakStoryDrifts')
        file_name = PREFIX + str(building_ID) + '_PSDR.xlsx'
        writer = pd.ExcelWriter(file_name)
        for scale in self.peak_story_drift:
            data = pd.DataFrame(self.peak_story_drift[scale])
            data.to_excel(writer, str(scale), header=False, index=False)
        writer.save()
        writer.close()
        # Save peak floor accelerations
        os.chdir(data_directory / 'PeakFloorAccelerations')
        file_name = PREFIX + str(building_ID) + '_PFA.xlsx'
        writer = pd.ExcelWriter(file_name)
        for scale in self.peak_floor_acceleration:
            data = pd.DataFrame(self.peak_floor_acceleration[scale])
            data.to_excel(writer, str(scale), header=False, index=False)
        writer.save()
        writer.close()
        # Save residual story drifts
        os.chdir(data_directory / 'ResidualStoryDrifts')
        file_name = PREFIX + str(building_ID) + '_RSDR.xlsx'
        writer = pd.ExcelWriter(file_name)
        for scale in self.residual_drift:
            data = pd.DataFrame(self.residual_drift[scale])
            data.to_excel(writer, str(scale), header=False, index=False)
        writer.save()
        writer.close()

    def process_peak_story_drift(self, IDA_scales, GM_IDs):
        """
        This method is used to extract the maximum peak story drift per building
        :param self.peak_story_drift: a dictionary with intensity as the key and each value is a M*N array
                                      M: number of story; N: number of GM
        :param IDA_scales: a list of intensity scales
        :param GM_IDs: a list of integers to denote the ground motion IDs
        :return: a N*K array. N: number of Gm; K: number of intensity scales
        """
        number_GM = len(GM_IDs)
        result = np.zeros([number_GM, len(IDA_scales)])
        count = 0
        for scale in self.peak_story_drift:
            max_drift = np.max(self.peak_story_drift[scale], axis=0)
            result[:, count] = max_drift.transpose()
            count += 1
        self.maximum_drift = result

    def save_IDA_results(self, data_directory, IDA_scales, building_ID):
        """
        This function is used to save the IDA results into the data folder
        :param data_directory: a string to specify the path to where the building data is stored
        :param IDA_scales: a list of numbers to specify the IDA scales in percent
        :return: save the self.max_drift results into a csv format
        """
        # Create a header for the .csv file
        header = list()
        for each_scale in IDA_scales:
            strr = 'Scale' + str(each_scale)
            header.append(strr)
        # Save the .csv file into the data directory
        os.chdir(data_directory / 'IDAResults')
        file_name = PREFIX + str(building_ID) + '_IDA.csv'
        dataframe = pd.DataFrame(data=self.maximum_drift, columns=header)
        dataframe.to_csv(file_name, sep=',', index=False)


    def count_collapse_case(self):
        """
        This function is used to count the number of collapse cases per intensity
        :return: a list which denote the number of collapse cases under different intensity levels
        """
        collapse_cases = list()
        row, col = self.maximum_drift.shape
        for i in range(0, col):
            count = np.sum(self.maximum_drift[:,i] >= 0.10)
            collapse_cases.append(count)
        self.collapse_cases = collapse_cases

    def neg_loglik(self, theta, intensity_levels, collapse_cases, number_of_GMs):
        """
        This function is used to define a negative log-likelihood function.
        Acknowledgement: This function was written by ZHENGXIANG YI @ UCLA.
        :param theta: a list with two values. 1st one is the central tendency and the 2nd is the dispersion.
        :param intensity_levels: an array of numbers to denote the Sa value of each intensity
        :param collapse_cases: an array of numbers to denote the number of collapse cases at each intensity
        :param number_of_GMs: a scalar to denote the number of ground motions
        :return: a scalar to denote the value of negative log-likelihood function results
        """
        p_pred = norm.cdf(np.log(intensity_levels), loc = np.log(theta[0]), scale = np.log(theta[1]))
        likelihood = binom.pmf(collapse_cases, number_of_GMs, p_pred)
        return -np.sum(np.log(likelihood))

    def squareerror(self, theta, intensity_levels, collapse_cases, number_of_GMs):
        """
        This function is used to compute the square error function.
        Acknowledgement: It was written by ZHENGXIANG YI @ UCLA.
        :param theta: a list with two values. 1st one is the central tendency and the 2nd is the dispersion.
        :param intensity_levels: an array of numbers to denote the Sa value of each intensity
        :param collapse_cases: an array of numbers to denote the number of collapse cases at each intensity
        :param number_of_GMs: a scalar to denote the number of ground motions
        :return: a scalar to denote the value of negative log-likelihood function results
        """
        p_real = collapse_cases/number_of_GMs
        p_pred = norm.cdf(np.log(intensity_levels), loc = np.log(theta[0]), scale = theta[1])
        return np.sum((p_real - p_pred)**2)

    def lognormfit (self, number_of_GMs, building_ID, Method='MLE'):
        """
        This method is used to fit the collapse fragility empirical data with a lognormal distribution.
        Acknowledgement: It was written by ZHENGXIANG YI @ UCLA.
        :param number_of_GMs: a scalar to denote the number of ground motions
        :param Method: 'MLE' or other fitting approach.
        :return: a list with two values to quantify lognorm distribution. 1st one is central tendency and 2nd is dispersion.
        """
        # Initial guess, pay attention to initial guess to avoid log(0) and log (1)
        theta_start = np.array([2,3])
        theta = []
        # Optimization by minimizing the negative log-likelihood function
        if Method == 'MLE':
            res = minimize(self.neg_loglik, theta_start, args = (self.intensity_levels, self.collapse_cases, number_of_GMs),
                           method = 'Nelder-Mead', options={'disp': True})
        else:
            res = minimize(self.squareerror, theta_start, args = (self.intensity_levels, self.collapse_cases, number_of_GMs),
                           method = 'Nelder-Mead', options={'disp': True})
        # Store the results into theta
        theta.append(res.x[0])
        theta.append(np.log(res.x[1]))
        # Return the mean and standard deviation
        self.lognorm_parameters['mean'] = theta[0]
        self.lognorm_parameters['standard deviation'] = theta[1]
        np.chdir(data_directory / 'CollapseResistance')
        file_name = PREFIX + str(building_id) + '_fragility.txt'
        np.savetxt(file_name, np.array([theta[0], theta[1]]), fmt='%.5f')


    def plot_fragility_curve(self, GM_IDs):
        """
        This method is used to plot the fragility curve
        :param GM_IDs: a list of integer to denote the ground motion IDs
        :return: a PNG figure
        """
        fig = plt.figure(figsize=(5, 4), dpi=150)
        plt.scatter(self.intensity_levels, np.array(self.collapse_cases)/len(GM_IDs),
                    label='Empirical collapse probability')
        IM_levels = np.linspace(0.01, 6.0, 600)
        probability = norm.cdf(np.log(IM_levels), loc=np.log(self.lognorm_parameters['mean']),
                               scale=self.lognorm_parameters['standard deviation'])
        plt.plot(IM_levels, probability, label='Lognormal fragility')
        plt.xlabel('Sa(T1)', fontname='Times New Roman', fontsize=12, fontweight='light')
        plt.ylabel('Probability', fontname='Times New Roman', fontsize=12, fontweight='light')
        plt.xticks(fontname='Times New Roman', fontsize=12, fontweight='light')
        plt.yticks(fontname='Times New Roman', fontsize=12, fontweight='light')
        plt.legend(prop={'family': 'Times New Roman', 'size': 12}, loc='upper left')
        plt.title('Collapse fragility curve', fontname='Times New Roman', fontsize=12)
        plt.show()


    def compute_performance_metrics(self, SaMCE, building_ID):
        """
        This function computes the performance metrics to evaluate the response of the design
        :param SaMCE: Sa value at MCE spectrum
        :param period: the building period
        :return: a dictionary to store the value of median collapse capcity, CMR, and ACMR
        """
        # Compute the median collapse capacity
        median_collapse = np.exp(norm.ppf(50/100, loc=np.log(self.lognorm_parameters['mean']),
                                          scale=self.lognorm_parameters['standard deviation']))
        # Compute CMR and ACMR value
        CMR = median_collapse / SaMCE
        # SSF = determine_spectral_shape_factor(5.0, period)
        # ACMR = SSF * CMR
        # Store the performance evaluation results into the class member data
        self.performance_metrics['median collapse capacity'] = median_collapse
        self.performance_metrics['CMR'] = CMR
        os.chdir(data_directory / 'CollapseResistance')
        file_name = PREFIX + str(building_ID) + '_CMR.txt'
        np.savetxt(file_name, np.array([CMR], fmt='%.5f'))