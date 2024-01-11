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


# Load combinations:
# 101 Dead load only
# 102 Live load only
# 103 Earthquake load only
# 104 Gravity and earthquake (for calculation of drift)
pattern	Plain	104	Constant	{# Define uniform loads on beams

# Level2
eleLoad	-ele	2121221	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor2 - 0.5*$BeamLiveLoadFloor2]; 
eleLoad	-ele	2221321	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor2 - 0.5*$BeamLiveLoadFloor2]; 
eleLoad	-ele	2321421	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor2 - 0.5*$BeamLiveLoadFloor2]; 
eleLoad	-ele	2421521	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor2 - 0.5*$BeamLiveLoadFloor2]; 
eleLoad	-ele	2521621	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor2 - 0.5*$BeamLiveLoadFloor2]; 
eleLoad	-ele	2621721	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor2 - 0.5*$BeamLiveLoadFloor2]; 
eleLoad	-ele	2721821	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor2 - 0.5*$BeamLiveLoadFloor2]; 
eleLoad	-ele	2821921	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor2 - 0.5*$BeamLiveLoadFloor2]; 

# Level3
eleLoad	-ele	2131231	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor3 - 0.5*$BeamLiveLoadFloor3]; 
eleLoad	-ele	2231331	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor3 - 0.5*$BeamLiveLoadFloor3]; 
eleLoad	-ele	2331431	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor3 - 0.5*$BeamLiveLoadFloor3]; 
eleLoad	-ele	2431531	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor3 - 0.5*$BeamLiveLoadFloor3]; 
eleLoad	-ele	2531631	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor3 - 0.5*$BeamLiveLoadFloor3]; 
eleLoad	-ele	2631731	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor3 - 0.5*$BeamLiveLoadFloor3]; 
eleLoad	-ele	2731831	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor3 - 0.5*$BeamLiveLoadFloor3]; 
eleLoad	-ele	2831931	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor3 - 0.5*$BeamLiveLoadFloor3]; 

# Level4
eleLoad	-ele	2141241	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor4 - 0.5*$BeamLiveLoadFloor4]; 
eleLoad	-ele	2241341	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor4 - 0.5*$BeamLiveLoadFloor4]; 
eleLoad	-ele	2341441	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor4 - 0.5*$BeamLiveLoadFloor4]; 
eleLoad	-ele	2441541	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor4 - 0.5*$BeamLiveLoadFloor4]; 
eleLoad	-ele	2541641	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor4 - 0.5*$BeamLiveLoadFloor4]; 
eleLoad	-ele	2641741	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor4 - 0.5*$BeamLiveLoadFloor4]; 
eleLoad	-ele	2741841	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor4 - 0.5*$BeamLiveLoadFloor4]; 
eleLoad	-ele	2841941	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor4 - 0.5*$BeamLiveLoadFloor4]; 

# Level5
eleLoad	-ele	2151251	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor5 - 0.5*$BeamLiveLoadFloor5]; 
eleLoad	-ele	2251351	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor5 - 0.5*$BeamLiveLoadFloor5]; 
eleLoad	-ele	2351451	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor5 - 0.5*$BeamLiveLoadFloor5]; 
eleLoad	-ele	2451551	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor5 - 0.5*$BeamLiveLoadFloor5]; 
eleLoad	-ele	2551651	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor5 - 0.5*$BeamLiveLoadFloor5]; 
eleLoad	-ele	2651751	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor5 - 0.5*$BeamLiveLoadFloor5]; 
eleLoad	-ele	2751851	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor5 - 0.5*$BeamLiveLoadFloor5]; 
eleLoad	-ele	2851951	-type	-beamUniform	[expr -(1.2+0.2*1.59)*$BeamDeadLoadFloor5 - 0.5*$BeamLiveLoadFloor5]; 


# Define point loads on leaning column
load	9102	0	[expr -(1.2+0.2*1.59)*$LeaningColumnDeadLoadFloor2 -0.5*$LeaningColumnLiveLoadFloor2]	0;
load	9103	0	[expr -(1.2+0.2*1.59)*$LeaningColumnDeadLoadFloor3 -0.5*$LeaningColumnLiveLoadFloor3]	0;
load	9104	0	[expr -(1.2+0.2*1.59)*$LeaningColumnDeadLoadFloor4 -0.5*$LeaningColumnLiveLoadFloor4]	0;
load	9105	0	[expr -(1.2+0.2*1.59)*$LeaningColumnDeadLoadFloor5 -0.5*$LeaningColumnLiveLoadFloor5]	0;

# Define earthquake lateral loads
load	121	[lindex $LateralLoad 0]	0.0	0.0;	# Level2
load	131	[lindex $LateralLoad 1]	0.0	0.0;	# Level3
load	141	[lindex $LateralLoad 2]	0.0	0.0;	# Level4
load	151	[lindex $LateralLoad 3]	0.0	0.0;	# Level5


}
# puts "Gravity and earthquake loads defined"