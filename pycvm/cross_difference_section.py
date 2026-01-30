##
#  @file cross_difference_section.py
#  @brief Take 2 slices of cross sections, plot a difference plot
#  @author Mei-Hui Su - SCEC
#  @version 
#
#  Imports
from .cross_section import CrossSection
from .cvm_ucvm import Point, MaterialProperties, UCVM, UCVM_CVMS
from .cvm_plot import Plot, math, plot_cmapDiscretize, cm, mcolors, basemap, plt, np
from .cvm_common import VERSION
import math
import pdb

try:
    import pyproj
except Exception:
    print("ERROR: PyProj must be installed for this script to work.")
    exit(1)

##
#  @class CrossDifferencSection
#  @brief Gets 2 cross section and make a difference plot
#
#  Retrieves 2 cross sections and make a difference plot 
class CrossDifferenceSection(CrossSection):
    
    ##
    #  Initializes the super class and copies the parameters over.
    #
    #  @param startingpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param endingpoint The @link common.Point ending point @endlink at which this plot will end.
    #  @param meta Metadata
    def __init__(self, startingpoint, endingpoint, meta={}):
    
        if 'cvm1' in meta and 'cvm2' in meta :
          meta['cvm'] = meta['cvm1'] + ',' + meta['cvm2']

        if 'title' not in meta :
          title = "%s Cross Section Difference Plot from (%.2f, %.2f) to (%.2f, %.2f)" % \
                  (meta['cvm'], startingpoint.longitude, startingpoint.latitude, \
                  endingpoint.longitude, endingpoint.latitude)
          meta['title'] = title

        #  Initializes the base class which is a cross section.
        CrossSection.__init__(self, startingpoint, endingpoint, meta)

        if 'datafile1' in self.meta :
            self.datafile1 = self.meta['datafile1']
        else:
            self.datafile1 = None

        if 'datafile2' in self.meta :
            self.datafile2 = self.meta['datafile2']
        else:
            self.datafile2 = None

        ## The number of points we retrieved. Stored as a property for the plot function to work.
        # How many y and x values will we need?
        self.num_x  = int(self.meta['num_x'])
        self.num_y = int(self.meta['num_y'])
    
    ##
    #  Retrieves the values for this cross section and stores them in the class.
    def getplotvals(self, property="vs") :

        point_list = []
        lon_list = []
        lat_list = []
        depth_list = []

        proj = pyproj.Proj(proj='utm', zone=11, ellps='WGS84')

        x1, y1 = proj(self.startingpoint.longitude, self.startingpoint.latitude)
        x2, y2 = proj(self.endingpoint.longitude, self.endingpoint.latitude)

        num_prof = int(math.sqrt((x2-x1)*(x2-x1) + \
                                 (y2-y1)*(y2-y1))/self.hspacing)
        
        ## figure out lats and lons
        jstart = self.startingdepth
        for j in range(int(self.startingdepth), int(self.todepth) + 1, int(self.vspacing)):
            depth_list.append( round(j,3))
            for i in range(0, num_prof + 1):
                x = x1 + i*(x2-x1)/float(num_prof)
                y = y1 + i*(y2-y1)/float(num_prof)
                lon, lat = proj(x, y, inverse=True)
                point_list.append(Point(lon, lat, j))
                if ( j == jstart) :
                  lon_list.append( round(lon,5))
                  lat_list.append( round(lat,5))

        self.lon_list=lon_list
        self.lat_list=lat_list
        self.depth_list=depth_list

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
            if self.datafile1.rfind(".binary") != -1 or self.datafile1.rfind(".bin") != -1 :
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
            if self.datafile2.rfind(".binary") != -1 or self.datafile2.rfind(".bin") != -1:
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
        mmax=None
        mmin=None

        for idx in range(len(dataA)) :
            dif = dataA[idx]-dataB[idx]
            self.materialproperties[i][j].vs = dif

            if mmax == None or dif > mmax :
              mmax=dif
            if mmin == None or dif < mmin :
              mmin=dif    

            j = j + 1
            if j >= self.num_x:
                j = 0
                i = i + 1

        ## DON'T Do this, user needs to make explicit request for the range
##reset the range if not set
#  if mmax > 0 and mmin < 0 and 'scalemin' not in self.meta and 'scalemax' not in self.meta :
## km
## mmid = math.ceil(max(abs(mmax/1000),abs(mmin/1000)))
## reset
## self.scalemin = -mmid
## self.scalemax = mmid
           
    ##
    #  Plots the Difference data as a cross section. This code is very similar to the
    #  CrossSection routine.
    #
    #  @param filename The location to which the plot should be saved. Optional.
    #  @param title The title of the plot to use. Optional.
    #  @param color_scale The color scale to use for the plot. Optional.
    def plot(self) :
 
        self.meta['mproperty']="vs"
        self.meta['difference']="vs"

        CrossSection.plot(self)
