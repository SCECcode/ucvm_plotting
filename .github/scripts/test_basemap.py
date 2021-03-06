#!/usr/bin/env python2

import matplotlib 
print(matplotlib)
print(matplotlib.__file__)

import mpl_toolkits
print(mpl_toolkits)
print(mpl_toolkits.__file__)

try:
    from mpl_toolkits import basemap
except Exception as e:
    print("ERROR: Basemap must be installed on your system in order to generate these plots.")
    print(e)
    exit(1)
