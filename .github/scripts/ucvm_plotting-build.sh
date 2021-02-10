#!/bin/bash

source $UCVM_INSTALL_PATH/conf/ucvm_env.sh

echo "--- Show where ucvm_query is from :"
which ucvm_query 
echo "--- Show ucvm built info :"
ucvm_query -H
echo "--- Unpac ucvm_plotting :"
conda install matplotlib basemap basemap-data-hires
./unpack-dist

conda list
