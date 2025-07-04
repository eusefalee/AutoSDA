# DynamicAnalysisCollapseSolver #########################################################
#
# This Solver is used for Collapse "hunting"
# Time Controlled Algorithm that keeps original run
#
# Developed by Dimitrios G. Lignos, Ph.D
#
# First Created: 04/20/2010
# Last Modified: 08/23/2011
#
# Modified by Muneera: 04/07/2022
#
# Uses:
# 1. dt            : Ground Motion step
# 2. dt_anal_Step  : Analysis time step
# 3. GMtime        : Ground Motion Total Time
# 4. numStories    : DriftLimit
# 
# Subroutines called:
# DriftLimitTester: Checks after loss of convergence the drifts 
#                 and guarantees convergence for collapse
#
# Integrator Used: Modified Implicit: Hilbert Hughes Taylor with Increment Reduction
# #######################################################################################

proc DynamicAnalysisCollapseSolver {dt dt_anal_Step GMtime numStories SDRlimit FloorNodes h1 htyp StartTime} {
 
global CollapseFlag;                                        # global variable to monitor collapse
set CollapseFlag "NO"

wipeAnalysis

constraints Plain
numberer RCM
system UmfPack
test EnergyIncr 1.0e-3 100
algorithm KrylovNewton
integrator Newmark 0.50 0.25
analysis Transient

set maxRunTime 14400;
set startT [clock seconds];

set NumSteps [expr round(($GMtime + 0.0)/$dt_anal_Step)];	# number of steps in analysis
set ok [analyze $NumSteps $dt_anal_Step];

# Check Max Drifts for Collapse by Monitoring the CollapseFlag Variable
source DriftLimitTester.tcl;
DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp


if  {$CollapseFlag == "YES"} {
	set ok 0
	puts "----> Collapse Occured";
}

# Check run time to see if it is in excess of maximum allotted time
set currentT [clock seconds];
set runTime [expr $currentT - $startT];
if  {$runTime > $maxRunTime} {
	set ok 0
}

# If analysis failed
 if {$ok != 0} {
	puts "Analysis did not converge..."
	# The analysis will be time-controlled and is done for the remaining time
	set ok 0;
	set controlTime [getTime];
	
	# While the GM did not finish OR while analysis is failing
	while {$controlTime < $GMtime || $ok !=0 } {
		DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp
		if  {$CollapseFlag == "YES"} {
			set ok 0; break;
		} else {
			set ok 1
		}
		# Check run time to see if it is in excess of maximum allotted time
		set currentT [clock seconds];
		set runTime [expr $currentT - $startT];
		if  {$runTime > $maxRunTime} {
			set ok 0; break;
		}	
		
	    # Get Control Time inside the loop
		set controlTime [getTime]
		puts "----> Currently at time $controlTime out of $GMtime"

		if {$ok != 0} {
			puts "Run Newton 100 steps with 1/2 of step.."
			set controlTime [getTime]
			set remainTime [expr $GMtime - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_anal_Step/2.0))]

			test EnergyIncr 1.0e-3 100   0
			algorithm KrylovNewton
			integrator Newmark 0.50 0.25
			set ok [analyze 10 [expr $dt_anal_Step/2.0]]
			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}
		if {$ok != 0 } {		
			puts "Go Back to KrylovNewton with tangent Tangent and original step.."
			set controlTime [getTime]
			set remainTime [expr $GMtime - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_anal_Step))]
			
			test EnergyIncr 1.0e-2 100   0
			algorithm KrylovNewton
			integrator Newmark 0.50 0.25
			set ok [analyze $NewRemainSteps [expr $dt_anal_Step]]
			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}
		if {$ok != 0 } {
			puts "Run 10 steps KrylovNewton with Initial Tangent with 1/2 of original step.."
			set controlTime [getTime]
			set remainTime [expr $GMtime - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_anal_Step/2.0))]
			test EnergyIncr 1.0e-2 200 0	
			algorithm KrylovNewton -initial
			set ok [analyze 10 [expr $dt_anal_Step/2.0]]
			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}
		if {$ok != 0 } {			
			puts "Go Back to KrylovNewton with tangent Tangent and original step.."
			set controlTime [getTime]
			set remainTime [expr $GMtime - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_anal_Step))]
			test EnergyIncr 1.0e-2 100   0
			algorithm KrylovNewton
			integrator Newmark 0.50 0.25
			set ok [analyze $NewRemainSteps [expr $dt_anal_Step]]
			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}			

		if {$ok != 0 } {	
			puts "Go Back to KrylovNewton with tangent Tangent and 0.001 step.."
			set controlTime [getTime]
			set remainTime [expr $GMtime - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/(0.001))]
			test EnergyIncr 1.0e-2 200   0
			algorithm KrylovNewton
			integrator Newmark 0.50 0.25
			set ok [analyze $NewRemainSteps [expr 0.001]]
			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}				
		if {$ok != 0 } {
			puts "KrylovNewton Initial with 1/2 of step and Displacement Control Convergence.."
			test EnergyIncr 1.0e-2 100  0
			algorithm KrylovNewton -initial
			set ok [analyze 10 [expr $dt_anal_Step/2.0]]
			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}
		if {$ok != 0 } {	
			puts "Go Back to KrylovNewton with tangent Tangent and 0.0001 step.."
			set controlTime [getTime]
			set remainTime [expr $GMtime - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/(0.0001))]
			test EnergyIncr 1.0e-2 100   0
			algorithm KrylovNewton
			integrator Newmark 0.50 0.25
			set ok [analyze 5 [expr 0.0001]]
			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}		

		if {$ok != 0 } {	
			puts "Go Back to KrylovNewton with tangent Tangent and original step.."
			set controlTime [getTime]
			set remainTime [expr $GMtime - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/($dt_anal_Step))]
			test EnergyIncr 1.0e-2 100   0
			algorithm KrylovNewton
			integrator Newmark 0.50 0.25
			set ok [analyze $NewRemainSteps [expr $dt_anal_Step]]
			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}	
		}		
		if {$ok != 0 } {
			puts "Newton with Fixed Number of Iterations else continue"
			set controlTime [getTime]
			set remainTime [expr $GMtime - $controlTime]
			set NewRemainSteps [expr round(($remainTime)/(0.0001))]
			puts $NewRemainSteps
			test FixedNumIter 50
			integrator NewmarkHSFixedNumIter 0.5 0.25

			algorithm Newton

			set ok [analyze 10 [expr 0.0001]]
			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp
			if  {$CollapseFlag == "YES"} {
				set ok 0
			}
			# Check run time to see if it is in excess of maximum allotted time
			set currentT [clock seconds];
			set runTime [expr $currentT - $startT];
			if  {$runTime > $maxRunTime} {
				set ok 0; break;
			}				
		}	
		set controlTime [getTime]

	}
 }
global recordcontrolTime
set recordcontrolTime [getTime]	
}
