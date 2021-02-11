#!/bin/bash

source $UCVM_INSTALL_PATH/conf/ucvm_env.sh

echo "--- Show where ucvm_query is from :"
which ucvm_query 

echo "--- Show ucvm built info :"
which installed_models.py
installed_models.py

echo "--- Setup basemap and matplotlib :"

pip install matplotlib
pip install basemap basemap-data-hires

echo "Test basemap :"
./.github/scripts/test_basemap.py

#echo "--- Unpack ucvm_plotting :"
#./unpack-dist
