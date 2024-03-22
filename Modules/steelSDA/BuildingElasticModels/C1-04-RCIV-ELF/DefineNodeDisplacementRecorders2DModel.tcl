# Define node displacement recorders


cd	$baseDir/$dataDir/NodeDisplacements

recorder	Node	-file	NodeDisplacementLevel1.out	-time	-node	111	211	311	411	511	611	711	811	911	1011	-dof	1	2	3	disp; 
recorder	Node	-file	NodeDisplacementLevel2.out	-time	-node	121	221	321	421	521	621	721	821	921	1021	-dof	1	2	3	disp; 
recorder	Node	-file	NodeDisplacementLevel3.out	-time	-node	131	231	331	431	531	631	731	831	931	1031	-dof	1	2	3	disp; 
recorder	Node	-file	NodeDisplacementLevel4.out	-time	-node	141	241	341	441	541	641	741	841	941	1041	-dof	1	2	3	disp; 
recorder	Node	-file	NodeDisplacementLevel5.out	-time	-node	151	251	351	451	551	651	751	851	951	1051	-dof	1	2	3	disp; 
