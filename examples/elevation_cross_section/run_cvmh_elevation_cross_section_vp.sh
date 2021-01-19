#!/bin/bash

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi
source $UCVM_INSTALL_PATH/conf/ucvm_env.sh

CWD=`pwd`
LABEL=cvmh_elevation_cross_section_vp
LAT1=35
LON1=-121
LAT2=35
LON2=-118
START_elevation=2000
END_elevation=-8000
MODEL=cvmh 

plot_elevation_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 1000 -v -100 -d vp -c ${MODEL} -a s -s ${START_elevation} -e ${END_elevation} -o ${CWD}/${LABEL}_o.png -i ${UCVM_INSTALL_PATH}

plot_elevation_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 1000 -v -100 -d vp -c ${MODEL} -a s -s ${START_elevation} -e ${END_elevation} -o ${CWD}/${LABEL}.png

plot_elevation_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 1000 -v -100 -d vp -c ${MODEL} -a d -s ${START_elevation} -e ${END_elevation} -f ${CWD}/${LABEL}_data.bin -o ${CWD}/${LABEL}_d.png

plot_elevation_cross_section.py -H


