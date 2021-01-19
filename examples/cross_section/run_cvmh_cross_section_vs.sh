#!/bin/bash

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi
source $UCVM_INSTALL_PATH/conf/ucvm_env.sh

LABEL=cvmh_cross_section_vs
LAT1=33.7
LON1=-118.21
LAT2=33.9
LON2=-118.22
START_depth=0.0
END_depth=1000
MODEL=cvmh 

## side effect is generate the label_data.bin
plot_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 10 -v 2 -d vs -c ${MODEL} -a s -s ${START_depth} -e ${END_depth} -i ${UCVM_INSTALL_PATH} -o ${LABEL}.png

## pick up the input file instead of doing explicit query
plot_cross_section.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -h 10 -v 2 -d vs -c ${MODEL} -a d -s ${START_depth} -e ${END_depth} -f ${LABEL}_data.bin -i ${UCVM_INSTALL_PATH} -o ${LABEL}_d.png

plot_cross_section.py -H


