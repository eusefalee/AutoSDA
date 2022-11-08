# This file will be used to define floor constraint 
# Nodes at same floor level have identical lateral displacement
# Select mid right node of each panel zone as the constrained node

set	ConstrainDOF	1;  # X-direction

# Level 2 
equalDOF	1211	2211	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	1211	3211	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	1211	4211	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	1211	5211	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	1211	6211	$ConstrainDOF;	# Pier 1 to Pier 6
equalDOF	1211	7211	$ConstrainDOF;	# Pier 1 to Pier 7
equalDOF	1211	8211	$ConstrainDOF;	# Pier 1 to Pier 8
equalDOF	1211	9211	$ConstrainDOF;	# Pier 1 to Pier 9
equalDOF	1211	102	$ConstrainDOF;	#Pier 1 to Leaning column

# Level 3 
equalDOF	1311	2311	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	1311	3311	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	1311	4311	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	1311	5311	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	1311	6311	$ConstrainDOF;	# Pier 1 to Pier 6
equalDOF	1311	7311	$ConstrainDOF;	# Pier 1 to Pier 7
equalDOF	1311	8311	$ConstrainDOF;	# Pier 1 to Pier 8
equalDOF	1311	9311	$ConstrainDOF;	# Pier 1 to Pier 9
equalDOF	1311	103	$ConstrainDOF;	#Pier 1 to Leaning column

# Level 4 
equalDOF	1411	2411	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	1411	3411	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	1411	4411	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	1411	5411	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	1411	6411	$ConstrainDOF;	# Pier 1 to Pier 6
equalDOF	1411	7411	$ConstrainDOF;	# Pier 1 to Pier 7
equalDOF	1411	8411	$ConstrainDOF;	# Pier 1 to Pier 8
equalDOF	1411	9411	$ConstrainDOF;	# Pier 1 to Pier 9
equalDOF	1411	104	$ConstrainDOF;	#Pier 1 to Leaning column

# Level 5 
equalDOF	1511	2511	$ConstrainDOF;	# Pier 1 to Pier 2
equalDOF	1511	3511	$ConstrainDOF;	# Pier 1 to Pier 3
equalDOF	1511	4511	$ConstrainDOF;	# Pier 1 to Pier 4
equalDOF	1511	5511	$ConstrainDOF;	# Pier 1 to Pier 5
equalDOF	1511	6511	$ConstrainDOF;	# Pier 1 to Pier 6
equalDOF	1511	7511	$ConstrainDOF;	# Pier 1 to Pier 7
equalDOF	1511	8511	$ConstrainDOF;	# Pier 1 to Pier 8
equalDOF	1511	9511	$ConstrainDOF;	# Pier 1 to Pier 9
equalDOF	1511	105	$ConstrainDOF;	#Pier 1 to Leaning column

puts "Floor constraint defined"