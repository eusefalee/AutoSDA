"""
Created by: Muneera Aladsani - UCLA

Last edit: Oct 24 2022

"""

from designClasses import *

def designWall14(inputfile):
    
    building_ID = inputfile['Building ID'].to_numpy()
    
    b_value = []
    story_sbeList = []
    story_obeList = []   
    lbeList = []
    A_tribList = []
    A_trib_leancolList = []
    SccList = []
    colsList = []
    spacing_web_tList = []
    spacing_web_lList = []
    n_bars_layerList = []
    ratio_web_tList = []
    ratio_web_lList = []
    ratio_be_t_sbeList = []
    ratio_be_t_obeList = []
    ratio_be_lList = []
    spacing_be_t_sbeList = []
    spacing_be_t_obeList = []
    
    for n in range(0,len(building_ID)):
        
        Ss = inputfile['Ss'].to_numpy()[n]
        S1 = inputfile['S1'].to_numpy()[n]
        site_class = inputfile['site class'].to_numpy()[n]
        TL = inputfile['TL'].to_numpy()[n]
        Building_length = inputfile['Building length'].to_numpy()[n]
        Building_width = inputfile['Building width'].to_numpy()[n]
        N_length = inputfile['number of parallel bays'].to_numpy()[n]
        N_width = inputfile['number of perpendicular bays'].to_numpy()[n]
        num_story = inputfile['number of story'].to_numpy()[n]
        first_story = inputfile['first story height'].to_numpy()[n]
        typical_story = inputfile['typical story height'].to_numpy()[n]
        DL_floor = inputfile['floor dead load'].to_numpy()[n]
        DL_roof = inputfile['roof dead load'].to_numpy()[n]
        LL_floor = inputfile['floor live load'].to_numpy()[n]
        LL_roof = inputfile['roof live load'].to_numpy()[n]
        fc = inputfile['fc'].to_numpy()[n]
        concrete_type = inputfile['concrete type'].to_numpy()[n]
        cc = inputfile['concrete cover'].to_numpy()[n]
        fy = inputfile['fy'].to_numpy()[n]
        A_bar1 = inputfile['area of bar 1'].to_numpy()[n]
        A_bar2 = inputfile['area of bar 2'].to_numpy()[n]
        R = inputfile['R'].to_numpy()[n]
        Ie = inputfile['Ie'].to_numpy()[n]
        Cd = inputfile['Cd'].to_numpy()[n]
        rho = inputfile['rho'].to_numpy()[n]
        allow_story_drift = inputfile['allowable story drift'].to_numpy()[n]
        lw = inputfile['wall length'].to_numpy()[n]
        b = inputfile['initial thickness'].to_numpy()[n]
        num_walls = inputfile['number of walls'].to_numpy()[n]
        edge_wall = inputfile['edge wall'].to_numpy()[n]
        
        #Check 25.7.2.2
        if (A_bar1 <= 1.27 and A_bar2 < 0.11):
            raise ValueError('Error - A_bar2 cannot be < 0.11 (25.7.2.2)')

        if (A_bar1 >= 1.56 and A_bar2 < 0.20):
            raise ValueError('Error - A_bar2 cannot be < 0.20 (25.7.2.2)')
        
        error = 1 #To start the while loop
        
        while error == 1:
            
            
            building = WallDesign14(Building_length,Building_width,DL_floor,DL_roof,LL_floor,LL_roof,num_story,N_length,N_width,first_story,typical_story,Ss,S1,site_class,TL,
                     lw,b,fc,num_walls,edge_wall,R,Ie,Cd,fy,rho,concrete_type,cc,A_bar1,A_bar2)
            
            building.iteration = 0
            building.shear_strength()
            building.pm_interc()
            building.na_depth
            building.boundary_element()
    
            
            while building.lbe < max(building.na_depth-0.1*building.lw , building.na_depth/2):
                building.iteration = 1
                max_value = max(building.na_depth-0.1*building.lw , building.na_depth/2)
                building.lbe = np.ceil(max_value) 
                building.Scc = (building.lbe-2*building.cc)/(building.cols-1)
                building.shear_strength()
                building.pm_interc()
                building.na_depth
                building.boundary_element()
                
                while building.error_hx == 1:
                    building.iteration = 1
                    cols = 1 + ((building.lbe-2*building.cc)/building.hx_min)
                    building.cols = np.ceil(cols)
                    building.Scc = (building.lbe-2*building.cc)/(building.cols-1)
                    building.shear_strength()
                    building.pm_interc()
                    building.na_depth
                    building.boundary_element()
    
            
            while building.error_hx == 1:
                building.iteration = 1
                cols = 1 + ((building.lbe-2*building.cc)/building.hx_min)
                building.cols = np.ceil(cols)
                building.Scc = (building.lbe-2*building.cc)/(building.cols-1)
                building.shear_strength()
                building.pm_interc()
                building.na_depth
                building.boundary_element()
                
                while building.lbe < max(building.na_depth-0.1*building.lw , building.na_depth/2):
                    building.iteration = 1
                    max_value = max(building.na_depth-0.1*building.lw , building.na_depth/2)
                    building.lbe = np.ceil(max_value) 
                    building.Scc = (building.lbe-2*building.cc)/(building.cols-1)
                    building.shear_strength()
                    building.pm_interc()
                    building.na_depth
                    building.boundary_element()
    
    
            # Check moment and shear variables
            Mu = building.Mu
            PhiMn5 = building.phiMn
            PhiMn7 = building.phiMn7
            
            if PhiMn5 < Mu :
                error = 1
            elif PhiMn7 < Mu :
                error = 1
            elif building.error_shear == 1:
                error = 1
            else:
                error = 0
            
            # Check story drifts
            storyDrifts = []
            for i in range (0, building.num_story):
                myfile = open(Path("GravityEarthquake","StoryDrifts","Story%s.out" %(i+1)), "r") #ELF
                #myfile = open("EarthquakeLoad\\StoryDrifts\\Story%s.out" %(i+1), "r") #RSA
                lst = list(myfile.readlines())
                myfile.close()
                lastline = lst[len(lst)-1]
                intStart = lastline.find('1') + 2
                sub = lastline[intStart:]
                intEnd = sub.find('\n')
                finalvalue = sub[0:intEnd] #linear story drifts
                storyDrifts.append(float(finalvalue) * building.Cd / building.Ie) #nonlinear story drifts
            
            for i in storyDrifts:
                if i >= allow_story_drift:
                    error = 1
                    
            #Check 18.10.6.4(b)
            if building.SBE_db == 1:
                if b < (min(first_story,typical_story)*12)/16:
                    error = 1
            
            if error == 1:
                b += 1
    
            
        b_value.append(b)
        story_sbeList.append(building.story_sbe)
        story_obeList.append(building.story_obe)
        lbeList.append(building.lbe)
        A_tribList.append(building.A_trib)
        A_trib_leancolList.append(building.A_trib_leancol)
        colsList.append(building.cols)
        SccList.append(building.Scc)
        spacing_web_tList.append(building.spacing_web)
        spacing_web_lList.append(building.spacing_web)
        n_bars_layerList.append(building.n_bars_layer)
        ratio_web_tList.append(building.ratio_web_t)
        ratio_web_lList.append(building.ratio_web_l)
        ratio_be_t_sbeList.append(building.ratio_be_t_sbe)
        ratio_be_t_obeList.append(building.ratio_be_t_obe)
        ratio_be_lList.append(building.ratio_be_l)
        spacing_be_t_sbeList.append(building.spacing_be_t_sbe)
        spacing_be_t_obeList.append(building.spacing_be_t_obe)
                
                
    pd.DataFrame({'Building ID':building_ID,'b_value':b_value,'story_sbe':story_sbeList,
                  'story_obe':story_obeList,'lbe':lbeList,'A_trib':A_tribList,
                  'A_trib_leancol':A_trib_leancolList,'cols':colsList,'Scc':SccList,
                  'spacing_web_t':spacing_web_tList, 'spacing_web_l':spacing_web_lList,
                  'n_bars_layer':n_bars_layerList,'ratio_web_t':ratio_web_tList,
                  'ratio_web_l':ratio_web_lList, 'ratio_be_t_sbe':ratio_be_t_sbeList,
                  'ratio_be_t_obe':ratio_be_t_obeList,'ratio_be_l':ratio_be_lList,
                  'spacing_be_t_sbe':spacing_be_t_sbeList,'spacing_be_t_obe':spacing_be_t_obeList}).to_csv('Design Results.csv')      
    
    
    # Delete elastic analysis files (not needed)
    f = open("EAFilesNames.txt", "r")
    temp = f.read().splitlines()
    f.close()
    
    def remove(path):
        if os.path.isfile(path):
            os.remove(path)  # remove file
        elif os.path.isdir(path):
            shutil.rmtree(path)  # remove dir and all contains

    for x in temp:
        remove(x)


def designWall19(inputfile):
    
    building_ID = inputfile['Building ID'].to_numpy()
    
    b_value = []
    story_sbeList = []
    story_obeList = []   
    lbeList = []
    A_tribList = []
    A_trib_leancolList = []
    SccList = []
    colsList = []
    spacing_web_tList = []
    spacing_web_lList = []
    n_bars_layerList = []
    ratio_web_tList = []
    ratio_web_lList = []
    ratio_be_t_sbeList = []
    ratio_be_t_obeList = []
    ratio_be_lList = []
    spacing_be_t_sbeList = []
    spacing_be_t_obeList = []
    
    for n in range(0,len(building_ID)):
        
        Ss = inputfile['Ss'].to_numpy()[n]
        S1 = inputfile['S1'].to_numpy()[n]
        site_class = inputfile['site class'].to_numpy()[n]
        TL = inputfile['TL'].to_numpy()[n]
        Building_length = inputfile['Building length'].to_numpy()[n]
        Building_width = inputfile['Building width'].to_numpy()[n]
        N_length = inputfile['number of parallel bays'].to_numpy()[n]
        N_width = inputfile['number of perpendicular bays'].to_numpy()[n]
        num_story = inputfile['number of story'].to_numpy()[n]
        first_story = inputfile['first story height'].to_numpy()[n]
        typical_story = inputfile['typical story height'].to_numpy()[n]
        DL_floor = inputfile['floor dead load'].to_numpy()[n]
        DL_roof = inputfile['roof dead load'].to_numpy()[n]
        LL_floor = inputfile['floor live load'].to_numpy()[n]
        LL_roof = inputfile['roof live load'].to_numpy()[n]
        fc = inputfile['fc'].to_numpy()[n]
        concrete_type = inputfile['concrete type'].to_numpy()[n]
        cc = inputfile['concrete cover'].to_numpy()[n]
        fy = inputfile['fy'].to_numpy()[n]
        A_bar1 = inputfile['area of bar 1'].to_numpy()[n]
        A_bar2 = inputfile['area of bar 2'].to_numpy()[n]
        R = inputfile['R'].to_numpy()[n]
        Ie = inputfile['Ie'].to_numpy()[n]
        Cd = inputfile['Cd'].to_numpy()[n]
        rho = inputfile['rho'].to_numpy()[n]
        allow_story_drift = inputfile['allowable story drift'].to_numpy()[n]
        lw = inputfile['wall length'].to_numpy()[n]
        b = inputfile['initial thickness'].to_numpy()[n]
        num_walls = inputfile['number of walls'].to_numpy()[n]
        edge_wall = inputfile['edge wall'].to_numpy()[n]
        
        #Check 25.7.2.2
        if (A_bar1 <= 1.27 and A_bar2 < 0.11):
            raise ValueError('Error - A_bar2 cannot be < 0.11 (25.7.2.2)')

        if (A_bar1 >= 1.56 and A_bar2 < 0.20):
            raise ValueError('Error - A_bar2 cannot be < 0.20 (25.7.2.2)')
        
        error = 1 #To start the while loop
        
        while error == 1:
            
            
            building = WallDesign19(Building_length,Building_width,DL_floor,DL_roof,LL_floor,LL_roof,num_story,N_length,N_width,first_story,typical_story,Ss,S1,site_class,TL,
                     lw,b,fc,num_walls,edge_wall,R,Ie,Cd,fy,rho,concrete_type,cc,A_bar1,A_bar2)
            
            building.iteration = 0
            building.shear_strength()
            building.pm_interc()
            building.na_depth
            building.boundary_element()
    
            
            while building.lbe < max(building.na_depth-0.1*building.lw , building.na_depth/2):
                building.iteration = 1
                max_value = max(building.na_depth-0.1*building.lw , building.na_depth/2)
                building.lbe = np.ceil(max_value) 
                building.Scc = (building.lbe-2*building.cc)/(building.cols-1)
                building.shear_strength()
                building.pm_interc()
                building.na_depth
                building.boundary_element()
                
                while building.error_hx == 1:
                    building.iteration = 1
                    cols = 1 + ((building.lbe-2*building.cc)/building.hx_min)
                    building.cols = np.ceil(cols)
                    building.Scc = (building.lbe-2*building.cc)/(building.cols-1)
                    building.shear_strength()
                    building.pm_interc()
                    building.na_depth
                    building.boundary_element()
    
            
            while building.error_hx == 1:
                building.iteration = 1
                cols = 1 + ((building.lbe-2*building.cc)/building.hx_min)
                building.cols = np.ceil(cols)
                building.Scc = (building.lbe-2*building.cc)/(building.cols-1)
                building.shear_strength()
                building.pm_interc()
                building.na_depth
                building.boundary_element()
                
                while building.lbe < max(building.na_depth-0.1*building.lw , building.na_depth/2):
                    building.iteration = 1
                    max_value = max(building.na_depth-0.1*building.lw , building.na_depth/2)
                    building.lbe = np.ceil(max_value) 
                    building.Scc = (building.lbe-2*building.cc)/(building.cols-1)
                    building.shear_strength()
                    building.pm_interc()
                    building.na_depth
                    building.boundary_element()
    
    
            # Check moment and shear variables
            Mu = building.Mu
            PhiMn5 = building.phiMn
            PhiMn7 = building.phiMn7
            
            if PhiMn5 < Mu :
                error = 1
            elif PhiMn7 < Mu :
                error = 1
            elif building.error_shear == 1:
                error = 1
            else:
                error = 0
            
            # Check story drifts
            storyDrifts = []
            for i in range (0, building.num_story):
                myfile = open(Path("GravityEarthquake","StoryDrifts","Story%s.out" %(i+1)), "r") #ELF
                #myfile = open("EarthquakeLoad\\StoryDrifts\\Story%s.out" %(i+1), "r") #RSA
                lst = list(myfile.readlines())
                myfile.close()
                lastline = lst[len(lst)-1]
                intStart = lastline.find('1') + 2
                sub = lastline[intStart:]
                intEnd = sub.find('\n')
                finalvalue = sub[0:intEnd] #linear story drifts
                storyDrifts.append(float(finalvalue) * building.Cd / building.Ie) #nonlinear story drifts
            
            for i in storyDrifts:
                if i >= allow_story_drift:
                    error = 1
                    
            #Check 18.10.6.4(b)
            if building.SBE_db == 1:
                if b < (min(first_story,typical_story)*12)/16:
                    error = 1
            
            #Check minimum longitudinal reinforcement shear
            if building.error_miniratio == 1:
                error = 1
                
            #Check 18.10.6.2(b-ii)
            if building.SBE_db == 1:
                if b < building.bmin:
                    error = 1
            
            if error == 1:
                b += 1
    
            
        b_value.append(b)
        story_sbeList.append(building.story_sbe)
        story_obeList.append(building.story_obe)
        lbeList.append(building.lbe)
        A_tribList.append(building.A_trib)
        A_trib_leancolList.append(building.A_trib_leancol)
        colsList.append(building.cols)
        SccList.append(building.Scc)
        spacing_web_tList.append(building.spacing_web_t)
        spacing_web_lList.append(building.spacing_web_l)
        n_bars_layerList.append(building.n_bars_layer)
        ratio_web_tList.append(building.ratio_web_t)
        ratio_web_lList.append(building.ratio_web_l)
        ratio_be_t_sbeList.append(building.ratio_be_t_sbe)
        ratio_be_t_obeList.append(building.ratio_be_t_obe)
        ratio_be_lList.append(building.ratio_be_l)
        spacing_be_t_sbeList.append(building.spacing_be_t_sbe)
        spacing_be_t_obeList.append(building.spacing_be_t_obe)
                
                
    pd.DataFrame({'Building ID':building_ID,'b_value':b_value,'story_sbe':story_sbeList,
                  'story_obe':story_obeList,'lbe':lbeList,'A_trib':A_tribList,
                  'A_trib_leancol':A_trib_leancolList,'cols':colsList,'Scc':SccList,
                  'spacing_web_t':spacing_web_tList, 'spacing_web_l':spacing_web_lList,
                  'n_bars_layer':n_bars_layerList,'ratio_web_t':ratio_web_tList,
                  'ratio_web_l':ratio_web_lList, 'ratio_be_t_sbe':ratio_be_t_sbeList,
                  'ratio_be_t_obe':ratio_be_t_obeList,'ratio_be_l':ratio_be_lList,
                  'spacing_be_t_sbe':spacing_be_t_sbeList,'spacing_be_t_obe':spacing_be_t_obeList}).to_csv('Design Results.csv')     
    
    
    # Delete elastic analysis files (not needed)
    f = open("EAFilesNames.txt", "r")
    temp = f.read().splitlines()
    f.close()
    
    def remove(path):
        if os.path.isfile(path):
            os.remove(path)  # remove file
        elif os.path.isdir(path):
            shutil.rmtree(path)  # remove dir and all contains

    for x in temp:
        remove(x)

