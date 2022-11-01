from curses import nonl
from genericpath import isfile
from http.client import SEE_OTHER
from re import S
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

# Define top level directory
topLevelDirectory = os.getcwd()

def onlineParamLookup(latitude,longitude,siteClass,riskCat):
    """
    Function that accesses the seismicmaps.org website and looks up the seismic
    design parameters using ASCE 7-16
    """

    # Use Chrome to access web
    options = webdriver.ChromeOptions()
    options.add_argument('headless') # navigate website in background w/o opening a window
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

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
    if lfrsType == 'steelmf':
        # For steelSDA:
        # R is always 8, x is always 0.8, Ct is always 0.028,
        # Cd always 5.5 and rho is always 1.0
        Cd = 5.5; R = 8; rho = 1; Ct = 0.028; x = 0.8
    elif lfrsType == 'woodframe':
        pass
    elif lfrsType == 'rcwall':
        pass
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
    
    # Read in building-specific inputs from excel file
    filePath = Path(
        "BuildingInfo",
        "Building_" + str(buildingData['BuildingID'].item()) + ".xlsx"
        )
    buildingInfo = pd.ExcelFile(filePath)

    if buildingData['LFRS'].item() == 'steelmf':

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
        mainPath = Path("Modules","woodSDA")

    elif buildingData['LFRS'].item() == 'rcwall':
        mainPath = Path("Modules","RCWallSDA")


    # Return to main directory
    os.chdir(topLevelDirectory)


def runSDA(lfrsType,id):
    """
    Function to execute the necessary module for design and analysis
    """

    # Determine module based on lfrs type
    if lfrsType == 'steelmf':
        module = 'steelSDA'
        funcExecute = 'run_AutoSDA'
    elif lfrsType == 'woodframe':
        module = 'woodSDA'
    elif lfrsType == 'rcwall':
        module = 'RCWallSDA'

    os.chdir(Path("Modules",module))
    run(["python3 -c 'from main_program import " + str(funcExecute) + "; " + 
    str(funcExecute) + "([" + str(id) + "])'"],shell=True)



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
    
    elif lfrsType == 'woodframe':
        pass
    elif lfrsType == 'rcwall':
        pass


    # List of data sources
    fileSources = [outDataSource,elasticModelSource,nonlinModelSource]

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
                shutil.copytree(origin, dest)




