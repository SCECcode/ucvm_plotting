#
#

LAT1=35.02
LON1=-126.4
LAT2=41.50
LON2=-118.8
SPACING=0.1
MODEL=sfcvm 

rm -rf sfcvm_z25_data.bin sfcvm_z25_meta.json sfcvm_z25.png
rm -rf sfcvm_d_z25.png

## generate data and plot
time plot_z25_map.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -c ${MODEL} -a s -s ${SPACING} -o ${MODEL}_z25.png -i ${UCVM_INSTALL_PATH} -t "Z25 ${MODEL}"

## generate plot from given data
time plot_z25_map.py -b ${LAT1},${LON1} -u ${LAT2},${LON2} -c ${MODEL} -a s -s ${SPACING} -o ${MODEL}_d_z25.png -i ${UCVM_INSTALL_PATH} -t "Z25 ${MODEL}" -f ${MODEL}_z25_data.bin

## convert to csv
## using ucvm_metadata_utilities
#./ucvm_horizontal_slice2csv.py sfcvm_z25_data.bin sfcvm_z25_meta.json 

