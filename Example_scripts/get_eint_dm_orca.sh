#!/bin/bash


e_dm=$(grep 'FINAL SINGLE POINT ENERGY' ./ORCA_dm/output|awk '{print $5}')
e_om=$(grep 'FINAL SINGLE POINT ENERGY' ./ORCA_om/output|awk '{print $5}')
e_rec=$(grep 'FINAL SINGLE POINT ENERGY' ./ORCA_rec/output|awk '{print $5}')
e_bd=$(echo "scale=6; ($e_dm - $e_om - $e_rec)*27.2107"|bc)
echo $e_bd > ./bd.dat

   



