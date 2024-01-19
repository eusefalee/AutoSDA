"""
Created by: Muneera Aladsani - UCLA

Previous edit: Dec 4 2021
Last edit: Oct 22 2022

"""

from genericpath import exists
import numpy as np
import pandas as pd
import os
from NLRHA_tclfiles import *
from pathlib import Path

def createNLRHAfiles(inputfile,designfile):
    original_folder = os.getcwd()
    nonlinear_folder = Path(original_folder,"Nonlinear analysis")
    
    # Obtain number of ground motions
    os.chdir(nonlinear_folder)
    f = open("allGMname.txt", "r")
    temp = f.read().splitlines()
    f.close()
    numGM = len(temp)

    building_ID = designfile['Building ID'].to_numpy()  
    
    for n in range(0,len(building_ID)):
        
        Building_length = inputfile['Building length'].to_numpy()[n]
        Building_width = inputfile['Building width'].to_numpy()[n]
        N_length = inputfile['number of parallel bays'].to_numpy()[n]
        N_width = inputfile['number of perpendicular bays'].to_numpy()[n]
        num_story = inputfile['number of story'].to_numpy()[n]
        first_story = inputfile['first story height'].to_numpy()[n]
        typical_story = inputfile['typical story height'].to_numpy()[n]
        DL_floor = inputfile['floor dead load'].to_numpy()[n] * inputfile['bias - DL'].to_numpy()[n]
        DL_roof = inputfile['roof dead load'].to_numpy()[n] * inputfile['bias - DL'].to_numpy()[n]
        LL_floor = inputfile['floor live load'].to_numpy()[n] * inputfile['bias - LL'].to_numpy()[n]
        LL_roof = inputfile['roof live load'].to_numpy()[n] * inputfile['bias - LL'].to_numpy()[n]
        fc = inputfile['fc'].to_numpy()[n] * inputfile['bias - fc'].to_numpy()[n]
        cc = inputfile['concrete cover'].to_numpy()[n]
        fy = inputfile['fy'].to_numpy()[n] * inputfile['bias - fy'].to_numpy()[n]
        A_bar1 = inputfile['area of bar 1'].to_numpy()[n]
        A_bar2 = inputfile['area of bar 2'].to_numpy()[n]
        lw = inputfile['wall length'].to_numpy()[n]
        b = designfile['b_value'].to_numpy()[n]
        lbe = designfile['lbe'].to_numpy()[n]
        cols = designfile['cols'].to_numpy()[n]
        ratio_web_t = designfile['ratio_web_t'].to_numpy()[n]
        ratio_web_l = designfile['ratio_web_l'].to_numpy()[n]
        ratio_be_t_sbe = designfile['ratio_be_t_sbe'].to_numpy()[n]
        ratio_be_t_obe = designfile['ratio_be_t_obe'].to_numpy()[n]
        ratio_be_l = designfile['ratio_be_l'].to_numpy()[n]
        spacing_be_t_sbe = designfile['spacing_be_t_sbe'].to_numpy()[n]
        spacing_be_t_obe = designfile['spacing_be_t_obe'].to_numpy()[n]
        story_sbe = designfile['story_sbe'].to_numpy()[n]
        story_obe = designfile['story_obe'].to_numpy()[n]
        A_trib = designfile['A_trib'].to_numpy()[n]
        A_trib_leancol = designfile['A_trib_leancol'].to_numpy()[n]
        n_bars_layer = designfile['n_bars_layer'].to_numpy()[n]
        
        Ec = 57*np.sqrt(fc*1000)
        W_typical = (DL_floor * Building_length * Building_width) / 1000
        W_roof = (DL_roof * Building_length * Building_width) / 1000
        
    
        # Calculations for building concrete material
        
        #Confined concrete (Change & Mander 1998)
        Scc_x = (lbe - 2*cc) / (cols - 1)
        Scc_y = (b - 2*cc) / (n_bars_layer - 1)
        bc_x = (cols -1) * Scc_x + np.sqrt(4*A_bar1/3.14159) + np.sqrt(4*A_bar2/3.14159)
        bc_y = b - 2 * cc + np.sqrt(4*A_bar1/3.14159) + np.sqrt(4*A_bar2/3.14159)
        s_sbe = spacing_be_t_sbe
        s_obe = spacing_be_t_obe
        s_sbe_clear = s_sbe - np.sqrt(4*A_bar2/3.14159)
        s_obe_clear = s_obe - np.sqrt(4*A_bar2/3.14159)
        n_x = 2*(cols - 1)
        n_y = 2*(n_bars_layer - 1)
        w_x = Scc_x - np.sqrt(4*A_bar1/3.14159)
        w_y = Scc_y - np.sqrt(4*A_bar1/3.14159)
        
        #SBE
        Ae = ((bc_x*bc_y) - n_x*(w_x**2 / 6) - n_y*(w_y**2 / 6)) * (1-(s_sbe_clear/(2*bc_x))) * (1-(s_sbe_clear/(2*bc_y)))
        Acc = (bc_x*bc_y) - (cols*n_bars_layer*A_bar1)
        ke = Ae / Acc
        fl_x = ke * ((n_bars_layer*A_bar2) / (s_sbe*bc_y)) * fy
        fl_y = ke * ((cols*A_bar2) / (s_sbe*bc_x)) * fy
        
        if fl_x < fl_y:
            r = fl_x/fl_y
        else:
            r = fl_y/fl_x
            
        x_bar = (fl_x+fl_y) / (2*fc)
        A = 6.8886 - (0.6069+17.275*r)*np.exp(-4.989*r)
        B = (4.5 / ((5/A) * (0.9849 - 0.6306 * np.exp(-3.8939*r))  - 0.1)) - 5
        k1 = A * (0.1+0.9/(1+b*x_bar))
        k2 = 5*k1
        fl = (fl_x+fl_y) / 2
        fcc_sbe = fc + k1*fl
        epsc0_sbe = 0.002 * (1+k2*x_bar)
        
        #OBE
        w_y = Scc_y - np.sqrt(4*A_bar1/3.14159)
        Ae = ((bc_x*bc_y) - n_x*(w_x**2 / 6) - n_y*(w_y**2 / 6)) * (1-(s_obe_clear/(2*bc_x))) * (1-(s_obe_clear/(2*bc_y)))
        Acc = (bc_x*bc_y) - (cols*n_bars_layer*A_bar1)
        ke = Ae / Acc
        fl_x = ke * ((n_bars_layer*A_bar2) / (s_obe*bc_y)) * fy
        fl_y = ke * ((cols*A_bar2) / (s_obe*bc_x)) * fy
        
        if fl_x < fl_y:
            r = fl_x/fl_y
        else:
            r = fl_y/fl_x
            
        x_bar = (fl_x+fl_y) / (2*fc)
        A = 6.8886 - (0.6069+17.275*r)*np.exp(-4.989*r)
        B = (4.5 / ((5/A) * (0.9849 - 0.6306 * np.exp(-3.8939*r))  - 0.1)) - 5
        k1 = A * (0.1+0.9/(1+b*x_bar))
        k2 = 5*k1
        fl = (fl_x+fl_y) / 2
        fcc_obe = fc + k1*fl
        epsc0_obe = 0.002 * (1+k2*x_bar)
    
        building_nonlinear = NRHA_tclfiles(DL_floor,DL_roof,LL_floor,LL_roof,num_story,first_story,typical_story,story_sbe,story_obe,lw,b,lbe,W_typical,W_roof,Ec,fy,A_trib,A_trib_leancol,
                      fc,fcc_sbe,epsc0_sbe,fcc_obe,epsc0_obe,ratio_web_t,ratio_web_l,ratio_be_t_sbe,ratio_be_t_obe,ratio_be_l,numGM)
        
        
        #Create and open corresponsing folder
        building_folder = Path(nonlinear_folder,'building_'+str(building_ID[n]))
        os.makedirs(building_folder, exist_ok = True)
        os.chdir(building_folder)
        
        building_nonlinear.run_OpenSees()
        
        os.chdir(original_folder)
        
