# This file will be used to define columns 


# Define exterior column section sizes 
set	ExteriorColumnStory1	[SectionProperty W24X250];
set	ExteriorColumnStory2	[SectionProperty W24X250];
set	ExteriorColumnStory3	[SectionProperty W24X146];
set	ExteriorColumnStory4	[SectionProperty W24X146];


# Define interior column section sizes 
set	InteriorColumnStory1	[SectionProperty W36X194];
set	InteriorColumnStory2	[SectionProperty W36X194];
set	InteriorColumnStory3	[SectionProperty W30X132];
set	InteriorColumnStory4	[SectionProperty W30X132];


# Define columns
# Story 1 
element	elasticBeamColumn	3111121	1114	1216	[lindex $ExteriorColumnStory1 2]	$Es	[expr ($n+1.0)/$n*[lindex $ExteriorColumnStory1 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3211221	2114	2216	[lindex $InteriorColumnStory1 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory1 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3311321	3114	3216	[lindex $InteriorColumnStory1 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory1 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3411421	4114	4216	[lindex $InteriorColumnStory1 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory1 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3511521	5114	5216	[lindex $InteriorColumnStory1 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory1 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3611621	6114	6216	[lindex $InteriorColumnStory1 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory1 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3711721	7114	7216	[lindex $InteriorColumnStory1 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory1 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3811821	8114	8216	[lindex $InteriorColumnStory1 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory1 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3911921	9114	9216	[lindex $ExteriorColumnStory1 2]	$Es	[expr ($n+1.0)/$n*[lindex $ExteriorColumnStory1 6]]	$PDeltaTransf; 
element	elasticBeamColumn	31011022	101	1022	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 2 
element	elasticBeamColumn	3121131	1214	1316	[lindex $ExteriorColumnStory2 2]	$Es	[expr ($n+1.0)/$n*[lindex $ExteriorColumnStory2 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3221231	2214	2316	[lindex $InteriorColumnStory2 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory2 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3321331	3214	3316	[lindex $InteriorColumnStory2 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory2 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3421431	4214	4316	[lindex $InteriorColumnStory2 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory2 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3521531	5214	5316	[lindex $InteriorColumnStory2 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory2 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3621631	6214	6316	[lindex $InteriorColumnStory2 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory2 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3721731	7214	7316	[lindex $InteriorColumnStory2 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory2 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3821831	8214	8316	[lindex $InteriorColumnStory2 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory2 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3921931	9214	9316	[lindex $ExteriorColumnStory2 2]	$Es	[expr ($n+1.0)/$n*[lindex $ExteriorColumnStory2 6]]	$PDeltaTransf; 
element	elasticBeamColumn	310241032	1024	1032	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 3 
element	elasticBeamColumn	3131141	1314	1416	[lindex $ExteriorColumnStory3 2]	$Es	[expr ($n+1.0)/$n*[lindex $ExteriorColumnStory3 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3231241	2314	2416	[lindex $InteriorColumnStory3 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory3 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3331341	3314	3416	[lindex $InteriorColumnStory3 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory3 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3431441	4314	4416	[lindex $InteriorColumnStory3 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory3 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3531541	5314	5416	[lindex $InteriorColumnStory3 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory3 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3631641	6314	6416	[lindex $InteriorColumnStory3 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory3 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3731741	7314	7416	[lindex $InteriorColumnStory3 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory3 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3831841	8314	8416	[lindex $InteriorColumnStory3 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory3 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3931941	9314	9416	[lindex $ExteriorColumnStory3 2]	$Es	[expr ($n+1.0)/$n*[lindex $ExteriorColumnStory3 6]]	$PDeltaTransf; 
element	elasticBeamColumn	310341042	1034	1042	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

# Story 4 
element	elasticBeamColumn	3141151	1414	1516	[lindex $ExteriorColumnStory4 2]	$Es	[expr ($n+1.0)/$n*[lindex $ExteriorColumnStory4 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3241251	2414	2516	[lindex $InteriorColumnStory4 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory4 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3341351	3414	3516	[lindex $InteriorColumnStory4 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory4 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3441451	4414	4516	[lindex $InteriorColumnStory4 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory4 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3541551	5414	5516	[lindex $InteriorColumnStory4 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory4 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3641651	6414	6516	[lindex $InteriorColumnStory4 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory4 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3741751	7414	7516	[lindex $InteriorColumnStory4 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory4 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3841851	8414	8516	[lindex $InteriorColumnStory4 2]	$Es	[expr ($n+1.0)/$n*[lindex $InteriorColumnStory4 6]]	$PDeltaTransf; 
element	elasticBeamColumn	3941951	9414	9516	[lindex $ExteriorColumnStory4 2]	$Es	[expr ($n+1.0)/$n*[lindex $ExteriorColumnStory4 6]]	$PDeltaTransf; 
element	elasticBeamColumn	310441052	1044	1052	$AreaRigid	$Es	$IRigid	$PDeltaTransf; 

puts "Columns defined"