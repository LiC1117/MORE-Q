#!/bin/bash

Func='PBE' #functional
bs='def2-TZVPP' # basis set
#nproc='16' # ncores
RI='NORI' # if RI approximation
Type='SP' 
Vdw='D3BJ'
Grad='EnGrad'
file='up_best.xyz' #for dimer
#file=$(ls|grep _om.xyz) #for om
#file=rcplx.xyz #for rec

cat > orca.inp << EOF
! $Func $bs $Grad $RI $Type $Vdw

%elprop
Dipole true
Quadrupole true
Polar 1 
end


%pal
nprocs 96
end

*xyzfile 0 1 $file

EOF


