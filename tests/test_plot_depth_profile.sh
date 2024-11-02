#
# test_plot_horizontal_slice.sh
#
plot_depth_profile.py  -n /usr/local/share/ucvm/install/conf/ucvm.conf 
-i /usr/local/share/ucvm/install -d vs -c sfcvm -o ../result/CVM_1730507668856_v.png -C 'San Francisco Bay Velocity Model
' -v 100 -b 0 -s 38.1729,-121.4332 -e 30000

MODEL=sfcvm
LAT1=38.1729
LON1=-121.4332
START=0
END=3000

rm -rf ${MODEL}_d_d_vs.png ${MODEL}_d_dd_vs.png
rm -rf ${MODEL}_d_vs_data.bin ${MODEL}_d_d_vs_data.bin 
rm -rf ${MODEL}_d_vs_meta.json ${MODEL}_d_d_vs_meta.json 

## generate data and plot
time plot_depth_profile.py -d vs -c ${MODEL} -o ${MODEL}_d_vs.png -i $UCVM_INSTALL_PATH -C "vertical profile vs ${MODEL}" -b ${LAT1},${LON1} -b ${START} -e ${END}

## generate data only
#time plot_depth_profile.py -d vs -c ${MODEL} -o ${MODEL}_d_d_vs.png -i $UCVM_INSTALL_PATH -C "vertical profile vs ${MODEL}" -b ${LAT1},${LON1} -b ${START} -e ${END} -S

## generate plot from given data
#time plot_depth_profile.py -d vs -c ${MODEL} -o ${MODEL}_d_dd_vs.png -i $UCVM_INSTALL_PATH -C "vertical profile vs ${MODEL}" -b ${LAT1},${LON1} -b ${START} -e ${END} -f ${MODEL}_d_d_vs.png

## should be about the same
#diff ${MODEL}_d_d_vs_meta.json  ${MODEL}_d_vs_meta.json


## convert to csv
## using ucvm_metadata_utilities
./ucvm_vertical_profile2csv.py ${MODEL}_d_vs_data.bin ${MODEL}_d_vs_meta.json
#./ucvm_vertical_profile2csv_line.py ${MODEL}_vs_data.bin ${MODEL}_vs_meta.json

