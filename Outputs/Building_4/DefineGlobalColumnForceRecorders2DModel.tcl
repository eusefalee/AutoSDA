# Define global column force recorders


cd	$baseDir/$dataDir/GlobalColumnForces

# X-Direction frame column element global force recorders
recorder	Element	-file	GlobalColumnForcesStory1.out	-time	-ele	3111121	3211221	3311321	3411421	3511521	3611621	3711721	3811821	3911921	force;
recorder	Element	-file	GlobalColumnForcesStory2.out	-time	-ele	3121131	3221231	3321331	3421431	3521531	3621631	3721731	3821831	3921931	force;
recorder	Element	-file	GlobalColumnForcesStory3.out	-time	-ele	3131141	3231241	3331341	3431441	3531541	3631641	3731741	3831841	3931941	force;
recorder	Element	-file	GlobalColumnForcesStory4.out	-time	-ele	3141151	3241251	3341351	3441451	3541551	3641651	3741751	3841851	3941951	force;
