#
# test_plot_horizontal_slice.py
#

MODEL=sfcvm
LAT1=37.2635
LON1=-122.1945
LAT2=38.3315
LON2=-121.1536

rm -rf ${MODEL}_vs.png ${MODEL}_dd_vs.png
rm -rf ${MODEL}_vs_data.bin ${MODEL}_d_vs_data.bin 
rm -rf ${MODEL}_vs_meta.json ${MODEL}_d_vs_meta.json 

## generate data and plot
time plot_horizontal_slice.py -s 0.1 -c ${MODEL} -a sd -o ${MODEL}_vs.png -i $UCVM_INSTALL_PATH -t "horizontal vs ${MODEL}" -d vs -b ${LAT1},${LON1} -u ${LAT2},${LON2} -e 1000

## generate data only
time plot_horizontal_slice.py -s 0.1 -c ${MODEL} -a sd -o ${MODEL}_d_vs.png -i $UCVM_INSTALL_PATH -t "horizontal vs ${MODEL}" -d vs -b ${LAT1},${LON1} -u ${LAT2},${LON2} -e 1000 -S

## generate plot from given data
time plot_horizontal_slice.py -s 0.1 -c ${MODEL} -a sd -o ${MODEL}_dd_vs.png -i $UCVM_INSTALL_PATH -t "horizontal vs ${MODEL}" -d vs -b ${LAT1},${LON1} -u ${LAT2},${LON2} -e 1000 -f  ${MODEL}_d_vs_data.bin

## should be about the same
diff ${MODEL}_d_vs_meta.json  ${MODEL}_vs_meta.json


## convert to csv
## using ucvm_metadata_utilities
#ucvm_horizontal_slice2csv.py ${MODEL}_d_vs_data.bin ${MODEL}_d_vs_meta.json
#ucvm_horizontal_slice2csv.py ${MODEL}_vs_data.bin ${MODEL}_vs_meta.json

