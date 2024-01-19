#!/bin/sh

source /u/local/Modules/default/init/modules.sh
module load python/anaconda3

echo "Task id is $SGE_TASK_ID"

python3 PostProcessingOnCluster.py $SGE_TASK_ID