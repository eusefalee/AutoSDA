# SDRlimitTester ########################################################################
#
# Procedure that checks if the Pre-Specified Collapse Drift Limit is reached and Generate 
# a Flag
#
# Developed by Dimitrios G. Lignos, Ph.D
# Modified  by Ahmed Elkady, Ph.D
#
# First Created: 04/20/2010
# Last Modified: 05/05/2020
#
# Modified by Muneera: 04/07/2022
#
# #######################################################################################

proc DriftLimitTester {numStories SDRlimit FloorNodes h1 htyp} {

 global CollapseFlag
 set CollapseFlag "NO"
 
 global CollapseFlagReader
 
	 # Read the Floor Node Displacements and Deduce the Story Drift Ratio
	 for {set i 0} {$i<=$numStories-1} {incr i} {
		if { $i==0 } {
			set Node [lindex $FloorNodes $i]
			set NodeDisplI [nodeDisp $Node 1]
			set SDR [expr $NodeDisplI/$h1]
			lappend Drift [list $SDR]
			
		} elseif { $i > 0 } {
			set NodeI [lindex $FloorNodes $i]
			set NodeDisplI [nodeDisp $NodeI 1]
			set NodeJ [lindex $FloorNodes [expr $i-1]]
			set NodeDisplJ [nodeDisp $NodeJ 1]
			set SDR [expr ($NodeDisplI - $NodeDisplJ)/$htyp]
			lappend Drift [list  $SDR]

		}
	 } 
	 
	# Check if any Story Drift Ratio Exceeded the Drift Limit	 
	for {set i 0} {$i <= $numStories-1} {incr i} {
	    set TDrift [ lindex $Drift [expr $i] ]
		set TDrift [expr abs($TDrift)]
		
		# IF the Story Drift Ratio at Current Story is Less than the Drift Limit then
		# Open a file named "CollapseState.txt" and write a value of "0" for no collapse
		if {$TDrift < $SDRlimit} {
			set CollapseFlagReader 0;                # Write value of 0 in case of no collapse 
		}
		
		# If Drift Limit was exceeded
		if { $TDrift > $SDRlimit} {
			set CollapseFlag "YES"
			puts "Collapse"
			set CollapseFlagReader 1;                # Write value of 1 in case of collapse
		}
	}
}
