#!/usr/bin/env python

try:
    from mpl_toolkits import basemap
except StandardError, e:
    print("ERROR: Basemap must be installed on your system in order to generate these plots.")
    print(e)
    exit(1)
