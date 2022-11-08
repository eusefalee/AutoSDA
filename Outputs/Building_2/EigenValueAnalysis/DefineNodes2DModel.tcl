# This file will be used to define all nodes 
# Units: inch


# Set bay width and story height
set	BayWidth	[expr 30.00*12]; 
set	FirstStory	[expr 18.00*12]; 
set	TypicalStory	[expr 16.00*12]; 

# Set panel zone size as column depth and beam depth
# Level 1 
set	PanelSizeLevel1Column1	[list 0 0];# No panel zone on ground floor so using [0, 0] is okay
set	PanelSizeLevel1Column2	[list 0 0];# No panel zone on ground floor so using [0, 0] is okay
set	PanelSizeLevel1Column3	[list 0 0];# No panel zone on ground floor so using [0, 0] is okay
set	PanelSizeLevel1Column4	[list 0 0];# No panel zone on ground floor so using [0, 0] is okay
set	PanelSizeLevel1Column5	[list 0 0];# No panel zone on ground floor so using [0, 0] is okay
set	PanelSizeLevel1Column6	[list 0 0];# No panel zone on ground floor so using [0, 0] is okay
set	PanelSizeLevel1Column7	[list 0 0];# No panel zone on ground floor so using [0, 0] is okay
set	PanelSizeLevel1Column8	[list 0 0];# No panel zone on ground floor so using [0, 0] is okay
set	PanelSizeLevel1Column9	[list 0 0];# No panel zone on ground floor so using [0, 0] is okay
# Level 2 
set	PanelSizeLevel2Column1	[list 36.2 27.8];
set	PanelSizeLevel2Column2	[list 37.1 27.8];
set	PanelSizeLevel2Column3	[list 37.1 27.8];
set	PanelSizeLevel2Column4	[list 37.1 27.8];
set	PanelSizeLevel2Column5	[list 37.1 27.8];
set	PanelSizeLevel2Column6	[list 37.1 27.8];
set	PanelSizeLevel2Column7	[list 37.1 27.8];
set	PanelSizeLevel2Column8	[list 37.1 27.8];
set	PanelSizeLevel2Column9	[list 36.2 27.8];
# Level 3 
set	PanelSizeLevel3Column1	[list 36.2 27.8];
set	PanelSizeLevel3Column2	[list 37.1 27.8];
set	PanelSizeLevel3Column3	[list 37.1 27.8];
set	PanelSizeLevel3Column4	[list 37.1 27.8];
set	PanelSizeLevel3Column5	[list 37.1 27.8];
set	PanelSizeLevel3Column6	[list 37.1 27.8];
set	PanelSizeLevel3Column7	[list 37.1 27.8];
set	PanelSizeLevel3Column8	[list 37.1 27.8];
set	PanelSizeLevel3Column9	[list 36.2 27.8];
# Level 4 
set	PanelSizeLevel4Column1	[list 25.7 24.5];
set	PanelSizeLevel4Column2	[list 35.9 24.5];
set	PanelSizeLevel4Column3	[list 35.9 24.5];
set	PanelSizeLevel4Column4	[list 35.9 24.5];
set	PanelSizeLevel4Column5	[list 35.9 24.5];
set	PanelSizeLevel4Column6	[list 35.9 24.5];
set	PanelSizeLevel4Column7	[list 35.9 24.5];
set	PanelSizeLevel4Column8	[list 35.9 24.5];
set	PanelSizeLevel4Column9	[list 25.7 24.5];
# Level 5 
set	PanelSizeLevel5Column1	[list 25.7 24.5];
set	PanelSizeLevel5Column2	[list 35.9 24.5];
set	PanelSizeLevel5Column3	[list 35.9 24.5];
set	PanelSizeLevel5Column4	[list 35.9 24.5];
set	PanelSizeLevel5Column5	[list 35.9 24.5];
set	PanelSizeLevel5Column6	[list 35.9 24.5];
set	PanelSizeLevel5Column7	[list 35.9 24.5];
set	PanelSizeLevel5Column8	[list 35.9 24.5];
set	PanelSizeLevel5Column9	[list 25.7 24.5];

# Set max number of columns (excluding leaning column) and floors (counting 1 for ground)
set	MaximumFloor	5; 
set	MaximumCol	9; 

# Define nodes for the frame 
# Level 1 
NodesAroundPanelZone	1	1	[expr 0*$BayWidth]	[expr 0*$FirstStory+0*$TypicalStory]	$PanelSizeLevel1Column1	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	2	1	[expr 1*$BayWidth]	[expr 0*$FirstStory+0*$TypicalStory]	$PanelSizeLevel1Column2	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	3	1	[expr 2*$BayWidth]	[expr 0*$FirstStory+0*$TypicalStory]	$PanelSizeLevel1Column3	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	4	1	[expr 3*$BayWidth]	[expr 0*$FirstStory+0*$TypicalStory]	$PanelSizeLevel1Column4	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	5	1	[expr 4*$BayWidth]	[expr 0*$FirstStory+0*$TypicalStory]	$PanelSizeLevel1Column5	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	6	1	[expr 5*$BayWidth]	[expr 0*$FirstStory+0*$TypicalStory]	$PanelSizeLevel1Column6	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	7	1	[expr 6*$BayWidth]	[expr 0*$FirstStory+0*$TypicalStory]	$PanelSizeLevel1Column7	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	8	1	[expr 7*$BayWidth]	[expr 0*$FirstStory+0*$TypicalStory]	$PanelSizeLevel1Column8	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	9	1	[expr 8*$BayWidth]	[expr 0*$FirstStory+0*$TypicalStory]	$PanelSizeLevel1Column9	$MaximumFloor	$MaximumCol; 
# Level 2 
NodesAroundPanelZone	1	2	[expr 0*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory]	$PanelSizeLevel2Column1	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	2	2	[expr 1*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory]	$PanelSizeLevel2Column2	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	3	2	[expr 2*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory]	$PanelSizeLevel2Column3	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	4	2	[expr 3*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory]	$PanelSizeLevel2Column4	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	5	2	[expr 4*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory]	$PanelSizeLevel2Column5	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	6	2	[expr 5*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory]	$PanelSizeLevel2Column6	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	7	2	[expr 6*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory]	$PanelSizeLevel2Column7	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	8	2	[expr 7*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory]	$PanelSizeLevel2Column8	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	9	2	[expr 8*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory]	$PanelSizeLevel2Column9	$MaximumFloor	$MaximumCol; 
# Level 3 
NodesAroundPanelZone	1	3	[expr 0*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory]	$PanelSizeLevel3Column1	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	2	3	[expr 1*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory]	$PanelSizeLevel3Column2	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	3	3	[expr 2*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory]	$PanelSizeLevel3Column3	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	4	3	[expr 3*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory]	$PanelSizeLevel3Column4	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	5	3	[expr 4*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory]	$PanelSizeLevel3Column5	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	6	3	[expr 5*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory]	$PanelSizeLevel3Column6	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	7	3	[expr 6*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory]	$PanelSizeLevel3Column7	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	8	3	[expr 7*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory]	$PanelSizeLevel3Column8	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	9	3	[expr 8*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory]	$PanelSizeLevel3Column9	$MaximumFloor	$MaximumCol; 
# Level 4 
NodesAroundPanelZone	1	4	[expr 0*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory]	$PanelSizeLevel4Column1	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	2	4	[expr 1*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory]	$PanelSizeLevel4Column2	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	3	4	[expr 2*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory]	$PanelSizeLevel4Column3	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	4	4	[expr 3*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory]	$PanelSizeLevel4Column4	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	5	4	[expr 4*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory]	$PanelSizeLevel4Column5	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	6	4	[expr 5*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory]	$PanelSizeLevel4Column6	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	7	4	[expr 6*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory]	$PanelSizeLevel4Column7	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	8	4	[expr 7*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory]	$PanelSizeLevel4Column8	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	9	4	[expr 8*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory]	$PanelSizeLevel4Column9	$MaximumFloor	$MaximumCol; 
# Level 5 
NodesAroundPanelZone	1	5	[expr 0*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory]	$PanelSizeLevel5Column1	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	2	5	[expr 1*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory]	$PanelSizeLevel5Column2	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	3	5	[expr 2*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory]	$PanelSizeLevel5Column3	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	4	5	[expr 3*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory]	$PanelSizeLevel5Column4	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	5	5	[expr 4*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory]	$PanelSizeLevel5Column5	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	6	5	[expr 5*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory]	$PanelSizeLevel5Column6	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	7	5	[expr 6*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory]	$PanelSizeLevel5Column7	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	8	5	[expr 7*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory]	$PanelSizeLevel5Column8	$MaximumFloor	$MaximumCol; 
NodesAroundPanelZone	9	5	[expr 8*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory]	$PanelSizeLevel5Column9	$MaximumFloor	$MaximumCol; 

puts "Nodes for frame defined" 

# Define nodes for leaning column 
node	 101	[expr 9*$BayWidth]	[expr 0*$FirstStory+0*$TypicalStory];	#Level 1
node	 102	[expr 9*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory];	#Level 2
node	 103	[expr 9*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	# Level 3
node	 104	[expr 9*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	# Level 4
node	 105	[expr 9*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	# Level 5

puts "Nodes for leaning column defined" 

# Define extra nodes needed to define leaning column springs 
node	1022	[expr 9*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory];	# Node below floor level 2
node	1024	[expr 9*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory];	# Node above floor level 2
node	1032	[expr 9*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	# Node below floor level 3
node	1034	[expr 9*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	# Node above floor level 3
node	1042	[expr 9*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	# Node below floor level 4
node	1044	[expr 9*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	# Node above floor level 4
node	1052	[expr 9*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	# Node below floor level 5

puts "Extra nodes for leaning column springs defined"
