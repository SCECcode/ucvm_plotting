#!/usr/bin/env python

import sys
import os
import time

# test the ucvm_query call from ucvm_plotting

# get installed models
cmd="$UCVM_INSTALL_PATH/utilities/run_ucvm_query.sh -H"
os.system(cmd)

