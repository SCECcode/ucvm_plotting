#!/bin/bash

source $UCVM_INSTALL_PATH/conf/ucvm_env.sh

echo "--- Show where ucvm_query is from :"
which ucvm_query 

echo "--- Show ucvm built info :"
which installed_models.py
installed_models.py

echo "--- Unpac ucvm_plotting :"
conda install -y matplotlib basemap basemap-data-hires
./unpack-dist
