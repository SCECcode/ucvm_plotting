#!/usr/bin/env python

import sys
import os
import time

# Generate a master mesh grid, out.grd, 
# and time the model population speed of the
# available crustal models 

#
# get installed models
cmd="$UCVM_INSTALL_PATH/bin/ucvm_query.sh -J"
os.system(cmd)

