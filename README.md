# Automated Seismic Design and Analysis Platform (AutoSDA)

An end-to-end computation tool to automate seismic design and analysis for steelframe, woodframe, and RCWall buildings

&nbsp;

### Implementation
AutoSDA interfaces three previously developed programs for design and analysis by including them as submodules. AutoSDA was originally developed by (Guan et al 2020) as a steelframe building design and analysis platform. woodSDA developed by (Dahal et al 2021) for woodframe buildings and RCWall-SDA was developed by (Aladsani et al 2022) for reinforced concrete wall design. 

&nbsp;

### Pre-requisites

The Open System for Earthquake Engineering Simulation (OpenSees) is required in order to run AutoSDA. Install OpenSees into a folder called 'OpenSees' in the top-level folder of AutoSDA. The subfolders within should be the 'bin' and 'lib' folders, where the bin folder contains the executable and the lib folder contains an "init.tcl" file. i.e folder structures should follow: AutoSDA/OpenSees/bin/OpenSees and AutoSDA/OpenSees/lib/init.tcl

** It is not required, but reccommended that you first create and activate a virtual environment before installing the python dependencies below. 

In terminal, navigate to the AutoSDA folder and type "pip install -r requirements.txt", all of the necessary python dependencies will automatically be installed. This only needs to be performed once. If you create a virtual environment, remember to activate it for each new session.

&nbsp;

### Running the program

The Templates folder contains the template files for the inputs to each of the 3 submodules that are necessary for them to run. Only the steelTemplate.xlsx, woodTemplate.xlsx, and rcwallTemplate.xlsx files need to be copied and filled out. The templates within the subfolders named after the modules are just to show an example of what the modules see once they are run.

The main_program.py file can then be used to run the program and the output design and analysis files will be located in the Outputs folder after the program is finished running. Seismic design parameters do not need to be provided, as they are looked up by the code on seismicmaps.org website.
