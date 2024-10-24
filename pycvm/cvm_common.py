##
#  @file common.py
#  @brief Common definitions and functions for plotting scripts.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Provides common definitions and functions that are shared amongst all UCVM
#  plotting scripts. Facilitates easier multi-processing as well.

#  Imports
from subprocess import call, Popen, PIPE, STDOUT
import sys
import os
import multiprocessing
import math
import struct
import getopt

## Version string.
VERSION = "25.1.0"

## Constant for all material properties.
ALL_PROPERTIES = ["vp", "vs", "density"]
## Constant for just Vs.
VS = ["vs"]
## Constant for just Vp.
VP = ["vp"]
## Constant for just density.
DENSITY = ["density"]

#  Class Definitions

## Common Access Functions

global ask_number
## Makes sure the response is a number.
def ask_number(question):
    temp_val = None
    
    while temp_val is None:
        temp_val = raw_input(question)
        try:
            float(temp_val)
            return float(temp_val)
        except ValueError:
            print(temp_val + " is not a number. Please enter a number.")
            temp_val = None

    
global ask_path
## get optional answer
def ask_path(question,target):
    temp_val = raw_input(question + target+", Enter different path or blank :")

    if temp_val.strip() == "":
        temp_val = target
        return temp_val

    while temp_val != "":
    # Check to see that that path exists
        if os.exists(temp_val) and os.isdir(tmp_val) :
            return temp_val
        else :
            print("\n" + str(temp_val) + " does not exist or not a directory")
            temp_val= raw_input("Please enter a different path or blank to use the default path: ")
    return target

global ask_file
## get optional answer
def ask_file(question,target):
    temp_val = raw_input(question + target+", Enter different file or blank :")

    if temp_val.strip() == "":
        temp_val = target
        return temp_val

    while temp_val != "":
    # Check to see that that file exists
        if os.exists(temp_val) and os.isfile(tmp_val) :
            return temp_val
        else :
            print("\n" + str(temp_val) + " does not exist or not a file")
            temp_val= raw_input("Please enter a different file or blank to use the default file: ")
    return target


## Gets the options and assigns them to the correct variables.
#
#"option short-form, optionlong-form, optional": "meta variable"
#{"b,bottomleft":"lat1,lon1", \
# "u,upperright":"lat2,lon2", \
# ...
# "t,title,o":"title", \
# "H,help,o":"" })
#
global get_user_opts
def get_user_opts(options):
        
    short_opt_string = ""
    long_opts = []
    opts_left = []
    opts_opt = []
    optional_opts = []
    ret_val = {}

    for key, value in options.items():
        items=key.split(",")
        short_opt_string = short_opt_string + items[0] 
        if value != "" :
            short_opt_string = short_opt_string + ":"
        long_opts.append(items[1])
        opts_left.append(items[0])
        if len(items) > 2 and items[2] != None  and items[2] =='o' :
            optional_opts.append(key.split(",")[0])

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opt_string, long_opts)
    except getopt.GetoptError as err:
        print(str(err))   
        exit(1)

    if len(opts) == 0 :
        return {}

    for o, a in opts:
## special case
        if o == "-H" or o == "--help" :
            return "help"
        if o == "-S" or o == "--skip" :
            ret_val['skip'] = '1'
            continue
## regular case
        for key, value in options.items():
            if o == "-" + key.split(",")[0] or o == "--" + key.split(",")[1]:
                opts_left.remove(key.split(",")[0])
                if "," in value:
                    vlist=value.split(",")
                    alist=a.split(",")
                    sz=len(vlist) 
                    for i in range(0, sz):
                      ret_val[vlist[i]] = alist[i]
                else:
                    ret_val[value] = a
                break

    for l in opts_left :
        if l in optional_opts :
          opts_opt.append(l)

    if len(opts_left) == 0 or len(opts_left) == len(opts_opt):
        return ret_val
    else: 
        return "bad"


#  Function Definitions
##
#  Displays an error message and exits the program.
#  @param message The error message to be displayed.
def pycvm_display_error(message):
    print("An error has occurred while executing this script. The error was:\n")
    print(message)
    print("\nPlease contact software@scec.org and describe both the error and a bit")
    print("about the computer you are running CVM-S5 on (Linux, Mac, etc.).")
    exit(0)
    
##
#  Returns true if value is a number. False otherwise.
#
#  @param value The value to test if numeric or not.
#  @return True if it is a number, false if not.
def pycvm_is_num(value):
    try:
        float(value)
        return True
    except Exception:
        return False
