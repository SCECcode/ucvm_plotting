#!/bin/bash

source $UCVM_INSTALL_PATH/conf/ucvm_env.sh

echo "--- Show where ucvm_query is from :"
which ucvm_query 

echo "--- Show ucvm built info :"
which installed_models.py
installed_models.py

echo "--- Setup basemap and matplotlib :"
which pip
pip -V
conda -V
which python
python -V

#pip install basemap basemap-data-hires
#pip install matplotlib
#conda install -y -c conda-forge basemap basemap-data-hires
#conda install -y  matplotlib

echo "--- Unpack ucvm_plotting :"
./unpack-dist
