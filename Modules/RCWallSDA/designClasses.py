"""
Created by: Muneera Aladsani - UCLA

Previous edit: Nov 26 2021
Last edit: Oct 24 2022

"""

import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

import scipy
import shutil
import os

class AccParam():
    
    def __init__(self, Building_length,Building_width,DL_floor,DL_roof,LL_floor,LL_roof,num_story,N_length,N_width,first_story,typical_story,Ss,S1,site_class,TL):
        self.Building_length = Building_length #ft (parallel to length of wall)
        self.Building_width = Building_width #ft (perpendicular to length of wall)
        self.DL_floor = DL_floor #psf
        self.DL_roof = DL_roof #psf
        self.LL_floor = LL_floor #psf
        self.LL_roof = LL_roof #psf
        self.num_story = num_story
        self.N_length = N_length #parallel to length
        self.N_width = N_width #perpendicular to length
        self.first_story = first_story #ft
        self.typical_story = typical_story #ft
        self.Ss = Ss #g
        self.S1 = S1 #g
        self.site_class = site_class #"X"
        self.TL = TL #seconds
        
        
    def acc_params(self):
        """
        Finding design earthquake spectral response acceleration parameters at 
        short periods (Sds) and at 1-s periods (Sd1) using ASCE 7-16.
        
        Inputs:
        - Ss: The mapped MCE_R spectral response acceleration parameter
        at short periods (in g).
        - S1: The mapped MCER spectral response acceleration parameter
        at a period of 1 s (in g).
        - site_class: Site class (as string in capital letters).
        
        Returns a tuple of:
        - SDs
        - SD1
        """
    
        #Finding Short-Period Site Coefficient (Fa) from Table 11.4-1
        if self.site_class == 'A':
            Fa = 0.8
        elif self.site_class == 'B':
            Fa = 0.9
        elif self.site_class == 'C':
            if self.Ss <= 0.5:
                Fa = 1.3
            elif (self.Ss > 0.5 and self.Ss < 0.75):
                Fa = 1.3 + (self.Ss-0.5) * ((1.2-1.3)/(0.75-0.5))
            elif self.Ss >= 0.75:
                Fa = 1.3
        elif self.site_class == 'D':
            if self.Ss <= 0.25:
                Fa = 1.6
            elif (self.Ss > 0.25 and self.Ss <= 0.5):
                Fa = 1.6 + (self.Ss-0.25) * ((1.4-1.6)/(0.5-0.25))
            elif (self.Ss > 0.5 and self.Ss <= 0.75):
                Fa = 1.4 + (self.Ss-0.5) * ((1.2-1.4)/(0.75-0.5))
            elif (self.Ss > 0.75 and self.Ss <= 1):
                Fa = 1.2 + (self.Ss-0.75) * ((1.1-1.2)/(1-0.75))
            elif (self.Ss > 1 and self.Ss <= 1.25):
                Fa =1.1 + (self.Ss-1) * ((1-1.1)/(1.25-1))
            elif self.Ss >= 1.25:
                Fa = 1
        elif self.site_class == 'E':
            if self.Ss <= 0.25:
                Fa = 2.4
            elif (self.Ss > 0.25 and self.Ss <= 0.5):
                Fa = 2.4 + (self.Ss-0.25) * ((1.7-2.4)/(0.5-0.25))
            elif (self.Ss > 0.5 and self.Ss <= 0.75):
                Fa = 1.7 + (self.Ss-0.5) * ((1.3-1.7)/(0.75-0.5))
            else:
                raise ValueError('Invalid - Check ASCE 7-16 Table 11.4-1')              
        else:
            raise ValueError('Invalid - Check ASCE 7-16 Table 11.4-1')
                
        #Finding Long-Period Site Coefficient (Fv) from Table 11.4-2
        if self.site_class == 'A':
            Fv = 0.8
        elif self.site_class == 'B':
            Fv = 0.8
        elif self.site_class == 'C':
            if self.S1 <= 0.5:
                Fv = 1.5
            elif (self.S1 > 0.5 and self.S1 < 0.6):
                Fv = 1.5 + (self.S1-0.5) * ((1.4-1.5)/(0.6-0.5))
            elif self.S1 >= 0.6:
                Fv = 1.4
        elif self.site_class == 'D':
            if self.S1 <= 0.1:
                Fv = 2.4
            elif (self.S1 > 0.1 and self.S1 <= 0.2):
                Fv = 2.4 + (self.S1-0.1) * ((2.2-2.4)/(0.2-0.1))
            elif (self.S1 > 0.2 and self.S1 <= 0.3):
                Fv = 2.2 + (self.S1-0.2) * ((2-2.2)/(0.3-0.2))
            elif (self.S1 > 0.3 and self.S1 <= 0.4):
                Fv = 2 + (self.S1-0.3) * ((1.9-2)/(0.4-0.3))        
            elif (self.S1 > 0.4 and self.S1 <= 0.5):
                Fv = 1.9 + (self.S1-0.4) * ((1.8-1.9)/(0.5-0.4))
            elif (self.S1 > 0.5 and self.S1 <= 0.6):
                Fv = 1.8 + (self.S1-0.5) * ((1.7-1.8)/(0.6-0.5))
            elif self.S1 >= 0.6:
                Fv = 1.7
        elif self.site_class == 'E':
            if self.S1 <= 0.1:
                Fv = 4.2
            else:
                raise ValueError('Invalid - Check ASCE 7-16 Table 11.4-2')             
        else:
            raise ValueError('Invalid - Check ASCE 7-16 Table 11.4-2')
                
        #Finding Risk-Targeted Maximum Considered Earthquake Spectral Response
        #Acceleration Parameters.
        Sms = Fa * self.Ss
        Sm1 = Fv * self.S1
        
        self.SDs = (2/3) * Sms
        self.SD1 = (2/3) * Sm1
        


class ELF(AccParam):

    def __init__(self, Building_length,Building_width,DL_floor,DL_roof,LL_floor,LL_roof,num_story,N_length,N_width,first_story,typical_story,Ss,S1,site_class,TL,lw,
                 b,fc,num_walls,edge_wall,R,Ie,Cd):  
            self.lw = lw #inch
            self.b = b #inch
            self.fc = fc*1000 #psi
            self.num_walls = num_walls
            self.edge_wall = edge_wall #"Yes" or "No"
            self.R = R
            self.Ie = Ie
            self.Cd = Cd
            self.Ct = 0.02 #Table 12.8-2 (ASCE 7-16)
            self.x_asce = 0.75 #Table 12.8-2 (ASCE 7-16)

            # invoking the constructor of the AccParam class   
            AccParam.__init__(self, Building_length,Building_width,DL_floor,DL_roof,LL_floor,LL_roof,num_story,N_length,N_width,first_story,typical_story,Ss,S1,site_class,TL)
            
            AccParam.acc_params(self)
    
    def wall_params(self):
        """
        Returns parameters such as seismic weights and tributary areas
        """
        self.I = self.b*(self.lw**3)/12  
        self.Ec = 57000*np.sqrt(self.fc)/1000
        self.Ieff = 0.5*self.I
        self.W_typical = (self.DL_floor*self.Building_length*self.Building_width) / 1000
        self.W_roof = (self.DL_roof*self.Building_length*self.Building_width) / 1000
        
        if self.edge_wall == "Yes":
            B_trib = self.b + ((self.Building_width/self.N_width)*12-self.b)/2
        if self.edge_wall == "No":
            B_trib = self.b + (2*(self.Building_width/self.N_width)*12-self.b)/2
            
        self.L_trib = self.lw + (3*(self.Building_length/self.N_length)*12-self.lw)/2
        self.A_trib = self.L_trib * B_trib / (12)**2 #ft2
        self.A_trib_leancol = (self.Building_length*self.Building_width/2) - self.A_trib

        
    def vertical_dist_forces(self):
        """
        Finding Vertical Distribution of Seismic Forces using ASCE 7-16 Section 12.8.
        
        Inputs:
        - b: Thickness of the wall (in inch).
        - lw: length of the wall (in inch).
        - typical_story: Height of stories above the first story (in ft).
        - first_story: Height of the first story (in ft).
        - num_story: Number of stories.
        - DL_roof: Dead load for the roof (in psf).
        - DL_floor: Dead load for the floor (in psf).
        - Building_length: Length of the building which is parallel to length
        of wall (in ft).
        - Building_width: Width of the building which is perpendicular to length
        of wall (in ft).
        - num_walls: Number of walls in the desired direction.
        - R: Response modification factor.
        - Ie: Importance Factor.
        - S1: The mapped MCER spectral response acceleration parameter
        at a period of 1 s (in g). 
        - SDs: Design spectral response acceleration parameter at short periods.
        - SD1: Design spectral response acceleration parameter at a 1-s period.
        - TL: long-period transition period (in seconds).
        - Ct: Approximate period parameter (Table 12.8-2)
        - x_asce:  Approximate period parameter (Table 12.8-2)
        
        Returns a list of:
        - F
        """
        
        # Structural height
        hn = (self.typical_story*(self.num_story-1)+self.first_story)
        
        # The approximate fundamental period
        Ta = self.Ct * (hn)**self.x_asce
        
        # Seismic response coefficient (Cs)            
        Cs = self.SDs / (self.R/self.Ie)
        
        if Ta <= self.TL:
            Cs1 = self.SD1 / (Ta*self.R/self.Ie)
        else:
            Cs1 = self.SD1*self.TL / (Ta**2 * (self.R/self.Ie))
        
        if Cs > Cs1:
            Cs = Cs1
        
        Cs2 = 0.044*self.SDs*self.Ie
        if Cs2 <= 0.01:
            Cs2 = 0.01
        
        if Cs < Cs2:
            Cs = Cs2
        
        Cs3 = 0    
        if self.S1 > 0.6:
            Cs3 = 0.5*self.S1 / (self.R/self.Ie)
            
        if Cs < Cs3:
            Cs = Cs3
            
        # Effective seismic weight
        W_typical = (self.DL_floor * self.Building_length * self.Building_width) / 1000
        W_roof = (self.DL_roof * self.Building_length * self.Building_width) / 1000
        
        # Seismic base shear
        self.V = Cs*W_typical*(self.num_story-1) + Cs*W_roof
        self.V = self.V/self.num_walls #for each wall
        
        # Finding k (an exponent related to the structure period)
        if Ta <= 0.5:
            k = 1
        elif Ta >= 2.5: 
            k = 2
        else:
            k = 0.5*Ta+0.75
        
        # Finding the sum
        the_sum = 0
        for i in range(0,self.num_story):
            if i==0:
                cv = W_typical*((i+1)*self.first_story)**k
            elif i==(self.num_story-1):
                cv = W_roof*((i+1)*self.typical_story)**k
            else:
                cv = W_typical*((i+1)*self.typical_story)**k
            the_sum = the_sum + cv
        
        # Vertical Distribution of Seismic Force  
        self.F = []
        for i in range(0,self.num_story):
            if i==0:
                f = self.V * (W_typical*((i+1)*self.first_story)**k) / the_sum
            elif i==(self.num_story-1):
                f = self.V * (W_roof*((i+1)*self.typical_story)**k) / the_sum
            else:
                f = self.V * (W_typical*((i+1)*self.typical_story)**k) / the_sum
            self.F.append(f)
            
        for i in range(0,self.num_story):
            self.F.append(0)
            
            

class ElasticAnalysis(ELF,AccParam):
      
    def __init__(self, Building_length,Building_width,DL_floor,DL_roof,LL_floor,LL_roof,num_story,N_length,N_width,first_story,typical_story,Ss,S1,site_class,TL,
                     lw,b,fc,num_walls,edge_wall,R,Ie,Cd):

        # invoking the constructor of the ELF class   
        ELF.__init__(self, Building_length,Building_width,DL_floor,DL_roof,LL_floor,LL_roof,num_story,N_length,N_width,first_story,typical_story,Ss,S1,site_class,TL,
                     lw,b,fc,num_walls,edge_wall,R,Ie,Cd)
        
        ELF.wall_params(self)
        ELF.vertical_dist_forces(self)
        
    
    def define_variables(self):
        f = open('DefineVariables.tcl','w')

        textList =[
        "# Define Geometric Transformations",
        "	set PDeltaTransf 1;",
        "	set LinearTransf 2;",
        "",
        "# Set up geometric transformations of element",
        "	geomTransf PDelta $PDeltaTransf; 							# PDelta transformation",
        "	geomTransf Linear $LinearTransf;",
        "",
        "# Define Young's modulus of concrete",
        "	set Ec 	%.3f;"%(self.Ec),
        "",
        "# Define very small number",
        "	set Negligible 1e-12;",
        "",
        "# Define gravity constant",
        "	set g 386.4;",
        "",
        "# Define rigid links between leaning column and frame",
        "	set TrussMatID 600; 	# Material tag",
        "	set AreaRigid  1e9; 	# Large area",
        "	set IRigid 	   1e9;     # Large moment of inertia",
        "	uniaxialMaterial Elastic $TrussMatID $Ec;",
        "",
        '# puts "Variables defined"'
        ]

        for line in textList:
          f.write(line)
          f.write("\n")
          
        f.close()


    def define_functions(self):
        
        f = open('DefineFunctionsAndProcedures.tcl','w')
        
        textList =[
        "##############################################################################################################################",
        "#          	  				       Define rotational springs for leaning column 						    				 #",
        "##############################################################################################################################",
        "",
        "proc rotLeaningCol {eleID nodeR nodeC} {",
        "",
        "# 	Formal arguments",
        "#       eleID   - unique element ID for this zero length rotational spring",
        "#       nodeR   - node ID which will be retained by the multi-point constraint",
        "#       nodeC   - node ID which will be constrained by the multi-point constraint",
        "",
        "	#Spring Stiffness",
        "	set K 1e-9; # k/in",
        "",
        "	# Create the material and zero length element (spring)",
        "    uniaxialMaterial Elastic  $eleID  $K	",
        "	element zeroLength $eleID $nodeR $nodeC -mat $eleID -dir 6",
        "",
        "",
        "	# Constrain the translational DOF with a multi-point constraint	",
        "	#   		retained constrained DOF_1 DOF_2",
        "",
        "	equalDOF    $nodeR     $nodeC     1     2",
        "}",
        ""
        ]
        
        for line in textList:
          f.write(line)
          f.write("\n")
          
        f.close()
        
        
    def define_nodes(self):
        
        f = open('DefineNodes2DModel.tcl','w')
        
        f.write("# This file will be used to define all nodes\n")
        f.write("# Units: inch\n\n\n")
                
        f.write("# Set wall length and story height\n")
        f.write("set Lw %.3f;\n" %(self.lw))
        f.write("set	FirstStory	%.3f;\n" %(self.first_story*12))
        f.write("set	TypicalStory	%.3f;\n\n\n" %(self.typical_story*12))
        
        f.write("# Define nodes for wall\n")
        for i in range(0,self.num_story+1):
            if i == 0 or i == 1:
                f.write("node	%s	0	[expr %s*$FirstStory+0*$TypicalStory]; # Level %s\n" %((i+1)*100, i, (i+1)))
            else:
                f.write("node	%s	0	[expr 1*$FirstStory+%s*$TypicalStory]; # Level %s\n" %((i+1)*100, (i-1), (i+1)))
                            
        f.write('\n# puts "Nodes for wall defined"\n\n\n')
        
        f.write("# Define nodes for leaning column\n")
        for i in range(0,self.num_story+1):
            if i == 0 or i == 1:
                f.write("node	2%s	[expr 1*$Lw]	[expr %s*$FirstStory+0*$TypicalStory]; # Level %s\n" %((i+1), i, (i+1)))
            else:
                f.write("node	2%s	[expr 1*$Lw]	[expr 1*$FirstStory+%s*$TypicalStory]; # Level %s\n" %((i+1), (i-1), (i+1)))
        
        f.write('\n# puts "Nodes for leaning column defined"\n\n\n')    
                
        f.write("# Define extra nodes needed to define leaning column springs\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("node 2%s2 [expr 1*$Lw]	[expr 1*$FirstStory+%s*$TypicalStory];	# Node below floor level %s\n" %((i+2), i, (i+2)))
                f.write("node 2%s4 [expr 1*$Lw]	[expr 1*$FirstStory+%s*$TypicalStory];	# Node above floor level %s\n" %((i+2), i, (i+2)))
            else:
                f.write("node 2%s2 [expr 1*$Lw]	[expr 1*$FirstStory+%s*$TypicalStory];	# Node below floor level %s\n" %((i+2), i, (i+2)))
        
        f.write('\n# puts "Extra nodes for leaning column springs defined"\n')    
        
        f.close()
        
        
    def define_fixities(self):

        f = open('DefineFixities2DModel.tcl','w')
        
        textList =[
        "# This file will be used to define the fixity at all wall and column bases",
        "",
        "",
        "# Defining fixity at column base",
        "fix	100	1	1	1;",
        "fix	21	1	1	0;",
        "",
        '# puts "All base fixities have been defined"'
        ]
        
        for line in textList:
          f.write(line)
          f.write("\n")
          
        f.close()


    def define_floorconstraint(self):

        f = open('DefineFloorConstraint2DModel.tcl','w')
        
        f.write("# This file will be used to define floor constraint\n\n")
        f.write("set	ConstrainDOF	1;	# Nodes at same floor level have identical lateral displacement\n\n")
        
        for i in range(0,self.num_story):
            f.write("equalDOF	%s	2%s	$ConstrainDOF;	# wall to Leaning column - level %s\n" %((i+2)*100, (i+2), (i+2)))
        
        f.write('\n\n# puts "Floor constraint defined"\n')
        
        f.close()
        
        
    def define_beams(self):
        
        f = open('DefineBeams2DModel.tcl','w')
        
        f.write("# This file will be used to define beam elements\n\n")
        f.write("# Define beams\n")
        
        for i in range(0,self.num_story):
            f.write("element	truss	2%s002%s	%s00	2%s	$AreaRigid	$TrussMatID; # Level %s\n" %((i+2), (i+2), (i+2), (i+2), (i+2)))
        
        f.write('\n# puts "Beams defined"\n')
        
        f.close()
        
        
    def define_columns(self):
        
        f = open('DefineColumns2DModel.tcl','w')
        
        f.write("# This file will be used to define walls and columns\n\n")
        
        f.write("# Define leaning columns\n")
        for i in range(0,self.num_story):
            if i == 0:
                f.write("# Story %s\n" %(i+1))
                f.write("element	elasticBeamColumn	32%s2%s2	2%s	2%s2	$AreaRigid	$Ec	$IRigid	$PDeltaTransf;\n\n" %((i+1), (i+2), (i+1), (i+2)))
            else:
                f.write("# Story %s\n" %(i+1))
                f.write("element	elasticBeamColumn	32%s42%s2	2%s4	2%s2	$AreaRigid	$Ec	$IRigid	$PDeltaTransf;\n\n" %((i+1), (i+2), (i+1), (i+2)))
                
        f.write('# puts "Leaning column defined"\n\n\n')
        
        f.write("# Define wall\n")
        for i in range(0,self.num_story):
            f.write("# Story %s\n" %(i+1))
            f.write("element	elasticBeamColumn	3%s%s	%s	%s	%.3f	$Ec	%.3f	$PDeltaTransf;\n\n" %((i+1)*100, (i+2)*100, (i+1)*100, (i+2)*100, (self.lw*self.b), self.Ieff))
             
        f.write('# puts "Wall defined"\n')
        
        f.close()
        
        
    def define_leaningcolumns(self):
        
        f = open('DefineLeaningColumnSpring.tcl','w')
        
        f.write("# This file will be used to define column hinges \n\n")
        
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("rotLeaningCol	2%s2%s2	2%s	2%s2;	# Spring below floor level %s\n" %((i+2), (i+2), (i+2), (i+2), (i+2)))
                f.write("rotLeaningCol	2%s2%s4	2%s	2%s4;	# Spring above floor level %s\n" %((i+2), (i+2), (i+2), (i+2), (i+2)))
            else:
                f.write("rotLeaningCol	2%s2%s2	2%s	2%s2;	# Spring below floor level %s\n" %((i+2), (i+2), (i+2), (i+2), (i+2)))
                
        f.write('\n# puts "Leaning column springs defined"\n')
                
        f.close()
        
        
    def define_masses(self):
        
        f = open('DefineMasses2DModel.tcl','w')
        
        f.write("# This file will be used to define all nodal masses\n\n")
        
        f.write("# Define floor weights and each nodal mass\n")
                
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	Floor%sWeight	%.3f;\n" %((i+2), self.W_typical))
            else:
                f.write("set	Floor%sWeight	%.3f;\n" %((i+2), self.W_roof))
         
        f.write("set	WallTributaryMassRatio	%.3f;\n" %(1/self.num_walls))
        f.write("set	TotalNodesPerFloor	1;\n")
        
        for i in range(0,self.num_story):
            f.write("set	NodalMassFloor%s	[expr $Floor%sWeight*$WallTributaryMassRatio/$TotalNodesPerFloor/$g];\n" %((i+2), (i+2)))
        
        for i in range(0,self.num_story):
            f.write("\n# Level %s \n" %(i+2))
            f.write("mass	%s00	$NodalMassFloor%s	$Negligible	$Negligible\n" %((i+2), (i+2)))
            
        f.write('\n# puts "Nodal mass defined"')
        
        f.close()
        
        
    def define_Eigen_analysis(self):
        
        f = open('EigenValueAnalysis.tcl','w')
        
        textList =[
        "##############################################################################################################################",
        "#                                                       Eigenvalue Analysis                                                  #",
        "##############################################################################################################################",
        "",
        "",
        "    set pi [expr 2.0*asin(1.0)];                        # Definition of pi",
        "    set nEigenI 1;                                      # mode i = 1",
        "    set nEigenJ 2;                                      # mode j = 2",
        "    set nEigenK 3;                                      # mode k = 3"
        ]
        
        for line in textList:
          f.write(line)
          f.write("\n")
          
        if self.num_story == 1:
            f.write("    set nEigenL 1;                                     ")
        elif self.num_story == 2:
            f.write("    set nEigenL 3;                                     ")
        else:
            f.write("    set nEigenL 4;                                      # mode l = 4")
          
        textList =[          
        "",
        "",
        "	set lambdaN [eigen [expr $nEigenL]];                # eigenvalue analysis for nEigenJ modes",
        "    foreach lambda $lambdaN {",
        "        # lappend omegalist [expr {sqrt($lambda)}]; # Obtaining angular frequencies",
        "        lappend Tlist [expr {2*$pi/sqrt($lambda)}]; # Obtaining modal periods",
        "    }",
        "",
        "    # Saving periods",
        "    # Defining mode-shape recorders",
        "    set recorderdir EigenAnalysisOutput; # Recorder folder",
        "    file mkdir $recorderdir; # Creating recorder folder if it doesn't exist",
        "",
        "	# Record eigen vectors",
        "	for { set k 1 } { $k <= $nEigenL } { incr k } {"
        ]
        
        for line in textList:
          f.write(line)
          f.write("\n")
        
        f.write('		recorder Node -file [format "$recorderdir/Vector%iDirection1.out" $k] -node ')
        for i in range(0,self.num_story+1):
            f.write("%s00 " %(i+1))
        f.write('-dof 1 "eigen $k"\n')
        
        textList =[
        "	}",
        "",
        "    set period_file [open $recorderdir/Periods.out w];",
        "    foreach T $Tlist {",
        '        puts $period_file "$T";',
        "    }",
        "    close $period_file",
        "",
        "    record",
        "",
        '    puts "Eigen value analysis succeed"'
        ]
        
        for line in textList:
          f.write(line)
          f.write("\n")
          
        f.close()
        
        
    def define_records(self):
        
        f = open('DefineAllRecorders2DModel.tcl','w')
        
        textList =[
        "# This file will be used to define all recorders",
        "",
        "",
        "# Setting up main folders for different load scenarios",
        "set	baseDir	[pwd]",
        "set	dataDir	$LoadType",
        "file	mkdir	$dataDir",
        "cd	$baseDir/$dataDir",
        "",
        "# Creating all the sub-folders for different quantities",
        "file	mkdir	StoryDrifts",
        "file	mkdir	NodeDisplacements",
        "file	mkdir	GlobalColumnForces",
        "",
        "# Source all the tcl files that define the output",
        "cd	$baseDir",
        "source	DefineStoryDriftRecorders2DModel.tcl",
        "",
        "cd	$baseDir",
        "source	DefineNodeDisplacementRecorders2DModel.tcl",
        "",
        "cd	$baseDir",
        "source	DefineGlobalColumnForceRecorders2DModel.tcl",
        "",
        "cd	$baseDir",
        '# puts "All recorders defined"'
        ]
        
        for line in textList:
          f.write(line)
          f.write("\n")
          
        f.close()
        
        #######################################################################
        
        f = open('DefineStoryDriftRecorders2DModel.tcl','w')
        
        f.write("# Define story drift recorders\n\n\n")
        f.write("cd	$baseDir/$dataDir/StoryDrifts\n\n")
        
        for i in range(0,self.num_story):
            f.write("recorder	Drift	-file	$baseDir/$dataDir/StoryDrifts/Story%s.out	-time	-iNode	%s00	-jNode	%s00	-dof	1	-perpDirn	2;\n" %((i+1), (i+1), (i+2)))
        
        f.write("recorder	Drift	-file	$baseDir/$dataDir/StoryDrifts/Roof.out	-time	-iNode	100	-jNode	%s00	-dof	1	-perpDirn	2;" %(self.num_story+1))
        
        f.close()
        
        #######################################################################
        
        f = open('DefineNodeDisplacementRecorders2DModel.tcl','w')
        
        f.write("# Define node displacement recorders\n\n\n")
        f.write("cd	$baseDir/$dataDir/NodeDisplacements\n\n")
        
        for i in range(0,self.num_story+1):
            f.write("recorder	Node	-file	NodeDisplacementLevel%s.out	-time	-node	%s00	-dof	1	2	3	disp; \n" %((i+1), (i+1)))
        
        f.close()
        
        #######################################################################
        
        f = open('DefineGlobalColumnForceRecorders2DModel.tcl','w')
        
        f.write("# Define global column force recorders\n\n\n")
        f.write("cd	$baseDir/$dataDir/GlobalColumnForces\n\n")
        
        for i in range(0,self.num_story):
            f.write("recorder	Element	-file	GlobalColumnForcesStory%s.out	-time	-ele	3%s00%s00	force;\n" %((i+1), (i+1), (i+2)))
            
        f.close()
        
        
    def define_loads_analysis(self):
        
        f = open('PerformLoadsAnalysis.tcl','w')
        
        textList =[
        "##############################################################################################################################",
        "# PerformLoadsAnalysis									                            									 #",
        "#	This file will apply a previously defined gravity load to the wall						     							 #",
        "#	This file should be executed before running the EQ or pushover							     							 #",
        "# 														            													     #",
        "# Created by: Henry Burton, Stanford University, 2010									     								 #",
        "# Revised by: XINGQUAN GUAN, UCLA, 2018																						 #",
        "#								     						             												     #",
        "# Units: kips, inches, seconds                                                                                               #",
        "##############################################################################################################################",
        "",
        "# Gravity-analysis parameters -- load-controlled static analysis",
        "set Tol 1.0e-8; 									# Covergence tolerance for test",
        "variable constraintsTypeGravity Plain;				# Default",
        "if {[info exists RigidDiaphragm] == 1} {",
        '	if {$RigidDiaphragm=="ON"} {',
        "		variable constraintsTypeGravity Lagrange;	# 3D model: try different constraints",
        "	};												# If rigid diaphragm is on",
        "};													# If rigid diaphragm exists",
        "constraints $constraintsTypeGravity;				# How it handles boundary conditions",
        "numberer RCM; 										# Renumber dof's to minimize band-width (optimization)",
        "system BandGeneral; 								# How to store and solve the system of equations in the analysis (large model: try UmfPack)",
        "",
        "# set UmfPackLvalueFact 40",
        "# system UmfPack -lvalueFact $UmfPackLvalueFact",
        "# system SparseSPD",
        "",
        "test EnergyIncr $Tol 6 ; 							# Determine if convergence has been achieved at the end of an iteration step",
        "algorithm Newton;									# Use Newton's solution algorithm: updates tangent stiffness at every iteration",
        "set NstepGravity 5;  								# Apply gravity in 5 steps",
        "set DGravity [expr 1./$NstepGravity]; 				# Load increment",
        "integrator LoadControl $DGravity;					# Determine the next time step for an analysis",
        "analysis Static;									# Define type of analysis static or transient",
        "analyze $NstepGravity;								# Apply gravity",
        "",
        "",
        "# ------------------------------------------------- maintain constant gravity loads and reset time to zero",
        "loadConst -time 0.0",
        "set Tol 1.0e-6;										# reduce tolerance after gravity loads",
        'puts "$LoadType Performed Successfully"'
        ]
            
        for line in textList:
          f.write(line)
          f.write("\n")
          
        f.close()
        
        
    def define_GravityDeadLoads(self):
        
        f = open('DefineGravityDeadLoads2DModel.tcl','w')
        
        f.write("# Define gravity dead loads\n\n\n")
        
        f.write("# Assign point dead load values on wall: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	WallDeadLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib*self.DL_floor/1000)))
            else:
                f.write("set	WallDeadLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib*self.DL_roof/1000)))
        
        f.write("# Assign point live load values on wall: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	WallLiveLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib*self.LL_floor/1000)))
            else:
                f.write("set	WallLiveLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib*self.LL_roof/1000)))
        
        f.write("# Assign point dead load values on leaning column: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	LeaningColumnDeadLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib_leancol*self.DL_floor/1000)))
            else:
                f.write("set	LeaningColumnDeadLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib_leancol*self.DL_roof/1000)))
        
        f.write("# Assign point live load values on leaning column: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	LeaningColumnLiveLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib_leancol*self.LL_floor/1000)))
            else:
                f.write("set	LeaningColumnLiveLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib_leancol*self.LL_roof/1000)))
        
        f.write("# Assign lateral load values caused by earthquake (kip)\n")
        f.write("set	LateralLoad	[list")
        for i in range(0,self.num_story):
            f.write(" %.3f" %(self.F[i]))
        f.write("];\n\n\n")
        
        f.write("# Load combinations:\n")
        f.write("# 101 Dead load only\n")
        f.write("# 102 Live load only\n")
        f.write("# 103 Earthquake load only\n")
        f.write("# 104 Gravity and earthquake (for calculation of drift)\n\n")
                
        f.write("pattern	Plain	101	Constant	{\n")
        f.write("# Define point loads on wall\n")
        for i in range(0,self.num_story):
            f.write("load	%s00	0	[expr -1*$WallDeadLoadFloor%s]	0; \n" %((i+2), (i+2)))
        
        f.write("\n# Define point loads on leaning column\n")
        for i in range(0,self.num_story):
            f.write("load	2%s	0	[expr -1*$LeaningColumnDeadLoadFloor%s]	0;  \n" %((i+2), (i+2)))
        
        f.write("\n}\n")
        f.write('# puts "Dead load defined"')
                
        f.close()
        
        
    def define_GravityLiveLoads(self):
                
        f = open('DefineGravityLiveLoads2DModel.tcl','w')
        
        f.write("# Define gravity live loads\n\n\n")
        
        
        f.write("# Assign point dead load values on wall: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	WallDeadLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib*self.DL_floor/1000)))
            else:
                f.write("set	WallDeadLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib*self.DL_roof/1000)))
        
        f.write("# Assign point live load values on wall: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	WallLiveLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib*self.LL_floor/1000)))
            else:
                f.write("set	WallLiveLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib*self.LL_roof/1000)))
        
        f.write("# Assign point dead load values on leaning column: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	LeaningColumnDeadLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib_leancol*self.DL_floor/1000)))
            else:
                f.write("set	LeaningColumnDeadLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib_leancol*self.DL_roof/1000)))
        
        f.write("# Assign point live load values on leaning column: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	LeaningColumnLiveLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib_leancol*self.LL_floor/1000)))
            else:
                f.write("set	LeaningColumnLiveLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib_leancol*self.LL_roof/1000)))
        
        f.write("# Assign lateral load values caused by earthquake (kip)\n")
        f.write("set	LateralLoad	[list")
        for i in range(0,self.num_story):
            f.write(" %.3f" %(self.F[i]))
        f.write("];\n\n\n")
        
        f.write("# Load combinations:\n")
        f.write("# 101 Dead load only\n")
        f.write("# 102 Live load only\n")
        f.write("# 103 Earthquake load only\n")
        f.write("# 104 Gravity and earthquake (for calculation of drift)\n\n")
                
        f.write("pattern	Plain	102	Constant	{\n")
        f.write("# Define point loads on wall\n")
        for i in range(0,self.num_story):
            f.write("load	%s00	0	[expr -1*$WallLiveLoadFloor%s]	0; \n" %((i+2), (i+2)))
        
        f.write("\n# Define point loads on leaning column\n")
        for i in range(0,self.num_story):
            f.write("load	2%s	0	[expr -1*$LeaningColumnLiveLoadFloor%s]	0;  \n" %((i+2), (i+2)))
        
        f.write("\n}\n")
        f.write('# puts "Live load defined"')
                
        f.close()
        
        
    def define_EarthquakeLaterLoads(self):
        
        f = open('DefineEarthquakeLaterLoads2DModel.tcl','w')
        
        f.write("# Define Earthquake lateral loads\n\n\n")
        
        f.write("# Assign point dead load values on wall: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	WallDeadLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib*self.DL_floor/1000)))
            else:
                f.write("set	WallDeadLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib*self.DL_roof/1000)))
        
        f.write("# Assign point live load values on wall: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	WallLiveLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib*self.LL_floor/1000)))
            else:
                f.write("set	WallLiveLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib*self.LL_roof/1000)))
        
        f.write("# Assign point dead load values on leaning column: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	LeaningColumnDeadLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib_leancol*self.DL_floor/1000)))
            else:
                f.write("set	LeaningColumnDeadLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib_leancol*self.DL_roof/1000)))
        
        f.write("# Assign point live load values on leaning column: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	LeaningColumnLiveLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib_leancol*self.LL_floor/1000)))
            else:
                f.write("set	LeaningColumnLiveLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib_leancol*self.LL_roof/1000)))
        
        f.write("# Assign lateral load values caused by earthquake (kip)\n")
        f.write("set	LateralLoad	[list")
        for i in range(0,self.num_story):
            f.write(" %.3f" %(self.F[i]))
        f.write("];\n\n\n")
        
        f.write("# Load combinations:\n")
        f.write("# 101 Dead load only\n")
        f.write("# 102 Live load only\n")
        f.write("# 103 Earthquake load only\n")
        f.write("# 104 Gravity and earthquake (for calculation of drift)\n\n")
                
        f.write("pattern	Plain	103	Linear	{\n")
        f.write("# Define earthquake lateral loads\n")
        for i in range(0,self.num_story):
            f.write("load	%s00	[lindex $LateralLoad %s]	0.0	0.0;	# Level%s\n" %((i+2), i, (i+2)))
        
        f.write("\n}\n")
        f.write('# puts "Earthquake load defined"')
                
        f.close()
        
        
    def define_GravityEarthquakeLoads(self):
        
        f = open('DefineGravityEarthquakeLoads2DModel.tcl','w')
        
        f.write("# Define gravity and earthquake loads\n\n\n")
        
        
        f.write("# Assign point dead load values on wall: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	WallDeadLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib*self.DL_floor/1000)))
            else:
                f.write("set	WallDeadLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib*self.DL_roof/1000)))
        
        f.write("# Assign point live load values on wall: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	WallLiveLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib*self.LL_floor/1000)))
            else:
                f.write("set	WallLiveLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib*self.LL_roof/1000)))
        
        f.write("# Assign point dead load values on leaning column: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	LeaningColumnDeadLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib_leancol*self.DL_floor/1000)))
            else:
                f.write("set	LeaningColumnDeadLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib_leancol*self.DL_roof/1000)))
        
        f.write("# Assign point live load values on leaning column: (kip)\n")
        for i in range(0,self.num_story):
            if i != (self.num_story-1):
                f.write("set	LeaningColumnLiveLoadFloor%s	%.3f;\n" %((i+2), (self.A_trib_leancol*self.LL_floor/1000)))
            else:
                f.write("set	LeaningColumnLiveLoadFloor%s	%.3f;\n\n" %((i+2), (self.A_trib_leancol*self.LL_roof/1000)))
        
        f.write("# Assign lateral load values caused by earthquake (kip)\n")
        f.write("set	LateralLoad	[list")
        for i in range(0,self.num_story):
            f.write(" %.3f" %(self.F[i]))
        f.write("];\n\n\n")
        
        f.write("# Load combinations:\n")
        f.write("# 101 Dead load only\n")
        f.write("# 102 Live load only\n")
        f.write("# 103 Earthquake load only\n")
        f.write("# 104 Gravity and earthquake (for calculation of drift)\n\n")
                
        f.write("pattern	Plain	104	Constant	{\n")
        f.write("# Define point loads on wall\n")
        for i in range(0,self.num_story):
            f.write("load	%s00	0	[expr -(1.2+0.2*%.3f)*$WallDeadLoadFloor%s -0.5*$WallLiveLoadFloor%s]	0;\n" %((i+2), self.SDs, (i+2), (i+2)))
        
        f.write("\n# Define point loads on leaning column\n")
        for i in range(0,self.num_story):
            f.write("load	2%s	0	[expr -(1.2+0.2*%.3f)*$LeaningColumnDeadLoadFloor%s -0.5*$LeaningColumnLiveLoadFloor%s]	0;\n" %((i+2), self.SDs, (i+2), (i+2)))
        
        f.write("\n# Define earthquake lateral loads\n")
        for i in range(0,self.num_story):
            f.write("load	%s00	[lindex $LateralLoad %s]	0.0	0.0;	# Level%s\n" %((i+2), i, (i+2)))
            
        f.write("\n}\n")
        f.write('# puts "Gravity and earthquake loads defined"')
                
        f.close()
        
        
    def define_model(self):
        
        f = open('Model.tcl','w')
        
        textList =[
        "# Define analysis series",
        "set AnalysisLoadType [list EigenValue DeadLoad LiveLoad EarthquakeLoad GravityEarthquake]",
        "",
        "# Loop over all the analysis types",
        "foreach LoadType $AnalysisLoadType {",
        "",
        'puts "Analysis type is $LoadType"',
        "",
        "# Define model builder",
        "model BasicBuilder -ndm 2 -ndf 3",
        "",
        "# Defining variables",
        "source DefineVariables.tcl",
        "",
        "# Defining functions and procedures",
        "source DefineFunctionsAndProcedures.tcl",
        "",
        "# Defining nodes",
        "source DefineNodes2DModel.tcl",
        "",
        "# Defining node fixities",
        "source DefineFixities2DModel.tcl",
        "",
        "# Defining floor constraint",
        "source DefineFloorConstraint2DModel.tcl",
        "",
        "# Defining column elements",
        "source DefineColumns2DModel.tcl",
        "",
        "# Defining rotational springs for leaning columns",
        "source DefineLeaningColumnSpring.tcl",
        "",
        "# Defining masses",
        "source DefineMasses2DModel.tcl",
        "",
        "# Perform eigen value analysis",
        'if {$LoadType == "EigenValue"} {',
        "	source EigenValueAnalysis.tcl",
        "	}",
        "",
        "# Defining all recorders",
        'if {$LoadType != "EigenValue"} {',
        "	source DefineAllRecorders2DModel.tcl",
        "	}",
        "",
        "# Defining gravity dead load",
        'if {$LoadType == "DeadLoad"} {',
        "	source DefineGravityDeadLoads2DModel.tcl",
        "	source PerformLoadsAnalysis.tcl",
        "	}",
        "",
        "# Defining gravity live load",
        'if {$LoadType == "LiveLoad"} {',
        "	source DefineGravityLiveLoads2DModel.tcl",
        "	source PerformLoadsAnalysis.tcl",
        "	}",
        "",
        "# Defining earthquake load",
        'if {$LoadType == "EarthquakeLoad"} {',
        "	source DefineEarthquakeLaterLoads2DModel.tcl",
        "	source PerformLoadsAnalysis.tcl",
        "	}",
        "",
        "# Defining the load cases for checking drift",
        'if {$LoadType == "GravityEarthquake"} {',
        "	source DefineGravityEarthquakeLoads2DModel.tcl",
        "	source PerformLoadsAnalysis.tcl",
        "}",
        "",
        "# Clear the memory",
        "wipe all",
        "",
        "# Create a blank line among different analysis",
        'puts " "',
        "}"
        ]
        
        for line in textList:
          f.write(line)
          f.write("\n")
          
        f.close()


    def run_OpenSees(self):
        from main_design import baseDirectory
        self.define_EarthquakeLaterLoads()
        self.define_Eigen_analysis()
        self.define_GravityDeadLoads()
        self.define_GravityEarthquakeLoads()
        self.define_GravityLiveLoads()
        #self.define_beams()
        self.define_columns()
        self.define_fixities()
        self.define_floorconstraint()
        self.define_functions()
        self.define_leaningcolumns()
        self.define_loads_analysis()
        self.define_masses()
        self.define_model()
        self.define_nodes()
        self.define_records()
        self.define_variables()
        # path = Path(baseDirectory,"..","..","OpenSees","bin","OpenSees")
        # os.system(baseDirectory + ' OpenSees Model.tcl')
        # subprocess.call([Path('..','..','OpenSees','bin','OpenSees'), 'Model.tcl'])
        os.system('C:\\OpenSees\\bin\\OpenSees Model.tcl')


    def drift_demand(self):
        self.Sxe_list = []
        for i in range (0, self.num_story):
            #myfile = open("EarthquakeLoad\\NodeDisplacements\\NodeDisplacementLevel%s.out" %(i+2), "r") #Use this for RSA
            myfile = open(Path("GravityEarthquake","NodeDisplacements","NodeDisplacementLevel%s.out" %(i+2)), "r") #Use this for ELF
            lst = list(myfile.readlines())
            myfile.close()
            lastline = lst[len(lst)-1]
            intStart = lastline.find('') + 2
            sub = lastline[intStart:]
            intEnd = sub.find(' ')
            finalvalue = sub[0:intEnd]
            self.Sxe_list.append(float(finalvalue))
        
        self.Sxe_Opensees = np.array(self.Sxe_list)
        self.Su_Opensees =  self.Cd * self.Sxe_Opensees / self.Ie
        self.drift_demand1 = ( self.Su_Opensees[ self.num_story-1]/(( self.typical_story*( self.num_story-1)+ self.first_story)*12))*100 #%

 
  
class PMInteraction():
    
    def __init__(self,table,fc,b,lw,fy,Pu):
        self.table = table
        self.fc = fc #psi
        self.b = b #in
        self.lw = lw #in
        self.fy = fy #ksi
        self.Es = 29000 #ksi
        self.B1 = min(max(0.65,(1.05-(0.05*fc)/1000)),0.85) #beta1
        self.Pu = Pu


    def critical_diagram_points_pure(self):

        # Pure Compression
        Po = (0.85*self.fc/1000) * ((self.b*self.lw)-(sum(self.table[2]))) + (self.fy*sum(self.table[2]))
        Pn_max = 0.8*Po
        phiPn_max = 0.65*Pn_max

        # Pure Tension
        Pnt = -self.fy*sum(self.table[2])
        PhiPnt = 0.9*Pnt
        
        return(Pn_max,Pnt)

        
    def interaction_diagram_points(self):
        
        Z = np.concatenate((np.arange(1,-5,-0.01), np.arange(-5,-50,-0.25), np.arange(-50,-100,-1), np.arange(-100,-500,-5), np.arange(-500,-1500,-10), np.arange(-1500,-2000,-25), np.arange(-2000,-5050,-50)))
        fy_E = self.fy / self.Es
        et = fy_E * Z
        c = (-0.003 * max(self.table[0]))/(et-0.003)
        a = np.zeros(len(Z))
        for i in range(0,len(Z)):
            a[i]= min(self.B1*c[i],self.lw)
        
        Cc = 0.85 * a * self.b *(self.fc/1000)
        es = np.zeros((len(Z),len(self.table[0])))
        Fs = np.zeros((len(Z),len(self.table[0])))
        d = np.zeros((len(Z),len(self.table[0])))
        Mni = np.zeros((len(Z),len(self.table[0])))
  
        for j in range(0,len(self.table[0])):
            for i in range(0,len(Z)):
                if self.table[2][j] == 0:
                    es[i,j] = 0
                elif c[i] >= self.table[0][j]:
                    es[i,j] = min((0.003)*((c[i]-self.table[0][j])/c[i]),fy_E)
                else:
                    es[i,j] = max((0.003)*((c[i]-self.table[0][j])/c[i]),-fy_E)

        for j in range(0,len(self.table[0])):
            for i in range(0,len(Z)):
                if es[i,j] > 0:
                    Fs[i,j] = (es[i,j]*self.table[2][j]*self.Es) - (0.85*self.table[2][j]*self.fc/1000)
                else:
                    Fs[i,j] = es[i,j]*self.table[2][j]*self.Es
                    
        d_concrete = self.lw/2 - a/2
            
        for j in range(0,len(self.table[0])):
            for i in range(0,len(Z)):
                if self.table[0][j] == 0:
                    d[i,j] = 0
                else:
                    d[i,j] = (self.lw/2) - self.table[0][j]

        Mn_concrete = Cc*d_concrete/12
        
        for j in range(0,len(self.table[0])):
            for i in range(0,len(Z)):
                Mni[i,j] = Fs[i,j]*d[i,j]/12
                
        Pn = np.zeros(len(Z))
        Mn = np.zeros(len(Z))
        for i in range(0,len(Z)):
            Pn[i]= Cc[i] + sum(Fs[i,])
            Mn[i] = Mn_concrete[i]+sum(Mni[i,])
            
        phi = np.zeros(len(Z))
        for i in range(0,len(Z)):
            if et[i] >= -0.002:
                phi[i] = 0.65
            elif et[i] <= -0.005:
                phi[i] = 0.9
            else:
                phi[i] = 0.65 - (-0.002*(0.9-0.65))/(-0.005+0.002) + (et[i]*(0.9-0.65)/(-0.005+0.002))

        phiPn = np.zeros(len(Z))
        for i in range(0,len(Z)):
            phiPn[i]= min((phi[i]*Pn[i]), (0.65*self.critical_diagram_points_pure()[0]))
            
        phiMn = phi * Mn
        
        ####################################################
        #######   General point interpolation (GP)   #######
        ####################################################
        
        Pn_find = max(Pn)+10**6 #very large number
        for i in range(0,len(Z)):
            if Pn[i] >= self.Pu:
                if Pn[i] < Pn_find:
                    Pn_find = Pn[i]
                    i_target = i
        
        P_GP1 = Pn[i_target]
        Z_GP1 = Z[i_target]
        phi_GP1 = phi[i_target]
        M_GP1 = Mn[i_target]
        P_GP3 = Pn[i_target+1]
        Z_GP3 = Z[i_target+1]
        phi_GP3 = phi[i_target+1]
        M_GP3 = Mn[i_target+1]
        P_GP2 = self.Pu
        Z_GP2 = ((Z_GP3-Z_GP1)*(P_GP2-P_GP1)/(P_GP3-P_GP1))+Z_GP1
        phi_GP2 = ((phi_GP3-phi_GP1)*(P_GP2-P_GP1)/(P_GP3-P_GP1))+phi_GP1
        M_GP2 = ((M_GP3-M_GP1)*(Z_GP2-Z_GP1)/(Z_GP3-Z_GP1))+M_GP1 
        
        ####################################################
        #######   Pure bending interpolation (PB)    #######
        ####################################################
        
        Pn_find = max(Pn)+10**6 #very large number
        for i in range(0,len(Z)):
            if Pn[i] >= 0:
                if Pn[i] < Pn_find:
                    Pn_find = Pn[i]
                    i_target = i
        
        P_PB1 = Pn[i_target]
        Z_PB1 = Z[i_target]
        phi_PB1 = phi[i_target]
        M_PB1 = Mn[i_target]
        P_PB3 = Pn[i_target+1]
        Z_PB3 = Z[i_target+1]
        phi_PB3 = phi[i_target+1]
        M_PB3 = Mn[i_target+1]
        P_PB2 = 0
        Z_PB2 = ((Z_PB3-Z_PB1)*(P_PB2-P_PB1)/(P_PB3-P_PB1))+Z_PB1
        phi_PB2 = ((phi_PB3-phi_PB1)*(P_PB2-P_PB1)/(P_PB3-P_PB1))+phi_PB1
        M_PB2 = ((M_PB3-M_PB1)*(Z_PB2-Z_PB1)/(Z_PB3-Z_PB1))+M_PB1
        
        return(Z_GP2, phi_GP2, Z_PB2, phi_PB2, phi[100], phi[150], Pn, Mn, phiPn, phiMn)
                
        
    def critical_diagram_points_pb(self):

        ####################################################
        #############       Pure Bending       #############
        ####################################################
        
        #This point is where the interaction diagram crosses the x-axis (moment axis), where the axial load capacity is zero.
        
        fy_E = -self.fy / self.Es
        Z = self.interaction_diagram_points()[2]
        et = -fy_E * Z
        c = (-0.003 * max(self.table[0]))/(et-0.003)
        a = min(self.B1*c,self.lw)
        Cc = (0.85*self.fc*a*self.b)/1000

        esi = np.zeros(len(self.table[0]))  
        fsi = np.zeros(len(self.table[0]))  
        Fsi = np.zeros(len(self.table[0]))  
        dsi = np.zeros(len(self.table[0]))  

        for j in range(0,len(self.table[0])):
            if self.table[0][j] == 0:
                esi[j] = 0
            elif c >= self.table[0][j]:
                esi[j] = min((0.003)*((c-self.table[0][j])/c),-fy_E)
            else:
                esi[j] = max((0.003)*((c-self.table[0][j])/c),fy_E)
                
        for j in range(0,len(self.table[0])):
            if esi[j] > 0:
                fsi[j] = (esi[j]*self.Es)-(0.85*self.fc/1000)
            else:
                fsi[j] = esi[j]*self.Es
                
        for j in range(0,len(self.table[0])):
            if fsi[j] == 0:
                Fsi[j] = 0
            else:
                Fsi[j] = fsi[j]*self.table[2][j]

        for j in range(0,len(self.table[0])):
            if esi[j] == 0:
                dsi[j] = 0
            else:
                dsi[j] = (self.lw/2)-self.table[0][j]
 
        Mnsi = (Fsi*dsi)/12  

        Pn = 0
        Mn = ((Cc*(self.lw/2-a/2))/12) + sum(Mnsi)
        phi = self.interaction_diagram_points()[3]
        phiPn = phi*Pn
        phiMn = phi*Mn
        
        
    def critical_diagram_points_bp(self):

        ####################################################
        #############      Balanced Point      #############
        ####################################################
        
        #At this point, extreme layer of tension steel yields at the same load as the concrete reaches its maximum usable strain.
        
        fy_E = -self.fy / self.Es
        c = (0.003/(0.003-fy_E)) * max(self.table[0])
        a = min(self.B1*c,self.lw)
        Cc = (0.85*self.fc*a*self.b)/1000

        esi = np.zeros(len(self.table[0]))  
        fsi = np.zeros(len(self.table[0]))  
        Fsi = np.zeros(len(self.table[0]))  
        dsi = np.zeros(len(self.table[0]))  

        for j in range(0,len(self.table[0])):
            if self.table[0][j] == 0:
                esi[j] = 0
            elif c >= self.table[0][j]:
                esi[j] = min((0.003)*((c-self.table[0][j])/c),-fy_E)
            else:
                esi[j] = max((0.003)*((c-self.table[0][j])/c),fy_E)
                                
        for j in range(0,len(self.table[0])):
            if esi[j] > 0:
                fsi[j] = (esi[j]*self.Es)-(0.85*self.fc/1000)
            else:
                fsi[j] = esi[j]*self.Es
                
        for j in range(0,len(self.table[0])):
            if fsi[j] == 0:
                Fsi[j] = 0
            else:
                Fsi[j] = fsi[j]*self.table[2][j]

        for j in range(0,len(self.table[0])):
            if esi[j] == 0:
                dsi[j] = 0
            else:
                dsi[j] = (self.lw/2)-self.table[0][j]
 
        Mnsi = (Fsi*dsi)/12  

        Pn = Cc + sum(Fsi)
        Mn = ((Cc*(self.lw/2-a/2))/12) + sum(Mnsi)
        phi = 0.65
        phiPn = phi*Pn
        phiMn = phi*Mn

        
    def critical_diagram_points_0(self):

        ####################################################
        #############      Stress = 0 fy       #############
        ####################################################
        
        #Strain in extreme tension layer is zero. Once tension develops in this layer, tension lap splices are required.
        #Compression lap splices are no longer allowed.
        
        fy_E = -self.fy / self.Es
        Z = 0
        et = -fy_E * Z
        c = (-0.003 * max(self.table[0]))/(et-0.003)
        a = min(self.B1*c,self.lw)
        Cc = (0.85*self.fc*a*self.b)/1000

        esi = np.zeros(len(self.table[0]))  
        fsi = np.zeros(len(self.table[0]))  
        Fsi = np.zeros(len(self.table[0]))  
        dsi = np.zeros(len(self.table[0]))  

        for j in range(0,len(self.table[0])):
            if self.table[0][j] == 0:
                esi[j] = 0
            elif c >= self.table[0][j]:
                esi[j] = min((0.003)*((c-self.table[0][j])/c),-fy_E)
            else:
                esi[j] = max((0.003)*((c-self.table[0][j])/c),fy_E)
                                
        for j in range(0,len(self.table[0])):
            if esi[j] > 0:
                fsi[j] = (esi[j]*self.Es)-(0.85*self.fc/1000)
            else:
                fsi[j] = esi[j]*self.Es
                
        for j in range(0,len(self.table[0])):
            if fsi[j] == 0:
                Fsi[j] = 0
            else:
                Fsi[j] = fsi[j]*self.table[2][j]

        for j in range(0,len(self.table[0])):
            if esi[j] == 0:
                dsi[j] = 0
            else:
                dsi[j] = (self.lw/2)-self.table[0][j]
 
        Mnsi = (Fsi*dsi)/12  

        Pn = Cc + sum(Fsi)
        Mn = ((Cc*(self.lw/2-a/2))/12) + sum(Mnsi)
        phi = self.interaction_diagram_points()[4]
        phiPn = phi*Pn
        phiMn = phi*Mn
        
        
    def critical_diagram_points_05(self):

        ####################################################
        #############     Stress = 0.5 fy      #############
        ####################################################
        
        #Length of tension lap splices are changed after the strain in the tension steel reaches 0.5 εy.
        
        fy_E = -self.fy / self.Es
        Z = 0.5
        et = -fy_E * Z
        c = (0.003 * max(self.table[0]))/((0.5*-fy_E)+0.003)
        a = min(self.B1*c,self.lw)
        Cc = (0.85*self.fc*a*self.b)/1000

        esi = np.zeros(len(self.table[0]))  
        fsi = np.zeros(len(self.table[0]))  
        Fsi = np.zeros(len(self.table[0]))  
        dsi = np.zeros(len(self.table[0]))  

        for j in range(0,len(self.table[0])):
            if self.table[0][j] == 0:
                esi[j] = 0
            elif c >= self.table[0][j]:
                esi[j] = min((0.003)*((c-self.table[0][j])/c),-fy_E)
            else:
                esi[j] = max((0.003)*((c-self.table[0][j])/c),fy_E)
                                
        for j in range(0,len(self.table[0])):
            if esi[j] > 0:
                fsi[j] = (esi[j]*self.Es)-(0.85*self.fc/1000)
            else:
                fsi[j] = esi[j]*self.Es
                
        for j in range(0,len(self.table[0])):
            if fsi[j] == 0:
                Fsi[j] = 0
            else:
                Fsi[j] = fsi[j]*self.table[2][j]

        for j in range(0,len(self.table[0])):
            if esi[j] == 0:
                dsi[j] = 0
            else:
                dsi[j] = (self.lw/2)-self.table[0][j]
 
        Mnsi = (Fsi*dsi)/12  

        Pn = Cc + sum(Fsi)
        Mn = ((Cc*(self.lw/2-a/2))/12) + sum(Mnsi)
        phi = self.interaction_diagram_points()[5]
        phiPn = phi*Pn
        phiMn = phi*Mn
        

    def select_axial_load(self):
        fy_E = self.fy / self.Es
        Z = self.interaction_diagram_points()[0]
        et = fy_E * Z
        c = (-0.003 * max(self.table[0]))/(et-0.003)
        a = min(self.B1*c,self.lw)
        Cc = (0.85*self.fc*a*self.b)/1000

        esi = np.zeros(len(self.table[0]))  
        fsi = np.zeros(len(self.table[0]))  
        Fsi = np.zeros(len(self.table[0]))  
        dsi = np.zeros(len(self.table[0]))  

        for j in range(0,len(self.table[0])):
            if self.table[0][j] == 0:
                esi[j] = 0
            elif c >= self.table[0][j]:
                esi[j] = min((0.003)*((c-self.table[0][j])/c),fy_E)
            else:
                esi[j] = max((0.003)*((c-self.table[0][j])/c),-fy_E)
                                
        for j in range(0,len(self.table[0])):
            if esi[j] > 0:
                fsi[j] = (esi[j]*self.Es)-(0.85*self.fc/1000)
            else:
                fsi[j] = esi[j]*self.Es
                
        for j in range(0,len(self.table[0])):
            if fsi[j] == 0:
                Fsi[j] = 0
            else:
                Fsi[j] = fsi[j]*self.table[2][j]

        for j in range(0,len(self.table[0])):
            if esi[j] == 0:
                dsi[j] = 0
            else:
                dsi[j] = (self.lw/2)-self.table[0][j]
 
        Mnsi = (Fsi*dsi)/12  

        Pn = self.Pu
        Mn = ((Cc*(self.lw/2-a/2))/12) + sum(Mnsi)
        phi = self.interaction_diagram_points()[1]
        if Pn > self.critical_diagram_points_pure()[0]:
            phiPn = phi*self.critical_diagram_points_pure()[0]
        else:
            phiPn = phi*Pn
        phiMn = phi*Mn
        
        return(c, Pn, Mn, phiPn, phiMn)

        
    def plot(self):
        
        Pn = self.interaction_diagram_points()[6]
        Mn = self.interaction_diagram_points()[7]
        phiPn = self.interaction_diagram_points()[8]
        phiMn = self.interaction_diagram_points()[9]
        
        fig = plt.figure(figsize=(15,10))
        plt.plot(Mn, Pn, linewidth=4, label = "Nominal Capacity")
        plt.plot(phiMn, phiPn, linewidth=4, label = "Design Capacity")
        plt.axvline(x=0,color='k')
        plt.axhline(y=0,color='k')
        plt.xlabel('Moment (kips-ft)', fontsize=25)
        plt.ylabel('Axial Load(kips)', fontsize=25)
        plt.rc('xtick',labelsize=20)
        plt.rc('ytick',labelsize=20)
        plt.legend(fontsize=20)



class WallDesign14(PMInteraction,ElasticAnalysis, ELF, AccParam):
    
    def __init__(self,Building_length,Building_width,DL_floor,DL_roof,LL_floor,LL_roof,num_story,N_length,N_width,first_story,typical_story,Ss,S1,site_class,TL,
             lw,b,fc,num_walls,edge_wall,R,Ie,Cd,fy,rho,concrete_type,cc,A_bar1,A_bar2):
        self.fy = fy #ksi
        self.rho = rho
        self.concrete_type = concrete_type #'normal' or 'light'
        self.cc = cc #in
        self.A_bar1 = A_bar1 #in2
        self.A_bar2 = A_bar2 #in2
        
        ElasticAnalysis.__init__(self, Building_length,Building_width,DL_floor,DL_roof,LL_floor,LL_roof,num_story,N_length,N_width,first_story,typical_story,Ss,S1,site_class,TL,
             lw,b,fc,num_walls,edge_wall,R,Ie,Cd)
     
        
    def design_forces_moments(self):
        
        self.Vu = self.rho*self.V #kips
        
        Mi = []
        M = 0
        story_shear = 0
        for i in range(0,self.num_story):
            story_shear = story_shear + self.F[self.num_story-1-i]
            if i == (self.num_story-1):
                m = story_shear * self.first_story
            else:
                m = story_shear * self.typical_story
            M = M + m
            Mi.append(self.rho*M)
        
        Mi.reverse()    
        self.Mu = self.rho * M

        Pd_floor = self.DL_floor * self.A_trib / 1000
        Pl_floor = self.LL_floor * self.A_trib / 1000
        Pd_roof = self.DL_roof * self.A_trib / 1000
        Pl_roof = self.LL_roof * self.A_trib / 1000
        
        self.Pd = Pd_floor * (self.num_story-1) + Pd_roof #kips
        self.Pl = Pl_floor * (self.num_story-1) + Pl_roof #kips
 
        ############################################
        #############   LC 1,2,5,7    ##############
        ############################################
        # LC1: 1.4D
        self.Pu1 = 1.4*self.Pd
        
        # LC2: 1.2D+1.6L
        self.Pu2 = 1.2*self.Pd + 1.6*self.Pl
        
        #LC5: (1.2+0.2Sds)D+0.5L+rho*Qe
        self.Pu5 = (1.2+0.2*self.SDs)*self.Pd + 0.5*self.Pl
        
        #LC7: (0.9-0.2Sds)D+rho*Qe
        self.Pu7 = (0.9-0.2*self.SDs)*self.Pd
        
        self.Pu = min(self.Pu5,self.Pu7)
        
        
    def boundary_long_reinf(self):
        
        self.design_forces_moments()
        Tu = (self.Mu/(0.8*(self.lw/12))) - (self.Pu/2) #kips
        Asb = (Tu/(0.9*self.fy)) #in2
        n_bars = np.ceil(Asb/self.A_bar1)
        
        ##############################################################
        ##########         Bars distribution in BE          ##########
        ##############################################################
        self.Scc = 6 #spacing between BE long. bars
        self.Scc_y = 5 #spacing between BE long. bars in y direction
        space = self.b-2*self.cc
        
        if space < (2*self.Scc_y):
            n = 2 #put 2 bars in "1 column"
        elif space < (3*self.Scc_y):
            n = 3 #put 3 bars in "1 column"
        else:
            n = 4 #put 4 bars in "1 column"
            
        cols = n_bars/n
        self.cols = np.ceil(cols)
        if self.cols < 2:
            self.cols = 2
        self.true_n_bars = self.cols * n
        self.n_bars_layer = n

        
    def shear_strength(self):

        self.design_forces_moments()
        Acv = self.lw*self.b
        hw = self.typical_story*(self.num_story-1)+self.first_story
        hw_lw = hw/(self.lw/12)
        
        if hw_lw <= 1.5:
            alpha_c = 3
        elif hw_lw >= 2:
            alpha_c = 2
        else:
            alpha_c = -2*(hw_lw-2)+2
        
        if self.concrete_type == 'normal':
            lambda_shear = 1
        elif self.concrete_type == 'light':
            lambda_shear = 0.75
            
        rho_t = (self.Vu*1000/(0.75*Acv)-alpha_c*lambda_shear*np.sqrt(self.fc))/(self.fy*1000)
        
        if rho_t < 0.0025:
            rho_t = 0.0025
        
        spacing_web = (2*self.A_bar2)/(self.b*rho_t) #spacing must be less than that
        self.spacing_web = np.floor(spacing_web)
        
        if self.spacing_web > 18:
            self.spacing_web = 18
            rho_t = (2*self.A_bar2)/(self.b*self.spacing_web)
        
        rho_l = rho_t 
        Vn = (Acv*(alpha_c*lambda_shear*np.sqrt(self.fc)+rho_t*(self.fy*1000)))/1000 #kips
        Vn_limit = 10*Acv*np.sqrt(self.fc)/1000
        
        if Vn > Vn_limit:
            self.error_shear = 1
        else:
            self.error_shear = 0
          

    
    def pm_interc(self):
        
        if self.iteration == 0:
            self.boundary_long_reinf()
        self.shear_strength()

        layers_BE = self.cols
        layers_BE = np.asarray(layers_BE, dtype=int)
        web_length = self.lw-2*(self.cc+(self.cols-1)*self.Scc)
        web_sp = web_length/self.spacing_web 
        web_sp = np.floor(web_sp)
        spacing_BE_web = (web_length-web_sp*self.spacing_web)/2
        cols_web = web_sp+1
        cols_web = np.asarray(cols_web, dtype=int)
        layers_web = cols_web
        bars_weblayer = 2
        
        total_layers = 2*layers_BE + layers_web
        total_layers = np.asarray(total_layers, dtype=int)
        
        d_i = []
        d_counter = 0
        for i in range(0,total_layers):
            if i == 0:
                d_counter += self.cc
                d_i.append(d_counter)
            elif i < layers_BE:
                d_counter += self.Scc
                d_i.append(d_counter)
            elif i == layers_BE:
                d_counter += spacing_BE_web
                d_i.append(d_counter)
            elif i > layers_BE and i < (layers_BE+layers_web):
                d_counter += self.spacing_web
                d_i.append(d_counter)
            elif i == (layers_BE+layers_web):
                d_counter += spacing_BE_web
                d_i.append(d_counter)
            elif i > (layers_BE+layers_web):
                d_counter += self.Scc
                d_i.append(d_counter)
                
        num_bars = []
        As_i = []
        for i in range(0,layers_BE):    
            num_bars.append(self.n_bars_layer)
            As_i.append(self.n_bars_layer*self.A_bar1)
        for i in range(0,layers_web):    
            num_bars.append(bars_weblayer)
            As_i.append(bars_weblayer*self.A_bar2)
        for i in range(0,layers_BE):    
            num_bars.append(self.n_bars_layer)
            As_i.append(self.n_bars_layer*self.A_bar1)
            
        table = [d_i,num_bars,As_i]
        PMInteraction.__init__(self,table,self.fc,self.b,self.lw,self.fy,self.Pu5)
        self.na_depth = self.select_axial_load()[0]
        self.Pn = self.select_axial_load()[1]
        self.Mn = self.select_axial_load()[2]
        self.phiPn = self.select_axial_load()[3]
        self.phiMn = self.select_axial_load()[4]
        
        PMInteraction.__init__(self,table,self.fc,self.b,self.lw,self.fy,self.Pu7)
        self.Pn7 = self.select_axial_load()[1]
        self.Mn7 = self.select_axial_load()[2]
        self.phiPn7 = self.select_axial_load()[3]
        self.phiMn7 = self.select_axial_load()[4]
       
        
    def boundary_element(self):
        # SBE or OBE for now for 1st level
        self.design_forces_moments()
        if self.iteration == 0:
            self.boundary_long_reinf()
        self.shear_strength()
        self.pm_interc()
        self.run_OpenSees()
        self.drift_demand()
           
        self.SBE_sb=0
        self.SBE_db=0
        
        self.lbe = 2*self.cc + (self.cols-1)*self.Scc
        self.lbe_old = 2*self.cc + (self.cols-1)*self.Scc
        
        # Stress-based 
        I = self.b*(self.lw**3)/12 
        fcc = (self.Mu/I) + (self.Pu5 / (self.b*self.lw))
        if fcc > (0.2*self.fc):
            self.SBE_sb = 1
            
        # Displacement-based
        Su_hw = self.drift_demand1/100
        if Su_hw < 0.005:
            Su_hw = 0.005
        if (self.na_depth >= (self.lw / (600 * 1.5 * Su_hw))):
            self.SBE_db=1     
                
        self.hx_min = min(14,(2/3)*self.b)
        least_dim_be = min(self.lbe,self.b)
        
        hx1 = (self.lbe - 2*self.cc) / (self.cols-1)
        hx2 = (self.b - 2*self.cc) / (self.n_bars_layer-1)       
                            
        hx = max(hx1,hx2)
        
        if hx > self.hx_min:
            self.error_hx = 1
        else:
            self.error_hx = 0
            
        s0 = 4+((14-hx)/3)
        if s0 < 4:
            s0 = 4
        elif s0 > 6:
            s0 = 6
            
        if self.SBE_db == 1:
            s3 = min(least_dim_be/3 , 6*np.sqrt(4*self.A_bar1/3.14159) , s0)
            
            Ag = self.lbe*self.b
            
            bc1 = self.lbe - 2*self.cc
            bc2 = self.b - 2*self.cc
            Ash1 = self.A_bar2 * self.cols
            Ash2 = self.A_bar2 * self.n_bars_layer
            Ach = bc1*bc2
            
            max_trans_rein = max(0.3*((Ag/Ach)-1)*(self.fc/1000)/self.fy, 0.09*(self.fc/1000)/self.fy )
            s1 = Ash1/(bc1*max_trans_rein)
            s2 = Ash2/(bc2*max_trans_rein)
               
            spacing_be_t_sbe = min(s1,s2,s3)
            
        else:
            spacing_be_t_sbe = min(6, 6*np.sqrt(4*self.A_bar1/3.14159))
        
        #Technically variable spacing_be_t_sbe is for anything below max(lw,Mu/4Vu) even if OBE
        self.spacing_be_t_sbe = np.floor(spacing_be_t_sbe)    
            
        self.ratio_be_t_sbe = (self.A_bar2 * self.n_bars_layer)/(self.b*self.spacing_be_t_sbe)
        
        #Technically variable spacing_be_t_obe is for anything above max(lw,Mu/4Vu) even if OBE
        spacing_be_t_obe = min(8 , 8*np.sqrt(4*self.A_bar1/3.14159))
        self.spacing_be_t_obe = np.floor(spacing_be_t_obe)
        self.ratio_be_t_obe = (self.A_bar2 * self.n_bars_layer)/(self.b*self.spacing_be_t_obe)
            
        # Ratios
        self.ratio_web_t = (self.A_bar2*2)/(self.b*self.spacing_web)
        self.ratio_web_l = (self.A_bar2*2)/(self.b*self.spacing_web)
        self.ratio_be_l = (self.A_bar1*self.true_n_bars)/(self.lbe * self.b)
        
        # OBE - SBE stories
        h_sbe = max((self.lw/12),(self.Mu/(4*self.Vu)))
        count_N_SBE = 1
        diff_sbe = h_sbe - self.first_story
        for i in range(0,self.num_story-1):
            if diff_sbe <= 0:
                break
            else:
                count_N_SBE += 1
            diff_sbe = diff_sbe - self.typical_story
            
        self.story_sbe = count_N_SBE
        self.story_obe = self.num_story - count_N_SBE  
          
        
    def plot_prelim_design(self):
        
        self.boundary_long_reinf()
        self.shear_strength()
        
        n = self.true_n_bars / self.cols
        n = np.asarray(n, dtype=int)
        y_BE = []
        y_BE.append(self.cc)
        ynum = n-2
        y_sp = (self.b-2*self.cc)/(n-1)
        for i in range(0,ynum):
            y_BE.append(self.cc+y_sp*(i+1))
        y_BE.append(self.b-self.cc)
        
        x_BE = []
        x_BE.append(self.cc)
        cols_forloop = np.asarray(self.cols, dtype=int)
        for i in range(0,cols_forloop-1):
            x_BE.append(self.cc+self.Scc*(i+1))
        
        x_rev = []
        x_rev.append(self.lw-self.cc)
        for i in range(0,cols_forloop-1):
            x_rev.append((self.lw-self.cc)-self.Scc*(i+1))
        
        web_length = self.lw-2*(self.cc+(self.cols-1)*self.Scc)
        web_sp = web_length/self.spacing_web 
        web_sp = np.floor(web_sp)
        spacing_BE_web = (web_length-web_sp*self.spacing_web)/2
        cols_web = web_sp+1
        cols_web = np.asarray(cols_web, dtype=int)
        
        x_web = []
        x_web.append(self.cc+self.Scc*(self.cols-1)+spacing_BE_web)
        for i in range(0,cols_web-1):
            x_web.append(self.cc+self.Scc*(self.cols-1)+spacing_BE_web+self.spacing_web*(i+1))
        y_web = []
        y_web.append(self.cc)
        y_web.append(self.b-self.cc)
            
        plt.axes()
        rectangle = plt.Rectangle((0,0), self.lw, self.b, fc='white',ec="red",lw=3)
        plt.gca().add_patch(rectangle)
        plt.axis('scaled')
        plt.gca().axes.get_xaxis().set_visible(False) #Hiding x-axis
        plt.gca().axes.get_yaxis().set_visible(False) #Hiding y-axis
        plt.show()
            
        for i in x_BE:
            for j in y_BE:
                plt.plot(i,j,'bo')
                
        for i in x_rev:
            for j in y_BE:
                plt.plot(i,j,'bo')
                
        for i in x_web:
            for j in y_web:
                plt.plot(i,j,'ko', markersize=3)
                


class WallDesign19(PMInteraction,ElasticAnalysis, ELF, AccParam):
    
    def __init__(self,Building_length,Building_width,DL_floor,DL_roof,LL_floor,LL_roof,num_story,N_length,N_width,first_story,typical_story,Ss,S1,site_class,TL,
             lw,b,fc,num_walls,edge_wall,R,Ie,Cd,fy,rho,concrete_type,cc,A_bar1,A_bar2):
        self.fy = fy #ksi
        self.rho = rho
        self.concrete_type = concrete_type #'normal' or 'light'
        self.cc = cc #in
        self.A_bar1 = A_bar1 #in2
        self.A_bar2 = A_bar2 #in2
        
        ElasticAnalysis.__init__(self, Building_length,Building_width,DL_floor,DL_roof,LL_floor,LL_roof,num_story,N_length,N_width,first_story,typical_story,Ss,S1,site_class,TL,
             lw,b,fc,num_walls,edge_wall,R,Ie,Cd)
     
        
    def design_forces_moments(self):
        
        self.Vu = self.rho*self.V #kips
        
        Mi = []
        M = 0
        story_shear = 0
        for i in range(0,self.num_story):
            story_shear = story_shear + self.F[self.num_story-1-i]
            if i == (self.num_story-1):
                m = story_shear * self.first_story
            else:
                m = story_shear * self.typical_story
            M = M + m
            Mi.append(self.rho*M)
        
        Mi.reverse()    
        self.Mu = self.rho * M

        Pd_floor = self.DL_floor * self.A_trib / 1000
        Pl_floor = self.LL_floor * self.A_trib / 1000
        Pd_roof = self.DL_roof * self.A_trib / 1000
        Pl_roof = self.LL_roof * self.A_trib / 1000
        
        self.Pd = Pd_floor * (self.num_story-1) + Pd_roof #kips
        self.Pl = Pl_floor * (self.num_story-1) + Pl_roof #kips
 
        ############################################
        #############   LC 1,2,5,7    ##############
        ############################################
        # LC1: 1.4D
        self.Pu1 = 1.4*self.Pd
        
        # LC2: 1.2D+1.6L
        self.Pu2 = 1.2*self.Pd + 1.6*self.Pl
        
        #LC5: (1.2+0.2Sds)D+0.5L+rho*Qe
        self.Pu5 = (1.2+0.2*self.SDs)*self.Pd + 0.5*self.Pl
        
        #LC7: (0.9-0.2Sds)D+rho*Qe
        self.Pu7 = (0.9-0.2*self.SDs)*self.Pd
        
        self.Pu = min(self.Pu5,self.Pu7)
        
        
    def boundary_long_reinf(self):
        
        self.design_forces_moments()
        Tu = (self.Mu/(0.8*(self.lw/12))) - (self.Pu/2) #kips
        Asb = (Tu/(0.9*self.fy)) #in2
        n_bars = np.ceil(Asb/self.A_bar1)
        
        ##############################################################
        ##########         Bars distribution in BE          ##########
        ##############################################################
        self.Scc = 6 #spacing between BE long. bars
        self.Scc_y = 5 #spacing between BE long. bars in y direction
        space = self.b-2*self.cc
        
        if space < (2*self.Scc_y):
            n = 2 #put 2 bars in "1 column"
        elif space < (3*self.Scc_y):
            n = 3 #put 3 bars in "1 column"
        else:
            n = 4 #put 4 bars in "1 column"
            
        cols = n_bars/n
        self.cols = np.ceil(cols)
        if self.cols < 2:
            self.cols = 2
        self.true_n_bars = self.cols * n
        self.n_bars_layer = n
        
        ##############################################################
        ##########               18.10.2.4(a)               ##########
        ##############################################################

        x = (0.15*self.lw - self.cc)/self.Scc
        x = np.floor(x)
        cols_mini = min(self.cols, (x+1))
        
        n_bars_mini = cols_mini*self.n_bars_layer
        ratio_mini = (n_bars_mini*self.A_bar1) / (0.15*self.lw*self.b)
        
        if ratio_mini < (6*np.sqrt(self.fc)/(self.fy * 1000)):
            self.error_miniratio = 1
        else:
            self.error_miniratio = 0
            
        
    def shear_strength(self):

        self.design_forces_moments()
        Acv = self.lw*self.b
        hw = self.typical_story*(self.num_story-1)+self.first_story
        hw_lw = hw/(self.lw/12)
        
        if hw_lw <= 1.5:
            self.alpha_c = 3
        elif hw_lw >= 2:
            self.alpha_c = 2
        else:
            self.alpha_c = -2*(hw_lw-2)+2
        
        if self.concrete_type == 'normal':
            self.lambda_shear = 1
        elif self.concrete_type == 'light':
            self.lambda_shear = 0.75
            
        rho_t = (self.Vu*1000/(0.75*Acv)- self.alpha_c*self.lambda_shear*np.sqrt(self.fc))/(self.fy*1000)
        
        if rho_t < 0.0025:
            rho_t = 0.0025
        
        spacing_web = (2*self.A_bar2)/(self.b*rho_t) #spacing must be less than that
        spacing_web = np.floor(spacing_web)
        
        if spacing_web > 18:
            spacing_web = 18
            rho_t = (2*self.A_bar2)/(self.b*spacing_web)
        
        rho_l = rho_t
        self.spacing_web_l = spacing_web
          
  
    def pm_interc(self):
        
        if self.iteration == 0:
            self.boundary_long_reinf()
        self.shear_strength()

        layers_BE = self.cols
        layers_BE = np.asarray(layers_BE, dtype=int)
        web_length = self.lw-2*(self.cc+(self.cols-1)*self.Scc)
        web_sp = web_length/self.spacing_web_l 
        web_sp = np.floor(web_sp)
        spacing_BE_web = (web_length-web_sp*self.spacing_web_l)/2
        cols_web = web_sp+1
        cols_web = np.asarray(cols_web, dtype=int)
        layers_web = cols_web
        bars_weblayer = 2
        
        total_layers = 2*layers_BE + layers_web
        total_layers = np.asarray(total_layers, dtype=int)
        
        d_i = []
        d_counter = 0
        for i in range(0,total_layers):
            if i == 0:
                d_counter += self.cc
                d_i.append(d_counter)
            elif i < layers_BE:
                d_counter += self.Scc
                d_i.append(d_counter)
            elif i == layers_BE:
                d_counter += spacing_BE_web
                d_i.append(d_counter)
            elif i > layers_BE and i < (layers_BE+layers_web):
                d_counter += self.spacing_web_l
                d_i.append(d_counter)
            elif i == (layers_BE+layers_web):
                d_counter += spacing_BE_web
                d_i.append(d_counter)
            elif i > (layers_BE+layers_web):
                d_counter += self.Scc
                d_i.append(d_counter)
                
        num_bars = []
        As_i = []
        for i in range(0,layers_BE):    
            num_bars.append(self.n_bars_layer)
            As_i.append(self.n_bars_layer*self.A_bar1)
        for i in range(0,layers_web):    
            num_bars.append(bars_weblayer)
            As_i.append(bars_weblayer*self.A_bar2)
        for i in range(0,layers_BE):    
            num_bars.append(self.n_bars_layer)
            As_i.append(self.n_bars_layer*self.A_bar1)
            
        table = [d_i,num_bars,As_i]
        PMInteraction.__init__(self,table,self.fc,self.b,self.lw,self.fy,self.Pu5)
        self.na_depth = self.select_axial_load()[0]
        self.Pn = self.select_axial_load()[1]
        self.Mn = self.select_axial_load()[2]
        self.phiPn = self.select_axial_load()[3]
        self.phiMn = self.select_axial_load()[4]
        
        PMInteraction.__init__(self,table,self.fc,self.b,self.lw,self.fy,self.Pu7)
        self.Pn7 = self.select_axial_load()[1]
        self.Mn7 = self.select_axial_load()[2]
        self.phiPn7 = self.select_axial_load()[3]
        self.phiMn7 = self.select_axial_load()[4]

        
    def actual_shear_strength(self):
        
        self.design_forces_moments()
        self.pm_interc()
        
        #dynamic shear amplification
        h = (self.typical_story*(self.num_story-1)+self.first_story) * 12
        if (h/self.lw) < 2:
            omega1 = 1
        else:
            ns = max(self.num_story , (0.007*h))
            if ns <= 6:
                omega1 = 0.9 + (ns/10)
            else:
                omega1 = min((1.3+(ns/30)) , 1.8)
               
        #overstrength factor
        Mpr = 1.25 * max(self.Mn,self.Mn7)
        omega2 = max (1.5, Mpr/self.Mu)
        
        #Design shear force
        self.Ve = min(omega1*omega2*self.Vu , 3*self.Vu)

        Acv = self.lw*self.b
        
        rho_t = (self.Ve*1000/(0.75*Acv)- self.alpha_c*self.lambda_shear*np.sqrt(self.fc))/(self.fy*1000)
        
        if rho_t < 0.0025:
            rho_t = 0.0025
        
        spacing_web = (2*self.A_bar2)/(self.b*rho_t) #spacing must be less than that
        self.spacing_web_t = np.floor(spacing_web)
        
        if self.spacing_web_t > 18:
            self.spacing_web_t = 18
            rho_t = (2*self.A_bar2)/(self.b*self.spacing_web_t)
        
        Vn = (Acv*(self.alpha_c*self.lambda_shear*np.sqrt(self.fc)+rho_t*(self.fy*1000)))/1000 #kips
        Vn_limit = 10*Acv*np.sqrt(self.fc)/1000
        
        if Vn > Vn_limit:
            self.error_shear = 1
        else:
            self.error_shear = 0
            
        if h/self.lw < 2: #18.10.4.3
            self.spacing_web_l = self.spacing_web_t

        
    def boundary_element(self):
        # SBE or OBE for now for 1st level
        self.design_forces_moments()
        if self.iteration == 0:
            self.boundary_long_reinf()
        self.shear_strength()
        self.pm_interc()
        self.actual_shear_strength()
        self.run_OpenSees()
        self.drift_demand()
           
        self.SBE_sb=0
        self.SBE_db=0
        
        self.lbe = 2*self.cc + (self.cols-1)*self.Scc
        self.lbe_old = 2*self.cc + (self.cols-1)*self.Scc
        
        # Stress-based 
        I = self.b*(self.lw**3)/12 
        fcc = (self.Mu/I) + (self.Pu5 / (self.b*self.lw))
        if fcc > (0.2*self.fc):
            self.SBE_sb = 1
            
        # Displacement-based
        Su_hw = self.drift_demand1/100
        if Su_hw < 0.005:
            Su_hw = 0.005
        if (self.na_depth >= (self.lw / (600 * 1.5 * Su_hw))):
            self.SBE_db=1     
                
        self.hx_min = min(14,(2/3)*self.b)
        least_dim_be = min(self.lbe,self.b)
        
        hx1 = (self.lbe - 2*self.cc) / (self.cols-1)
        hx2 = (self.b - 2*self.cc) / (self.n_bars_layer-1)       
                            
        hx = max(hx1,hx2)
        
        if hx > self.hx_min:
            self.error_hx = 1
        else:
            self.error_hx = 0
            
        s0 = 4+((14-hx)/3)
        if s0 < 4:
            s0 = 4
        elif s0 > 6:
            s0 = 6
            
        if self.SBE_db == 1:
            
            self.bmin = 0.025 * self.lw * self.na_depth
            
            s3 = min(least_dim_be/3 , 6*np.sqrt(4*self.A_bar1/3.14159) , s0)
            
            Ag = self.lbe*self.b
            
            bc1 = self.lbe - 2*self.cc
            bc2 = self.b - 2*self.cc
            Ash1 = self.A_bar2 * self.cols
            Ash2 = self.A_bar2 * self.n_bars_layer
            Ach = bc1*bc2
            
            max_trans_rein = max(0.3*((Ag/Ach)-1)*(self.fc/1000)/self.fy, 0.09*(self.fc/1000)/self.fy )
            s1 = Ash1/(bc1*max_trans_rein)
            s2 = Ash2/(bc2*max_trans_rein)
               
            spacing_be_t_sbe = min(s1,s2,s3)
            
        else:
            spacing_be_t_sbe = min(6, 6*np.sqrt(4*self.A_bar1/3.14159))
        
        #Technically variable spacing_be_t_sbe is for anything below max(lw,Mu/4Vu) even if OBE
        self.spacing_be_t_sbe = np.floor(spacing_be_t_sbe)    
            
        self.ratio_be_t_sbe = (self.A_bar2 * self.n_bars_layer)/(self.b*self.spacing_be_t_sbe)
        
        #Technically variable spacing_be_t_obe is for anything above max(lw,Mu/4Vu) even if OBE
        spacing_be_t_obe = min(8 , 8*np.sqrt(4*self.A_bar1/3.14159))
        self.spacing_be_t_obe = np.floor(spacing_be_t_obe)
        self.ratio_be_t_obe = (self.A_bar2 * self.n_bars_layer)/(self.b*self.spacing_be_t_obe)
            
        # Ratios
        self.ratio_web_t = (self.A_bar2*2)/(self.b*self.spacing_web_t)
        self.ratio_web_l = (self.A_bar2*2)/(self.b*self.spacing_web_l)
        self.ratio_be_l = (self.A_bar1*self.true_n_bars)/(self.lbe * self.b)
        
        # OBE - SBE stories
        h_sbe = max((self.lw/12),(self.Mu/(4*self.Vu)))
        count_N_SBE = 1
        diff_sbe = h_sbe - self.first_story
        for i in range(0,self.num_story-1):
            if diff_sbe <= 0:
                break
            else:
                count_N_SBE += 1
            diff_sbe = diff_sbe - self.typical_story
            
        self.story_sbe = count_N_SBE
        self.story_obe = self.num_story - count_N_SBE  

              
    def plot_prelim_design(self):
        
        self.boundary_long_reinf()
        self.shear_strength()
        self.actual_shear_strength()
        
        n = self.true_n_bars / self.cols
        n = np.asarray(n, dtype=int)
        y_BE = []
        y_BE.append(self.cc)
        ynum = n-2
        y_sp = (self.b-2*self.cc)/(n-1)
        for i in range(0,ynum):
            y_BE.append(self.cc+y_sp*(i+1))
        y_BE.append(self.b-self.cc)
        
        x_BE = []
        x_BE.append(self.cc)
        cols_forloop = np.asarray(self.cols, dtype=int)
        for i in range(0,cols_forloop-1):
            x_BE.append(self.cc+self.Scc*(i+1))
        
        x_rev = []
        x_rev.append(self.lw-self.cc)
        for i in range(0,cols_forloop-1):
            x_rev.append((self.lw-self.cc)-self.Scc*(i+1))
        
        web_length = self.lw-2*(self.cc+(self.cols-1)*self.Scc)
        web_sp = web_length/self.spacing_web_l 
        web_sp = np.floor(web_sp)
        spacing_BE_web = (web_length-web_sp*self.spacing_web_l)/2
        cols_web = web_sp+1
        cols_web = np.asarray(cols_web, dtype=int)
        
        x_web = []
        x_web.append(self.cc+self.Scc*(self.cols-1)+spacing_BE_web)
        for i in range(0,cols_web-1):
            x_web.append(self.cc+self.Scc*(self.cols-1)+spacing_BE_web+self.spacing_web_l*(i+1))
        y_web = []
        y_web.append(self.cc)
        y_web.append(self.b-self.cc)
            
        plt.axes()
        rectangle = plt.Rectangle((0,0), self.lw, self.b, fc='white',ec="red",lw=3)
        plt.gca().add_patch(rectangle)
        plt.axis('scaled')
        plt.gca().axes.get_xaxis().set_visible(False) #Hiding x-axis
        plt.gca().axes.get_yaxis().set_visible(False) #Hiding y-axis
        plt.show()
            
        for i in x_BE:
            for j in y_BE:
                plt.plot(i,j,'bo')
                
        for i in x_rev:
            for j in y_BE:
                plt.plot(i,j,'bo')
                
        for i in x_web:
            for j in y_web:
                plt.plot(i,j,'ko', markersize=3)
                
