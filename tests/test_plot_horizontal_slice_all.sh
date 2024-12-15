# test_plot_horizontal_slice.sh
#

MODEL=sfcvm
LAT1=37.2635
LON1=-122.1945
LAT2=38.3315
LON2=-121.1536
LABEL=taper2_1734139660226

## generate data only
time plot_horizontal_slice.py -s 0.1 -c ${MODEL} -a sd -o ${LABEL}_ALL.png -i $UCVM_INSTALL_PATH -t "horizontal vs ${MODEL}" -d all -b ${LAT1},${LON1} -u ${LAT2},${LON2} -e 1000 -S

./ucvm_horizontal_slice2csv_line.py taper2_1734139660226_vp_data.bin taper2_1734139660226_vp_meta.json 

./ucvm_horizontal_slice2csv_all.py taper2_1734139660226_vp_data.bin taper2_1734139660226_vp_meta.json taper2_1734139660226_vs_data.bin taper2_1734139660226_vs_meta.json taper2_1734139660226_density_data.bin taper2_1734139660226_density_meta.json
