##
#  @file PLOT.py
#  @brief Functions for making plots using matplotlib and basemap
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 
#
#  Provides functions used by  plotting scripts. 

#  Imports
from subprocess import call, Popen, PIPE, STDOUT
import sys
import os
import multiprocessing
import math
import struct
import getopt
import json

#  Numpy is required.
try:
    import numpy as np
except:
    print("ERROR: NumPy must be installed on your system in order to generate these plots.")
    exit(1)
    
#  Matplotlib is required.
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import matplotlib.cm as cm
except:
    print("ERROR: Matplotlib must be installed on your system in order to generate these plots.")
    exit(1)    

#  Basemap is required.
try:
    from mpl_toolkits import basemap
except Exception as e:
    print("ERROR: Basemap must be installed on your system in order to generate these plots.")
    print(e)
    exit(1)

#  Constants

## Constant for all material properties.
ALL_PROPERTIES = ["vp", "vs", "density"]
## Constant for just Vs.
VS = ["vs"]
## Constant for just Vp.
VP = ["vp"]
## Constant for just density.
DENSITY = ["density"]

## Version string.
VERSION = "19.4.0"

#  Class Definitions

##
#  @class Plot
#  @brief Returns a basic plot given a set of parameters.
#
#  This forms the basis for generating a plot using this suite of tools.
#  It returns a Matplotlib plot with certain parameters already set up.
class Plot:
    
    ##
    #  Initializes the Plot with a set of basic parameters. Use the
    #  addsubplot() method to add a sub-plot to the plot.
    #
    #  @param title The title for the plot.
    #  @param xlabel The label to be displayed on the x-axis.
    #  @param ylabel The label for the y-axis.
    #  @param legend A legend to be displayed on the lower left of the plot.
    #  @param width The width of the plot in inches (dpi = 100).
    #  @param height The height of the plot in inches (dpi = 100).
    def __init__(self, title = None, xlabel = None, ylabel = None, legend = None, width = 10, height = 10):
        ## Defines the figure and plot object to which we can add subplots.

        self.figure = plt.figure(figsize=(width, height), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)

        if ylabel != None:
            plt.ylabel(ylabel, fontsize=14)
        
        if xlabel != None:
            plt.xlabel(xlabel, fontsize=14)  
        
        if title != None:
            plt.title(title)
        
        if legend != None:
            plt.legend(legend, loc='lower left')
            
        ## Internal counter for how many subplots we have.
        self.subplotcounter = 1
            
    ##
    #  Adds a subplot to the figure and returns it.
    # 
    #  @return The subplot that has been added to the already generated plot.
    def addsubplot(self):
        self.subplotcounter += 1;
        return self.plot;

    ## 
    #  Shows the plot.
    def show(self):
        plt.show()
        
    ##
    #  Saves the figure to disk.
    #
    #  @param filename The name fo the file to save.
    def savefig(self, filename):
        plt.savefig(filename)

## MEI ToDO
    def savehtml(self, filename):
        import mpld3
#        mpld3.save_html(self.figure,filename)
#        mpld3.save_json(self.figure, filename)
        mpld3.fig_to_dict(self.figure)

