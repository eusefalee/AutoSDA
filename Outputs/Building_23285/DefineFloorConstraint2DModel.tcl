# This file will be used to define floor constraint 

set	ConstrainDOF	1;	# Nodes at same floor level have identical lateral displacement 

# Level 2 
equalDOF	121	221	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	121	321	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	121	421	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	121	521	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	121	621	$ConstrainDOF;	# Pier 1 to Pier 6
equalDOF	121	721	$ConstrainDOF;	# Pier 1 to Pier 7
equalDOF	121	821	$ConstrainDOF;	# Pier 1 to Pier 8
equalDOF	121	921	$ConstrainDOF;	# Pier 1 to Pier 9
equalDOF	121	9102	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 3 
equalDOF	131	231	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	131	331	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	131	431	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	131	531	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	131	631	$ConstrainDOF;	# Pier 1 to Pier 6
equalDOF	131	731	$ConstrainDOF;	# Pier 1 to Pier 7
equalDOF	131	831	$ConstrainDOF;	# Pier 1 to Pier 8
equalDOF	131	931	$ConstrainDOF;	# Pier 1 to Pier 9
equalDOF	131	9103	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 4 
equalDOF	141	241	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	141	341	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	141	441	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	141	541	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	141	641	$ConstrainDOF;	# Pier 1 to Pier 6
equalDOF	141	741	$ConstrainDOF;	# Pier 1 to Pier 7
equalDOF	141	841	$ConstrainDOF;	# Pier 1 to Pier 8
equalDOF	141	941	$ConstrainDOF;	# Pier 1 to Pier 9
equalDOF	141	9104	$ConstrainDOF;	# Pier 1 to Leaning column

# Level 5 
equalDOF	151	251	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	151	351	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	151	451	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	151	551	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	151	651	$ConstrainDOF;	# Pier 1 to Pier 6
equalDOF	151	751	$ConstrainDOF;	# Pier 1 to Pier 7
equalDOF	151	851	$ConstrainDOF;	# Pier 1 to Pier 8
equalDOF	151	951	$ConstrainDOF;	# Pier 1 to Pier 9
equalDOF	151	9105	$ConstrainDOF;	# Pier 1 to Leaning column

# puts "Floor constraint defined"