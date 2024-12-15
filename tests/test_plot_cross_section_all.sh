#
# test_plot_cross_section.sh
#

MODEL=sfcvm
START=0
END=5000
## horizontal step
HSTEP=852
## vertical step
VSTEP=50
LAT1=37.5783
LON1=-122.658 
LAT2=-37.7505
LON2=-121.1362 
LABEL=CVM_1734139660226

## generate data only
time plot_cross_section.py -a sd -s ${START} -e ${END} -h ${HSTEP} -d all -c sfcvm -o ${LABEL}_ALL.png -i $UCVM_INSTALL_PATH -t "cross section vs ${MODEL}" -v ${VSTEP} -b ${LAT1},${LON1} -u ${LAT2},${LON2} -S

./ucvm_cross_section2csv_line.py CVM_1734139660226_density_data.bin CVM_1734139660226_density_meta.json

./ucvm_cross_section2csv_all.py CVM_1734139660226_vp_data.bin CVM_1734139660226_vp_meta.json CVM_1734139660226_vs_data.bin CVM_1734139660226_vs_meta.json CVM_1734139660226_density_data.bin CVM_1734139660226_density_meta.json 


