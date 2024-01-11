##############################################################################################################################
# 	RunIDAtoCollapse														                             		             #
#	This module runs incremental dynamic analyses for a given model for a specified number of ground motions to collapse     #
# 														             														 #
# 	Created by: Henry Burton, Stanford University, October 7, 2012									                         #
#   Revised by: Xingquan Guan, University of California, Los Angeles, April 2019                                             #
#								     						                                                                 #
# 	Units: kips, inches, seconds                                                                                             #
##############################################################################################################################

# Clear all memory 
wipe all;

# Ground motion scales to run
set allScales **intensityScales**;

# Scale factor is required in order to anchor median ground motion Sa to MCE level
set MCEScaleFactor **SaMCEFactor**;

# Define the total number of ground motions
set numGMs 1;

# Define the total number of models for dynamic analysis
set numModels 1;

# Define the building models' names (the name of the building model folder)
set modelNames [list **buildingID**]

# Defining a variable to record the stating time
set AllStartTime [clock seconds];

# Set the root directory
set rootDir [pwd];

# Set the data output directory name
set dataDir IDAOutput

# Initializing processor information
set np [getNP];  # Getting the number of processors
set pid [getPID];  # Getting the processor ID number

# Setting up a vector of ground motion IDs
set groundMotionIDs {}; 
set numberOfGroundMotionIDs $numGMs; 
for {set gm 1} {$gm <= $numberOfGroundMotionIDs} {incr gm} {
	lappend groundMotionIDs $gm
}
puts "Ground motion ID's defined"

# Setting up a vector with the number of steps in each ground motion record
set groundMotionNumPoints {}; 
set pathToTextFile $rootDir/GroundMotionInfo;
set groundMotionNumPointsFile [open $pathToTextFile/GMNumPoints.txt r];
while {[gets $groundMotionNumPointsFile line] >= 0} {
	lappend groundMotionNumPoints $line;
}
close $groundMotionNumPointsFile;
puts "Ground motion number of steps defined"

# Setting up a vector with the names for each ground motion record txt file
set eqFileName {};
set eqFile [open $pathToTextFile/GMFileNames.txt r];
while {[gets $eqFile line] >= 0} {
	lappend eqFileName $line;
}
close $eqFile
puts "Ground motion file names defined"

# Setting up a vector with the time step for each ground motion record
set groundMotionTimeStep {}; 
set groundMotionTimeStepFile [open $pathToTextFile/GMTimeSteps.txt r];
while {[gets $groundMotionTimeStepFile line] >= 0} {
	lappend groundMotionTimeStep $line;
}
close $groundMotionTimeStepFile;
puts "Ground motion time steps defined"

# Total number of analysis for al models
set numSimulations [expr $numGMs*$numModels];

# Define a series of integers to denote the number of each simulation
set RunIDs {}; 
for {set ID 0} {$ID < $numSimulations} {incr ID} {
	lappend RunIDs $ID
} 
puts "Routine ID's defined"

# The following line is used in Hoffman2
# set globalCounter [lindex $argv 0];

# The following line is used to test the file on loca machine using ordinary OpenSees
# set globalCounter 1;

# The following line is used to run OpenSees on local machine using OpenSeesMP
# set globalCounter [expr $pid+1];
# set groundMotionNumber $globalCounter

# The number of GMs per core
# set numGMsPerCore [expr $numGMs/$np];
# set globalCounter {};
# for {set gmCore [expr $pid*$numGMsPerCore+1]} {$gmCore <= [expr ($pid+1)*$numGMsPerCore]} {incr gmCore} {
	# lappend globalCounter $gmCore
# }

# The following line is used to run OpenSeesMP with generic algorithm to assign the cores
# The alogirthms: N analyses assigned to K cores
# The first N%K cores take N/K+1 analyses whereas the rest take N/K analyses
set firstNumGMsPerCore [expr $numGMs/$np+1];
set typicalNumGMsPerCore [expr $numGMs/$np];
if {$pid < [expr $numGMs%$np]} {
	set startGM [expr $pid*$firstNumGMsPerCore+1];
	set endGM [expr ($pid+1)*$firstNumGMsPerCore]
} else {
	set startGM [expr ($numGMs%$np)*$firstNumGMsPerCore+($pid-$numGMs%$np)*$typicalNumGMsPerCore+1];
	set endGM [expr ($numGMs%$np)*$firstNumGMsPerCore+($pid-$numGMs%$np)*$typicalNumGMsPerCore+$typicalNumGMsPerCore];
}

for {set gmCore $startGM} {$gmCore <= $endGM} {incr gmCore} {
	lappend globalCounter $gmCore
}

# Each global counter corresponds to one building subjected to one ground motion
for {set modelIndex 0} {$modelIndex < $numModels} {incr modelIndex} {
	# Define the base folder for each model
	set baseDir "$rootDir/[lindex $modelNames $modelIndex]/DynamicAnalysis"
	
	
	foreach groundMotionNumber $globalCounter {
	#if {[expr {$groundMotionNumber % $np}] == $pid} {
		set eqNumber $groundMotionNumber;
		set dt [lindex $groundMotionTimeStep [expr $groundMotionNumber - 1]];
		set numPoints [lindex $groundMotionNumPoints [expr $groundMotionNumber - 1]];

		# Run IDA until maximum scale is reached
		foreach scale $allScales {	
			cd $baseDir
			source Model.tcl
			wipe;
		}
		
		puts "********************************"
		puts "Current ModelIndex: $modelIndex."
		puts "Current GMIndex: $eqNumber."
		puts "********************************"
		
	#	}
	#}
}