# This file will be used to define all nodes 
# Units: inch 


# Set bay width and story height 
set	BayWidth	[expr 30.00*12]; 
set	FirstStory	[expr 18.00*12]; 
set	TypicalStory	[expr 16.00*12]; 


# Define nodes at corner of frames 
# Level 1 
node	111	[expr 0*$BayWidth]	[expr 0*$FirstStory];	 # Column #1 
node	211	[expr 1*$BayWidth]	[expr 0*$FirstStory];	 # Column #2 
node	311	[expr 2*$BayWidth]	[expr 0*$FirstStory];	 # Column #3 
node	411	[expr 3*$BayWidth]	[expr 0*$FirstStory];	 # Column #4 
node	511	[expr 4*$BayWidth]	[expr 0*$FirstStory];	 # Column #5 
node	611	[expr 5*$BayWidth]	[expr 0*$FirstStory];	 # Column #6 
node	711	[expr 6*$BayWidth]	[expr 0*$FirstStory];	 # Column #7 
node	811	[expr 7*$BayWidth]	[expr 0*$FirstStory];	 # Column #8 
node	911	[expr 8*$BayWidth]	[expr 0*$FirstStory];	 # Column #9 
node	1011	[expr 9*$BayWidth]	[expr 0*$FirstStory];	 # Column #10 

# Level 2 
node	121	[expr 0*$BayWidth]	[expr 1*$FirstStory];	 # Column #1 
node	221	[expr 1*$BayWidth]	[expr 1*$FirstStory];	 # Column #2 
node	321	[expr 2*$BayWidth]	[expr 1*$FirstStory];	 # Column #3 
node	421	[expr 3*$BayWidth]	[expr 1*$FirstStory];	 # Column #4 
node	521	[expr 4*$BayWidth]	[expr 1*$FirstStory];	 # Column #5 
node	621	[expr 5*$BayWidth]	[expr 1*$FirstStory];	 # Column #6 
node	721	[expr 6*$BayWidth]	[expr 1*$FirstStory];	 # Column #7 
node	821	[expr 7*$BayWidth]	[expr 1*$FirstStory];	 # Column #8 
node	921	[expr 8*$BayWidth]	[expr 1*$FirstStory];	 # Column #9 
node	1021	[expr 9*$BayWidth]	[expr 1*$FirstStory];	 # Column #10 

# Level 3 
node	131	[expr 0*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #1 
node	231	[expr 1*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #2 
node	331	[expr 2*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #3 
node	431	[expr 3*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #4 
node	531	[expr 4*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #5 
node	631	[expr 5*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #6 
node	731	[expr 6*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #7 
node	831	[expr 7*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #8 
node	931	[expr 8*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #9 
node	1031	[expr 9*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	 # Column #10 

# Level 4 
node	141	[expr 0*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #1 
node	241	[expr 1*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #2 
node	341	[expr 2*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #3 
node	441	[expr 3*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #4 
node	541	[expr 4*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #5 
node	641	[expr 5*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #6 
node	741	[expr 6*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #7 
node	841	[expr 7*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #8 
node	941	[expr 8*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #9 
node	1041	[expr 9*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	 # Column #10 

# Level 5 
node	151	[expr 0*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #1 
node	251	[expr 1*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #2 
node	351	[expr 2*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #3 
node	451	[expr 3*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #4 
node	551	[expr 4*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #5 
node	651	[expr 5*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #6 
node	751	[expr 6*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #7 
node	851	[expr 7*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #8 
node	951	[expr 8*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #9 
node	1051	[expr 9*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	 # Column #10 

# puts "Nodes at frame corner defined" 

# Define nodes for leaning column 
node	9111	[expr 10*$BayWidth]	[expr 0*$FirstStory]; 	# Level 1
node	9112	[expr 10*$BayWidth]	[expr 1*$FirstStory]; 	# Level 2
node	9113	[expr 10*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	# Level 3
node	9114	[expr 10*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	# Level 4
node	9115	[expr 10*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	# Level 5

# puts "Nodes for leaning column defined" 

# Define extra nodes needed to define leaning column springs 
node	91122	[expr 10*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory];	# Node below floor level 2
node	91124	[expr 10*$BayWidth]	[expr 1*$FirstStory+0*$TypicalStory];	# Node above floor level 2
node	91132	[expr 10*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	# Node below floor level 3
node	91134	[expr 10*$BayWidth]	[expr 1*$FirstStory+1*$TypicalStory];	# Node above floor level 3
node	91142	[expr 10*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	# Node below floor level 4
node	91144	[expr 10*$BayWidth]	[expr 1*$FirstStory+2*$TypicalStory];	# Node above floor level 4
node	91152	[expr 10*$BayWidth]	[expr 1*$FirstStory+3*$TypicalStory];	# Node below floor level 5

# puts "Extra nodes for leaning column springs defined"
