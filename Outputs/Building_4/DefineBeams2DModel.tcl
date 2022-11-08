# This file will be used to define beam elements 


# Define beam section sizes 
set	BeamLevel2	[SectionProperty W27X146]; 
set	BeamLevel3	[SectionProperty W27X146]; 
set	BeamLevel4	[SectionProperty W27X94]; 
set	BeamLevel5	[SectionProperty W27X94]; 


# Define beams 
# Level 2
element	elasticBeamColumn	2121221	121	221	[lindex $BeamLevel2 2]	$Es	[expr 0.900000*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2221321	221	321	[lindex $BeamLevel2 2]	$Es	[expr 0.900000*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2321421	321	421	[lindex $BeamLevel2 2]	$Es	[expr 0.900000*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2421521	421	521	[lindex $BeamLevel2 2]	$Es	[expr 0.900000*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2521621	521	621	[lindex $BeamLevel2 2]	$Es	[expr 0.900000*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2621721	621	721	[lindex $BeamLevel2 2]	$Es	[expr 0.900000*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2721821	721	821	[lindex $BeamLevel2 2]	$Es	[expr 0.900000*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2821921	821	921	[lindex $BeamLevel2 2]	$Es	[expr 0.900000*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	truss	2921102	921	9102	$AreaRigid	$TrussMatID; 

# Level 3
element	elasticBeamColumn	2131231	131	231	[lindex $BeamLevel3 2]	$Es	[expr 0.900000*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2231331	231	331	[lindex $BeamLevel3 2]	$Es	[expr 0.900000*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2331431	331	431	[lindex $BeamLevel3 2]	$Es	[expr 0.900000*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2431531	431	531	[lindex $BeamLevel3 2]	$Es	[expr 0.900000*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2531631	531	631	[lindex $BeamLevel3 2]	$Es	[expr 0.900000*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2631731	631	731	[lindex $BeamLevel3 2]	$Es	[expr 0.900000*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2731831	731	831	[lindex $BeamLevel3 2]	$Es	[expr 0.900000*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2831931	831	931	[lindex $BeamLevel3 2]	$Es	[expr 0.900000*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	truss	2931103	931	9103	$AreaRigid	$TrussMatID; 

# Level 4
element	elasticBeamColumn	2141241	141	241	[lindex $BeamLevel4 2]	$Es	[expr 0.900000*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2241341	241	341	[lindex $BeamLevel4 2]	$Es	[expr 0.900000*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2341441	341	441	[lindex $BeamLevel4 2]	$Es	[expr 0.900000*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2441541	441	541	[lindex $BeamLevel4 2]	$Es	[expr 0.900000*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2541641	541	641	[lindex $BeamLevel4 2]	$Es	[expr 0.900000*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2641741	641	741	[lindex $BeamLevel4 2]	$Es	[expr 0.900000*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2741841	741	841	[lindex $BeamLevel4 2]	$Es	[expr 0.900000*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2841941	841	941	[lindex $BeamLevel4 2]	$Es	[expr 0.900000*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	truss	2941104	941	9104	$AreaRigid	$TrussMatID; 

# Level 5
element	elasticBeamColumn	2151251	151	251	[lindex $BeamLevel5 2]	$Es	[expr 0.900000*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2251351	251	351	[lindex $BeamLevel5 2]	$Es	[expr 0.900000*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2351451	351	451	[lindex $BeamLevel5 2]	$Es	[expr 0.900000*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2451551	451	551	[lindex $BeamLevel5 2]	$Es	[expr 0.900000*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2551651	551	651	[lindex $BeamLevel5 2]	$Es	[expr 0.900000*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2651751	651	751	[lindex $BeamLevel5 2]	$Es	[expr 0.900000*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2751851	751	851	[lindex $BeamLevel5 2]	$Es	[expr 0.900000*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2851951	851	951	[lindex $BeamLevel5 2]	$Es	[expr 0.900000*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	truss	2951105	951	9105	$AreaRigid	$TrussMatID; 

# puts "Beams defined"