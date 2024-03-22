# This file will be used to define all nodal masses 

# Define floor weights and each nodal mass 
set	Floor2Weight	10137.60; 
set	Floor3Weight	10137.60; 
set	Floor4Weight	10137.60; 
set	Floor5Weight	14169.60; 
set	FrameTributaryMassRatio	0.5; 
set	TotalNodesPerFloor	10; 
set	NodalMassFloor2	[expr $Floor2Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor3	[expr $Floor3Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor4	[expr $Floor4Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor5	[expr $Floor5Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 


# Level 2 
mass	121	$NodalMassFloor2	$Negligible	$Negligible
mass	221	$NodalMassFloor2	$Negligible	$Negligible
mass	321	$NodalMassFloor2	$Negligible	$Negligible
mass	421	$NodalMassFloor2	$Negligible	$Negligible
mass	521	$NodalMassFloor2	$Negligible	$Negligible
mass	621	$NodalMassFloor2	$Negligible	$Negligible
mass	721	$NodalMassFloor2	$Negligible	$Negligible
mass	821	$NodalMassFloor2	$Negligible	$Negligible
mass	921	$NodalMassFloor2	$Negligible	$Negligible
mass	1021	$NodalMassFloor2	$Negligible	$Negligible

# Level 3 
mass	131	$NodalMassFloor3	$Negligible	$Negligible
mass	231	$NodalMassFloor3	$Negligible	$Negligible
mass	331	$NodalMassFloor3	$Negligible	$Negligible
mass	431	$NodalMassFloor3	$Negligible	$Negligible
mass	531	$NodalMassFloor3	$Negligible	$Negligible
mass	631	$NodalMassFloor3	$Negligible	$Negligible
mass	731	$NodalMassFloor3	$Negligible	$Negligible
mass	831	$NodalMassFloor3	$Negligible	$Negligible
mass	931	$NodalMassFloor3	$Negligible	$Negligible
mass	1031	$NodalMassFloor3	$Negligible	$Negligible

# Level 4 
mass	141	$NodalMassFloor4	$Negligible	$Negligible
mass	241	$NodalMassFloor4	$Negligible	$Negligible
mass	341	$NodalMassFloor4	$Negligible	$Negligible
mass	441	$NodalMassFloor4	$Negligible	$Negligible
mass	541	$NodalMassFloor4	$Negligible	$Negligible
mass	641	$NodalMassFloor4	$Negligible	$Negligible
mass	741	$NodalMassFloor4	$Negligible	$Negligible
mass	841	$NodalMassFloor4	$Negligible	$Negligible
mass	941	$NodalMassFloor4	$Negligible	$Negligible
mass	1041	$NodalMassFloor4	$Negligible	$Negligible

# Level 5 
mass	151	$NodalMassFloor5	$Negligible	$Negligible
mass	251	$NodalMassFloor5	$Negligible	$Negligible
mass	351	$NodalMassFloor5	$Negligible	$Negligible
mass	451	$NodalMassFloor5	$Negligible	$Negligible
mass	551	$NodalMassFloor5	$Negligible	$Negligible
mass	651	$NodalMassFloor5	$Negligible	$Negligible
mass	751	$NodalMassFloor5	$Negligible	$Negligible
mass	851	$NodalMassFloor5	$Negligible	$Negligible
mass	951	$NodalMassFloor5	$Negligible	$Negligible
mass	1051	$NodalMassFloor5	$Negligible	$Negligible

# puts "Nodal mass defined"