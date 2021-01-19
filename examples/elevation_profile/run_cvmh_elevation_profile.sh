#!/bin/bash
if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi
source $UCVM_INSTALL_PATH/conf/ucvm_env.sh

CWD=`pwd`
LABEL=cvmh_elevation_profile
LAT=34
LON=-115
STEP=-10
START_elevation=1000
END_elevation=-3000
MODEL=cvmh 

plot_elevation_profile.py -s ${LAT},${LON} -b ${START_elevation} -e ${END_elevation} -d vs,vp,density -v ${STEP} -c ${MODEL} -o ${CWD}/${LABEL}_o.png -i ${UCVM_INSTALL_PATH}

plot_elevation_profile.py -s ${LAT},${LON} -b ${START_elevation} -e ${END_elevation} -d vs,vp,density -v ${STEP} -c ${MODEL} -o ${CWD}/${LABEL}.png

plot_elevation_profile.py -s ${LAT},${LON} -b ${START_elevation} -e ${END_elevation} -d vs -v ${STEP} -c ${MODEL} -f ${CWD}/${LABEL}_matprops.json -o ${CWD}/${LABEL}_vs.png

plot_elevation_profile.py -H
