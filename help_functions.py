from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pathlib import Path
import os
from subprocess import run
import shutil
import glob

# Define top level directory
topLevelDirectory = os.getcwd()


# Write these functions as part of a class???

def onlineParamLookup(latitude,longitude,siteClass,riskCat):
    """
    Function that accesses the seismicmaps.org website and looks up the seismic
    design parameters using ASCE 7-16
    """

    # Use Chrome to access web
    options = webdriver.ChromeOptions()
    options.add_argument('headless') # navigate website in background w/o opening a window
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    
    print("webdriver created")
    # Open seismic maps website
    driver.get('https://www.seismicmaps.org/')

    # Select ASCE Version 7-16:
    versionSelector = Select(driver.find_element(By.ID,'dcrd'))
    versionSelector.select_by_value('asce7-16')

    # Select Risk Category
    riskSelector = Select(driver.find_element(By.ID,'risk-category'))
    riskSelector.select_by_value(riskCat)

    # Select Site Class
    siteClassSelector = Select(driver.find_element(By.ID,'site-class'))
    siteClassSelector.select_by_value(siteClass)

    # Choose to search by coordinates
    searchTypeButton=driver.find_element(By.XPATH,
    "//label[@class='btn btn-secondary']")
    searchTypeButton.click()

    # Inputs latitude and longitude coordinates
    latCoord = driver.find_element(By.XPATH,
    "//input[@class='form-control input-group input-coords input-latitude']")
    latCoord.send_keys(latitude)

    lonCoord = driver.find_element(By.XPATH,
    "//input[@class='form-control input-group input-coords input-longitude']")
    lonCoord.send_keys(longitude)

    # Click "Go"
    goButton = driver.find_element(By.XPATH,
    "//button[@class='btn btn-primary searchbutton']")
    goButton.click()

    # Fetch the resulting tables
    tables = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "table")))
    df1 = pd.read_html(tables[1].get_attribute('outerHTML'))[0]
    df2 = pd.read_html(tables[2].get_attribute('outerHTML'))[0]
    allParams = pd.concat([df1,df2],axis=0,ignore_index=True)
    allParams['Type'] = allParams['Type'].replace(['SS'],'Ss')
    seismicLocParams = allParams.iloc[[0,1,12],[0,1]]

    return seismicLocParams



def nonLocParamLookup(lfrsType,riskCat):
    """
    Function that defines the non-location based parameters
    """

    # Determine Ie based on Table 1.5-2 in ASCE 7-16
    if riskCat == "I" or riskCat == "II":
        Ie = 1
    elif riskCat == "III":
        Ie = 1.25
    elif riskCat == "IV":
        Ie = 1.5
    else:
        raise Exception('Not a valid risk category, choose I,II,III, or IV')

    # Determine Cd, R, rho, Ct, and x based on LFRS
    # ASCE 7-16 Table 12.2-1
    if lfrsType == 'steelmf':
        # For steelSDA:
        # R is always 8, x is always 0.8, Ct is always 0.028,
        # Cd always 5.5 and rho is always 1.0
        Cd = 5.5; R = 8; rho = 1; Ct = 0.028; x = 0.8
    elif lfrsType == 'woodframe':
        return
    elif lfrsType == 'rcwall':
        Cd = 5; R = 5; rho = 1.3; Ct = 0.02; x = 0.75
    else:
        raise Exception('Not a supported LFRS type, please enter "steelmf", "woodframe", or "rcwall"')

    data = {'Type':['Cd','R','Ie','rho','Ct','x'], 'Value':[Cd,R,Ie,rho,Ct,x]}
    seismicNonLocParams = pd.DataFrame(data)

    return seismicNonLocParams



def writeFiles(buildingData, seismicParams):
    """
    Function to create the necessary files and directories for the corresponding
    module for each building
    """
    print("writing files")
    # Read in building-specific inputs from excel file


    if buildingData['LFRS'].item() == 'steelmf':

        filePath = Path(
            "BuildingInfo",
            "Building_" + str(buildingData['BuildingID'].item()) + ".xlsx"
            )
        buildingInfo = pd.ExcelFile(filePath)

        # Get required inputs from buildingInfo file
        geometry = pd.read_excel(buildingInfo, "Geometry")
        loads = pd.read_excel(buildingInfo, "Loads")
        memDepth = pd.read_excel(buildingInfo, "Member Depth")

        # Create a folder for the building in the BuildingData folder of steelSDA
        mainPath = Path(
            "Modules",
            "steelSDA",
            "BuildingData",
            "Building_" + str(buildingData['BuildingID'].item())
            )
        os.makedirs(mainPath, exist_ok=True)
        os.chdir(mainPath)

        # Insert site class for ELFParameters.csv file compatibility with steelSDA
        siteclass = pd.DataFrame({"Type": 'site class', "Value": buildingData['Site Class'].item()},index=[7])
        elfParams = pd.concat(
            [seismicParams.iloc[:7],
            siteclass,
            seismicParams.iloc[7:]]).set_index('Type').T

        # Write csv files in folder
        geometry.to_csv('Geometry.csv',index=False)
        loads.to_csv('Loads.csv',index=False)
        memDepth.to_csv('MemberDepth.csv',index=False)
        elfParams.to_csv('ELFParameters.csv',index=False)

    elif buildingData['LFRS'].item() == 'woodframe':

        topLevelFolder = Path("BuildingInfo", "Building_" + str(buildingData['BuildingID'].item()))
        print("top level building folder defined as ", topLevelFolder)
        mainPath = Path("Modules",
                        "woodSDA",
                        "BuildingInfo",
                        "Building_" + str(buildingData['BuildingID'].item()))
        print("main path defined as ",mainPath)
        os.makedirs(mainPath,exist_ok=True)

        # Copy the entire input folder from the top level building info directory to the woodSDA building info
        shutil.copytree(topLevelFolder,mainPath,dirs_exist_ok=True)
        os.chdir(mainPath)

    elif buildingData['LFRS'].item() == 'rcwall':
        filePath = Path(
        "BuildingInfo",
        "Building_" + str(buildingData['BuildingID'].item()) + ".xlsx"
        )
        buildingInfo = pd.ExcelFile(filePath)
        # Read input file
        geometry = pd.read_excel(buildingInfo,header = None).T
        geometry.columns = ['Type', 'Value']

        # Define path to input files
        mainPath = Path("Modules","RCWallSDA")
        os.chdir(mainPath)

        # Combine seismic params and other inputs for compatibility with rcwallsda
        siteclass = pd.DataFrame({"Type": 'site class', "Value": buildingData['Site Class'].item()},index=[3])
        buildingID = pd.DataFrame({"Type": 'Building ID', "Value": buildingData['BuildingID'].item()},index=[0])
        elfParams = pd.concat([buildingID,seismicParams,siteclass,geometry]).T
        elfParams.rename(columns={"SS": "$S_s$"})
        
        # Write inputs to excel file in rcwallsda folder
        elfParams.to_excel("input.xlsx", index = False,header=None)


    # Return to main directory
    os.chdir(topLevelDirectory)



# def selectGroundMotions(GMIDs,lfrsType):
#     """
#     Function to select and apply user specified ground motions to model
#     """

#     # Should the IDA scales match for each module?

#     # Locate master ground motion folder
#     allGMsFolder = Path("GMs")
#     allHistories = Path(allGMsFolder, "Histories")
#     allInfo = Path(allGMsFolder,"GroundMotionInfo") 
    
#     # Initialize variables to store GMInfo
#     GMFileNames = []
#     GMNumPoints = []
#     GMTimeSteps = []

#     # GM source files from top level directory
#     srcfile = Path(allHistories, str(GMIDs[newid]) + ".txt")
#     numpointsFile = open(Path(allInfo, "GMNumPoints.txt"))
#     timeStepsFile = open(Path(allInfo, "GMTimeSteps.txt"))


#     # steelSDA
#     if lfrsType == 'steelmf':

#         steelHistories = Path("Modules","steelSDA","BuildingNonlinearModels","Histories")
#         steelInfo = Path("Modules","steelSDA","BuildingNonlinearModels","GoundMotionInfo")

#         # Deleting the previous history files
#         files = glob.glob(steelHistories + '/*')
    
#         for f in files:os.remove(f)

#         # Get the GM IDs from main input excel file
#         newid = 0 # Assigns new IDs in ascending order to the selected ground motions
#         for id in GMIDs:

#             # Copy Histories and rename/reindex
#             dstfile = Path(steelHistories, str(newid) + ".txt")
#             shutil.copy2(srcfile,dstfile)

#             # Get NumPoints and TimeSteps for current GM            
#             numpoints = numpointsFile.read(id)
#             timesteps = timeStepsFile.read(id)

#             # Create lists for writing to GMInfo files
#             GMFileNames.append(newid)
#             GMTimeSteps.append(timesteps)
#             GMNumPoints.append(numpoints)

#             newid += 1
        
#         # Write to GMInfo files
#         with open(Path(steelInfo, "GMNumPoints.txt"),'w') as f, open(Path(steelInfo, "GMTimeSteps.txt"),'w') as g:
#             f.write(GMNumPoints)
#             g.write(GMTimeSteps)

#             # OR change the code to use an array of IDs
    
#     # woodSDA
#     if lfrsType == 'woodframe':

#         woodHistories = Path("Modules","woodSDA","BuildingNonlinearModels","Histories")
#         woodInfo = Path("Modules","woodSDA","BuildingNonlinearModels","GoundMotionInfo")

#         files = glob.glob(woodHistories + '/*')

#         dstfile = Path(woodHistories, str(newid) + ".txt")
#         shutil.copy2(srcfile,dstfile) 

#         # Deleting the previous history files
#         files = glob.glob(steelHistories + '/*')
    
#         for f in files:os.remove(f)

#         # Get the GM IDs from main input excel file
#         newid = 0 # Assigns new IDs in ascending order to the selected ground motions       
#         pass

#         # May need a similar process to steelSDA. Either assign new IDs or rewrite code

#     if lfrsType == 'rcwall':
#         pass
#         # rcwallSDA
#         # May be okay. Can use as template for other two modules.
#         # May only need to modify the scales

#     pass

def selectGroundMotions(GMIDs,lfrsType):
    """
    Function to select and apply user specified ground motions to model
    """

    # Should the IDA scales match for each module?
    print("Enter GM function")

    # Locate master ground motion folder
    allGMsFolder = Path(topLevelDirectory,"GMs")
    allHistories = Path(allGMsFolder, "Histories")
    allInfo = Path(allGMsFolder,"GroundMotionInfo") 

    # if GMIDs == "all":
    #     GMIDs = os.listdir(allHistories)
    
    # Initialize variables to store GMInfo
    GMFileNames = []
    GMNumPoints = []
    GMTimeSteps = []

    # GM source files from top level directory
    numpointsFile = open(Path(allInfo, "GMNumPoints.txt"))
    timeStepsFile = open(Path(allInfo, "GMTimeSteps.txt"))

     # Get NumPoints and TimeSteps          
    numpoints = numpointsFile.read().split('\n')
    timesteps = timeStepsFile.read().split('\n')
    numpointsFile.close()
    timeStepsFile.close()

    print("Source files defined")
    # Select path to copy GM files to based on LFRS-type
    # steelSDA
    if lfrsType == 'steelmf':

        print("Steel directories defined")
        dstHistories = Path(topLevelDirectory,"Modules","steelSDA","BuildingNonlinearModels","Histories")
        dstInfo = Path(topLevelDirectory,"Modules","steelSDA","BuildingNonlinearModels","GroundMotionInfo")
    
    # woodSDA
    elif lfrsType == 'woodframe':

        dstHistories = Path(topLevelDirectory,"Modules","woodSDA","BuildingModels","GM_sets","Histories")
        dstInfo = Path(topLevelDirectory,"Modules","woodSDA","BuildingModels","GM_sets","GroundMotionInfo")

    elif lfrsType == 'rcwall':
        pass
        # rcwallSDA
        # May be okay. Can use as template for other two modules.
        # May only need to modify the scales
    
    # Deleting the previous history files
    [f.unlink() for f in Path(dstHistories).glob("*") if f.is_file()] 
    print("Previous files deleted")

    # Get the GM IDs from main input excel file
    newid = 1 # Assigns new IDs in ascending order to the selected ground motions
    for id in GMIDs:

        # Copy Histories and rename/reindex
        srcfile = Path(allHistories, str(id) + ".txt")
        dstfile = Path(dstHistories, str(newid) + ".txt")
        with open(dstfile, 'w'): pass
        shutil.copy2(srcfile,dstfile)

        # Create lists for writing to GMInfo files
        GMFileNames.append(str(newid) + ".txt")
        GMTimeSteps.append(timesteps[id-1])
        GMNumPoints.append(numpoints[id-1])

        newid += 1

    # Write to GMInfo files
    with open(Path(dstInfo, "GMNumPoints.txt"),'w') as f, open(Path(dstInfo, "GMTimeSteps.txt"),'w') as g, open(Path(dstInfo, "GMFileNames.txt"),'w') as h:
        f.write("\n".join(GMNumPoints))
        g.write("\n".join(GMTimeSteps))
        h.write("\n".join(GMFileNames))

    return "Ground Motions Defined for Submodule"

def runSDA(lfrsType,id):
    """
    Function to execute the necessary module for design and analysis
    """

    # Determine module based on lfrs type
    if lfrsType == 'steelmf':
        module = 'steelSDA'
        mainProgram = 'main_program.py'
        # funcExecute = 'run_AutoSDA'
    elif lfrsType == 'woodframe':
        module = 'woodSDA\Codes'
        mainProgram = 'woodSDA_driver.py'
    elif lfrsType == 'rcwall':
        module = 'RCWallSDA'
        # funcExecute = 'run_rcwallsda'
        mainProgram = 'main_design.py'

    # Execute submodule
    os.chdir(Path("Modules",module))
    os.system("python " + mainProgram + " " + str(id))
    # run(["python " + mainProgram],shell=True)
    # run(["python -c 'from " + mainProgram + " import " + str(funcExecute) + "; " + str(funcExecute) +
    #       "([" + str(id) + "])'"],shell=True)



def getOutputs(lfrsType,id):
    """
    Function that copies the output files from the modules to a folder in the
    top level
    """
    buildingFolder = "Building_" + str(id)

    # Determine module based on lfrs type
    if lfrsType == 'steelmf':

        # Locate output data
        outDataSource = Path("BuildingData",buildingFolder)
        elasticModelSource = Path("BuildingElasticModels",buildingFolder)
        nonlinModelSource = Path("BuildingNonlinearModels",buildingFolder)

        # List of data sources
        fileSources = [outDataSource,elasticModelSource,nonlinModelSource]

    elif lfrsType == 'woodframe':
        pass
    elif lfrsType == 'rcwall':
        outDataSource = os.getcwd()
        nonlinModelSource = Path('Nonlinear analysis')

        # List of data sources
        fileSources = [outDataSource,nonlinModelSource]

    # Define destination folder location
    destination = Path("..","..","Outputs",buildingFolder)

    # Make the directory
    os.makedirs(destination, exist_ok=True)

    # loop over source directories
    for sources in fileSources:

        # List the files in the current source directory
        files = os.listdir(sources)

        # Copy the files into destination directory
        for file in files:
            origin = Path(sources,file)
            dest = Path(destination,file)

            if os.path.isfile(origin):
                shutil.copy2(origin,dest)
            else:
                shutil.copytree(origin, dest,dirs_exist_ok=True)


def clean(cmd):
    """
    Function to clean the module subdirectories
    """
    
    if cmd == "no":
        return
    elif cmd == "yes":
        pass
    else:
        raise Exception("Invalid selection: Choose 'yes' or 'no'")

