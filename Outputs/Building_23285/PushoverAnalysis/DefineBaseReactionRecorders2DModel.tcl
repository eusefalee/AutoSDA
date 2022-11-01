# Define base node reaction recorders


cd	$baseDir/$dataDir/BaseReactions

# Vertical reactions
recorder	Node	-file	VerticalReactions.out	-time	-node	1110	2110	3110	4110	5110	6110	7110	8110	9110	101	-dof	2	reaction;

# X-Direction reactions
recorder	Node	-file	XReactions.out	-time	-node	1110	2110	3110	4110	5110	6110	7110	8110	9110	101	-dof	1	reaction;

