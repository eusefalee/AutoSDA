# Define gravity live loads


# Assign uniform beam dead load values (kip/inch)
set	BeamDeadLoadFloor2	0.023833; 
set	BeamDeadLoadFloor3	0.023167; 
set	BeamDeadLoadFloor4	0.023167; 
set	BeamDeadLoadFloor5	0.039833; 

# Assign uniform beam live load values (kip/inch)
set	BeamLiveLoadFloor2	0.035000; 
set	BeamLiveLoadFloor3	0.035000; 
set	BeamLiveLoadFloor4	0.035000; 
set	BeamLiveLoadFloor5	0.010000; 

# Assign point dead load values on leaning column: kip
set	LeaningColumnDeadLoadFloor2	4983.000000; 
set	LeaningColumnDeadLoadFloor3	4983.000000; 
set	LeaningColumnDeadLoadFloor4	4983.000000; 
set	LeaningColumnDeadLoadFloor5	4985.000000; 

# Assign point live load values on leaning column (kip)
set	LeaningColumnLiveLoadFloor2	3906.000000; 
set	LeaningColumnLiveLoadFloor3	3906.000000; 
set	LeaningColumnLiveLoadFloor4	3906.000000; 
set	LeaningColumnLiveLoadFloor5	1116.000000; 

# Assign lateral load values caused by earthquake (kip)
set	LateralLoad	[list	31.327915	72.053689	119.400314	171.755711];


# Define uniform loads on beams
# Load combinations:
# 101 Dead load only
# 102 Live load only
# 103 Earthquake load only
# 104 Gravity and earthquake (for calculation of drift)
pattern	Plain	103	Linear	{

load	121	[lindex $LateralLoad 0] 0.0 0.0;	# Level2
load	131	[lindex $LateralLoad 1] 0.0 0.0;	# Level3
load	141	[lindex $LateralLoad 2] 0.0 0.0;	# Level4
load	151	[lindex $LateralLoad 3] 0.0 0.0;	# Level5

}
# puts "Earthquake load defined"