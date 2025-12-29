##This example shows briefly how to obtain the input features of a (new) CPLX system used for its binding feature prediction.

[] Step1 Splitting systems

splitting_CPLX.py


[] Step2 do ORCA and for each system

orca_run.sh 


[] Step3 extract propeties into json

get_eint_dm_orca.sh
get_json_sg_orca.py

[] Step 4 Load json file into DataFrame.


[] Step 5 Use the ML models to predict binding features
