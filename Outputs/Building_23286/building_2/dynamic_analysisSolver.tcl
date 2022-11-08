# ----------------------------------------------------------------
# Dynamic Time-History Analysis
# ----------------------------------------------------------------

# Perform modal analysis
source Modal.tcl
source Solver.tcl

# First, set gravity loads acting constant and time in domain to 0.0
	loadConst -time 0.0

# Define ground motion parameters
	cd $rootDir
	set GMfile "GMfiles/$GMname.txt";				# Ground motion filename, input is in g units
	set DtSeries	$GMdt;							# time-step Dt for definition of time series
	set NSteps 		$GMnumOfSteps;					# Number of steps in ground motion

# Define ground motion parameters
	set patternID 2;								# Load pattern ID
	set GMdirection 1;								# Ground motion direction (1 = x)
	set Scalefactor [expr $GMsf*$g];				# Ground motion scaling factor

	set DtAnalysis	[expr $GMdt/2.0];				# time-step Dt for lateral analysis
	set TmaxAnalysis [expr $DtSeries*$NSteps];		# maximum duration of ground-motion analysis -- should be 50*$sec

# Define the acceleration series for the ground motion
	# Command: "Series -dt $timestep_of_record -filePath $filename_with_acc_history -factor $scale_record_by_this_amount"
	set accelSeries "Series -dt $DtSeries -filePath $GMfile -factor $Scalefactor";

# Create load pattern: apply acceleration to all fixed nodes with UniformExcitation
	# Command: pattern UniformExcitation $patternID $GMdir -accel $timeSeriesID 
	pattern UniformExcitation $patternID $GMdirection -accel $accelSeries;

	puts "GM parameters and acceleration series defined."

	wipeAnalysis; # destroy all components of the Analysis object


set FloorNodes [list 102 104 106 108 110 112 114 116];
set firstTimeCheck [clock seconds];

# To be able to source DriftLimitTester.tcl within the "DynamicAnalysisCollapseSolver"
cd $baseDir 

DynamicAnalysisCollapseSolver  $DtSeries $DtAnalysis $TmaxAnalysis $NumStories 0.2 $FloorNodes $FirstStory $TypicalStory $firstTimeCheck


###################################################################################################
###################################################################################################
							puts "Ground Motion Done. End Time: [getTime]"
###################################################################################################
###################################################################################################
