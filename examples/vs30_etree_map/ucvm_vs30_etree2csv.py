#!/usr/bin/env python3
"""
just like 
ucvm_horizontal_slice2csv.py

no need for depth
TODO: a bug in output of the lon_list and lat_list that they are off by one,

"""
import pandas as pd
import json
import sys
import numpy as np

# import raw floats array data from the external file into
# numpy array
def import_np_float_array(num_x, num_y):
    global fh
    try:
        fh = open(input_data_file, 'rb')
    except:
        print("ERROR: binary np float array data does not exist.")
        exit(1)

    floats = np.load(fh)
    fh.close()
    return floats


if __name__ == '__main__':
    """
    :input: h_data.bin h_meta.json
    :return: h_data.csv file
    
    example input_metadata_file = "h_meta.json"
    example input_data_file = "h_data.bin"
    Reads file names from header of this file.
    Outputs a CSV file with header:
    # cvm (abbr) : string
    # data_type : string
    # datapoints (# rows) : XX
    # starting_depth : XX 
    # ending_depth: XX
    # horizontal_spacing: XX
    # vertical_spacing: XX
    # starting_lat_lon: lat1,lon1
    # ending_lat_lon: lat2, lon2
    #
    depth, at_lon, vp, rho columns
    """

    if len(sys.argv) != 3:
        raise ValueError("Please provide arguments: ucvm_horizontal_slice2csv.py h_data.bin h_meta.json.\n"
                         "e.g. ./ucvm_horizontal_slice2csv.py h_data.bin h_meta.json")

    input_data_file = sys.argv[1]
    input_metadata_file = sys.argv[2]
    with open(input_metadata_file) as json_data:
        obj = json.load(json_data)

    #
    # The return values here are
    """
    ['num_y', 'lat1', 'data_type', 'lat2', 'color', 'max',
     'title', 'spacing', 'configfile', 'lon_list', 'num_x',
     'outfile', 'cvm', 'min', 'datapoints', 'lon1',
     'lat_list', 'lon2', 'installdir', 'mean']
    """
    latlist = obj["lat_list"]
    lonlist = obj["lon_list"]
    num_x = obj["num_x"]
    num_y = obj["num_y"]
## wrong by off by one
    npts = obj["datapoints"]

## remove when ucvm_plotting is fixed
    lat2 = obj["lat2"]
    lon2 = obj["lon2"]
    if(len(latlist) != num_y ):
      latlist.append(lat2)
    if(len(lonlist) != num_x ):
      lonlist.append(lon2)

    #
    total_pts = len(lonlist) * len(latlist)
    datalist = import_np_float_array(len(lonlist), len(latlist))
    # Use shape to return the dimensions of the np array that is returned
    # We assume it is 2D array
    datasizes = datalist.shape
    print("lonpts:",datasizes[1],"latpts:",datasizes[0])
    if npts != (datasizes[0] * datasizes[1]) :
        raise Exception("Number of data points does not each number of 1ddata points. Exiting", npts, datasizes[0] * datasizes[1])
    #
    # Combine the
    mystrlist = []
    for i in range(len(lonlist)):
        mystr = str(lonlist[i])
        mystrlist.append(mystr)

    if len(mystrlist) * len(latlist) != npts:
        print("Error: Total points should equal the number of lats times the number of lons",
              len(mystrlist) * len(latlist),npts)
        sys.exit(0)

    #
    # Find properties type
    propstr = "vs30"

    dlist = []
    # Create a dataframe with one columen of Lat values
    for idx in range(len(latlist)):
        dlist.append(latlist[idx])

    #Convert it to dataframe
    df = pd.DataFrame(dlist,columns=["Lats"])

    # Add each lonlist point as a column. 
    for indx in range(len(lonlist)):
        colstr = mystrlist[indx]
        vals = []
        for d in range(len(latlist)):
            vals.append(datalist[d][indx])
        df[colstr] = vals

    #
    # Create output file name
    # Example filename: input_data_file = "cross-cvmsi_meta.json"
    # cross-cvmsi_data.bin cross-cvmsi_meta.json
    output_file_name = input_data_file.replace(".bin",".csv")
    print("Writing CSV file: ", output_file_name)
    f = open(output_file_name, "w")

    """
  ['num_y', 'lat1', 'data_type', 'lat2', 'color', 'max',
   'title', 'spacing', 'configfile', 'lon_list', 'num_x',
   'outfile', 'cvm', 'min', 'datapoints', 'lon1',
   'lat_list', 'lon2', 'installdir', 'mean']
    """

    header_str = '''\
    # Input Data files: {0} {1}
    # Title: {7}
    # CVM(abbr): {2}
    # Spacing(m): {3}
    # Lon_pts: {4} 
    # Lat_pts: {5} 
    # Total_pts: {6}\n'''.format(
                input_data_file,
                input_metadata_file,
                obj["cvm"],
                obj["spacing"],
                len(lonlist),
                len(latlist),
                npts,
                obj["title"])

    print(header_str)
    f.write(header_str)
    df.to_csv(f, float_format='{:5.4f}'.format, index=False, mode="a")
    # This version will remove the column name headers
    #  df.to_csv(f, header=False,float_format='{:5.4f}'.format, index=False, mode="a")
    f.close()
    sys.exit(True)
