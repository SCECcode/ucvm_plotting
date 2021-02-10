#!/bin/bash

source $UCVM_INSTALL_PATH/conf/ucvm_env.sh

tmp=`uname -s`

./unpack-dist

which ucvm_query 
ucvm_query -H
