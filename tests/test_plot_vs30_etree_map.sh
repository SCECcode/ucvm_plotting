#
# test_plot_vs30_etree_map.sh
#

MODEL=1d
LAT1=37.2635
LON1=-122.1945
LAT2=38.3315
LON2=-121.1536

#rm -rf ${MODEL}_vs30.png ${MODEL}_vs30_dd.png 
#rm -rf ${MODEL}_vs30_data.bin ${MODEL}_vs30_dd_data.bin ${MODEL}_vs30_d_data.bin 
#rm -rf ${MODEL}_vs30_meta.json ${MODEL}_vs30_dd_meta.json ${MODEL}_vs30_d_meta.json 

## generate data and plot
time plot_vs30_etree_map.py -s 0.1 -c ${MODEL} -a sd -o ${MODEL}_vs30.png -i $UCVM_INSTALL_PATH -t "Thompson Caliornia vs30 Model v2020 thru UCVM" -b ${LAT1},${LON1} -u ${LAT2},${LON2}

## generate data only
time plot_vs30_etree_map.py -s 0.1 -c ${MODEL} -a sd -o ${MODEL}_vs30_d.png -i $UCVM_INSTALL_PATH -t "Thompson Caliornia vs30 Model v2020 thru UCVM" -b ${LAT1},${LON1} -u ${LAT2},${LON2} -S

## generate plot from given data
time plot_vs30_etree_map.py -s 0.1 -c ${MODEL} -a sd -o ${MODEL}_vs30_dd.png -i $UCVM_INSTALL_PATH -t "Thompson Caliornia vs30 Model v2020 thru UCVM" -b ${LAT1},${LON1} -u ${LAT2},${LON2} -f ${MODEL}_vs30_d_data.bin

## should be about the same
diff ${MODEL}_vs30_meta.json  ${MODEL}_vs30_dd_meta.json


## convert to csv
## using ucvm_metadata_utilities
./ucvm_horizontal_slice2csv.py ${MODEL}_vs30_data.bin ${MODEL}_vs30_meta.json
./ucvm_horizontal_slice2csv_line.py ${MODEL}_vs30_dd_data.bin ${MODEL}_vs30_dd_meta.json

