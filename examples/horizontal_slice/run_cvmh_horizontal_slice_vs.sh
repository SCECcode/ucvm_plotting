#!/bin/bash
if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi
source $UCVM_INSTALL_PATH/conf/ucvm_env.sh

CWD=`pwd`
LABEL=cvmh_horizontal_slice_vs
LAT1=33.35
LON1=-118
LAT2=34.35
LON2=-117
DEPTH=1000
SPACING=0.01
MODEL=cvmh 

plot_horizontal_slice.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -e ${DEPTH} -d vs -c ${MODEL} -a s -s ${SPACING} -o ${CWD}/${LABEL}_o.png -i ${UCVM_INSTALL_PATH}

plot_horizontal_slice.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -e ${DEPTH} -d vs -c ${MODEL} -a s -s ${SPACING} -o ${CWD}/${LABEL}.png

plot_horizontal_slice.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -e ${DEPTH} -d vs -c ${MODEL} -a d -s ${SPACING} -f ${CWD}/${LABEL}_data.bin -o ${CWD}/${LABEL}_d.png

plot_horizontal_slice.py -H

