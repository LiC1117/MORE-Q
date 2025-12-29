#!/bin/bash

#module load ORCA 5.0.3
ulimit -s unlimited
b=$PWD
orca_sys=($(find -type d -name "ORCA" -print|sort))
for ((i=0; i<3; i++)); do
        cd ${orca_sys[i]}
        orca_input.sh
        orca orca.inp > output
        echo ${orca_sys[i]}
        cd $b
done
