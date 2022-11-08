# Define expected gravity loads


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

# Assign point live load values on leaning column: kip
set	LeaningColumnLiveLoadFloor2	3906.000000; 
set	LeaningColumnLiveLoadFloor3	3906.000000; 
set	LeaningColumnLiveLoadFloor4	3906.000000; 
set	LeaningColumnLiveLoadFloor5	1116.000000; 

# Define uniform loads on beams
# Load combinations:
# 104 Expected gravity loads: 1.05 DL + 0.25 LL
pattern	Plain	104	Constant	{

# Level2
eleLoad	-ele	2121221	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor2 - 0.25*$BeamLiveLoadFloor2];
eleLoad	-ele	2221321	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor2 - 0.25*$BeamLiveLoadFloor2];
eleLoad	-ele	2321421	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor2 - 0.25*$BeamLiveLoadFloor2];
eleLoad	-ele	2421521	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor2 - 0.25*$BeamLiveLoadFloor2];
eleLoad	-ele	2521621	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor2 - 0.25*$BeamLiveLoadFloor2];
eleLoad	-ele	2621721	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor2 - 0.25*$BeamLiveLoadFloor2];
eleLoad	-ele	2721821	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor2 - 0.25*$BeamLiveLoadFloor2];
eleLoad	-ele	2821921	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor2 - 0.25*$BeamLiveLoadFloor2];

# Level3
eleLoad	-ele	2131231	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor3 - 0.25*$BeamLiveLoadFloor3];
eleLoad	-ele	2231331	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor3 - 0.25*$BeamLiveLoadFloor3];
eleLoad	-ele	2331431	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor3 - 0.25*$BeamLiveLoadFloor3];
eleLoad	-ele	2431531	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor3 - 0.25*$BeamLiveLoadFloor3];
eleLoad	-ele	2531631	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor3 - 0.25*$BeamLiveLoadFloor3];
eleLoad	-ele	2631731	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor3 - 0.25*$BeamLiveLoadFloor3];
eleLoad	-ele	2731831	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor3 - 0.25*$BeamLiveLoadFloor3];
eleLoad	-ele	2831931	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor3 - 0.25*$BeamLiveLoadFloor3];

# Level4
eleLoad	-ele	2141241	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor4 - 0.25*$BeamLiveLoadFloor4];
eleLoad	-ele	2241341	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor4 - 0.25*$BeamLiveLoadFloor4];
eleLoad	-ele	2341441	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor4 - 0.25*$BeamLiveLoadFloor4];
eleLoad	-ele	2441541	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor4 - 0.25*$BeamLiveLoadFloor4];
eleLoad	-ele	2541641	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor4 - 0.25*$BeamLiveLoadFloor4];
eleLoad	-ele	2641741	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor4 - 0.25*$BeamLiveLoadFloor4];
eleLoad	-ele	2741841	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor4 - 0.25*$BeamLiveLoadFloor4];
eleLoad	-ele	2841941	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor4 - 0.25*$BeamLiveLoadFloor4];

# Level5
eleLoad	-ele	2151251	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor5 - 0.25*$BeamLiveLoadFloor5];
eleLoad	-ele	2251351	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor5 - 0.25*$BeamLiveLoadFloor5];
eleLoad	-ele	2351451	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor5 - 0.25*$BeamLiveLoadFloor5];
eleLoad	-ele	2451551	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor5 - 0.25*$BeamLiveLoadFloor5];
eleLoad	-ele	2551651	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor5 - 0.25*$BeamLiveLoadFloor5];
eleLoad	-ele	2651751	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor5 - 0.25*$BeamLiveLoadFloor5];
eleLoad	-ele	2751851	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor5 - 0.25*$BeamLiveLoadFloor5];
eleLoad	-ele	2851951	-type	-beamUniform	[expr -1.05*$BeamDeadLoadFloor5 - 0.25*$BeamLiveLoadFloor5];


# Define point loads on leaning column
load	102	0	[expr -1*$LeaningColumnDeadLoadFloor2 - 0.25*$LeaningColumnLiveLoadFloor2]	0;
load	103	0	[expr -1*$LeaningColumnDeadLoadFloor3 - 0.25*$LeaningColumnLiveLoadFloor3]	0;
load	104	0	[expr -1*$LeaningColumnDeadLoadFloor4 - 0.25*$LeaningColumnLiveLoadFloor4]	0;
load	105	0	[expr -1*$LeaningColumnDeadLoadFloor5 - 0.25*$LeaningColumnLiveLoadFloor5]	0;

}
puts "Expected gravity loads defined"