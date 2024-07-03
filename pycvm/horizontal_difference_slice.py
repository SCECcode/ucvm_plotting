##
#  @file horizontal_difference_slice.py
#  @brief Take 2 slices of horizontal slice values, plot a difference plot
#  @author Mei-Hui Su - SCEC
#  @version 
#
#  Imports
from .horizontal_slice import HorizontalSlice
from .common import Point, MaterialProperties, UCVM, UCVM_CVMS, \
                   math, pycvm_cmapDiscretize, cm, mcolors, basemap, np, plt

##
#  @class HorizontalDifferencSlice
#  @brief Gets 2 horizontal slice and make a difference plot
#
#  Retrieves 2 horizontal slices and make a difference plot 
class HorizontalDifferenceSlice(HorizontalSlice):
    
    ##
    #  Initializes the super class and copies the parameters over.
    #
    #  @param upperleftpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param bottomrightpoint The @link common.Point ending point @endlink at which this plot should end.
    #  @param spacing The spacing, in degrees, for this plot. 
    #  @param cvm The community velocity model from which this data should come.
    #  
    def __init__(self, upperleftpoint, bottomrightpoint, meta={}):
    
        #  Initializes the base class which is a horizontal slice.
        HorizontalSlice.__init__(self, upperleftpoint, bottomrightpoint, meta)

        if 'datafile1' in self.meta :
            self.datafile1 = self.meta['datafile1']
        else:
            self.datafile1 = None

        if 'datafile2' in self.meta :
            self.datafile2 = self.meta['datafile2']
        else:
            self.datafile2 = None

        if 'debug' in self.meta :
            self.debug = self.meta['debug']
        else:
            self.debug = None
    
    
    ##
    #  Retrieves the values for this horizontal slice and stores them in the class.
    def getplotvals(self, property="vs") :
        
        #  How many y and x values will we need?
        
        ## The plot width - needs to be stored as property for the plot function to work.
        self.plot_width  = self.bottomrightpoint.longitude - self.upperleftpoint.longitude
        ## The plot height - needs to be stored as a property for the plot function to work.
        self.plot_height = self.upperleftpoint.latitude - self.bottomrightpoint.latitude 
        ## The number of x points we retrieved. Stored as a property for the plot function to work.
        if ( self.xsteps ):
           self.num_x = int(self.xsteps)
        else :
           self.num_x = int(math.ceil(self.plot_width / self.spacing)) + 1
        ## The number of y points we retrieved. Stored as a property for the plot function to work.
        if ( self.ysteps ) :
           self.num_y = int(self.ysteps)  
        else :
           self.num_y = int(math.ceil(self.plot_height / self.spacing)) + 1
        
        ## The 2D array of retrieved values.
        self.materialproperties = [[MaterialProperties(-1, -1, -1) for x in range(self.num_x)] for x in range(self.num_y)] 
        
        u = UCVM(install_dir=self.installdir, config_file=self.configfile)

        ### should be 2 datafiles
        if (self.datafile1 == None or self.datafile2 == None) :
            print("Require 2 data files to make a difference plot")
            return False
        else:
            print("\nUsing --> "+self.datafile1)
            # print("expecting x ",self.num_x," y ",self.num_y)
            dataA=[]
            if self.datafile1.rfind(".binary") != -1 :
                dataA = u.import_binary(self.datafile1, self.num_x, self.num_y)
            else :
                if self.datafile1.rfind(".raw") != -1 :
                    dataA = u.import_raw_data(self.datafile1, self.num_x, self.num_y)
                else:  ## with .bin file
                    dataA2d = u.import_np_float_array(self.datafile1, self.num_x, self.num_y)
                       ## flatten them
                    dataA1d = dataA2d.reshape([1, self.num_x * self.num_y])
                       ## turn first one into a list
                    dataA=dataA1d[0].tolist()

            print("\nUsing --> "+self.datafile2)
            dataB=[]
            if self.datafile2.rfind(".binary") != -1 :
                dataB = u.import_binary(self.datafile2, self.num_x, self.num_y)
            else :
                if self.datafile2.rfind(".raw") != -1 :
                    dataB = u.import_raw_data(self.datafile2, self.num_x, self.num_y)
                else:  ## with .bin file
                    dataB2d = u.import_np_float_array(self.datafile2, self.num_x, self.num_y)
                       ## flatten them
                    dataB1d = dataB2d.reshape([1, self.num_x * self.num_y])
                       ## turn first one into a list
                    dataB=dataB1d[0].tolist()

        i = 0
        j = 0

        collect_text=""
        collect_points=""
        collect_cnt=0
        collect_less=0
        max_less = 0.0
        max_less_i=0
        max_less_j=0
        collect_more=0
        collect_zero=0

        i_list=""
        j_list=""
        A_list=""
        B_list=""
        diff_list=""

        for idx in range(len(dataA)) :
            tmp = dataA[idx]-dataB[idx]
            self.materialproperties[i][j].vs = tmp

            if(tmp < 0.0) :
               collect_less += 1
               if(tmp < max_less):
                 max_less = tmp
                 max_less_i = i
                 max_less_j = j
               if( collect_cnt == 0 ) : 
                 i_list += "%d" %i
                 j_list += "%d" %j
                 A_list += "%0.4f" %dataA[idx] 
                 B_list += "%0.4f" %dataB[idx] 
                 diff_list += "%0.4f" %tmp
               else:
                 i_list += ",%d" %i
                 j_list += ",%d" %j
                 A_list += ",%0.4f" %dataA[idx] 
                 B_list += ",%0.4f" %dataB[idx] 
                 diff_list += ",%0.4f" %tmp
               collect_cnt += 1 
            elif ( tmp > 0.0 ) :
               collect_more += 1
            else :
               collect_zero += 1

            j = j + 1
            if j >= self.num_x:
                j = 0
                i = i + 1

        if(self.debug != None) :
          collect_text= "{ \"max_j\": %d, \"max_i\": %d, \"max_less\":%0.5f, \"max_less_i\":%d, \"max_less_j\":%d, \"less\":%d, \"more\":%d, \"zero\":%d,\n" % (self.num_x, self.num_y, max_less, max_less_i, max_less_j, collect_less, collect_more, collect_zero)
          collect_text += " \"A\":[ %s ], \"B\": [ %s ], \"D\": [ %s ], \n" % (A_list,B_list, diff_list)
          collect_text += " \"i\":[ %s ], \"j\": [ %s ] }\n" % (i_list,j_list)
          fp = open(self.debug, 'w')
          fp.write(collect_text);
          fp.close()

    ##
    #  Plots the Difference data as a horizontal slice. This code is very similar to the
    #  HorizontalSlice routine.
    #
    #  @param filename The location to which the plot should be saved. Optional.
    #  @param title The title of the plot to use. Optional.
    #  @param color_scale The color scale to use for the plot. Optional.
    def plot(self) :
 
        if self.upperleftpoint.description == None:
            location_text = ""
        else:
            location_text = self.upperleftpoint.description + " "

        # Gets the better CVM description if it exists.
        try:
            cvmdesc = UCVM_CVMS[self.cvm]
        except: 
            cvmdesc = self.cvm
        
        if 'title' not in self.meta:
            title = "%sHorizontal Difference Plot For %s" % (location_text, cvmdesc)
            self.meta['title'] = title

        self.meta['mproperty']="vs"
        self.meta['difference']="vs"

        HorizontalSlice.plot(self)
