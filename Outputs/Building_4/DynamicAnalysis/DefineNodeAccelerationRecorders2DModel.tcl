# Define node acceleration recorders


cd $baseDir/$dataDir/EQ_$eqNumber/Scale_$scale/NodeAccelerations

recorder	Node	-file	NodeAccLevel1.out	-timeSeries	2	-time	-node	1110	2110	3110	4110	5110	6110	7110	8110	9110	-dof	1	accel;
recorder	Node	-file	NodeAccLevel2.out	-timeSeries	2	-time	-node	1211	2211	3211	4211	5211	6211	7211	8211	9211	-dof	1	accel;
recorder	Node	-file	NodeAccLevel3.out	-timeSeries	2	-time	-node	1311	2311	3311	4311	5311	6311	7311	8311	9311	-dof	1	accel;
recorder	Node	-file	NodeAccLevel4.out	-timeSeries	2	-time	-node	1411	2411	3411	4411	5411	6411	7411	8411	9411	-dof	1	accel;
recorder	Node	-file	NodeAccLevel5.out	-timeSeries	2	-time	-node	1511	2511	3511	4511	5511	6511	7511	8511	9511	-dof	1	accel;
