# This file will be used to define all nodal masses 

# Define floor weights and each nodal mass 
set	Floor2Weight	5000.00; 
set	Floor3Weight	5000.00; 
set	Floor4Weight	5000.00; 
set	Floor5Weight	5000.00; 
set	FrameTributaryMassRatio	0.125; 
set	TotalNodesPerFloor	9; 
set	NodalMassFloor2	[expr $Floor2Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor3	[expr $Floor3Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor4	[expr $Floor4Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 
set	NodalMassFloor5	[expr $Floor5Weight*$FrameTributaryMassRatio/$TotalNodesPerFloor/$g]; 


# Level2 
mass	1211	$NodalMassFloor2	$Negligible	$Negligible 
mass	2211	$NodalMassFloor2	$Negligible	$Negligible 
mass	3211	$NodalMassFloor2	$Negligible	$Negligible 
mass	4211	$NodalMassFloor2	$Negligible	$Negligible 
mass	5211	$NodalMassFloor2	$Negligible	$Negligible 
mass	6211	$NodalMassFloor2	$Negligible	$Negligible 
mass	7211	$NodalMassFloor2	$Negligible	$Negligible 
mass	8211	$NodalMassFloor2	$Negligible	$Negligible 
mass	9211	$NodalMassFloor2	$Negligible	$Negligible 

# Level3 
mass	1311	$NodalMassFloor3	$Negligible	$Negligible 
mass	2311	$NodalMassFloor3	$Negligible	$Negligible 
mass	3311	$NodalMassFloor3	$Negligible	$Negligible 
mass	4311	$NodalMassFloor3	$Negligible	$Negligible 
mass	5311	$NodalMassFloor3	$Negligible	$Negligible 
mass	6311	$NodalMassFloor3	$Negligible	$Negligible 
mass	7311	$NodalMassFloor3	$Negligible	$Negligible 
mass	8311	$NodalMassFloor3	$Negligible	$Negligible 
mass	9311	$NodalMassFloor3	$Negligible	$Negligible 

# Level4 
mass	1411	$NodalMassFloor4	$Negligible	$Negligible 
mass	2411	$NodalMassFloor4	$Negligible	$Negligible 
mass	3411	$NodalMassFloor4	$Negligible	$Negligible 
mass	4411	$NodalMassFloor4	$Negligible	$Negligible 
mass	5411	$NodalMassFloor4	$Negligible	$Negligible 
mass	6411	$NodalMassFloor4	$Negligible	$Negligible 
mass	7411	$NodalMassFloor4	$Negligible	$Negligible 
mass	8411	$NodalMassFloor4	$Negligible	$Negligible 
mass	9411	$NodalMassFloor4	$Negligible	$Negligible 

# Level5 
mass	1511	$NodalMassFloor5	$Negligible	$Negligible 
mass	2511	$NodalMassFloor5	$Negligible	$Negligible 
mass	3511	$NodalMassFloor5	$Negligible	$Negligible 
mass	4511	$NodalMassFloor5	$Negligible	$Negligible 
mass	5511	$NodalMassFloor5	$Negligible	$Negligible 
mass	6511	$NodalMassFloor5	$Negligible	$Negligible 
mass	7511	$NodalMassFloor5	$Negligible	$Negligible 
mass	8511	$NodalMassFloor5	$Negligible	$Negligible 
mass	9511	$NodalMassFloor5	$Negligible	$Negligible 

puts "Nodal mass defined"