#!/bin/bash
## comparing data input of two plots

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi
source $UCVM_INSTALL_PATH/conf/ucvm_env.sh

CWD=`pwd`
LABEL=cvmh_compare_plot
LAT1=33.35
LON1=-118
LAT2=34.35
LON2=-117
SPACING=0.01
MODEL=cvmh 

XLABEL=cvmh_vs30_map
YLABEL=cvmh_vs30_etree_map


plot_vs30_map.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -c ${MODEL} -a s -s ${SPACING} -o ${CWD}/${XLABEL}.png

plot_vs30_etree_map.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -c ${MODEL} -a s -s ${SPACING} -o ${CWD}/${YLABEL}.png

plot_compare_plot.py -x ${CWD}/${XLABEL}_data.bin -y ${CWD}/${YLABEL}_data.bin -o ${CWD}/${LABEL}.png

plot_compare_plot.py -x ${CWD}/${XLABEL}_data.bin -y ${CWD}/${XLABEL}_data.bin -o ${CWD}/${LABEL}_x.png

plot_compare_plot.py -x ${CWD}/${YLABEL}_data.bin -y ${CWD}/${YLABEL}_data.bin -o ${CWD}/${LABEL}_y.png

