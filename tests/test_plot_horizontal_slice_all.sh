# test_plot_horizontal_slice_all.sh
#
#

MODEL=sfcvm
LAT1=38.35
LON1=-122.9064
LAT2=39.0291
LON2=-122.0213
LABEL_VP=CVM_4132_h_vp
LABEL_ALL=CVM_4132

#baseline test data
plot_horizontal_slice.py -d vp -c ${MODEL} -s 0.0078 -a sd -o ${LABEL_VP}.png -i $UCVM_INSTALL_PATH  -b 38.35,-122.9064 -u 39.0291,-122.0213 -e 1000
./ucvm_horizontal_slice2csv_line.py ${LABEL_VP}_data.bin ${LABEL_VP}_meta.json 

#generate data files only
plot_horizontal_slice.py -S -d all -c ${MODEL} -s 0.0078 -a sd -o ${LABEL_ALL}_all.png -i $UCVM_INSTALL_PATH  -b 38.35,-122.9064 -u 39.0291,-122.0213 -e 1000
./ucvm_horizontal_slice2csv_all.py ${LABEL_ALL}_vp_data.bin ${LABEL_ALL}_vp_meta.json ${LABEL_ALL}_vs_data.bin ${LABEL_ALL}_vs_meta.json ${LABEL_ALL}_density_data.bin ${LABEL_ALL}_density_meta.json

## on docker
#./plotCVM-horzSlice2.pl CVM_4132_all_data.csv 1 0 0 0 1 0
#./plotCVM-horzSlice.pl CVM_4132_h_vp_data.csv 0 0 0 1 0

