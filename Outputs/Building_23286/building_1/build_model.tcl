# *******************************************************************************************
# ************************* BUILD MODEL AND RUN GRAVITY ANALYSIS ****************************
# *******************************************************************************************

# Clear all memory
wipe all

# ************************************* INPUT START *****************************************

# ----------------------------------- Building Geometry ------------------------------------

# Define model builder
model BasicBuilder -ndm 2 -ndf 3

# Units: kips, inches, seconds

# Define basic geometry ....................................................................
# Vertical geometry
set NumStories 6;
set NumStories_sbe 3;
set NumStories_obe 3;
set	FirstStory	[expr 12.000*12];
set	TypicalStory	[expr 12.000*12];

# Wall geometry
set Lw [expr 384.000];		# Wall length, inches
set LengthBoundEl 35.000;			# Boundary Length
set Twall 17.000;    # Wall thickness
set WallElPerStory 2;			# Number of wall elements per story

# Define rigid beam/column properties
set A_rigid 1.0e9;
set I_rigid 1.0e9;
set Econ_rigid 1.0e9;

# Calculate floor masses - nodal mass
set g 386.4;								# Acceleration due to gravity, in/(sec^2)
set pi 3.141593;							# pi
set FloorWeight 1476.562;
set RoofWeight	1476.562;
set	WallTributaryMassRatio	0.500;
set	TotalNodesPerFloor	1
set	NodalMassFloor	[expr $FloorWeight*$WallTributaryMassRatio/$TotalNodesPerFloor/$g];
set	NodalMassRoof	[expr $RoofWeight*$WallTributaryMassRatio/$TotalNodesPerFloor/$g];
set Negligible 1.0e-9;						# A very small number to avoid problems with zero

# ********************************* MODEL GENERATION *************************************

# ------------------------------------- Nodes --------------------------------------------

# Command: node nodeID x-coord y-coord -mass mass_dof1 mass_dof2 mass_dof3
# Ground Floor Nodes - no mass
node 100	0.0	0.0; 							# Axis 1 - COORDINATE SYSTEM ORIGIN

node [expr 100 + (2*1 - 1)]	0.0					[expr (2*1 - 1)*$FirstStory/$WallElPerStory];	# 1xx - Wall @ 1 - no mass at inter-story nodes
node [expr 100 + 2*1]			0.0				[expr 1*$FirstStory] -mass $NodalMassFloor $Negligible $Negligible;	# 1xx - Wall   @ 1 - mass

for {set i 2} {$i <= $NumStories-1} {incr i} { 
	node [expr 100 + (2*$i - 1)]	0.0			[expr (2*$i - 1)*$TypicalStory/$WallElPerStory];	# 1xx - Wall @ 1 - no mass at inter-story nodes
	node [expr 100 + 2*$i]			0.0			[expr $i*$TypicalStory] -mass $NodalMassFloor $Negligible $Negligible;	# 1xx - Wall   @ 1 - mass

}
node [expr 100 + (2*$NumStories - 1)]	0.0					[expr (2*$NumStories - 1)*$TypicalStory/$WallElPerStory];	# 1xx - Wall @ 1 - no mass at inter-story nodes 
node [expr 100 + 2*$NumStories]			0.0				[expr $NumStories*$TypicalStory] -mass $NodalMassRoof $Negligible $Negligible;	# 1xx - Wall   @ 1 - mass 

# Define boundary conditions at ground nodes
fix 100 1 1 1;		# Fix node 1 in X, Y, Z-dir 

# Set controlling parameters for displacement controlled analysis
set IDctrlNode [expr 100 + 2*$NumStories];	# Controlling node, Right-side, roof node
set IDctrlDOF 1;							# Controlling DOF, Constrain X-dir movements


# ----------------------------------- Material / Element Tags ------------------------------------	
# Material tags
set MatReinf 1; 	# Steel
set MatUncConc 2;	# Unconfined concrete
set MatConConc_sbe 3;	# Confined conditions - SBE
set MatConConc_obe 4;	# Confined conditions - OBE
set MatFSAM_Unc 5; 	# Unconfined concrete(FSAM) - wall
set MatFSAM_Con_sbe 6;	# Confined concrete(FSAM) - wall
set MatFSAM_Con_obe 7;	# Confined concrete(FSAM) - wall

# ---------------------------------------  PD columns  -------------------------------------------

set PDeltaTransf 2;
geomTransf PDelta $PDeltaTransf;

set Ec 5034.104;
set AreaRigid  1e9; 	# Large area
set IRigid 	   1e9;     # Large moment of inertia
set PDcolI 0.001;

# Define nodes for leaning column
node	21	[expr 1*$Lw]	[expr 0*$FirstStory+0*$TypicalStory]; # Level 1
node	22	[expr 1*$Lw]	[expr 1*$FirstStory+0*$TypicalStory]; # Level 2
node	23	[expr 1*$Lw]	[expr 1*$FirstStory+1*$TypicalStory]; # Level 3
node	24	[expr 1*$Lw]	[expr 1*$FirstStory+2*$TypicalStory]; # Level 4
node	25	[expr 1*$Lw]	[expr 1*$FirstStory+3*$TypicalStory]; # Level 5
node	26	[expr 1*$Lw]	[expr 1*$FirstStory+4*$TypicalStory]; # Level 6
node	27	[expr 1*$Lw]	[expr 1*$FirstStory+5*$TypicalStory]; # Level 7
# puts "Nodes for leaning column defined" 

fix	21	1	1	0; 


# Define leaning columns 
# Story 1
element	elasticBeamColumn	32122	21	22	$AreaRigid	$Ec	$PDcolI	$PDeltaTransf;

# Story 2
element	elasticBeamColumn	32223	22	23	$AreaRigid	$Ec	$PDcolI	$PDeltaTransf;

# Story 3
element	elasticBeamColumn	32324	23	24	$AreaRigid	$Ec	$PDcolI	$PDeltaTransf;

# Story 4
element	elasticBeamColumn	32425	24	25	$AreaRigid	$Ec	$PDcolI	$PDeltaTransf;

# Story 5
element	elasticBeamColumn	32526	25	26	$AreaRigid	$Ec	$PDcolI	$PDeltaTransf;

# Story 6
element	elasticBeamColumn	32627	26	27	$AreaRigid	$Ec	$PDcolI	$PDeltaTransf;

# puts "Leaning column defined"


# Define floor constraint
set	ConstrainDOF	1;	# Nodes at same floor level have identical lateral displacement 
equalDOF	102	22	$ConstrainDOF;	# wall to Leaning column - level 2 
equalDOF	104	23	$ConstrainDOF;	# wall to Leaning column - level 3 
equalDOF	106	24	$ConstrainDOF;	# wall to Leaning column - level 4 
equalDOF	108	25	$ConstrainDOF;	# wall to Leaning column - level 5 
equalDOF	110	26	$ConstrainDOF;	# wall to Leaning column - level 6 
equalDOF	112	27	$ConstrainDOF;	# wall to Leaning column - level 7 


# --------------------------------------- Wall Section -------------------------------------------
# Define steel material ..........................................................................
# Command: uniaxialMaterial Steel02 $tag $fy $Es $b $R0 $cR1 $cR2 $a1 $a2 $a3 $a4

# Define reinforcement in X(horizontal), Y(vertical) in both boundary and web
set fy 69.000;
set b 0.02;		# strain hardening

# Reinforcing steel parameters
set Es 29000.0;		# Young's modulus
set R0 20.0;		# Initial value of curvature parameter
set cR1 0.925;		# Curvature degradation parameter
set cR2 0.15;		# Curvature degradation parameter

# Build steel material
uniaxialMaterial SteelMPF $MatReinf $fy $fy  $Es $b $b  $R0 $cR1 $cR2

# Define concrete materials ........................................................................
# Command: uniaxialMaterial ConcreteCM $matTag $fpcc $epcc $Ec $rc $xcrn $ft $et $rt $xcrp  <-GapClose $gap>

# Unconfined concrete
set fc_uc 7.800;		# peak compressive stress
set ec0_uc -0.0020; # strain at peak compressive stress
set Ec_uc [expr 57.0*pow($fc_uc*1000.0,0.5)];	# Youngs modulus
set r_uc [expr ($fc_uc/0.75)-1.9]; 		# shape parameter - compression
set xcrn_uc 1.015;	# cracking strain - compression
set ft [expr 3.7334/1000*pow(abs($fc_uc)*1000,0.5)]; # peak tensile stress
set et 0.00008;		# strain at peak tensile stress
set rt 1.2;			# shape parameter - tension
set xcrp 10000.0;	# cracking strain - tension

# Confined concrete - SBE
set fc_sbe 10.007; 	# peak compressive stress
set ec0_sbe -0.005;# strain at peak compressive stress
set Ec_sbe [expr 57.0*pow($fc_sbe*1000.0,0.5)];	# Youngs modulus
set r_sbe [expr ($fc_sbe/0.75)-1.9]; 		# shape parameter - compression
set xcrn_sbe 1.03;  # cracking strain - compression

# Confined concrete - OBE
set fc_obe 9.562; 	# peak compressive stress
set ec0_obe -0.004;# strain at peak compressive stress
set Ec_obe [expr 57.0*pow($fc_obe*1000.0,0.5)];	# Youngs modulus
set r_obe [expr ($fc_obe/0.75)-1.9]; 		# shape parameter - compression
set xcrn_obe 1.03;  # cracking strain - compression

# Build concrete materials
uniaxialMaterial ConcreteCM $MatUncConc -$fc_uc  $ec0_uc  $Ec_uc  $r_uc  $xcrn_uc  $ft $et $rt $xcrp; # Unconfined concrete
uniaxialMaterial ConcreteCM $MatConConc_sbe -$fc_sbe $ec0_sbe $Ec_sbe $r_sbe $xcrn_sbe $ft $et $rt $xcrp; # Confined concrete SBE
uniaxialMaterial ConcreteCM $MatConConc_obe -$fc_obe $ec0_obe $Ec_obe $r_obe $xcrn_obe $ft $et $rt $xcrp; # Confined concrete OBE

# Define FSAM (Fixed-Strut Angle Model) ..............................................................
# Command: nDMaterial FSAM $matTag $rho $sX $sY $conc $rouX $rouY $nu $alfadow

set rho   0.0;			# Density, use 0.0 (mass assigned at nodes)
set rouXw 0.010;		# Reinforcing in X (horizontal) direction, web
set rouYw 0.003;		# Reinforcing in Y (vertical) direction, web
set rouXb_sbe 0.013;		# Reinforcing in X (horizontal) direction, boundary
set rouXb_obe 0.010;		# Reinforcing in X (horizontal) direction, boundary
set rouYb 0.068;		# Reinforcing in Y (vertical) direction, boundary

set nu 1.0;				# Friction coefficient (0.0 < $nu < 1.0)
set alfadow 0.01;		# Stiffness coefficient of reinforcing dowel action (0.0 < $alfadow < 0.1)

# Build FSAM RC panel materials
nDMaterial FSAM $MatFSAM_Unc $rho $MatReinf $MatReinf $MatUncConc $rouXw $rouYw $nu $alfadow; 		# Unconfined concrete, web
nDMaterial FSAM $MatFSAM_Con_sbe $rho $MatReinf $MatReinf $MatConConc_sbe $rouXb_sbe $rouYb $nu $alfadow;		# Confined concrete, boundary SBE
nDMaterial FSAM $MatFSAM_Con_obe $rho $MatReinf $MatReinf $MatConConc_obe $rouXb_obe $rouYb $nu $alfadow;		# Confined concrete, boundary OBE

# Define SFI_MVLEM wall elements ......................................................................
set n_fibers 6; 	# No. of macro fibers in wall (1 per each boundary, rest for web)
set widthWebEl [expr ($Lw - 2*$LengthBoundEl)/($n_fibers-2)]; # Width of web element
set c_rot 0.4; 		# Location of center of rotation with respect to iNode (0.4 recommended)

# Command: element SFI_MVLEM eleTag iNode jNode m c -thick fiberThick -width fiberWidth -mat matTags
for {set i 1} {$i <= [expr 2*$NumStories_sbe]} {incr i} { 
	element SFI_MVLEM [expr 1000 + $i] [expr 100 + $i - 1] [expr 100 + $i] $n_fibers $c_rot -thick $Twall $Twall $Twall $Twall $Twall $Twall -width $LengthBoundEl $widthWebEl $widthWebEl $widthWebEl $widthWebEl $LengthBoundEl -mat $MatFSAM_Con_sbe $MatFSAM_Unc $MatFSAM_Unc $MatFSAM_Unc  $MatFSAM_Unc $MatFSAM_Con_sbe;
}
for {set i [expr (2*$NumStories_sbe)+1]} {$i <= [expr 2*$NumStories]} {incr i} { 
	element SFI_MVLEM [expr 1000 + $i] [expr 100 + $i - 1] [expr 100 + $i] $n_fibers $c_rot -thick $Twall $Twall $Twall $Twall $Twall $Twall -width $LengthBoundEl $widthWebEl $widthWebEl $widthWebEl $widthWebEl $LengthBoundEl -mat $MatFSAM_Con_obe $MatFSAM_Unc $MatFSAM_Unc $MatFSAM_Unc  $MatFSAM_Unc $MatFSAM_Con_obe;
}

puts "Wall elements defined."


# --------------------------------------- Define Recorders ------------------------------------ 

# Define Recorders
# Recorder Node <-file $fileName> <-precision $nSD> <-time> <-dT $deltaT> <-closeOnWrite> <-node $node1 $node2...> <-nodeRange $startNode $endNode> <-dof $dof1 $dof2> $respType
# Response Type: disp, vel, accel, incrDisp, "eigen i", reaction, rayleighForces

# Node recorders
# Displacements
recorder Node -file $dataDirName/NodeDisp.out -time -nodeRange 100 112 -dof 1 2 disp;

# Reactions 
recorder Node -file $dataDirName/NodeReactions.out -time -node 100 -dof 1 2 3 reaction; 

# Record drift histories 
# Command: recorder Drift -file $filename -time -iNode $NodeI_ID -jNode $NodeJ_ID -dof $dof -perpDirn $Record.drift.perpendicular.to.this.direction 
recorder Drift -file $dataDirName/DriftRoof.out -time -iNode 100 -jNode 112 -dof 1 -perpDirn 2; # Roof 
recorder Drift -file $dataDirName/DriftStory.out -time -iNode 100 102 104 106 108 110 -jNode 102 104 106 108 110 112 -dof 1 -perpDirn 2; # Story 


# Record responses for wall elements 
recorder Element -file $dataDirName/WallGlobalForces.out -time -ele 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 globalForce; 
recorder Element -file $dataDirName/WallCurvature.out -time -ele 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 Curvature; 
recorder Element -file $dataDirName/WallShearDef.out -time -ele 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 ShearDef; 

# Record responses for wall fibers (one panel per recorder)
# Command: RCPanel $fibTag $Response 
recorder Element -file $dataDirName/WallFiberStrain_f1.out -time -ele 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 RCPanel 1 panel_strain 
recorder Element -file $dataDirName/WallFiberStrain_f6.out -time -ele 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 RCPanel 6 panel_strain 
recorder Element -file $dataDirName/WallPanelStrain.out -time -ele 1001 RCPanel 1 panel_strain 
recorder Element -file $dataDirName/WallPanelStress.out -time -ele 1001 RCPanel 1 panel_stress 
recorder Element -file $dataDirName/WallStressConcrete.out -time -ele 1001 RCPanel 1 panel_stress_concrete 
recorder Element -file $dataDirName/WallStressSteel.out -time -ele 1001 RCPanel 1 panel_stress_steel 
recorder Element -file $dataDirName/WallPanelSteel1.out -time -ele 1001 RCPanel 1 strain_stress_steelX 
recorder Element -file $dataDirName/WallPanelSteel2.out -time -ele 1001 RCPanel 1 strain_stress_steelY 
recorder Element -file $dataDirName/WallPanelConcrete1.out -time -ele 1001 RCPanel 1 strain_stress_concrete1 
recorder Element -file $dataDirName/WallPanelConcrete2.out -time -ele 1001 RCPanel 1 strain_stress_concrete2 

# --------------------------------- Gravity Loads & Gravity Analysis ------------------------------------

# Apply gravity loads

# Assign point dead load values on wall: (kip)
set	WallDeadLoadFloor	180.521;
# Assign point live load values on wall: (kip)
set	WallLiveLoadFloor	13.754;
# Assign point dead load values on leaning column: (kip)
set	LeaningColumnDeadLoadFloor	557.761;
# Assign point live load values on leaning column: (kip)
set	LeaningColumnLiveLoadFloor	42.496;

# Construct a  time series where load factor applied is linearly proportional to the time domain
# Command: pattern PatternType $PatternID TimeSeriesType
# 104 Expected gravity loads: 1 DL + 0.25 LL (or 1.05 DL + 0.25 LL)
pattern Plain 104 Constant {

	# Nodal load on walls and PF columns - command: load nodeID xForce yForce
	for {set i 1} {$i <= $NumStories} {incr i} { 
		#load [expr 100 + 2*$i]  0.0 [expr -1*$WallDeadLoadFloor - 0.25*$WallLiveLoadFloor] 0.0;
		#load [expr 21 + $i]  0.0 [expr -1*$LeaningColumnDeadLoadFloor - 0.25*$LeaningColumnLiveLoadFloor] 0.0;
		load [expr 100 + 2*$i]  0.0 [expr -$WallDeadLoadFloor - $WallLiveLoadFloor] 0.0; # The inputs are already expected loads
		load [expr 21 + $i]  0.0 [expr -$LeaningColumnDeadLoadFloor - $LeaningColumnLiveLoadFloor] 0.0; # The inputs are already expected loads
	}
}


# Gravity-analysis: load-controlled static analysis
set Tol 1.0e-6;							# convergence tolerance for test
set NstepGravity 10;					# apply gravity in 10 steps
set DGravity [expr 1.0/$NstepGravity];	# load increment
constraints Plain;						# how it handles boundary conditions
numberer RCM;							# renumber dof's to minimize band-width (optimization)
system BandGeneral;						# how to store and solve the system of equations in the analysis (large model: try UmfPack)
test NormDispIncr $Tol 6;				# determine if convergence has been achieved at the end of an iteration step
algorithm Newton;						# use Newton's solution algorithm: updates tangent stiffness at every iteration
integrator LoadControl $DGravity;		# determine the next time step for an analysis
analysis Static;						# define type of analysis: static or transient
analyze $NstepGravity;					# apply gravity

puts "Model built & gravity analysis completed."
