# This file is used to exchange the data from Google drive and AutoSDA
# Developed by GUAN, XINGQUAN @ UCLA in Sept. 2020

import pathlib
import numpy as np
import os
import pandas as pd

from global_variables import base_directory
from main_program import run_AutoSDA

# Define the IDs for the building that will be analyzed
IDs = range(141, 150+1)
# IDs = range(11, 20+1)
# IDs = range(21, 30+1)
# IDs = range(31, 40+1)

run_AutoSDA(IDs)

# # The following path points to where the Google Drive shared folder is located on your PC
# data_exchange_directory = pathlib.Path('C:\\Users\\Guan\\Google Drive')
#
# # Define a limit for iteration times
# iteration_limit = 10
#
# # Keep reading R factor
# GLOBAL_COUNT = 0
# while True:
#     # Go into where the exchanged data is stored
#     os.chdir(data_exchange_directory)
#     R_file_name = 'R_' + str(GLOBAL_COUNT) + '.txt'
#     flag_file_name = 'Flag_' + str(GLOBAL_COUNT) + '.txt'
#     # Determine whether the new files for R factor and Flag exist or not
#     if os.path.exists(R_file_name) and os.path.exists(flag_file_name):
#         R_factor = np.loadtxt(R_file_name)
#         Flag = (pd.read_csv(flag_file_name, header=None)).values.item()
#         # Current R is the optimal value
#         if Flag:
#             break
#         # Current R is not the optimal value
#         else:
#             # Call AutoSDA to run the simulation
#             R_factor_1 = R_factor[0]
#             R_factor_2 = R_factor[1]
#             building_1, postprocess_results_1, steel_weight_1 = run_AutoSDA(IDs, R_factor_1)
#             building_2, postprocess_results_2, steel_weight_2 = run_AutoSDA(IDs, R_factor_2)
#
#             # Write the performance results back to google drive
#             os.chdir(data_exchange_directory)
#             ACMR_file_name = 'ACMR_' + str(GLOBAL_COUNT) + '.txt'
#             steel_weight_file_name = 'SteelWeight_' + str(GLOBAL_COUNT) + '.txt'
#             ACMR_summary = np.array([postprocess_results_1.performance_metrics['ACMR'],
#                                      postprocess_results_2.performance_metrics['ACMR']])
#             steel_weight_summary = np.array([steel_weight_1, steel_weight_2])
#             np.savetxt(ACMR_file_name, ACMR_summary)
#             np.savetxt(steel_weight_file_name, steel_weight_summary)
#
#             # Update the iteration counter
#             GLOBAL_COUNT += 1
#     # If next R and Flag files are not available: optimization algorithm is still running and I should wait
#     else:
#         continue
#     # If the iteration exceeds a certain number of times (e.g, 500). The analysis should be terminated since
#     # we don't wanna get into an infinite loop.
#     if GLOBAL_COUNT >= iteration_limit:
#         break
