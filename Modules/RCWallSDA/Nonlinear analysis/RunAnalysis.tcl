# Clear all memory 
wipe all;

# Set the root directory
set rootDir [pwd];

# Reading Ground Motion names
set fp1 [open "allGMname.txt" r];
set allGMname [read $fp1];
close $fp1;
puts "Ground motion names defined"

# Reading Ground Motion time intervals
set fp2 [open "allGMdt.txt" r];
set allGMdt [read $fp2];
close $fp2;
puts "Ground motion time intervals defined"

# Reading Ground Motion number of steps
set fp3 [open "allGMnumOfSteps.txt" r];
set allGMnumOfSteps [read $fp3];
close $fp3;
puts "Ground motion number of steps defined"

# Reading Ground Motion scale factor
set fp4 [open "allGMsf.txt" r];
set allGMsf [read $fp4];
close $fp4;
puts "Ground motion scale factors defined"

# Define the buildings IDS
set buildingID {}
set buildingIDFile [open BuildingIDs.txt r];
while {[gets $buildingIDFile line] >= 0} {
	set name Building_$line
	lappend buildingID $name
}
puts "Building IDs defined"


# Define the total number of models for nonlinear analysis
set numModels [llength $buildingID];
	 
#set globalCounter [lindex $argv 0];  # Use this line if you run OpenSees/OpenSeesMP on Hoffman2
set globalCounter 1;  # Use this line if you test the program on your PC. [this is the GM number]


# Each glorbal counter corresponds to one building subjected to one ground motion
for {set modelIndex 0} {$modelIndex < $numModels} {incr modelIndex} {
	# Define the base folder for each model
	set baseDir "$rootDir/[lindex $buildingID $modelIndex]"
	cd $baseDir

	set GMname [lindex $allGMname [expr $globalCounter - 1]];
	puts "Current Ground Motion name is: $GMname";

	set GMdt [lindex $allGMdt [expr $globalCounter - 1]];
	puts "Time increment of current ground motion is: $GMdt";

	set GMnumOfSteps [lindex $allGMnumOfSteps [expr $globalCounter - 1]];
	puts "The number of steps for current Ground Motion is: $GMnumOfSteps";

	set GMsf [lindex $allGMsf [expr $globalCounter - 1]];
	puts "The scale factor for current Ground Motion is: $GMsf";

	# Creating the model, applying gravity load and running for dynamic analysis

	# Setting Up directories
	set dataDirName GM$globalCounter;
	cd $baseDir
	file mkdir $dataDirName;

	source dynamic_analysisSolver.tcl;
	
	wipe;
	
	puts "********************************"
	puts "Current ModelIndex: $modelIndex."
	puts "********************************"
	
}
