# Define story drift recorders


cd	$baseDir/$dataDir/EQ_$eqNumber/Scale_$scale/StoryDrifts

recorder	Drift	-file	$baseDir/$dataDir/EQ_$eqNumber/Scale_$scale/StoryDrifts/Story1.out	-time	-iNode	1110	-time	-jNode	1211	-dof	1	-perpDirn	2; 
recorder	Drift	-file	$baseDir/$dataDir/EQ_$eqNumber/Scale_$scale/StoryDrifts/Story2.out	-time	-iNode	1211	-time	-jNode	1311	-dof	1	-perpDirn	2; 
recorder	Drift	-file	$baseDir/$dataDir/EQ_$eqNumber/Scale_$scale/StoryDrifts/Story3.out	-time	-iNode	1311	-time	-jNode	1411	-dof	1	-perpDirn	2; 
recorder	Drift	-file	$baseDir/$dataDir/EQ_$eqNumber/Scale_$scale/StoryDrifts/Story4.out	-time	-iNode	1411	-time	-jNode	1511	-dof	1	-perpDirn	2; 
recorder	Drift	-file	$baseDir/$dataDir/EQ_$eqNumber/Scale_$scale/StoryDrifts/Roof.out	-time	-iNode	1110	-jNode	1511	-dof	1	-perpDirn	2; 
