# This file will be used to define damping

# A damping ratio of 2% is used for steel buildings
set	dampingRatio	0.02;
# Define the value for pi
set	pi	[expr 2.0*asin(1.0)];

# Defining damping parameters
set	omegaI	[expr (2.0*$pi) / $periodForRayleighDamping_1];
set	omegaJ	[expr (2.0*$pi) / $periodForRayleighDamping_2];
set	alpha0	[expr ($dampingRatio*2.0*$omegaI*$omegaJ) / ($omegaI+$omegaJ)];
set	alpha1	[expr ($dampingRatio*2.0) / ($omegaI+$omegaJ) * ($n+1.0) / $n];	 # (n+1.0)/n factor is because stiffness for elastic elements have been modified

# Assign damping to beam elements
region	1	-ele	2121221	2221321	2321421	2421521	2521621	2621721	2721821	2821921	2131231	2231331	2331431	2431531	2531631	2631731	2731831	2831931	2141241	2241341	2341441	2441541	2541641	2641741	2741841	2841941	2151251	2251351	2351451	2451551	2551651	2651751	2751851	2851951	-rayleigh	0.0	0.0	$alpha1	0.0;
# Assign damping to column elements
region	2	-ele	3111121	3211221	3311321	3411421	3511521	3611621	3711721	3811821	3911921	3121131	3221231	3321331	3421431	3521531	3621631	3721731	3821831	3921931	3131141	3231241	3331341	3431441	3531541	3631641	3731741	3831841	3931941	3141151	3241251	3341351	3441451	3541551	3641651	3741751	3841851	3941951	-rayleigh	0.0	0.0	$alpha1	0.0;
# Assign damping to nodes
region	3	-node	1211	2211	3211	4211	5211	6211	7211	8211	9211	102	1311	2311	3311	4311	5311	6311	7311	8311	9311	103	1411	2411	3411	4411	5411	6411	7411	8411	9411	104	1511	2511	3511	4511	5511	6511	7511	8511	9511	105	-rayleigh	$alpha0	0.0	0.0	0.0;

puts "Rayleigh damping defined"