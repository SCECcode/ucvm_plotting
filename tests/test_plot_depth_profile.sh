#
# test_plot_horizontal_slice.sh
#

MODEL=sfcvm
LAT1=38.1729
LON1=-121.4332
START=0
END=3000
STEP=100

rm -rf ${MODEL}_d_d_vs.png ${MODEL}_d_dd_vs.png
rm -rf ${MODEL}_d_vs_data.bin ${MODEL}_d_d_vs_data.bin 
rm -rf ${MODEL}_d_vs_meta.json ${MODEL}_d_d_vs_meta.json 


time plot_depth_profile.py -d vs -c ${MODEL} -o ${MODEL}_d_vs.png -i $UCVM_INSTALL_PATH -C "vertical profile vs ${MODEL}" -s ${LAT1},${LON1} -b ${START} -e ${END} -v ${STEP}


## generate data only
time plot_depth_profile.py -d vs -c ${MODEL} -o ${MODEL}_d_d_vs.png -i $UCVM_INSTALL_PATH -C "vertical profile vs ${MODEL}" -s ${LAT1},${LON1} -b ${START} -e ${END} -v ${STEP} -S

## generate plot from given data
time plot_depth_profile.py -d vs -c ${MODEL} -o ${MODEL}_d_dd_vs.png -i $UCVM_INSTALL_PATH -C "vertical profile vs ${MODEL}" -s ${LAT1},${LON1} -b ${START} -e ${END} -f ${MODEL}_d_d_vs_matprops.json -v ${STEP}

## should be about the same
diff ${MODEL}_d_d_vs_meta.json  ${MODEL}_d_vs_meta.json


## convert to csv
## using ucvm_metadata_utilities
./ucvm_vertical_profile2csv.py ${MODEL}_d_vs_matprops.json ${MODEL}_d_vs_meta.json
./ucvm_vertical_profile2csv.py ${MODEL}_vs_matprops.json ${MODEL}_vs_meta.json

