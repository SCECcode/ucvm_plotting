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
which python
python -V
which conda
conda -V

#ls /usr/share/miniconda/bin
/usr/share/miniconda/bin/python -V

#/usr/share/miniconda/bin/activate
#conda init

pip install matplotlib
pip install basemap basemap-data-hires

#conda list |grep matplotlib
#conda install pyqt
#conda install matplotlib
#conda install basemap basemap-data-hires
#conda install -c conda-forge basemap basemap-data-hires

echo "Test basemap :"
./.github/scripts/test_basemap.py

#echo "--- Unpack ucvm_plotting :"
#./unpack-dist
