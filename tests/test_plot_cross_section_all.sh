#
# test_plot_cross_section_all.sh
#

MODEL=sfcvm
START=0
END=5000
## horizontal step
HSTEP=1424.4
## vertical step
VSTEP=50
Lat1=38.35
Lon1=-122.6424
Lat2=37.4674
Lon2=-121.5244
LABEL_VP=CVM_4133_c_vp
LABEL_ALL=CVM_4133

## geneate vp as baseline
plot_cross_section.py -s 0 -h ${HSTEP} -d density -c ${MODEL} -a sd -o ${LABEL_VP}.png -i ${UCVM_INSTALL_PATH} -v ${VSTEP} -b ${Lat1},${Lon1} -u ${Lat2},${Lon2} -e 5000
./ucvm_cross_section2csv_line.py ${LABEL_VP}_data.bin ${LABEL_VP}_meta.json

## generate data only
plot_cross_section.py -S -s 0 -h ${HSTEP}.4 -d all -c ${MODEL} -a sd -o ${LABEL_ALL}_all.png -i ${UCVM_INSTALL_PATH} -v ${VSTEP} -b${Lat1},${Lon1}, -u ${Lat2},${Lon2} -e 5000
./ucvm_cross_section2csv_all.py ${LABEL_ALL}_vp_data.bin ${LABEL_ALL}_vp_meta.json ${LABEL_ALL}_vs_data.bin ${LABEL_ALL}_vs_meta.json ${LABEL_ALL}_density_data.bin ${LABEL_ALL}_density_meta.json 

### run on docker container
#./plotCVM-vertSection.pl ${LABEL_VP}_data.csv 1 0 0 0 1 1 0
#./plotCVM-vertSection2.pl ${LABEL_VP}_all.csv 1 1 0 0 0 1 1 0
