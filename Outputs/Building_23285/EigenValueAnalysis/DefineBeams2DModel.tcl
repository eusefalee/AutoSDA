# This file will be used to define beam elements 


# Define beam section sizes 
set	BeamLevel2	[SectionProperty W27X178];
set	BeamLevel3	[SectionProperty W27X178];
set	BeamLevel4	[SectionProperty W24X131];
set	BeamLevel5	[SectionProperty W24X131];


# Define beams 
# Level2
element	elasticBeamColumn	2121221	1215	2213	[lindex $BeamLevel2 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2221321	2215	3213	[lindex $BeamLevel2 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2321421	3215	4213	[lindex $BeamLevel2 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2421521	4215	5213	[lindex $BeamLevel2 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2521621	5215	6213	[lindex $BeamLevel2 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2621721	6215	7213	[lindex $BeamLevel2 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2721821	7215	8213	[lindex $BeamLevel2 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	elasticBeamColumn	2821921	8215	9213	[lindex $BeamLevel2 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel2 6]]	$LinearTransf; 
element	truss	2921102	9211	102	$AreaRigid	$TrussMatID; 

# Level3
element	elasticBeamColumn	2131231	1315	2313	[lindex $BeamLevel3 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2231331	2315	3313	[lindex $BeamLevel3 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2331431	3315	4313	[lindex $BeamLevel3 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2431531	4315	5313	[lindex $BeamLevel3 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2531631	5315	6313	[lindex $BeamLevel3 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2631731	6315	7313	[lindex $BeamLevel3 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2731831	7315	8313	[lindex $BeamLevel3 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	elasticBeamColumn	2831931	8315	9313	[lindex $BeamLevel3 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel3 6]]	$LinearTransf; 
element	truss	2931103	9311	103	$AreaRigid	$TrussMatID; 

# Level4
element	elasticBeamColumn	2141241	1415	2413	[lindex $BeamLevel4 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2241341	2415	3413	[lindex $BeamLevel4 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2341441	3415	4413	[lindex $BeamLevel4 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2441541	4415	5413	[lindex $BeamLevel4 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2541641	5415	6413	[lindex $BeamLevel4 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2641741	6415	7413	[lindex $BeamLevel4 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2741841	7415	8413	[lindex $BeamLevel4 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	elasticBeamColumn	2841941	8415	9413	[lindex $BeamLevel4 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel4 6]]	$LinearTransf; 
element	truss	2941104	9411	104	$AreaRigid	$TrussMatID; 

# Level5
element	elasticBeamColumn	2151251	1515	2513	[lindex $BeamLevel5 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2251351	2515	3513	[lindex $BeamLevel5 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2351451	3515	4513	[lindex $BeamLevel5 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2451551	4515	5513	[lindex $BeamLevel5 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2551651	5515	6513	[lindex $BeamLevel5 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2651751	6515	7513	[lindex $BeamLevel5 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2751851	7515	8513	[lindex $BeamLevel5 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	elasticBeamColumn	2851951	8515	9513	[lindex $BeamLevel5 2]	$Es	[expr ($n+1.0)/$n*[lindex $BeamLevel5 6]]	$LinearTransf; 
element	truss	2951105	9511	105	$AreaRigid	$TrussMatID; 

puts "Beams defined"