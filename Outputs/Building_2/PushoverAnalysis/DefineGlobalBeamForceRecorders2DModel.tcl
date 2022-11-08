# Define global beam force recorders


cd	$baseDir/$dataDir/GlobalBeamForces

# X-Direction beam element global force recorders
recorder	Element	-file	GlobalXBeamForcesLevel2.out	-time	-ele	2121221	2221321	2321421	2421521	2521621	2621721	2721821	2821921	force
recorder	Element	-file	GlobalXBeamForcesLevel3.out	-time	-ele	2131231	2231331	2331431	2431531	2531631	2631731	2731831	2831931	force
recorder	Element	-file	GlobalXBeamForcesLevel4.out	-time	-ele	2141241	2241341	2341441	2441541	2541641	2641741	2741841	2841941	force
recorder	Element	-file	GlobalXBeamForcesLevel5.out	-time	-ele	2151251	2251351	2351451	2451551	2551651	2651751	2751851	2851951	force
