"""
Created by: Muneera Aladsani - UCLA

Previous edit: Sept 29 2021
Last edit: Oct 16 2022

"""

class NRHA_tclfiles():
      
    def __init__(self, DL_floor,DL_roof,LL_floor,LL_roof,num_story,first_story,typical_story,story_sbe,story_obe,lw,b,lbe,W_typical,W_roof,Ec,fy,A_trib,A_trib_leancol,fc,fcc_sbe,epsc0_sbe,fcc_obe,epsc0_obe,ratio_web_t,ratio_web_l,ratio_be_t_sbe,ratio_be_t_obe,ratio_be_l,numGM):
        self.DL_floor = DL_floor #psf
        self.DL_roof = DL_roof #psf
        self.LL_floor = LL_floor #psf
        self.LL_roof = LL_roof #psf
        self.num_story = num_story
        self.first_story = first_story #ft
        self.typical_story =typical_story  #ft
        self.story_sbe = story_sbe
        self.story_obe = story_obe
        self.lw = lw #inch
        self.b = b #inch
        self.lbe = lbe #inch
        self.W_typical = W_typical #kips
        self.W_roof = W_roof #kips
        self.Ec = Ec
        self.fy = fy
        self.A_trib = A_trib #ft2
        self.A_trib_leancol = A_trib_leancol #ft2
        self.fc = fc #ksi
        self.fcc_sbe = fcc_sbe #ksi
        self.epsc0_sbe = epsc0_sbe
        self.fcc_obe = fcc_obe
        self.epsc0_obe = epsc0_obe
        self.ratio_web_t = ratio_web_t
        self.ratio_web_l = ratio_web_l
        self.ratio_be_t_sbe = ratio_be_t_sbe
        self.ratio_be_t_obe = ratio_be_t_obe
        self.ratio_be_l = ratio_be_l
        self.numGM = numGM

    
    def build_model(self):
        f = open('build_model.tcl','w')

        textList =[     
        '# *******************************************************************************************',
        '# ************************* BUILD MODEL AND RUN GRAVITY ANALYSIS ****************************',
        '# *******************************************************************************************',
        '',
        '# Clear all memory',
        'wipe all',
        '',
        '# ************************************* INPUT START *****************************************',
        '',
        '# ----------------------------------- Building Geometry ------------------------------------',
        '',
        '# Define model builder',
        'model BasicBuilder -ndm 2 -ndf 3',
        '',
        '# Units: kips, inches, seconds',
        '',
        '# Define basic geometry ....................................................................',
        '# Vertical geometry',
        'set NumStories %.0f;' %(self.num_story),
        'set NumStories_sbe %.0f;' %(self.story_sbe),
        'set NumStories_obe %.0f;' %(self.story_obe),
        'set	FirstStory	[expr %.3f*12];' %(self.first_story),
        'set	TypicalStory	[expr %.3f*12];' %(self.typical_story),
        '',
        '# Wall geometry',
        'set Lw [expr %.3f];		# Wall length, inches' %(self.lw),
        'set LengthBoundEl %.3f;			# Boundary Length' %(self.lbe),
        'set Twall %.3f;    # Wall thickness' %(self.b),
        'set WallElPerStory 2;			# Number of wall elements per story',
        '',
        '# Define rigid beam/column properties',
        'set A_rigid 1.0e9;',
        'set I_rigid 1.0e9;',
        'set Econ_rigid 1.0e9;',
        '',
        '# Calculate floor masses - nodal mass',
        'set g 386.4;								# Acceleration due to gravity, in/(sec^2)',
        'set pi 3.141593;							# pi',
        'set FloorWeight %.3f;' %(self.W_typical),
        'set RoofWeight	%.3f;' %(self.W_roof),
        'set	WallTributaryMassRatio	0.500;',
        'set	TotalNodesPerFloor	1',
        'set	NodalMassFloor	[expr $FloorWeight*$WallTributaryMassRatio/$TotalNodesPerFloor/$g];',
        'set	NodalMassRoof	[expr $RoofWeight*$WallTributaryMassRatio/$TotalNodesPerFloor/$g];',
        'set Negligible 1.0e-9;						# A very small number to avoid problems with zero',
        '',
        '# ********************************* MODEL GENERATION *************************************',
        '',
        '# ------------------------------------- Nodes --------------------------------------------',
        '',
        '# Command: node nodeID x-coord y-coord -mass mass_dof1 mass_dof2 mass_dof3',
        '# Ground Floor Nodes - no mass',
        'node 100	0.0	0.0; 							# Axis 1 - COORDINATE SYSTEM ORIGIN',
        '',
        'node [expr 100 + (2*1 - 1)]	0.0					[expr (2*1 - 1)*$FirstStory/$WallElPerStory];	# 1xx - Wall @ 1 - no mass at inter-story nodes',
        'node [expr 100 + 2*1]			0.0				[expr 1*$FirstStory] -mass $NodalMassFloor $Negligible $Negligible;	# 1xx - Wall   @ 1 - mass',
        '',
        'for {set i 2} {$i <= $NumStories-1} {incr i} { ',
        '	node [expr 100 + (2*$i - 1)]	0.0			[expr (2*$i - 1)*$TypicalStory/$WallElPerStory];	# 1xx - Wall @ 1 - no mass at inter-story nodes',
        '	node [expr 100 + 2*$i]			0.0			[expr $i*$TypicalStory] -mass $NodalMassFloor $Negligible $Negligible;	# 1xx - Wall   @ 1 - mass',
        '',
        '}']

        for line in textList:
          f.write(line)
          f.write("\n") 
          
         
        if self.num_story != 1:
            f.write('node [expr 100 + (2*$NumStories - 1)]	0.0					[expr (2*$NumStories - 1)*$TypicalStory/$WallElPerStory];	# 1xx - Wall @ 1 - no mass at inter-story nodes \n')
            f.write('node [expr 100 + 2*$NumStories]			0.0				[expr $NumStories*$TypicalStory] -mass $NodalMassRoof $Negligible $Negligible;	# 1xx - Wall   @ 1 - mass \n')
        
        textList =[
        '',
        '# Define boundary conditions at ground nodes',
        'fix 100 1 1 1;		# Fix node 1 in X, Y, Z-dir ',
        '',
        '# Set controlling parameters for displacement controlled analysis',
        'set IDctrlNode [expr 100 + 2*$NumStories];	# Controlling node, Right-side, roof node',
        'set IDctrlDOF 1;							# Controlling DOF, Constrain X-dir movements',
        '',
        '',
        '# ----------------------------------- Material / Element Tags ------------------------------------	',
        '# Material tags',
        'set MatReinf 1; 	# Steel',
        'set MatUncConc 2;	# Unconfined concrete',
        'set MatConConc_sbe 3;	# Confined conditions - SBE',
        'set MatConConc_obe 4;	# Confined conditions - OBE',
        'set MatFSAM_Unc 5; 	# Unconfined concrete(FSAM) - wall',
        'set MatFSAM_Con_sbe 6;	# Confined concrete(FSAM) - wall',
        'set MatFSAM_Con_obe 7;	# Confined concrete(FSAM) - wall',
        '',
        '# ---------------------------------------  PD columns  -------------------------------------------',
        '',
        'set PDeltaTransf 2;',
        'geomTransf PDelta $PDeltaTransf;',
        '',
        'set Ec %.3f;' %(self.Ec),
        'set AreaRigid  1e9; 	# Large area',
        'set IRigid 	   1e9;     # Large moment of inertia',
        'set PDcolI 0.001;',
        '',
        '# Define nodes for leaning column'
        ]

        for line in textList:
          f.write(line)
          f.write("\n")      
          
        for i in range(0,self.num_story+1):
            if i == 0 or i == 1:
                f.write("node	%s	[expr 1*$Lw]	[expr %s*$FirstStory+0*$TypicalStory]; # Level %s\n" %((i+21), i, (i+1)))
            else:
                f.write("node	%s	[expr 1*$Lw]	[expr 1*$FirstStory+%s*$TypicalStory]; # Level %s\n" %((i+21), (i-1), (i+1)))
                        
        f.write('# puts "Nodes for leaning column defined" \n\n')
        f.write('fix	21	1	1	0; \n\n\n')
        f.write('# Define leaning columns \n')
                
        for i in range(0,self.num_story):
            f.write("# Story %s\n" %(i+1))
            f.write("element	elasticBeamColumn	32%s2%s	%s	%s	$AreaRigid	$Ec	$PDcolI	$PDeltaTransf;\n\n" %((i+1), (i+2), (i+21), (i+22)))
                
        f.write('# puts "Leaning column defined"\n\n\n')
                
        f.write('# Define floor constraint\n')
        f.write('set	ConstrainDOF	1;	# Nodes at same floor level have identical lateral displacement \n')
        for i in range(0,self.num_story):
            f.write("equalDOF	%s	%s	$ConstrainDOF;	# wall to Leaning column - level %s \n" %((2*i+102), (i+22), (i+2)))                
        f.write('\n\n')

        textList =[
        '# --------------------------------------- Wall Section -------------------------------------------',
        '# Define steel material ..........................................................................',
        '# Command: uniaxialMaterial Steel02 $tag $fy $Es $b $R0 $cR1 $cR2 $a1 $a2 $a3 $a4',
        '',
        '# Define reinforcement in X(horizontal), Y(vertical) in both boundary and web',
        'set fy %.3f;' %(self.fy),
        'set b 0.02;		# strain hardening',
        '',
        '# Reinforcing steel parameters',
        "set Es 29000.0;		# Young's modulus",
        'set R0 20.0;		# Initial value of curvature parameter',
        'set cR1 0.925;		# Curvature degradation parameter',
        'set cR2 0.15;		# Curvature degradation parameter',
        '',
        '# Build steel material',
        'uniaxialMaterial SteelMPF $MatReinf $fy $fy  $Es $b $b  $R0 $cR1 $cR2',
        '',
        '# Define concrete materials ........................................................................',
        '# Command: uniaxialMaterial ConcreteCM $matTag $fpcc $epcc $Ec $rc $xcrn $ft $et $rt $xcrp  <-GapClose $gap>',
        '',
        '# Unconfined concrete',
        'set fc_uc %.3f;		# peak compressive stress' %(self.fc),
        'set ec0_uc -0.0020; # strain at peak compressive stress',
        'set Ec_uc [expr 57.0*pow($fc_uc*1000.0,0.5)];	# Youngs modulus',
        'set r_uc [expr ($fc_uc/0.75)-1.9]; 		# shape parameter - compression', #?
        'set xcrn_uc 1.015;	# cracking strain - compression', #? left as is from Kol. code from OpenSees example
        'set ft [expr 3.7334/1000*pow(abs($fc_uc)*1000,0.5)]; # peak tensile stress',
        'set et 0.00008;		# strain at peak tensile stress',
        'set rt 1.2;			# shape parameter - tension',
        'set xcrp 10000.0;	# cracking strain - tension',
        '',
        '# Confined concrete - SBE',
        'set fc_sbe %.3f; 	# peak compressive stress' %(self.fcc_sbe),
        'set ec0_sbe -%.3f;# strain at peak compressive stress' %(self.epsc0_sbe),
        'set Ec_sbe [expr 57.0*pow($fc_sbe*1000.0,0.5)];	# Youngs modulus',
        'set r_sbe [expr ($fc_sbe/0.75)-1.9]; 		# shape parameter - compression', #?
        'set xcrn_sbe 1.03;  # cracking strain - compression', #? left as is from Kol. code from OpenSees example
        '',
        '# Confined concrete - OBE',
        'set fc_obe %.3f; 	# peak compressive stress' %(self.fcc_obe),
        'set ec0_obe -%.3f;# strain at peak compressive stress' %(self.epsc0_obe),
        'set Ec_obe [expr 57.0*pow($fc_obe*1000.0,0.5)];	# Youngs modulus',
        'set r_obe [expr ($fc_obe/0.75)-1.9]; 		# shape parameter - compression', #?
        'set xcrn_obe 1.03;  # cracking strain - compression', #? left as is from Kol. code from OpenSees example
        '',
        '# Build concrete materials',
        'uniaxialMaterial ConcreteCM $MatUncConc -$fc_uc  $ec0_uc  $Ec_uc  $r_uc  $xcrn_uc  $ft $et $rt $xcrp; # Unconfined concrete',
        'uniaxialMaterial ConcreteCM $MatConConc_sbe -$fc_sbe $ec0_sbe $Ec_sbe $r_sbe $xcrn_sbe $ft $et $rt $xcrp; # Confined concrete SBE',
        'uniaxialMaterial ConcreteCM $MatConConc_obe -$fc_obe $ec0_obe $Ec_obe $r_obe $xcrn_obe $ft $et $rt $xcrp; # Confined concrete OBE',
        '',
        '# Define FSAM (Fixed-Strut Angle Model) ..............................................................',
        '# Command: nDMaterial FSAM $matTag $rho $sX $sY $conc $rouX $rouY $nu $alfadow',
        '',
        'set rho   0.0;			# Density, use 0.0 (mass assigned at nodes)',
        'set rouXw %.3f;		# Reinforcing in X (horizontal) direction, web'  %(self.ratio_web_t),
        'set rouYw %.3f;		# Reinforcing in Y (vertical) direction, web'  %(self.ratio_web_l),
        'set rouXb_sbe %.3f;		# Reinforcing in X (horizontal) direction, boundary'  %(self.ratio_be_t_sbe),
        'set rouXb_obe %.3f;		# Reinforcing in X (horizontal) direction, boundary'  %(self.ratio_be_t_obe),
        'set rouYb %.3f;		# Reinforcing in Y (vertical) direction, boundary'  %(self.ratio_be_l),
        '',
        'set nu 1.0;				# Friction coefficient (0.0 < $nu < 1.0)',
        'set alfadow 0.01;		# Stiffness coefficient of reinforcing dowel action (0.0 < $alfadow < 0.1)',
        '',
        '# Build FSAM RC panel materials',
        'nDMaterial FSAM $MatFSAM_Unc $rho $MatReinf $MatReinf $MatUncConc $rouXw $rouYw $nu $alfadow; 		# Unconfined concrete, web',
        'nDMaterial FSAM $MatFSAM_Con_sbe $rho $MatReinf $MatReinf $MatConConc_sbe $rouXb_sbe $rouYb $nu $alfadow;		# Confined concrete, boundary SBE',
        'nDMaterial FSAM $MatFSAM_Con_obe $rho $MatReinf $MatReinf $MatConConc_obe $rouXb_obe $rouYb $nu $alfadow;		# Confined concrete, boundary OBE',
        '',
        '# Define SFI_MVLEM wall elements ......................................................................',
        'set n_fibers 6; 	# No. of macro fibers in wall (1 per each boundary, rest for web)',
        'set widthWebEl [expr ($Lw - 2*$LengthBoundEl)/($n_fibers-2)]; # Width of web element',
        'set c_rot 0.4; 		# Location of center of rotation with respect to iNode (0.4 recommended)',
        '',
        '# Command: element SFI_MVLEM eleTag iNode jNode m c -thick fiberThick -width fiberWidth -mat matTags',
        'for {set i 1} {$i <= [expr 2*$NumStories_sbe]} {incr i} { ',
        '	element SFI_MVLEM [expr 1000 + $i] [expr 100 + $i - 1] [expr 100 + $i] $n_fibers $c_rot -thick $Twall $Twall $Twall $Twall $Twall $Twall -width $LengthBoundEl $widthWebEl $widthWebEl $widthWebEl $widthWebEl $LengthBoundEl -mat $MatFSAM_Con_sbe $MatFSAM_Unc $MatFSAM_Unc $MatFSAM_Unc  $MatFSAM_Unc $MatFSAM_Con_sbe;',
        '}',
        'for {set i [expr (2*$NumStories_sbe)+1]} {$i <= [expr 2*$NumStories]} {incr i} { ',
        '	element SFI_MVLEM [expr 1000 + $i] [expr 100 + $i - 1] [expr 100 + $i] $n_fibers $c_rot -thick $Twall $Twall $Twall $Twall $Twall $Twall -width $LengthBoundEl $widthWebEl $widthWebEl $widthWebEl $widthWebEl $LengthBoundEl -mat $MatFSAM_Con_obe $MatFSAM_Unc $MatFSAM_Unc $MatFSAM_Unc  $MatFSAM_Unc $MatFSAM_Con_obe;',
        '}',
        '',
        'puts "Wall elements defined."',
        '',
        '',
        ]

        for line in textList:
          f.write(line)
          f.write("\n")        
        
        f.write('# --------------------------------------- Define Recorders ------------------------------------ \n\n')
        f.write('# Define Recorders\n')
        f.write('# Recorder Node <-file $fileName> <-precision $nSD> <-time> <-dT $deltaT> <-closeOnWrite> <-node $node1 $node2...> <-nodeRange $startNode $endNode> <-dof $dof1 $dof2> $respType\n')
        f.write('# Response Type: disp, vel, accel, incrDisp, "eigen i", reaction, rayleighForces\n\n')
        f.write('# Node recorders\n')
        f.write('# Displacements\n')
        f.write('recorder Node -file $dataDirName/NodeDisp.out -time -nodeRange 100 %s -dof 1 2 disp;\n\n' %(2*self.num_story+100))
        f.write('# Reactions \n')
        f.write('recorder Node -file $dataDirName/NodeReactions.out -time -node 100 -dof 1 2 3 reaction; \n\n')
        f.write('# Record drift histories \n')
        f.write('# Command: recorder Drift -file $filename -time -iNode $NodeI_ID -jNode $NodeJ_ID -dof $dof -perpDirn $Record.drift.perpendicular.to.this.direction \n')
        f.write('recorder Drift -file $dataDirName/DriftRoof.out -time -iNode 100 -jNode %s -dof 1 -perpDirn 2; # Roof \n' %(2*self.num_story+100))
        f.write('recorder Drift -file $dataDirName/DriftStory.out -time -iNode ')
        for i in range(0,self.num_story):
            f.write("%s " %(2*i+100))
        f.write('-jNode ')
        for i in range(1,self.num_story+1):
            f.write("%s " %(2*i+100))
        f.write('-dof 1 -perpDirn 2; # Story \n\n\n')
        f.write('# Record responses for wall elements \n')
        f.write('recorder Element -file $dataDirName/WallGlobalForces.out -time -ele ')
        for i in range(0,2*self.num_story):
            f.write("%s " %(1001+i))
        f.write('globalForce; \n')
        f.write('recorder Element -file $dataDirName/WallCurvature.out -time -ele ')
        for i in range(0,2*self.num_story):
            f.write("%s " %(1001+i))
        f.write('Curvature; \n')
        f.write('recorder Element -file $dataDirName/WallShearDef.out -time -ele ')
        for i in range(0,2*self.num_story):
            f.write("%s " %(1001+i))
        f.write('ShearDef; \n\n')
        f.write('# Record responses for wall fibers (one panel per recorder)\n')
        f.write('# Command: RCPanel $fibTag $Response \n')
        f.write('recorder Element -file $dataDirName/WallFiberStrain_f1.out -time -ele ')
        for i in range(0,2*self.num_story):
            f.write("%s " %(1001+i))
        f.write('RCPanel 1 panel_strain \n')
        f.write('recorder Element -file $dataDirName/WallFiberStrain_f6.out -time -ele ')
        for i in range(0,2*self.num_story):
            f.write("%s " %(1001+i))
        f.write('RCPanel 6 panel_strain \n')
        f.write('recorder Element -file $dataDirName/WallPanelStrain.out -time -ele 1001 RCPanel 1 panel_strain \n')
        f.write('recorder Element -file $dataDirName/WallPanelStress.out -time -ele 1001 RCPanel 1 panel_stress \n')
        f.write('recorder Element -file $dataDirName/WallStressConcrete.out -time -ele 1001 RCPanel 1 panel_stress_concrete \n')
        f.write('recorder Element -file $dataDirName/WallStressSteel.out -time -ele 1001 RCPanel 1 panel_stress_steel \n')
        f.write('recorder Element -file $dataDirName/WallPanelSteel1.out -time -ele 1001 RCPanel 1 strain_stress_steelX \n')
        f.write('recorder Element -file $dataDirName/WallPanelSteel2.out -time -ele 1001 RCPanel 1 strain_stress_steelY \n')
        f.write('recorder Element -file $dataDirName/WallPanelConcrete1.out -time -ele 1001 RCPanel 1 strain_stress_concrete1 \n')
        f.write('recorder Element -file $dataDirName/WallPanelConcrete2.out -time -ele 1001 RCPanel 1 strain_stress_concrete2 \n\n')       
                

        textList =[
        '# --------------------------------- Gravity Loads & Gravity Analysis ------------------------------------',
        '',
        '# Apply gravity loads',
        '',
        '# Assign point dead load values on wall: (kip)',
        'set	WallDeadLoadFloor	%.3f;' %(self.A_trib * self.DL_floor /1000), # design A_trib*DL
        '# Assign point live load values on wall: (kip)',
        'set	WallLiveLoadFloor	%.3f;' %(self.A_trib * self.LL_floor /1000), # design A_trib*LL
        '# Assign point dead load values on leaning column: (kip)',
        'set	LeaningColumnDeadLoadFloor	%.3f;' %(self.A_trib_leancol * self.DL_floor /1000), # design A_trib_leancol*DL
        '# Assign point live load values on leaning column: (kip)',
        'set	LeaningColumnLiveLoadFloor	%.3f;' %(self.A_trib_leancol * self.LL_floor /1000), # design A_trib_leancol*LL
        '',
        '# Construct a  time series where load factor applied is linearly proportional to the time domain',
        '# Command: pattern PatternType $PatternID TimeSeriesType',
        '# 104 Expected gravity loads: 1 DL + 0.25 LL (or 1.05 DL + 0.25 LL)',
        'pattern Plain 104 Constant {',
        '',
        '	# Nodal load on walls and PF columns - command: load nodeID xForce yForce',
        '	for {set i 1} {$i <= $NumStories} {incr i} { ',
        '		#load [expr 100 + 2*$i]  0.0 [expr -1*$WallDeadLoadFloor - 0.25*$WallLiveLoadFloor] 0.0;',
        '		#load [expr 21 + $i]  0.0 [expr -1*$LeaningColumnDeadLoadFloor - 0.25*$LeaningColumnLiveLoadFloor] 0.0;',
        '		load [expr 100 + 2*$i]  0.0 [expr -$WallDeadLoadFloor - $WallLiveLoadFloor] 0.0; # The inputs are already expected loads',
        '		load [expr 21 + $i]  0.0 [expr -$LeaningColumnDeadLoadFloor - $LeaningColumnLiveLoadFloor] 0.0; # The inputs are already expected loads',
        '	}',
        '}',
        '',
        '',
        '# Gravity-analysis: load-controlled static analysis',
        'set Tol 1.0e-6;							# convergence tolerance for test',
        'set NstepGravity 10;					# apply gravity in 10 steps',
        'set DGravity [expr 1.0/$NstepGravity];	# load increment',
        'constraints Plain;						# how it handles boundary conditions',
        "numberer RCM;							# renumber dof's to minimize band-width (optimization)",
        'system BandGeneral;						# how to store and solve the system of equations in the analysis (large model: try UmfPack)',
        'test NormDispIncr $Tol 6;				# determine if convergence has been achieved at the end of an iteration step',
        "algorithm Newton;						# use Newton's solution algorithm: updates tangent stiffness at every iteration",
        'integrator LoadControl $DGravity;		# determine the next time step for an analysis',
        'analysis Static;						# define type of analysis: static or transient',
        'analyze $NstepGravity;					# apply gravity',
        '',
        'puts "Model built & gravity analysis completed."'
        ]

        for line in textList:
          f.write(line)
          f.write("\n")          
    
    
    def modal(self):
        
        
        f = open('Modal.tcl','w')
        
        if self.num_story != 1:
            textList =[
            "# ----------------------------------------------------",
            "# Modal Analysis",
            "# ----------------------------------------------------",
            "",
            "# Generate the model and run gravity analysis	",
            "source build_model.tcl",
            "",
            "# --------------------------------- Rayleigh Damping ------------------------------------",
            "# Apply Rayleigh damping from $xDamp: (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/1099.htm)",
            "# D=$alphaM*M + $betaKcurr*Kcurrent + $betaKcomm*KlastCommit + $betaKinit*$Kinitial",
            "	set xDamp 0.02;										# Damping ratio",
            "	set MpropSwitch 1.0;								# Type 1.0 for each M and K matrix you want damping matrix to be proportional to.",
            "	set KcurrSwitch 1.0;								# Use this: tangent stiffness changes per time series in dynamic nonlinear analysis",
            "	set KcommSwitch 0.0;",
            "	set KinitSwitch 0.0;",
            "	set nEigenI 1;										# Mode i: 1",
            "	set nEigenJ 3;										# Mode j: 3",
            "	#OLD: set lambdaN [eigen -generalized -fullGenLapack $nEigenJ];",
            "	set lambdaN [eigen $nEigenJ]",
            "	set lambdaI [lindex $lambdaN [expr $nEigenI-1]]; 	# Eigenvalue mode i",
            "	set lambdaJ [lindex $lambdaN [expr $nEigenJ-1]]; 	# Eigenvalue mode j",
            "	set omegaI [expr pow($lambdaI,0.5)];",
            "	set omegaJ [expr pow($lambdaJ,0.5)];",
            "	set alphaM [expr $MpropSwitch*$xDamp*(2*$omegaI*$omegaJ)/($omegaI+$omegaJ)];	# M-prop. damping; D = alphaM*M",
            "	set betaKcurr [expr $KcurrSwitch*2.0*$xDamp/($omegaI+$omegaJ)];         		# Current-K + betaKcurr*KCurrent",
            "	set betaKcomm [expr $KcommSwitch*2.0*$xDamp/($omegaI+$omegaJ)];   				# Last-committed K + betaKcomm*KlastCommitt",
            "	set betaKinit [expr $KinitSwitch*2.0*$xDamp/($omegaI+$omegaJ)];         		# initial- K + betaKinit*Kini",
            "",
            "# Eigen analysis - for period	",
            "	set T {};",
            "	foreach lam $lambdaN {",
            "		lappend Tperiod [expr (2.0*$pi)/sqrt($lam)];",
            "	}",
            '	puts "T1 = [lindex $Tperiod 0] s"',
            '	puts "T2 = [lindex $Tperiod 1] s"',
            "",
            "# Apply reyleigh damping ",
            "rayleigh $alphaM $betaKcurr $betaKinit $betaKcomm; ",
            "",
            "# Display Deformed Shape",
            "set ViewScale 10;					    				# Amplify display of deformed shape",
            "#DisplayModel2D nill $ViewScale;							# Display optional"
            ]
            
        else:
            textList =[
            "# ----------------------------------------------------",
            "# Modal Analysis",
            "# ----------------------------------------------------",
            "",
            "# Generate the model and run gravity analysis	",
            "source build_model.tcl",
            "",
            "# --------------------------------- Rayleigh Damping ------------------------------------",
            "# Apply Rayleigh damping from $xDamp: (http://opensees.berkeley.edu/OpenSees/manuals/usermanual/1099.htm)",
            "# D=$alphaM*M + $betaKcurr*Kcurrent + $betaKcomm*KlastCommit + $betaKinit*$Kinitial",
            "	set xDamp 0.02;										# Damping ratio",
            "	set MpropSwitch 1.0;								# Type 1.0 for each M and K matrix you want damping matrix to be proportional to.",
            "	set KcurrSwitch 1.0;								# Use this: tangent stiffness changes per time series in dynamic nonlinear analysis",
            "	set KcommSwitch 0.0;",
            "	set KinitSwitch 0.0;",
            "	set nEigenI 1;										# Mode i: 1",
            "	set nEigenJ 1;										# Mode j: 3",
            "	#OLD: set lambdaN [eigen -generalized -fullGenLapack $nEigenJ];",
            "	set lambdaN [eigen $nEigenJ]",
            "	set lambdaI [lindex $lambdaN [expr $nEigenI-1]]; 	# Eigenvalue mode i",
            "	set lambdaJ [lindex $lambdaN [expr $nEigenJ-1]]; 	# Eigenvalue mode j",
            "	set omegaI [expr pow($lambdaI,0.5)];",
            "	set omegaJ [expr pow($lambdaJ,0.5)];",
            "	set alphaM [expr $MpropSwitch*$xDamp*(2*$omegaI)];	# M-prop. damping; D = alphaM*M",
            "	set betaKcurr [expr $KcurrSwitch*2.0*$xDamp/($omegaI)];         		# Current-K + betaKcurr*KCurrent",
            "	set betaKcomm [expr $KcommSwitch*2.0*$xDamp/($omegaI)];   				# Last-committed K + betaKcomm*KlastCommitt",
            "	set betaKinit [expr $KinitSwitch*2.0*$xDamp/($omegaI)];         		# initial- K + betaKinit*Kini",
            "",
            "# Eigen analysis - for period	",
            "	set T {};",
            "	foreach lam $lambdaN {",
            "		lappend Tperiod [expr (2.0*$pi)/sqrt($lam)];",
            "	}",
            '	puts "T1 = [lindex $Tperiod 0] s"',
            '	puts "T2 = [lindex $Tperiod 1] s"',
            "",
            "# Apply reyleigh damping ",
            "rayleigh $alphaM $betaKcurr $betaKinit $betaKcomm; ",
            "",
            "# Display Deformed Shape",
            "set ViewScale 10;					    				# Amplify display of deformed shape",
            "#DisplayModel2D nill $ViewScale;							# Display optional"
            ]            
        

        for line in textList:
          f.write(line)
          f.write("\n")
          
        f.close()        


    def DriftLimitTester(self):
        f = open('DriftLimitTester.tcl','w')

        textList =[
        '# SDRlimitTester ########################################################################',
        '#',
        '# Procedure that checks if the Pre-Specified Collapse Drift Limit is reached and Generate ',
        '# a Flag',
        '#',
        '# Developed by Dimitrios G. Lignos, Ph.D',
        '# Modified  by Ahmed Elkady, Ph.D',
        '#',
        '# First Created: 04/20/2010',
        '# Last Modified: 05/05/2020',
        '#',
        '# Modified by Muneera: 04/07/2022',
        '#',
        '# #######################################################################################',
        '',
        'proc DriftLimitTester {numStories SDRlimit FloorNodes h1 htyp} {',
        '',
        ' global CollapseFlag',
        ' set CollapseFlag "NO"',
        ' ',
        ' global CollapseFlagReader',
        ' ',
        '	 # Read the Floor Node Displacements and Deduce the Story Drift Ratio',
        '	 for {set i 0} {$i<=$numStories-1} {incr i} {',
        '		if { $i==0 } {',
        '			set Node [lindex $FloorNodes $i]',
        '			set NodeDisplI [nodeDisp $Node 1]',
        '			set SDR [expr $NodeDisplI/$h1]',
        '			lappend Drift [list $SDR]',
        '			',
        '		} elseif { $i > 0 } {',
        '			set NodeI [lindex $FloorNodes $i]',
        '			set NodeDisplI [nodeDisp $NodeI 1]',
        '			set NodeJ [lindex $FloorNodes [expr $i-1]]',
        '			set NodeDisplJ [nodeDisp $NodeJ 1]',
        '			set SDR [expr ($NodeDisplI - $NodeDisplJ)/$htyp]',
        '			lappend Drift [list  $SDR]',
        '',
        '		}',
        '	 } ',
        '	 ',
        '	# Check if any Story Drift Ratio Exceeded the Drift Limit	 ',
        '	for {set i 0} {$i <= $numStories-1} {incr i} {',
        '	    set TDrift [ lindex $Drift [expr $i] ]',
        '		set TDrift [expr abs($TDrift)]',
        '		',
        '		# IF the Story Drift Ratio at Current Story is Less than the Drift Limit then',
        '		# Open a file named "CollapseState.txt" and write a value of "0" for no collapse',
        '		if {$TDrift < $SDRlimit} {',
        '			set CollapseFlagReader 0;                # Write value of 0 in case of no collapse ',
        '		}',
        '		',
        '		# If Drift Limit was exceeded',
        '		if { $TDrift > $SDRlimit} {',
        '			set CollapseFlag "YES"',
        '			puts "Collapse"',
        '			set CollapseFlagReader 1;                # Write value of 1 in case of collapse',
        '		}',
        '	}',
        '}'
        ]

        for line in textList:
          f.write(line)
          f.write("\n")
          
        f.close()           


    def solver(self):
        f = open('Solver.tcl','w')

        textList =[
        '# DynamicAnalysisCollapseSolver #########################################################',
        '#',
        '# This Solver is used for Collapse "hunting"',
        '# Time Controlled Algorithm that keeps original run',
        '#',
        '# Developed by Dimitrios G. Lignos, Ph.D',
        '#',
        '# First Created: 04/20/2010',
        '# Last Modified: 08/23/2011',
        '#',
        '# Modified by Muneera: 04/07/2022',
        '#',
        '# Uses:',
        '# 1. dt            : Ground Motion step',
        '# 2. dt_anal_Step  : Analysis time step',
        '# 3. GMtime        : Ground Motion Total Time',
        '# 4. numStories    : DriftLimit',
        '# ',
        '# Subroutines called:',
        '# DriftLimitTester: Checks after loss of convergence the drifts ',
        '#                 and guarantees convergence for collapse',
        '#',
        '# Integrator Used: Modified Implicit: Hilbert Hughes Taylor with Increment Reduction',
        '# #######################################################################################',
        '',
        'proc DynamicAnalysisCollapseSolver {dt dt_anal_Step GMtime numStories SDRlimit FloorNodes h1 htyp StartTime} {',
        ' ',
        'global CollapseFlag;                                        # global variable to monitor collapse',
        'set CollapseFlag "NO"',
        '',
        'wipeAnalysis',
        '',
        'constraints Plain',
        'numberer RCM',
        'system UmfPack',
        'test EnergyIncr 1.0e-3 100',
        'algorithm KrylovNewton',
        'integrator Newmark 0.50 0.25',
        'analysis Transient',
        '',
        'set maxRunTime 14400;',
        'set startT [clock seconds];',
        '',
        'set NumSteps [expr round(($GMtime + 0.0)/$dt_anal_Step)];	# number of steps in analysis',
        'set ok [analyze $NumSteps $dt_anal_Step];',
        '',
        '# Check Max Drifts for Collapse by Monitoring the CollapseFlag Variable',
        'source DriftLimitTester.tcl;',
        'DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp',
        '',
        '',
        'if  {$CollapseFlag == "YES"} {',
        '	set ok 0',
        '	puts "----> Collapse Occured";',
        '}',
        '',
        '# Check run time to see if it is in excess of maximum allotted time',
        'set currentT [clock seconds];',
        'set runTime [expr $currentT - $startT];',
        'if  {$runTime > $maxRunTime} {',
        '	set ok 0',
        '}',
        '',
        '# If analysis failed',
        ' if {$ok != 0} {',
        '	puts "Analysis did not converge..."',
        '	# The analysis will be time-controlled and is done for the remaining time',
        '	set ok 0;',
        '	set controlTime [getTime];',
        '	',
        '	# While the GM did not finish OR while analysis is failing',
        '	while {$controlTime < $GMtime || $ok !=0 } {',
        '		DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp',
        '		if  {$CollapseFlag == "YES"} {',
        '			set ok 0; break;',
        '		} else {',
        '			set ok 1',
        '		}',
        '		# Check run time to see if it is in excess of maximum allotted time',
        '		set currentT [clock seconds];',
        '		set runTime [expr $currentT - $startT];',
        '		if  {$runTime > $maxRunTime} {',
        '			set ok 0; break;',
        '		}	',
        '		',
        '	    # Get Control Time inside the loop',
        '		set controlTime [getTime]',
        '		puts "----> Currently at time $controlTime out of $GMtime"',
        '',
        '		if {$ok != 0} {',
        '			puts "Run Newton 100 steps with 1/2 of step.."',
        '			set controlTime [getTime]',
        '			set remainTime [expr $GMtime - $controlTime]',
        '			set NewRemainSteps [expr round(($remainTime)/($dt_anal_Step/2.0))]',
        '',
        '			test EnergyIncr 1.0e-3 100   0',
        '			algorithm KrylovNewton',
        '			integrator Newmark 0.50 0.25',
        '			set ok [analyze 10 [expr $dt_anal_Step/2.0]]',
        '			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp',
        '			if  {$CollapseFlag == "YES"} {',
        '				set ok 0',
        '			}',
        '			# Check run time to see if it is in excess of maximum allotted time',
        '			set currentT [clock seconds];',
        '			set runTime [expr $currentT - $startT];',
        '			if  {$runTime > $maxRunTime} {',
        '				set ok 0; break;',
        '			}	',
        '		}',
        '		if {$ok != 0 } {		',
        '			puts "Go Back to KrylovNewton with tangent Tangent and original step.."',
        '			set controlTime [getTime]',
        '			set remainTime [expr $GMtime - $controlTime]',
        '			set NewRemainSteps [expr round(($remainTime)/($dt_anal_Step))]',
        '			',
        '			test EnergyIncr 1.0e-2 100   0',
        '			algorithm KrylovNewton',
        '			integrator Newmark 0.50 0.25',
        '			set ok [analyze $NewRemainSteps [expr $dt_anal_Step]]',
        '			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp',
        '			if  {$CollapseFlag == "YES"} {',
        '				set ok 0',
        '			}',
        '			# Check run time to see if it is in excess of maximum allotted time',
        '			set currentT [clock seconds];',
        '			set runTime [expr $currentT - $startT];',
        '			if  {$runTime > $maxRunTime} {',
        '				set ok 0; break;',
        '			}	',
        '		}',
        '		if {$ok != 0 } {',
        '			puts "Run 10 steps KrylovNewton with Initial Tangent with 1/2 of original step.."',
        '			set controlTime [getTime]',
        '			set remainTime [expr $GMtime - $controlTime]',
        '			set NewRemainSteps [expr round(($remainTime)/($dt_anal_Step/2.0))]',
        '			test EnergyIncr 1.0e-2 200 0	',		
        '			algorithm KrylovNewton -initial',
        '			set ok [analyze 10 [expr $dt_anal_Step/2.0]]',
        '			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp',
        '			if  {$CollapseFlag == "YES"} {',
        '				set ok 0',
        '			}',
        '			# Check run time to see if it is in excess of maximum allotted time',
        '			set currentT [clock seconds];',
        '			set runTime [expr $currentT - $startT];',
        '			if  {$runTime > $maxRunTime} {',
        '				set ok 0; break;',
        '			}	',
        '		}',
        '		if {$ok != 0 } {			',
        '			puts "Go Back to KrylovNewton with tangent Tangent and original step.."',
        '			set controlTime [getTime]',
        '			set remainTime [expr $GMtime - $controlTime]',
        '			set NewRemainSteps [expr round(($remainTime)/($dt_anal_Step))]',
        '			test EnergyIncr 1.0e-2 100   0',
        '			algorithm KrylovNewton',
        '			integrator Newmark 0.50 0.25',
        '			set ok [analyze $NewRemainSteps [expr $dt_anal_Step]]',
        '			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp',
        '			if  {$CollapseFlag == "YES"} {',
        '				set ok 0',
        '			}',
        '			# Check run time to see if it is in excess of maximum allotted time',
        '			set currentT [clock seconds];',
        '			set runTime [expr $currentT - $startT];',
        '			if  {$runTime > $maxRunTime} {',
        '				set ok 0; break;',
        '			}	',
        '		}			',	
        '',
        '		if {$ok != 0 } {	',		
        '			puts "Go Back to KrylovNewton with tangent Tangent and 0.001 step.."',
        '			set controlTime [getTime]',
        '			set remainTime [expr $GMtime - $controlTime]',
        '			set NewRemainSteps [expr round(($remainTime)/(0.001))]',
        '			test EnergyIncr 1.0e-2 200   0',
        '			algorithm KrylovNewton',
        '			integrator Newmark 0.50 0.25',
        '			set ok [analyze $NewRemainSteps [expr 0.001]]',
        '			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp',
        '			if  {$CollapseFlag == "YES"} {',
        '				set ok 0',
        '			}',
        '			# Check run time to see if it is in excess of maximum allotted time',
        '			set currentT [clock seconds];',
        '			set runTime [expr $currentT - $startT];',
        '			if  {$runTime > $maxRunTime} {',
        '				set ok 0; break;',
        '			}	',
        '		}				',
        '		if {$ok != 0 } {',
        '			puts "KrylovNewton Initial with 1/2 of step and Displacement Control Convergence.."',
        '			test EnergyIncr 1.0e-2 100  0',
        '			algorithm KrylovNewton -initial',
        '			set ok [analyze 10 [expr $dt_anal_Step/2.0]]',
        '			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp',
        '			if  {$CollapseFlag == "YES"} {',
        '				set ok 0',
        '			}',
        '			# Check run time to see if it is in excess of maximum allotted time',
        '			set currentT [clock seconds];',
        '			set runTime [expr $currentT - $startT];',
        '			if  {$runTime > $maxRunTime} {',
        '				set ok 0; break;',
        '			}	',
        '		}',
        '		if {$ok != 0 } {	',		
        '			puts "Go Back to KrylovNewton with tangent Tangent and 0.0001 step.."',
        '			set controlTime [getTime]',
        '			set remainTime [expr $GMtime - $controlTime]',
        '			set NewRemainSteps [expr round(($remainTime)/(0.0001))]',
        '			test EnergyIncr 1.0e-2 100   0',
        '			algorithm KrylovNewton',
        '			integrator Newmark 0.50 0.25',
        '			set ok [analyze 5 [expr 0.0001]]',
        '			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp',
        '			if  {$CollapseFlag == "YES"} {',
        '				set ok 0',
        '			}',
        '			# Check run time to see if it is in excess of maximum allotted time',
        '			set currentT [clock seconds];',
        '			set runTime [expr $currentT - $startT];',
        '			if  {$runTime > $maxRunTime} {',
        '				set ok 0; break;',
        '			}	',
        '		}		',
        '',
        '		if {$ok != 0 } {	',		
        '			puts "Go Back to KrylovNewton with tangent Tangent and original step.."',
        '			set controlTime [getTime]',
        '			set remainTime [expr $GMtime - $controlTime]',
        '			set NewRemainSteps [expr round(($remainTime)/($dt_anal_Step))]',
        '			test EnergyIncr 1.0e-2 100   0',
        '			algorithm KrylovNewton',
        '			integrator Newmark 0.50 0.25',
        '			set ok [analyze $NewRemainSteps [expr $dt_anal_Step]]',
        '			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp',
        '			if  {$CollapseFlag == "YES"} {',
        '				set ok 0',
        '			}',
        '			# Check run time to see if it is in excess of maximum allotted time',
        '			set currentT [clock seconds];',
        '			set runTime [expr $currentT - $startT];',
        '			if  {$runTime > $maxRunTime} {',
        '				set ok 0; break;',
        '			}	',
        '		}		',
        '		if {$ok != 0 } {',
        '			puts "Newton with Fixed Number of Iterations else continue"',
        '			set controlTime [getTime]',
        '			set remainTime [expr $GMtime - $controlTime]',
        '			set NewRemainSteps [expr round(($remainTime)/(0.0001))]',
        '			puts $NewRemainSteps',
        '			test FixedNumIter 50',
        '			integrator NewmarkHSFixedNumIter 0.5 0.25',
        '',
        '			algorithm Newton',
        '',
        '			set ok [analyze 10 [expr 0.0001]]',
        '			DriftLimitTester $numStories $SDRlimit $FloorNodes $h1 $htyp',
        '			if  {$CollapseFlag == "YES"} {',
        '				set ok 0',
        '			}',
        '			# Check run time to see if it is in excess of maximum allotted time',
        '			set currentT [clock seconds];',
        '			set runTime [expr $currentT - $startT];',
        '			if  {$runTime > $maxRunTime} {',
        '				set ok 0; break;',
        '			}				',
        '		}	',
        '		set controlTime [getTime]',	
        '',
        '	}',
        ' }',
        'global recordcontrolTime',
        'set recordcontrolTime [getTime]	',
        '}'
        ]

        for line in textList:
          f.write(line)
          f.write("\n")
          
        f.close()   
        
       
    def dynamic_analysisSolver(self):
        f = open('dynamic_analysisSolver.tcl','w')

        textList =[
        '# ----------------------------------------------------------------',
        '# Dynamic Time-History Analysis',
        '# ----------------------------------------------------------------',
        '',
        '# Perform modal analysis',
        'source Modal.tcl',
        'source Solver.tcl',
        '',
        '# First, set gravity loads acting constant and time in domain to 0.0',
        '	loadConst -time 0.0',
        '',
        '# Define ground motion parameters',
        '	cd $rootDir',
        '	set GMfile "GMfiles/$GMname.txt";				# Ground motion filename, input is in g units',
        '	set DtSeries	$GMdt;							# time-step Dt for definition of time series',
        '	set NSteps 		$GMnumOfSteps;					# Number of steps in ground motion',
        '',
        '# Define ground motion parameters',
        '	set patternID 2;								# Load pattern ID',
        '	set GMdirection 1;								# Ground motion direction (1 = x)',
        '	set Scalefactor [expr $GMsf*$g];				# Ground motion scaling factor',
        '',
        '	set DtAnalysis	[expr $GMdt/2.0];				# time-step Dt for lateral analysis',
        '	set TmaxAnalysis [expr $DtSeries*$NSteps];		# maximum duration of ground-motion analysis -- should be 50*$sec',
        '',
        '# Define the acceleration series for the ground motion',
        '	# Command: "Series -dt $timestep_of_record -filePath $filename_with_acc_history -factor $scale_record_by_this_amount"',
        '	set accelSeries "Series -dt $DtSeries -filePath $GMfile -factor $Scalefactor";',
        '',
        '# Create load pattern: apply acceleration to all fixed nodes with UniformExcitation',
        '	# Command: pattern UniformExcitation $patternID $GMdir -accel $timeSeriesID ',
        '	pattern UniformExcitation $patternID $GMdirection -accel $accelSeries;',
        '',
        '	puts "GM parameters and acceleration series defined."',
        '',
        '	wipeAnalysis; # destroy all components of the Analysis object',
        '',
        ''
        ]
        
        for line in textList:
             f.write(line)
             f.write("\n")
        
        f.write('set FloorNodes [list')
        
        for i in range(1,self.num_story+1):
            f.write(" %s" %(2*i+100))
        
        textList =[
        '];',
        'set firstTimeCheck [clock seconds];',
        '',
        '# To be able to source DriftLimitTester.tcl within the "DynamicAnalysisCollapseSolver"',
        'cd $baseDir ',
        '',
        'DynamicAnalysisCollapseSolver  $DtSeries $DtAnalysis $TmaxAnalysis $NumStories 0.2 $FloorNodes $FirstStory $TypicalStory $firstTimeCheck',
        '',
        '',
        '###################################################################################################',
        '###################################################################################################',
        '							puts "Ground Motion Done. End Time: [getTime]"',
        '###################################################################################################',
        '###################################################################################################'
        ]

        for line in textList:
          f.write(line)
          f.write("\n")
          
        f.close()   
        

    def runAll(self):
            f = open('runAll.tcl','w')
    
            textList =[
            '# This file runs the model for the pushover analysis and all (or selected) ground motions.',
            '',
            'wipe all;',
            'set numOfGMs %.0f;'%(self.numGM),
            '',
            'set baseDir [pwd]',
            'cd $baseDir',
            '',
            '# Reading Ground Motion names',
            'set fp1 [open "allGMname.txt" r];',
            'set allGMname [read $fp1];',
            'close $fp1;',
            '',
            '# Reading Ground Motion time intervals',
            'set fp2 [open "allGMdt.txt" r];',
            'set allGMdt [read $fp2];',
            'close $fp2;',
            '',
            '# Reading Ground Motion number of steps',
            'set fp3 [open "allGMnumOfSteps.txt" r];',
            'set allGMnumOfSteps [read $fp3];',
            'close $fp3;',
            '',
            '# Reading Ground Motion scale factor',
            'set fp4 [open "allGMsf.txt" r];',
            'set allGMsf [read $fp4];',
            'close $fp4;',
            '',
            'puts "Total number of Ground Motions to be run is: $numOfGMs";',
            '',
            'for {set GMcounter 1} {$GMcounter <= $numOfGMs} {incr GMcounter} {',
            '',
            '	set GMname [lindex $allGMname [expr $GMcounter - 1]];',
            '	puts "Current Ground Motion name is: $GMname";',
            '',
            '	set GMdt [lindex $allGMdt [expr $GMcounter - 1]];',
            '	puts "Time increment of current ground motion is: $GMdt";',
            '',
            '	set GMnumOfSteps [lindex $allGMnumOfSteps [expr $GMcounter - 1]];',
            '	puts "The number of steps for current Ground Motion is: $GMnumOfSteps";',
            '',
            '	set GMsf [lindex $allGMsf [expr $GMcounter - 1]];',
            '	puts "The scale factor for current Ground Motion is: $GMsf";',
            '',
            '	# Creating the model, applying gravity load and running for dynamic analysis',
            '',
            '	# Setting Up directories',
            '	set dataDirName GM$GMcounter;',
            '	cd $baseDir',
            '	file mkdir $dataDirName;',
            '',
            '	source dynamic_analysisSolver.tcl;',
            '',
            '	puts "Ground Motion $GMname done.";',
            '	puts " ";',
            '	puts " ";',
            '	puts " ";',
            '	wipe;',
            '}',
            '',
            'puts "ALL ground motions are done!";'
            ]
    
            for line in textList:
              f.write(line)
              f.write("\n")
              
            f.close()
       
        
    def run_OpenSees(self):
        self.build_model()
        self.modal()
        self.DriftLimitTester()
        self.solver()
        #self.dynamic_analysis()
        self.dynamic_analysisSolver()
        #self.dynamic_analysis_extensive()
        #self.runAll()  