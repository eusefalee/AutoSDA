# This file is used to define the necessary functions and classes for modal response spectrum analysis.
# Developed by GUAN, XINGQUAN @ UCLA in June 2021

import numpy as np
import os
import pandas as pd
from elastic_analysis import ElasticAnalysis
from global_variables import GRAVITY_CONSTANT


class ResponseSpectrumAnalysis(object):
    """
    This class performs the modal response spectrum analysis for a building and collected the necessary information
    relevant to the RSA-based design.
    """

    def __init__(self, building):
        # Initialize the variables to store the mode-related information for RSA-based design
        self.modal_periods = list()  # 2D list: modes * stories
        self.modal_shapes = list()  # 2D list: modes * stories
        self.number_of_mode = 0
        self.floor_mass = list()  # 1D list: 1 * stories (excluding ground level).
        self.participation_factor = list()  # 2D list: modes * stories
        self.modal_mass_participation = list()  # 2D list: modes * stories
        self.spectral_acceleration = list()  # 1D list: 1 * modes
        self.lateral_forces = list()  # 2D list: modes * stories
        self.story_shears = list()  # 2D list: modes * stories
        self.base_shears = list()  # 1D list: 1 * modes
        self.scaling_factors = dict()
        self.final_RSA_responses = dict()  # The seismic forces scaled up to 100% of ELF force.
        # Perform the following methods to obtain the mode related information.
        self.perform_modal_analysis(building)
        self.extract_modal_analysis_results(building)
        self.calculate_mode_participation(building)
        self.determine_number_of_modes(building)
        self.calculate_spectral_acceleration(building)
        self.calculate_seismic_forces(building)
        self.determine_scaling_factor(building)
        self.perform_elastic_analysis(building)
        self.combine_analysis_results(building)
        self.determine_finalized_responses(building)
        self.calculate_mode_displacement(building)
        # Following function is for debug using only
        # self.save_results(building)

    def perform_modal_analysis(self, building):
        _ = ElasticAnalysis(building, design_method='RSA', analysis_load_type='EigenValue')

    def extract_modal_analysis_results(self, building):
        """
        This method is used to extract the modal periods and modal shapes from OpenSees analysis results.
        :param building: a class defined in "building_information.py" file
        :return: a [story*1] list to denote all modal periods; a [story*story] to denote all modal shapes.
        """
        # Change the working directory to the folder where the eigen value analysis results are stored
        path_modal_period = building.directory['building elastic model'] / 'EigenAnalysis'
        os.chdir(path_modal_period)
        # Read all modal periods
        period = pd.read_csv('Periods.out', header=None)
        self.modal_periods = list(period.iloc[:, 0].values)

        # Read all modal shapes
        modal_shapes = list()
        # Note that for a N-story 2D frame, it has a maximum of N modal shapes (in lateral direction).
        file_list = [('Vector' + str(mode + 1) + 'Direction1.out')
                     for mode in range(building.geometry['number of story'])]
        for file in file_list:
            eigen_vector = pd.read_csv(file, header=None, sep=' ')
            # Remove the element at the ground level which is always zero
            vector = np.array(eigen_vector.iloc[0, :].values)[1:]
            # Scale the eigenvector such that its maximum element is 1.0
            max_index = np.argmax(np.abs(vector))
            max_value = vector[max_index]
            scale_factor = 1.0 / max_value
            # Append each eigenvector into the list
            # scale_factor = 1.0
            modal_shapes.append(list(scale_factor * vector))
        self.modal_shapes = modal_shapes

    def calculate_mode_participation(self, building):
        """
        This method is used to compute the participation factor and modal mass participation, both of which are required
        for RSA-based design.
        :param building: a class defined in "building_information.py" file
        :return: two [story*1] arrays. One for participation factor (L) and the other for modal mass participation (MMP)
        """
        # Define mass vector
        floor_mass = np.array(building.gravity_loads['floor weight']) / GRAVITY_CONSTANT
        # Calculate the participation factor (denote as L in Chopra's book) and modal mass participation (MMP)
        modal_mass = list()
        participation_factor = list()
        for mode in range(building.geometry['number of story']):
            eigenvector = np.array(self.modal_shapes[mode])
            denominator = np.sum(floor_mass * eigenvector ** 2)
            numerator = (np.sum(floor_mass * eigenvector)) ** 2
            modal_mass.append(numerator / denominator)
            # Participation factor will be used later to calculate the lateral forces under each mode
            participation_factor.append(np.sum(floor_mass * eigenvector) / denominator)
        modal_mass_participation = np.array(modal_mass) / np.sum(modal_mass)
        # Store the results into class member data
        self.floor_mass = floor_mass
        self.participation_factor = participation_factor
        self.modal_mass_participation = modal_mass_participation

    def determine_number_of_modes(self, building):
        """
        This method is used to determine the required number of modes to achieve 90% of modal mass participation.
        :param building: a class defined in "building_information.py" file
        :return: an integer to denote the number of sufficient modes for 90% modal mass participation.
        """
        # Calculate the required number of modes to achieve 90% of mass participation
        sum_participation = 0
        count = 0
        for count in range(0, building.geometry['number of story']):
            sum_participation += self.modal_mass_participation[count]
            if sum_participation >= 0.9:
                break
        self.number_of_mode = count + 1

    def calculate_spectral_acceleration(self, building):
        """
        This method is used to calculate the Sa at different modal periods, which will be used later to calculate the
        lateral forces.
        :param building: a class defined in "building_information.py" file
        :return: a list to denote the Sa values at all modal periods.
        """
        T0 = 0.2 * building.elf_parameters['SD1'] / building.elf_parameters['SDS']
        Ts = building.elf_parameters['SD1'] / building.elf_parameters['SDS']
        TL = building.elf_parameters['TL']
        Sa_list = list()
        for mode in range(building.geometry['number of story']):
            T = self.modal_periods[mode]
            if T < T0:
                Sa = building.elf_parameters['SDS'] * (0.4 + 0.6 * T / T0)
            elif T < Ts:
                Sa = building.elf_parameters['SDS']
            elif T < TL:
                Sa = building.elf_parameters['SD1'] / T
            else:
                Sa = building.elf_parameters['SD1'] * TL / (T ** 2)
            Sa_list.append(Sa)
        self.spectral_acceleration = Sa_list

    def calculate_seismic_forces(self, building):
        """
        This method is used to compute the later forces under each mode.
        :param building: a class defined in "building_information.py" file
        :return: a [N*M] array where N is the number of stories and M is the required number of modes to achieve 90%
                modal mass participation.
        """
        # Compute the later forces under each mode.
        lateral_forces = list()
        for mode in range(0, self.number_of_mode):
            force = self.spectral_acceleration[mode] * self.floor_mass \
                    * self.participation_factor[mode] * self.modal_shapes[mode] * GRAVITY_CONSTANT
            force = force / (building.elf_parameters['R'] / building.elf_parameters['Ie'])
            lateral_forces.append(force)
        self.lateral_forces = lateral_forces
        # Compute the story shear force under each mode.
        story_shear_forces = list()
        base_shears = list()
        for mode in range(0, self.number_of_mode):
            story_shear = np.zeros(building.geometry['number of story'])
            for story in range(building.geometry['number of story'] - 1, -1, -1):
                story_shear[story] = np.sum(lateral_forces[mode][story:])
            story_shear_forces.append(list(story_shear))
            base_shears.append(story_shear[0].item())
        self.story_shears = story_shear_forces
        self.base_shears = base_shears

    def determine_scaling_factor(self, building):
        """
        This method is used to determine the
        :param building: a class defined in "building_information.py" file.
        :return: return two scalars. One for the force scaling factor and the other is for drift.
        """
        # Compute the base shear (Vt) combined from different modes
        sum_base_shear = 0
        for mode in range(self.number_of_mode):
            sum_base_shear += self.base_shears[mode] ** 2
        combine_base_shear = np.sqrt(sum_base_shear)
        if combine_base_shear < building.seismic_force_for_strength['base shear']:
            scaling_factor_force = building.seismic_force_for_strength['base shear'] / combine_base_shear
        else:
            scaling_factor_force = 1.0

        # This revision is for TDMF project design only (Dr. DeBock's requirement)
        # scaling_factor_force = 0.75 * building.seismic_force_for_strength['base shear'] / combine_base_shear
        # Determine the scaling factor for drift
        Cs = 0.5 * building.elf_parameters['S1'] / (building.elf_parameters['R'] / building.elf_parameters['Ie'])
        # This revision is for TDMF project design only (Dr. DeBock's requirement)
        # Cs = 0.75 * 0.5 * building.elf_parameters['S1'] / (building.elf_parameters['R'] / building.elf_parameters['Ie'])
        # Cs = 0.35 * building.elf_parameters['SD1'] / (building.elf_parameters['R'] / building.elf_parameters['Ie'])

        W = np.sum(building.gravity_loads['floor weight'])
        if combine_base_shear < Cs*W:
            scaling_factor_drift = Cs*W / combine_base_shear
        else:
            scaling_factor_drift = 1.0
        self.scaling_factors['force'] = scaling_factor_force
        self.scaling_factors['drift'] = scaling_factor_drift

    def perform_elastic_analysis(self, building):
        """
        This method is used to perform the elastic analysis to generate the force and deformation demands subjected to
        later load under each mode.
        :param building: a class defined in "building_information.py" file.
        :return: No return variable. Just perform the elastic analysis via OpenSees.
        """
        # Generate the OpenSees model
        for mode in range(self.number_of_mode):
            _ = ElasticAnalysis(building, design_method='RSA', analysis_load_type='EarthquakeLoad', which_mode=mode,
                                lateral_forces=self.lateral_forces[mode])

    def combine_analysis_results(self, building):
        """
        This method is used to combine the load and displacement results from different modes using SRSS method.
        :return: No return variable. All combined results are stored in new folder "RSACombineEarthquakeLoad" under
                building elastic model folder.
        """
        # Create a folder structure that is the same as those generated by OpenSees output.
        RSA_folder_name = 'RSACombineEarthquakeLoad'
        subfolder_list = ['GlobalBeamForces', 'GlobalColumnForces', 'NodeDisplacements', 'StoryDrifts']
        for subfolder in subfolder_list:
            path = building.directory['building elastic model'] / RSA_folder_name / subfolder
            if not os.path.exists(path):
                os.makedirs(path)
        # Use square root of the sum of squares (SRSS) to combine the physical quantities under each mode
        # Define the OpenSees output file name prefix
        file_name_prefix = ['GlobalXBeamForcesLevel', 'GlobalColumnForcesStory', 'NodeDisplacementLevel', 'Story']
        # Loop over all types of output
        for folder_index in range(len(subfolder_list)):
            for story in range(1, building.geometry['number of story'] + 1):
                # Define the OpenSees output file name postfix (output is counting on floor level or story).
                if subfolder_list[folder_index] == 'GlobalBeamForces' \
                        or subfolder_list[folder_index] == 'NodeDisplacements':
                    file_name_postfix = '%i.out' % (story + 1)
                else:
                    file_name_postfix = '%i.out' % story
                # Complete OpenSees output file name
                file_name = file_name_prefix[folder_index] + file_name_postfix
                result = dict()
                for mode in range(self.number_of_mode):
                    mode_folder = 'EarthquakeLoad' + str(mode)
                    os.chdir(building.directory['building elastic model'] / mode_folder / subfolder_list[folder_index])
                    result[mode] = np.loadtxt(file_name)
                combined_result = np.zeros(result[0].shape)
                combined_result[:, 0] = result[0][:, 0]
                for mode in range(self.number_of_mode):
                    combined_result[:, 1:] += result[mode][:, 1:] ** 2
                # Multiply with the force scaling factor to account for the requirement for 100% ELF base shear
                # The deformation scaling is handled in "determine_finalized_responses" function and thus skipped here.
                if subfolder_list[folder_index] == 'NodeDisplacements' \
                        or subfolder_list[folder_index] == 'StoryDrifts':
                    combined_result[:, 1:] = np.sqrt(combined_result[:, 1:]) * 1.0
                else:
                    combined_result[:, 1:] = np.sqrt(combined_result[:, 1:]) * self.scaling_factors['force']
                target_file = building.directory['building elastic model'] / RSA_folder_name \
                              / subfolder_list[folder_index] / file_name
                np.savetxt(target_file, X=combined_result, fmt='%.6f')

    def determine_finalized_responses(self, building):
        """
        This method is used to
        :param building: a class defined in "building_information.py" file.
        :return: a dictionary which includes the final RSA story drifts, story shear, base shear, etc.
        """
        # Change the working directory to the folder where the combined-mode displacements are saved.
        path_displacement = building.directory['building elastic model'] / 'RSACombineEarthquakeLoad' \
                            / 'NodeDisplacements'
        os.chdir(path_displacement)
        floor_displacement = np.zeros([building.geometry['number of story'], 1])
        # Read all the displacements
        for floor in range(building.geometry['number of story']):
            file_name = ('NodeDisplacementLevel%i.out' % (floor+2))
            read_data = pd.read_csv(file_name, header=None, sep=' ')
            # The last element of 2nd column is the lateral displacement
            floor_displacement[floor, 0] = read_data.iloc[-1, 1]
        self.final_RSA_responses['floor displacement'] = self.scaling_factors['drift'] * floor_displacement \
                                                         * building.elf_parameters['Cd'] / building.elf_parameters['Ie']

        # Use similar approach to obtain the story drift ratio
        path_displacement = building.directory['building elastic model'] / 'RSACombineEarthquakeLoad' \
                            / 'StoryDrifts'
        os.chdir(path_displacement)
        story_drift = np.zeros([building.geometry['number of story'], 1])
        # Read all the story drifts
        for story in range(building.geometry['number of story']):
            file_name = ('Story%i.out' % (story + 1))
            read_data = pd.read_csv(file_name, header=None, sep=' ')
            # The last element of 2nd column is the lateral displacement
            story_drift[story, 0] = read_data.iloc[-1, 1]
        self.final_RSA_responses['story drift'] = self.scaling_factors['drift'] * story_drift \
                                                  * building.elf_parameters['Cd'] / building.elf_parameters['Ie']

        # Determine the finalized story shear forces
        final_story_shears = np.zeros([building.geometry['number of story'], 1])
        for mode in range(self.number_of_mode):
            mode_shear_square = (np.array(self.story_shears[mode])) ** 2
            temp = np.reshape(mode_shear_square, final_story_shears.shape)
            final_story_shears += temp
        self.final_RSA_responses['story shear'] = self.scaling_factors['force'] * np.sqrt(final_story_shears)

    ###################################### Following functions are used to debug #######################################
    def calculate_mode_displacement(self, building):
        """
        This method is used to compute the displacement and story drift under different modes.
        :param building:
        :return:
        """
        mode_displacement = np.zeros([self.number_of_mode, building.geometry['number of story']])
        for mode in range(0, self.number_of_mode):
            omega = 2 * 3.14 / self.modal_periods[mode]
            for story in range(0, building.geometry['number of story']):
                mode_displacement[mode, story] = self.spectral_acceleration[mode] * self.participation_factor[mode] \
                                                 * self.modal_shapes[mode][story] / (omega ** 2) * GRAVITY_CONSTANT \
                                                 / (building.elf_parameters['R'] / building.elf_parameters['Ie'])
        self.mode_displacement = mode_displacement
        # Combine these displacements
        combine_displacement = np.zeros([building.geometry['number of story'], 1])
        for mode in range(0, self.number_of_mode):
            mode_displacement_square = mode_displacement[mode] ** 2
            temp = np.reshape(mode_displacement_square, combine_displacement.shape)
            combine_displacement += temp
        self.combine_displacement = np.sqrt(combine_displacement) * building.elf_parameters['Cd'] \
                                    * self.scaling_factors['drift']

    def save_results(self, building):
        os.chdir(building.directory['building data'])
        # This is the floor displacement obtained from modal equations
        header = ['mode %i' % (mode+1) for mode in range(self.number_of_mode)]
        df1 = pd.DataFrame(data=np.array(np.transpose(self.mode_displacement)), columns=header)
        df1.to_csv('RSAEquationDisplacement.csv', sep=',', index=False)

        # This is the floor displacement obtained from OpenSees analysis results
        OpenSeesDisplacement = np.zeros([self.number_of_mode, building.geometry['number of story']])
        for mode in range(self.number_of_mode):
            dir = building.directory['building elastic model'] / ('EarthquakeLoad%i' % mode) / 'NodeDisplacements'
            os.chdir(dir)
            for story in range(0, building.geometry['number of story']):
                file_name = 'NodeDisplacementLevel%i.out' % (story+2)
                read_data = pd.read_csv(file_name, header=None, sep=' ')
                # The last element of 2nd column is the lateral displacement
                OpenSeesDisplacement[mode, story] = read_data.iloc[-1, 1]
        self.OpenSeesDisplacement = OpenSeesDisplacement
        os.chdir(building.directory['building data'])
        df2 = pd.DataFrame(data=np.array(np.transpose(self.OpenSeesDisplacement)),
                           columns=header)
        df2.to_csv('OpenSeesDisplacement.csv', sep=',', index=False)

        # This is the relative floor displacement (i.e. story drift) from modal equations
        relative_displacement = np.zeros([self.number_of_mode, building.geometry['number of story']])
        for mode in range(self.number_of_mode):
            for story in range(building.geometry['number of story']):
                if story == 0:
                    relative_displacement[mode, story] = self.mode_displacement[mode, story]
                else:
                    relative_displacement[mode, story] = self.mode_displacement[mode, story] \
                                                         - self.mode_displacement[mode, story-1]
        os.chdir(building.directory['building data'])
        df3 = pd.DataFrame(data=np.array(np.transpose(relative_displacement)), columns=header)
        df3.to_csv('RSAEquationRelativeDisplacement.csv', sep=',', index=False)

        # This is the relative floor displacement (i.e., story drift) from OpenSees result.
        OpenSees_relative_displacement = np.zeros([self.number_of_mode, building.geometry['number of story']])
        for mode in range(self.number_of_mode):
            for story in range(building.geometry['number of story']):
                if story == 0:
                    OpenSees_relative_displacement[mode, story] = self.OpenSeesDisplacement[mode, story]
                else:
                    OpenSees_relative_displacement[mode, story] = self.OpenSeesDisplacement[mode, story] \
                                                         - self.OpenSeesDisplacement[mode, story-1]
        os.chdir(building.directory['building data'])
        df4 = pd.DataFrame(data=np.array(np.transpose(OpenSees_relative_displacement)), columns=header)
        df4.to_csv('OpenSeesRelativeDisplacement.csv', sep=',', index=False)

        # This is the story drift ratio from OpenSees output
        OpenSeesStoryDriftRatio = np.zeros([self.number_of_mode, building.geometry['number of story']])
        for mode in range(self.number_of_mode):
            dir = building.directory['building elastic model'] / ('EarthquakeLoad%i' % mode) / 'StoryDrifts'
            os.chdir(dir)
            for story in range(0, building.geometry['number of story']):
                file_name = 'Story%i.out' % (story + 1)
                read_data = pd.read_csv(file_name, header=None, sep=' ')
                # The last element of 2nd column is the lateral displacement
                OpenSeesStoryDriftRatio[mode, story] = read_data.iloc[-1, 1]
        self.OpenSeesStoryDriftRatio = OpenSeesStoryDriftRatio
        os.chdir(building.directory['building data'])
        df5 = pd.DataFrame(data=np.array(np.transpose(self.OpenSeesStoryDriftRatio)),
                           columns=header)
        df5.to_csv('OpenSeesStoryDriftRatio.csv', sep=',', index=False)

        # This is the finalized floor displacement from OpenSees.
        df6 = pd.DataFrame(data=np.array(self.final_RSA_responses['floor displacement']), columns=['Floor displacement'])
        df6.to_csv('RSACombinedFloorDisplacement.csv', sep=',', index=False)

        # This is the finalized story drift ratio from OpenSees
        df7 = pd.DataFrame(data=np.array(self.final_RSA_responses['story drift']),
                           columns=['Story drift'])
        df7.to_csv('RSACombinedStoryDrift.csv', sep=',', index=False)

        # This is the finalized story shear forces
        df8 = pd.DataFrame(data=np.array(self.final_RSA_responses['story shear']),
                           columns=['Story shear'])
        df8.to_csv('RSACombinedStoryShear.csv', sep=',', index=False)

        # This is the story shear force under each mode
        df5 = pd.DataFrame(data=np.array(np.transpose(self.story_shears)),
                           columns=header)
        df5.to_csv('RSAStoryShear.csv', sep=',', index=False)

