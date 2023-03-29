#!/usr/bin/env python
#
# Using META_FILE and a list of COLLECTED index
# extract a set of latlons
#
# specificially from plotting difference map
#   ./extract_latlon.py diff_cvmsi_taper_none_z1.0_meta.json data.json
#
# sample of data.json,
#
#  { "max_j": 1701, "max_i": 1101, "max_less":-270.00000, "max_less_i":640, 
#     "max_less_j":541, "less":441, "more":1776134, "zero":96226, "i":[ 613.00000,614.00000 ], 
#     "j": [ 767.00000,503.00000 ] }
#

import os
import sys
import json
import pdb

if len (sys.argv) != 3:
  print("Input format: % extract_latlon.py meta_file data_file")
  sys.exit()
else:
  meta_file = sys.argv[1]
  data_file = sys.argv[2]

try:
    mfile="./"+meta_file
    f = open(mfile, "r")
    json_string = f.read()
    f.close()
    meta_data = json.loads(json_string)
except OSError as e:
    eG(e, "Parsing meta data")

try:
    dfile="./"+data_file
    f = open(dfile, "r")
    json_string = f.read()
    f.close()
    collect_data = json.loads(json_string)
except OSError as e:
    eG(e, "Parsing collect data")


lon_list=meta_data["lon_list"]
lat_list=meta_data["lat_list"]
lats_idx=collect_data["i"]
lons_idx=collect_data["j"]
max_less_lat_idx=collect_data["max_less_i"]
max_less_lon_idx=collect_data["max_less_j"]

lon=float(lon_list[max_less_lon_idx])
lat=float(lat_list[max_less_lat_idx])
txt="#SPECIAL: %.5f %.5f" % (lon,lat)
print(txt)

for i in range(0, len(lons_idx)):
   lon_idx=int(lons_idx[i])
   lat_idx=int(lats_idx[i])
   lon=float(lon_list[lon_idx])
   lat=float(lat_list[lat_idx])
   txt="%.5f %.5f" % (lon,lat)
   print(txt)

