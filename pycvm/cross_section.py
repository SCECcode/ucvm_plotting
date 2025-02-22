##
#  @file cross_section.py
#  @brief Plots a cross section to an image or a pre-existing plot.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Allows for generation of a cross section between two points.

#  Imports

from mpl_toolkits import basemap
#XXX from mpl_toolkits.basemap import cm
from matplotlib import cm

from common import Plot, Point, MaterialProperties, UCVM, UCVM_CVMS, \
                   math, pycvm_cmapDiscretize, cm, mcolors, np, plt

import random
import string

try:
    import pyproj
except Exception:
    print("ERROR: PyProj must be installed for this script to work.")
    exit(1)

##
#  @class CrossSection
#  @brief Plots a cross section between two @link common.Point Points @endlink.
#
#  Generates a cross section that can either be saved as a file or displayed
#  to the user or differenced with another plot. 
class CrossSection:
    
    ##
    #  Initializes the cross section class.
    #
    #  @param startingpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param endingpoint The @link common.Point ending point @endlink at which this plot will end.
    #  @param meta Metadata
    def __init__(self, startingpoint, endingpoint, meta={}):

        self.meta = meta

        if not isinstance(startingpoint, Point):
            raise TypeError("The starting point must be an instance of Point.")
        else:
            ## Defines the @link common.Point starting point @endlink for the cross section.
            self.startingpoint = startingpoint
            
        if not isinstance(endingpoint, Point):
            raise TypeError("The ending point must be an instance of Point.")
        else:
            ## Defines the @link common.Point ending point @endlink for the cross section.
            self.endingpoint = endingpoint

 
        ## The discretization of the plot, in meters.
        if 'vertical_spacing' in self.meta :
            self.vspacing = float(self.meta['vertical_spacing'])
        else:
            self.vspacing = 0 
 
        if 'horizontal_spacing' in self.meta :
            self.hspacing = float(self.meta['horizontal_spacing'])
        else:
            self.hspacing = 0 

        if 'ending_depth' in self.meta :
            self.todepth = float(self.meta['ending_depth'])
        else:
            self.todepth = 50000 

        if (self.todepth - self.startingpoint.depth) % self.vspacing != 0:
            raise ValueError("%s\n%s\n%s" % ("The spacing value does not divide evenly into the requested depth. ", \
                          "Please make sure that the depth (%.2f - %.2f) divided by the spacing " % (self.todepth, startingpoint.depth), \
                          "%.2f has no remainder" % (self.vspacing)))
        else:
            ## Defines the depth to which the plot should go in meters.
            self.startingdepth=self.startingpoint.depth

        self.z_range = None
        if 'zrange1' in self.meta and 'zrange2' in self.meta :
            self.z_range=self.meta['zrange1']+","+self.meta['zrange2']

        self.floors = None
        if 'vsfloor' in self.meta and 'vpfloor' in self.meta and 'densityfloor' in self.meta :
            self.floors=self.meta['vsfloor']+","+self.meta['vpfloor']+","+self.meta['densityfloor']

        if 'scalemin' in self.meta and 'scalemax' in self.meta :
            ## user supplied a fixed scale bounds
            self.scalemin=float(self.meta['scalemin'])
            self.scalemax=float(self.meta['scalemax'])
        else:
            self.scalemin=None
            self.scalemax=None

        ## The CVM to use (must be installed with UCVM).
        if 'cvm' in self.meta :
            self.cvm = self.meta['cvm']
        else:
            self.cvm = None

        if 'datafile' in self.meta :
            self.datafile = self.meta['datafile']
        else:
            self.datafile = None

        if 'outfile' in self.meta:
            self.filename = self.meta['outfile']
        else:
            self.filename = None


    ## 
    #  Generates the depth profile in a format that is ready to plot.
    def getplotvals(self, mproperty='vs'):

        point_list = []
        lon_list = []
        lat_list = []
        depth_list = []

        proj = pyproj.Proj(proj='utm', zone=11, ellps='WGS84')

        x1, y1 = proj(self.startingpoint.longitude, self.startingpoint.latitude)
        x2, y2 = proj(self.endingpoint.longitude, self.endingpoint.latitude)

        num_prof = int(math.sqrt((x2-x1)*(x2-x1) + \
                                 (y2-y1)*(y2-y1))/self.hspacing)
        
#        cnt=0
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
#                if(cnt < 10) :
#                   print("point.. lon "+str(lon)+" lat "+str(lat)+" j "+str(j))
#                   cnt += 1
                
        self.lon_list=lon_list
        self.lat_list=lat_list
        self.depth_list=depth_list
#        print("total points generated.."+str(len(point_list)))
#        print("total lon.."+ str(len(lon_list)))
#        print("total lat.."+ str(len(lat_list)))
#        print("total lat.."+ str(len(depth_list)))

        u = UCVM(install_dir=self.installdir, config_file=self.configfile, z_range=self.z_range, floors=self.floors)
### MEI -- TODO, need to have separate routine that generates cross section datafile
        if (self.datafile != None) :
            ## Private number of x points.
            self.num_x = num_prof +1
            ## Private number of y points.
            self.num_y = (int(self.todepth) - int(self.startingdepth)) / int(self.vspacing) +1
            print("\nUsing -->"+self.datafile)
##            print("expecting x "+str(self.num_x)+" y "+str(self.num_y))


            if self.datafile.rfind(".binary") != -1 :
                data = u.import_binary(self.datafile, self.num_x, self.num_y)
            else :
                if self.datafile.rfind(".raw") != -1 :
                    data = u.import_raw_data(self.datafile, self.num_x, self.num_y)
                else:  ## with .bin file
                    data = u.import_np_float_array(self.datafile, self.num_x, self.num_y)

## this set of data is only for --datatype: either 'vs', 'vp', 'rho', or 'poisson'
        ## The 2D array of retrieved material properties.
            self.materialproperties = [[MaterialProperties(-1, -1, -1) for x in range(self.num_x)] for x in range(self.num_y)] 
            datapoints = data.reshape(self.num_y, self.num_x)

            for y in range(0, self.num_y):
                for x in range(0, self.num_x):   
                    tmp=datapoints[y][x]
                    if(mproperty == 'vp'):
                      self.materialproperties[y][x].setProperty('Vp',tmp)
                    if(mproperty == 'density'):
                      self.materialproperties[y][x].setProperty('Density',tmp)
                    if(mproperty == 'poisson'):
                      self.materialproperties[y][x].setProperty('Poisson',tmp)
                    if(mproperty == 'vs'):
                      self.materialproperties[y][x].setProperty('Vs',tmp)

            print("\nUsing --> "+self.datafile) 
        else:
            data = u.query(point_list, self.cvm)


            ## Private number of x points.
            self.num_x = num_prof + 1
            ## Private number of y points.
            self.num_y = (int(self.todepth) - int(self.startingdepth)) / int(self.vspacing) + 1
        
        ## The 2D array of retrieved material properties.
            self.materialproperties = [[MaterialProperties(-1, -1, -1) for x in range(self.num_x)] for x in range(self.num_y)] 

        
            for y in range(0, self.num_y):
                for x in range(0, self.num_x):   
                    self.materialproperties[y][x] = data[y * self.num_x + x]     
    ## 
    #  Plots the horizontal slice either to an image or a file name.
    # 
    def plot(self) :

        self.installdir = None
        if 'installdir' in self.meta :
           self.installdir = self.meta['installdir']

        self.configfile = None
        if 'configfile' in self.meta :
           self.configfile = self.meta['configfile']

        if 'color' in self.meta :
           color_scale = self.meta['color']

        scale_gate = None
        if 'gate' in self.meta :
           scale_gate = float(self.meta['gate'])

        if color_scale == "b" and scale_gate is None:
           scale_gate=2.5
        
        if self.startingpoint.description == None:
            location_text = ""
        else:
            location_text = self.startingpoint.description + " "

        if 'data_type' in self.meta :
           mproperty = self.meta['data_type']
        else:
           mproperty = "vs"

        # Gets the better CVM description if it exists.
        try:
            cvmdesc = UCVM_CVMS[self.cvm]
        except: 
            cvmdesc = self.cvm

        if 'title' in self.meta :
            title = self.meta['title']
        else:
            title = "%s%s Cross Section from (%.2f, %.2f) to (%.2f, %.2f)" % (location_text, cvmdesc, self.startingpoint.longitude, \
                        self.startingpoint.latitude, self.endingpoint.longitude, self.endingpoint.latitude)
            self.meta['title']=title
            
        self.getplotvals(mproperty)
        
        # Call the plot object.
        p = Plot(None, None, None, None, 10, 10)

        plt.axes([0.1,0.7,0.8,0.25])
    
        # Figure out which is upper-right and bottom-left.
        ur_lat = self.startingpoint.latitude if self.startingpoint.latitude > self.endingpoint.latitude else self.endingpoint.latitude
        ur_lon = self.startingpoint.longitude if self.startingpoint.longitude > self.endingpoint.longitude else self.endingpoint.longitude
        ll_lat = self.startingpoint.latitude if self.startingpoint.latitude < self.endingpoint.latitude else self.endingpoint.latitude
        ll_lon = self.startingpoint.longitude if self.startingpoint.longitude < self.endingpoint.longitude else self.endingpoint.longitude
    
        # Add 1% to each for good measure.
        ur_lat = ur_lat + 0.03 * ur_lat
        ur_lon = ur_lon - 0.015 * ur_lon
        ll_lat = ll_lat - 0.03 * ll_lat
        ll_lon = ll_lon + 0.015 * ll_lon
    
        # Plot map up top.
        m = basemap.Basemap(projection='cyl', llcrnrlat=ll_lat, urcrnrlat=ur_lat, \
                            llcrnrlon=ll_lon, urcrnrlon=ur_lon, \
                            resolution='f', anchor='C')
    
        lat_ticks = np.arange(ll_lat, ur_lat + 0.1, (ur_lat - ll_lat))
        lon_ticks = np.arange(ll_lon, ur_lon + 0.1, (ur_lon - ll_lon))
    
        m.drawparallels(lat_ticks, linewidth=1.0, labels=[1,0,0,0])
        m.drawmeridians(lon_ticks, linewidth=1.0, labels=[0,0,0,1])
        m.drawstates()
        m.drawcountries()
    
        m.drawcoastlines()
        m.drawmapboundary(fill_color='aqua')
        m.fillcontinents(color='brown',lake_color='aqua')
    
        m.plot([self.startingpoint.longitude,self.endingpoint.longitude], [self.startingpoint.latitude,self.endingpoint.latitude])
    
        valign1 = "top"
        valign2 = "bottom"
        if self.endingpoint.latitude < self.startingpoint.latitude:
            valign1 = "bottom"
            valign2 = "top"
    
        plt.text(self.startingpoint.longitude, self.startingpoint.latitude, \
                 '[S] %.1f, %.1f' % (self.startingpoint.longitude, self.startingpoint.latitude), \
                 color='k', horizontalalignment="center", verticalalignment=valign1)
    
        plt.text(self.endingpoint.longitude, self.endingpoint.latitude, \
                 '[E] %.1f, %.1f' % (self.endingpoint.longitude, self.endingpoint.latitude), \
                 color='k', horizontalalignment="center", verticalalignment=valign2)
    
        plt.axes([0.05,0.18,0.9,0.54])
    
        datapoints = np.arange(self.num_x * self.num_y,dtype=np.float32).reshape(self.num_y, self.num_x)
            

        for y in range(0, self.num_y):
            for x in range(0, self.num_x):
                if self.datafile != None : 
                    datapoints[y][x] = self.materialproperties[y][x].getProperty(mproperty)
                elif mproperty != "poisson" :
                    datapoints[y][x] = self.materialproperties[y][x].getProperty(mproperty)
                else:
                    datapoints[y][x] = u.poisson(self.materialproperties[y][x].getProperty("vs"), self.materialproperties[y][x].getProperty("vp")) 


        u = UCVM(install_dir=self.installdir, config_file=self.configfile)

        myInt=1000
        if mproperty == "poisson": ## no need to reduce.. should also be using sd or dd
           myInt=1
           if color_scale == "s" :
               color_scale = "sd"
           elif color_scale == "d" :
               color_scale = "dd"

        newdatapoints=datapoints/myInt

        self.max_val=np.nanmax(newdatapoints)
        self.min_val=np.nanmin(newdatapoints)
        self.mean_val=np.mean(newdatapoints)

        # Set colormap and range
        colormap = basemap.cm.GMT_seis

        if self.scalemin != None and self.scalemax != None:
            BOUNDS= u.makebounds(float(self.scalemin), float(self.scalemax), 5)
            TICKS = u.maketicks(float(self.scalemin), float(self.scalemax), 5)
            umax=round(self.scalemax)
            umin=round(self.scalemin)
            umean=round((umax+umin)/2)
        else:
            ## default BOUNDS are from 0 to 5
            BOUNDS = u.makebounds()
            TICKS = u.maketicks()
            umax=round(self.max_val)
            umin=round(self.min_val)
            umean=round(self.mean_val)

        if mproperty == "vp":
            BOUNDS = [bound * 1.7 for bound in BOUNDS]
            TICKS = [tick * 1.7 for tick in TICKS]

##   s, s_r   0,5 / scalemin,scalemax  
##   sd       umin,umax
##   b        0,5 / scalemin,scalemax
##   d, d_r   0,5 / scalemin,scalemax
##   dd       umin,umax
        if color_scale == "s":
            colormap = basemap.cm.GMT_seis
            norm = mcolors.Normalize(vmin=BOUNDS[0],vmax=BOUNDS[len(BOUNDS) - 1])
        elif color_scale == "s_r":
            colormap = basemap.cm.GMT_seis_r
            norm = mcolors.Normalize(vmin=BOUNDS[0],vmax=BOUNDS[len(BOUNDS) - 1])
        elif color_scale == "sd":
            colormap = basemap.cm.GMT_seis
            BOUNDS= u.makebounds(umin, umax, 5, umean, substep=5)
            TICKS = u.maketicks(umin, umax, 5)
            norm = mcolors.Normalize(vmin=BOUNDS[0],vmax=BOUNDS[len(BOUNDS) - 1])
        elif color_scale == "b":
            C = []
            for bound in BOUNDS :
               if bound < scale_gate :
                  C.append("grey")
               else:
                  C.append("red")
            colormap = mcolors.ListedColormap(C)
            norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)
        elif color_scale == 'd':
            colormap = pycvm_cmapDiscretize(basemap.cm.GMT_seis, len(BOUNDS) - 1)
            norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)  
        elif color_scale == 'd_r':
            colormap = pycvm_cmapDiscretize(basemap.cm.GMT_seis_r, len(BOUNDS) - 1)
            norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)  
        elif color_scale == 'dd':
            BOUNDS= u.makebounds(umin, umax, 5, umean, substep=5)
            TICKS = u.maketicks(umin, umax, 5)
            colormap = pycvm_cmapDiscretize(basemap.cm.GMT_seis, len(BOUNDS) - 1)
            norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)
        else: 
            print("ERROR: unknown option for colorscale.")

        if 'difference' in self.meta :
            bwr = cm.get_cmap('bwr')
            colormap = pycvm_cmapDiscretize(bwr, len(BOUNDS) - 1)


## MEI, TODO this is a temporary way to generate an output of a cross_section input file
        if( self.datafile == None ):
          self.meta['num_x'] = self.num_x
          self.meta['num_y'] = self.num_y
          self.meta['datapoints'] = datapoints.size
          self.meta['max'] = self.max_val.item()
          self.meta['min'] = self.min_val.item()
          self.meta['mean'] = self.mean_val.item()
          self.meta['lon_list'] = self.lon_list
          self.meta['lat_list'] = self.lat_list
          self.meta['depth_list'] = self.depth_list
          if self.filename:
              u.export_metadata(self.meta,self.filename)
              u.export_np_float_array(datapoints,self.filename)
          else:
#https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
              rnd=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
              f = "cross_section"+rnd
              u.export_metadata(self.meta,f)
              u.export_np_float_array(datapoints,f)


        img = plt.imshow(newdatapoints, cmap=colormap, norm=norm)
        plt.xticks([0,self.num_x/2,self.num_x], ["[S] %.3f" % self.startingpoint.longitude, \
                                                 "%.3f" % ((float(self.endingpoint.longitude) + float(self.startingpoint.longitude)) / 2), \
                                                 "[E] %.3f" % self.endingpoint.longitude])
        plt.yticks([0,self.num_y/2,self.num_y], ["%.2f" % (self.startingdepth/1000), \
                                                 "%.2f" % (self.startingdepth+ ((self.todepth-self.startingdepth)/2)/1000), \
                                                 "%.2f" % (self.todepth / 1000)])
    
        plt.title(title)
    
        cax = plt.axes([0.1, 0.1, 0.8, 0.02])
        cbar = plt.colorbar(img, cax=cax, orientation='horizontal',ticks=TICKS,spacing='regular')
        if mproperty != "poisson":
            if(mproperty.title() == "Density") :
              cbar.set_label(mproperty.title() + " (g/cm^3)")
            else:
              if 'difference' in self.meta :
                    cbar.set_label(mproperty.title() + " (km)")
              else:
                   cbar.set_label(mproperty.title() + " (km/s)")
        else:
            cbar.set_label("Poisson(Vs,Vp)")
       
        if self.filename:
            plt.savefig(self.filename)
        else:
            plt.show() 
