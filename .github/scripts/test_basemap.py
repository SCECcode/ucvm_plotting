#!/usr/bin/env python

import matplotlib 
print(matplotlib.__file__)

import mpl_toolkits
print(mpl_tookits.__file__)

try:
    from mpl_toolkits import basemap
except StandardError, e:
    print("ERROR: Basemap must be installed on your system in order to generate these plots.")
    print(e)
    exit(1)
