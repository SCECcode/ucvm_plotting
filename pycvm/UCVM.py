##
#  @file ucvm.py
#  @brief functions for accessing UCVM installation
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version
#
#  Provides access and manipulation function to UCVM via command line

#  Imports
from subprocess import call, Popen, PIPE, STDOUT
import sys
import os
import multiprocessing
import math
import struct
import json

#  Numpy is required.
try:
    import numpy as np
except:
    print("ERROR: NumPy must be installed on your system in order to generate these plots.")
    exit(1)
    
## Known CVMs that can be installed with UCVM.
UCVM_CVMS = {"1d":"1D(1d)", \
             "1dgtl":"1D w/ Vs30 GTL(1dgtl)", \
             "bbp1d":"Broadband Northridge Region 1D Model(bbp1d)", \
             "cvms":"CVM-S4(cvms)", \
             "cvms5":"CVM-S4.26(cvms5)", \
             "cvms426":"CVM-S4.26.M01(cvmsi)", \
             "cca":"CCA 06(cca)", \
             "cs173":"CyperShake 17.3(cs173)", \
             "cs173h":"CyperShake 17.3 with San Joaquin and Santa Maria Basins data(cs173h)", \
             "cvmh1511":"CVM-H 15.1.1(cvmh)", \
             "albacore":"ALBACORE(albacore)", \
             "cencal":"USGS Bay Area Model(cencal)"}

## Constant for all material properties.
ALL_PROPERTIES = ["vp", "vs", "density"]
## Constant for just Vs.
VS = ["vs"]
## Constant for just Vp.
VP = ["vp"]
## Constant for just density.
DENSITY = ["density"]

## Version string.
VERSION = "24.1.0"

##
#  @class Point
#  @brief Defines a point in WGS84 latitude, longitude projection.
#
#  Allows for a point to be defined within the 3D earth structure.
#  It has a longitude, latitude, and depth/elevation as minimum parameters,
#  but you can specify a type, e.g. "LA Basin", and a description, 
#  e.g. "New point of interest".
class Point:
    
    ##
    #  Initializes a new point. Checks that the parameters are all valid and
    #  raises an error if they are not.
    # 
    #  @param longitude Longitude provided as a float.
    #  @param latitude Latitude provided as a float.
    #  @param depth The depth in meters with the surface being 0.
    #  @param elevation The elevation in meters.
    #  @param type The type or classification of this location. Not required.
    #  @param code A short code for the site (unique identifier). Not required.
    #  @param description A longer description of what this point represents. Not required.
    def __init__(self, longitude, latitude, depth = 0, elevation = None, type = None, code = None, description = None):
        if pycvm_is_num(longitude):
            ## Longitude as a float in WGS84 projection.
            self.longitude = longitude
        else:
            raise TypeError("Longitude must be a number")
        
        if pycvm_is_num(latitude):
            ## Latitude as a float in WGS84 projection.
            self.latitude = latitude
        else:
            raise TypeError("Latitude must be a number")

        self.elevation = None;
        if elevation != None :
            self.elevation = elevation
        
        if pycvm_is_num(depth):
            if depth >= 0:
                ## Depth in meters below the surface. Must be greater than or equal to 0.
                self.depth = depth
            else:
                raise ValueError("Depth must be positive.")
        else:
            raise TypeError("Depth must be a number.")
        
        ## A classification or short description of what this point represents. Optional.
        self.type = type
        ## A short, unique code identifying the site. Optional.
        self.code = code
        ## A longer description of what this point represents. Optional.
        self.description = description
    
    ##
    #  String representation of the point.    
    def __str__(self):
        if(self.elevation) :
            return "(%.4f, %.4f, %.4f)" % (float(self.longitude), float(self.latitude), float(self.elevation))
        else:
            return "(%.4f, %.4f, %.4f)" % (float(self.longitude), float(self.latitude), float(self.depth))

##
#  @class MaterialProperties
#  @brief Defines the possible material properties that @link UCVM UCVM @endlink can return.
#
#  Provides a class for defining the three current material properties that
#  UCVM returns and also has placeholders for Qp and Qs.
class MaterialProperties:
    
    ## 
    #  Initializes the MaterialProperties class.
    #  
    #  @param vp P-wave velocity in m/s. Must be a float.
    #  @param vs S-wave velocity in m/s. Must be a float.
    #  @param density Density in g/cm^3. Must be a float.
    #  @param poisson Poisson as a calculated float. Optional.
    #  @param qp Qp as a float. Optional.
    #  @param qs Qs as a float. Optional.
    def __init__(self, vp, vs, density, poisson = None, qp = None, qs = None):
       if pycvm_is_num(vp):
           ## P-wave velocity in m/s
           self.vp = float(vp)
       else:
           raise TypeError("Vp must be a number.")
       
       if pycvm_is_num(vs):
           ## S-wave velocity in m/s
           self.vs = float(vs)
       else:
           raise TypeError("Vs must be a number.")
       
       if pycvm_is_num(density):
           ## Density in g/cm^3
           self.density = float(density)
       else:
           raise TypeError("Density must be a number.")

       if poisson != None:
           self.poisson = float(poisson)
       else:
           self.poisson = -1
       
       if qp != None:
           ## Qp
           self.qp = float(qp)
       else:
           self.qp = -1
           
       if qs != None:
           ## Qs
           self.qs = float(qs)
       else:
           self.qs = -1
       
    ##
    #  Defines subtraction of two MaterialProperties classes.
    #
    #  @param own This MaterialProperties class.
    #  @param other The other MaterialProperties class.
    #  @return The subtracted properties.
    def __sub__(own, other):
        return MaterialProperties(own.vp - other.vp, own.vs - other.vs, own.density - other.density, \
                                  own.poisson - other.poisson, own.qp - other.qp, own.qs - other.qs)

    ##
    #  Initializes the class from a UCVM output string line.
    #
    #  @param cls Not used. Call as MaterialProperties.fromUCVMOutput(line).
    #  @param line The line containing the material properties as generated by ucvm_query.
    #  @return A constructed MaterialProperties class.
    @classmethod
    def fromUCVMOutput(cls, line):
        new_line = line.split()
        return cls(new_line[14], new_line[15], new_line[16])

    ##
    #  Initializes the class from a float list.
    #
    #  @param cls Not used. Call as MaterialProperties.fromNPFloats(flist).
    #  @param flist The flist line containing the material properties as imported from np array
    #  @return A constructed MaterialProperties class.
    @classmethod
    def fromNPFloats(cls, flist):
        vp=flist[0]
        vs=flist[1]
        density=flist[2]
        return cls(vp, vs, density)

    ##
    #  Initializes the class from a JSON  output string line.
    #
    #  @param cls Not used. Call as MaterialProperties.fromJSONOutput(jdict).
    #  @param jdict The jdict line containing the material properties as imported from file
    #  @return A constructed MaterialProperties class.
    @classmethod
    def fromJSONOutput(cls, jdict):
        vp=jdict['vp']
        vs=jdict['vs']
        density=jdict['density']
        return cls(vp, vs, density)

    ##
    #  Create a JSON output string line
    #
    #  @param depth The depth from surface.
    #  @return A JSON string
    def toJSON(self, depth):
        return "{ 'depth':%2f, 'vp':%.5f, 'vs':%.5f, 'density':%.5f }" % (depth, self.vp, self.vs, self.density)
    
    ##
    #  Retrieves the corresponding property given the property as a string.
    # 
    #  @param property The property name as a string ("vs", "vp", "density", "poisson", "qp", or "qs").
    #  @return The property value.
    def getProperty(self, property):               
        if property.lower() == "vs":
            return self.vs
        elif property.lower() == "vp":
            return self.vp
        elif property.lower() == "density":
            return self.density
        elif property.lower() == "poisson":
            return self.poisson
        elif property.lower() == "qp":
            return self.qp
        elif property.lower() == "qs":
            return self.qs
        else:
            raise ValueError("Parameter property must be a valid material property unit.")
    ##
    #  Set the corresponding property given the property as a string.
    # 
    #  @param property The property name as a string ("vs", "vp", "density", "qp", or "qs").
    #  @param val The property value.
    def setProperty(self, property, val):               
        if property.lower() == "vs":
            self.vs=val
        elif property.lower() == "vp":
            self.vp=val
        elif property.lower() == "density":
            self.density=val
        elif property.lower() == "poisson":
            self.poisson=val
        elif property.lower() == "qp":
            self.qp=val
        elif property.lower() == "qs":
            self.qs=val
        else:
            raise ValueError("Parameter property must be a valid material property unit.")
        
    ##
    #  String representation of the material properties.
    def __str__(self):
        return "Vp: %.2fm/s, Vs: %.2fm/s, Density: %.2fg/cm^3" % (self.vp, self.vs, self.density)
 
##
#  @class UCVM
#  @brief Python functions to interact with the underlying C code.
#
#  Provides a Python mechanism for calling the underlying C programs and
#  getting their output in a format that is readily and easily interpreted
#  by other classes.
class UCVM:
    
    ##
    #  Initializes the UCVM class and reads in all the available models that have
    #  been installed.
    #  
    #  @param install_dir The base installation directory of UCVM.
    #  @param config_file The location of the UCVM configuration file.
    def __init__(self, install_dir = None, config_file = None, z_range = None, floors = None):
        if install_dir != None:
            ## Location of the UCVM binary directory.
            self.binary_dir = install_dir + "/bin"
            self.utility_dir = install_dir + "/utilities"
        elif 'UCVM_INSTALL_PATH' in os.environ:
            mypath=os.environ.get('UCVM_INSTALL_PATH')
            self.binary_dir = mypath+"/bin"
            self.utility_dir = mypath+"/utilities"
        else:
            self.binary_dir = "../bin"
            self.utility_dir = "../utilities"
        
        if config_file != None:
            ## Location of the UCVM configuration file.
            self.config = config_file
        else:
            if install_dir != None:
               self.config = install_dir + "/conf/ucvm.conf"
            elif 'UCVM_INSTALL_PATH' in os.environ:
               mypath=os.environ.get('UCVM_INSTALL_PATH')
               self.config = mypath+"/conf/ucvm.conf"
            else:
               self.config = "../conf/ucvm.conf"

        if z_range != None:
            self.z_range = z_range
        else:
            self.z_range= None

        if floors != None:
            self.floors = floors
        else:
            self.floors= None
        
        
        if install_dir != None:
            ## List of all the installed CVMs.
            self.models = [x for x in os.listdir(install_dir + "/model")]
        elif 'UCVM_INSTALL_PATH' in os.environ:
            mypath=os.environ.get('UCVM_INSTALL_PATH')
            self.models = [x for x in os.listdir(mypath + "/model")]
        else:
            self.models = [x for x in os.listdir("../model")]
            
        self.models.remove("ucvm")

    ##
    #  Given raw UCVM result
    #   this function will throw an an error: missing model or invalid data etc
    #   by checking if first 'item' is float or not
    #
    #  @param raw An array of output material properties
    def checkUCVMoutput(self,idx,rawoutput):
        output = rawoutput.split("\n")[idx:-1]
        if len(output) > 1:
            line = output[0]
            if ("WARNING" in line) or ("slow performance" in line) or ("Using Geo" in line):
                return output
            p=line.split()[0]
            try :
                f=float(p)
            except :
                print("ERROR: "+str(line))
                exit(1)
           
        return output

    ##
    #  Queries UCVM given a set of points and a CVM to query. If the CVM does not exist,
    #  this function will throw an error. The set of points must be an array of the 
    #  @link Point Point @endlink class. This function returns an array of @link MaterialProperties
    #  MaterialProperties @endlink.
    #
    #  @param point_list An array of @link Point Points @endlink for which UCVM should query.
    #  @param cvm The CVM from which this data should be retrieved.
    #  @return An array of @link MaterialProperties @endlink.
    def query(self, point_list, cvm, elevation = None):
        shared_object = "../model/" + cvm + "/lib/lib" + cvm + ".so"
        properties = []
        
        # Can we load this library dynamically and bypass the C code entirely?
        if os.path.isfile(shared_object):
            import ctypes
            #obj = ctypes.cdll.LoadLibrary(shared_object)
            #print(obj)
        
#        print("CVM", cvm)
        if( elevation ) :
            if self.z_range != None :
                if self.floors != None:
                  proc = Popen([self.utility_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "ge", "-z", self.z_range, "-L", self.floors], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
                else:
                  proc = Popen([self.utility_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "ge", "-z", self.z_range], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
            else :
                if self.floors != None:  ## z range is using default
                  proc = Popen([self.utility_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "ge", "-L", self.floors], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
                else:
                  proc = Popen([self.utility_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "ge"], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
        else :
            if self.z_range != None :
                if self.floors != None :
                  proc = Popen([self.utility_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "gd", "-z", self.z_range, "-L", self.floors], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
                else:
                  proc = Popen([self.utility_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "gd", "-z", self.z_range], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
            else:
                if self.floors != None:  ## z range is using default

                  proc = Popen([self.utility_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "gd", "-L", self.floors ], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
                else:
                  proc = Popen([self.utility_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "gd" ], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')

        
        text_points = ""
        
        if isinstance(point_list, Point):
            point_list = [point_list]
         
        for point in point_list:
            if( elevation ) :
              text_points += "%.5f %.5f %.5f\n" % (point.longitude, point.latitude, point.elevation)
            else:
              text_points += "%.5f %.5f %.5f\n" % (point.longitude, point.latitude, point.depth)

#       fp = open("input_points", 'w') 
#       fp.write(text_points);
#       fp.close()

        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(1,output)

        for line in output:
# it is material properties.. line
            try :
              mp = MaterialProperties.fromUCVMOutput(line)
              properties.append(mp)
            except :
              pass


        if len(properties) == 1:
            return properties[0]

        return properties

    ##
    #  Gets the Poisson value for a given set of Vs, Vp pair
    #  @param vs 
    #  @param vp
    #  @return poisson value
    def poisson(self, vs, vp) :
       if vs == 0 :
          return 0.0

       if vp == 0 :
          return 0.0

       return vp/vs

    ##
    #  Gets the Poisson value for a given set of Vs, Vp pair base on
    #  https://www.glossary.oilfield.slb.com/en/Terms/p/poissons_ratio.aspx
    #  @param vs 
    #  @param vp
    #  @return poisson value
    def poissonComplex(self, vs, vp) :
       if vs == 0 :
          return 0.5

       b=(vp * vp) - (vs * vs)
       t=((vp * vp) - 2*(vs * vs))/2

       if(b == 0) :
          return 0.0

       val = t/b
       return val

    ##
    #  Gets the Vs30 values for a given set of points and a CVM to query. If
    #  the CVM does not exist, this function will throw an error. The set of
    #  points is an array of @link Point Points @endlink. The function returns
    #  the Vs30 values as floats.
    #
    #  @param point_list An array of @link Point Points @endlink to query.
    #  @param cvm The CVM from which the Vs30 data should be retrieved.
    #  @return An array of floats which correspond to the points provided.
    def vs30(self, point_list, cvm):

        proc = Popen([self.binary_dir + "/vs30_query", "-f", self.config, "-m", cvm], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
        
        text_points = ""
        floats = []
        
        if isinstance(point_list, Point):
            point_list = [point_list]
        
        for point in point_list:
            text_points += "%.5f %.5f\n" % (point.longitude, point.latitude)
            
        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(0,output)
        
        for line in output:
            if ("WARNING" in line) or ("slow performance" in line) or ("Using Geo Depth coordinates as default mode" in line):
                 print("skipping text :"+line)
            else:
                 try :
                     p=float(line.split()[2])
                 except :
                     print("ERROR: should be a float.")
                     exit(1)
                 floats.append(p)
        
        if len(floats) == 1:
            return floats[0]
            
        return floats


    ##
    #  Gets the basin depths for a given set of points, CVM, and desired Vs.
    #  If the CVM does not exist, an error is given. The set of points is an
    #  array of @link Point Points @endlink. The function returns the depths
    #  as floats.
    # 
    #  @param point_list An array of @link Point Points @endlink to query.
    #  @param cvm The CVM from which the depths should come.
    #  @param vs_threshold The Vs threshold to check for (e.g. Z1.0 = 1000).
    #  @return An array of floats which correspond to the depths.
    def basin_depth(self, point_list, cvm, vs_threshold):

        proc = Popen([self.binary_dir + "/basin_query", "-f", self.config, "-m", \
                      cvm, "-v", "%.0f" % vs_threshold], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')

        text_points = ""
        floats = []

        if isinstance(point_list, Point):
            point_list = [point_list]

        for point in point_list:
            text_points += "%.5f %.5f\n" % (point.longitude, point.latitude)

        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(0,output)

        for line in output:
            try :
                p=float(line.split()[2])
            except :
                print("ERROR: should be a float.")
                exit(1)
            floats.append(p)

        if len(floats) == 1:
            return floats[0]

        return floats

    ##
    #  Queries UCVM given a set of points and a CVM to query. If the CVM does not exist,
    #  this function will throw an error. The set of points must be an array of the 
    #  @link Point Point @endlink class. This function returns an array of @link MaterialProperties
    #  MaterialProperties @endlink.
    #
    #  @param point_list An array of @link Point Points @endlink for which UCVM should query.
    #  @param cvm The CVM from which this data should be retrieved.
    #  @return An array of @link MaterialProperties @endlink.
    def elevation_etree(self, point_list, cvm):
        
        properties = []
        
        # shared_object = "../model/" + cvm + "/lib/lib" + cvm + ".so"
        # Can we load this library dynamically and bypass the C code entirely?
        #if os.path.isfile(shared_object):
            #import ctypes
            #obj = ctypes.cdll.LoadLibrary(shared_object)
            #print(obj)
        
        proc = Popen([self.utility_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        
        text_points = ""
        
        if isinstance(point_list, Point):
            point_list = [point_list]
         
        for point in point_list:
            text_points += "%.5f %.5f %.5f\n" % (point.longitude, point.latitude, point.depth)
            # print("%.5f %.5f %.5f" % (point.longitude, point.latitude, point.depth))
        
        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(1,output)

        for line in output:
            if ("WARNING" in line) or ("slow performance" in line) or ("Using Geo Depth coordinates as default mode" in line):
                print("skipping text :"+line)
            else:
                # Position 3 returned by ucvm_query is a elevation in the etree. Return this value
                try:
                    p=float(line.split()[3])
                except:
                    print("ERROR: should be a float value.")
                    exit(1)
                properties.append(p)

        if len(properties) == 1:
            return properties[0]
        
        return properties

    ##
    #  Queries UCVM given a set of points and a CVM to query. If the CVM does not exist,
    #  this function will throw an error. The set of points must be an array of the 
    #  @link Point Point @endlink class. This function returns an array of @link MaterialProperties
    #  MaterialProperties @endlink.
    #
    #  @param point_list An array of @link Point Points @endlink for which UCVM should query.
    #  @param cvm The CVM from which this data should be retrieved.
    #  @return An array of @link MaterialProperties @endlink.
    def map_grid(self, point_list, cvm):
        properties = []
        
        #shared_object = "../model/" + cvm + "/lib/lib" + cvm + ".so"
        # Can we load this library dynamically and bypass the C code entirely?
        #if os.path.isfile(shared_object):
        #import ctypes
        #obj = ctypes.cdll.LoadLibrary(shared_object)
        #print(obj)
        
        proc = Popen([self.utility_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
        
        text_points = ""
        
        if isinstance(point_list, Point):
            point_list = [point_list]
         
        for point in point_list:
            text_points += "%.5f %.5f %.5f\n" % (point.longitude, point.latitude, point.depth)
            #  print("%.5f %.5f %.5f" % (point.longitude, point.latitude, point.depth))
        
        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(1,output)

        for line in output:
            if ("WARNING" in line) or ("slow performance" in line) or ("Using Geo Depth coordinates as default mode" in line):
                print("skipping text",line)
            else:
                # print("line :"+line)
                # return the whole line which will be printed to file
                properties.append(line)

        if len(properties) == 1:
            return properties[0]
        
        return properties

    ##
    #  Queries UCVM given a set of points and a CVM to query. If the CVM does not exist,
    #  this function will throw an error. The set of points must be an array of the 
    #  @link Point Point @endlink class. This function returns an array of @link MaterialProperties
    #  MaterialProperties @endlink.
    #
    #  @param point_list An array of @link Point Points @endlink for which UCVM should query.
    #  @param cvm The CVM from which this data should be retrieved.
    #  @return An array of @link MaterialProperties @endlink.
    def vs30_etree(self, point_list, cvm):
        properties = []
        
        proc = Popen([self.utility_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf8')
        
        text_points = ""
        
        if isinstance(point_list, Point):
            point_list = [point_list]
         
        for point in point_list:
            text_points += "%.5f %.5f %.5f\n" % (point.longitude, point.latitude, point.depth)
            # print("%.5f %.5f %.5f" % (point.longitude, point.latitude, point.depth))
        
        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(1,output)

        for line in output:
            if ("WARNING" in line) or ("slow performance" in line) or ("Using Geo Depth coordinates as default mode" in line):
                print("skipping text :"+line)
            else:
                #print("line :"+line)
                # return position 4 from ucvm_query is the etree vs30 value. return that
                try :
                   p=float(line.split()[4])
                except :
                   print("ERROR: should be a float.")
                   exit(1)
                properties.append(p)

        if len(properties) == 1:
            return properties[0]
        
        return properties

# import raw floats array data from the external file into 
# numpy array
    def import_np_float_array(self, fname, num_x, num_y):
        rawfile=fname
        k = rawfile.rfind(".png")
        if( k != -1) : 
            rawfile = rawfile[:k] + "_data.raw"
        try :
            fh = open(rawfile, 'rb') 
        except:
            print("ERROR: binary np float array data does not exist.")
            exit(1)
            
        floats=[]
        sz = (num_x * num_y)
        floats = np.load(fh)
        fh.close()
        return floats
    
# import raw floats data from the external file 
# that is in ascii float format, 1 float per line
# file name is: filename_data.raw
#
    def import_raw_data(self, fname, num_x, num_y):
        rawfile=fname
        k = rawfile.rfind(".png")
        if( k != -1) : 
            rawfile = rawfile[:k] + "_data.raw"
        try :
            fh = open(rawfile, 'rb') 
        except:
            print("ERROR: binary data does not exist.")
            exit(1)
            
        floats=[]
        sz = (num_x * num_y)
        dlines = fh.readlines()
        for oline in dlines :
          parts = oline.split()
          floats.append(float(parts[0]))
        fh.close()
        return floats


#  import meta data as a json blob
#
    def import_json(self, fname):
        rawfile=fname
        k = rawfile.rfind(".json")
        if( k == -1) : 
            print("Supplied "+fname+" did not have .json suffix\n")
        try :
            fh = open(rawfile, 'r') 
        except :
            print("ERROR: json meta data does not exist.")
            exit(1)

        data = json.load(fh)
        fh.close()
        return data

#  import raw binary floats data from the external file 
#
#  file name is: filename_data.bin
#
#  if filename is image.png, look for a matching
#  image_data.bin
#
    def import_binary(self, fname, num_x, num_y):
        rawfile=fname
        k = rawfile.rfind(".png")
        if( k != -1) : 
            rawfile = rawfile[:k] + "_data.bin"
        try :
            fh = open(rawfile, 'rb') 
        except:
            print("ERROR: binary data does not exist.")
            exit(1)
            
        floats = np.fromfile(fh, dtype=np.float32)

## special case, when floats are written out as float64 instead of float32
        if len(floats) == 2 * (num_x * num_y) :
          fh.seek(0,0)
          floats = np.fromfile(fh, dtype=np.float)
        fh.close()

## maybe it is a np array
        if len(floats) != (num_x * num_y) :
          ffh = open(rawfile, 'rb') 
          ffloats = np.load(ffh)
          ffh.close()
          floats=ffloats.reshape([num_x * num_y]);

        print("TOTAL number of binary data read:"+str(len(floats))+"\n")

        # sanity check,  
        if len(floats) != (num_x * num_y) :
            print("import_binary(), wrong size !!!"+ str(len(floats)) + " expecting "+ str(num_x * num_y))
            exit(1)

        if len(floats) == 1:
            return floats[0]
        
        return floats

#  export np float array to an exernal file
#  
    def export_np_float_array(self, floats, fname):
#       print("calling export_np_float_array -",len(floats))
        rawfile = fname
        if rawfile is None :
            rawfile="data.bin"
        k = rawfile.rfind(".png")
        if( k != -1) : 
            rawfile = rawfile[:k] + "_data.bin"
        try :
            fh = open(rawfile, 'wb+') 
        except:
            print("ERROR: can not write out binary data.")
            exit(1)

        np.save(fh, floats)
        fh.close()

   

#  export raw floats nxy ndarray  to an external file 
    def export_binary(self, floats, fname):
        print("calling export_binary -",len(floats))
        rawfile = fname
        if rawfile is None :
            rawfile="data.bin"
        k = rawfile.rfind(".png")
        if( k != -1) : 
            rawfile = rawfile[:k] + "_data.bin"
        try :
            fh = open(rawfile, 'w+') 
        except:
            print("ERROR: can not write out binary data.")
            exit(1)

        floats.tofile(fh)
        print("export_binary(), size=" + str(floats.size))
        fh.close()

#  { 'num_x' : xval, 'num_y' : yval, 'total' : total }
#  import ascii meta jsoin data from an external file 
    def import_metadata(self, fname):
        metafile=fname
        k = metafile.rfind(".png")
        if( k != -1) : 
            metafile = metafile[:k] + "_meta.json"
        try :
            fh = open(metafile, 'r') 
        except:
            print("ERROR: can not find the meata data.")
            exit(1)
        meta = json.load(fh)
        fh.close()
        return meta

#  export ascii meta data to an external file 
    def export_metadata(self,meta,fname):
        print("calling export_metadata")
        metafile=fname
        if metafile is None:
          metafile = "meta.json"
        k = metafile.rfind(".png")
        if( k != -1) : 
            metafile = metafile[:k] + "_meta.json"
        try :
            fh = open(metafile, 'w+') 
        except:
            print("ERROR: can not write the meta data.")
            exit(1)
        json.dump(meta, fh, indent=2, sort_keys=False)
        fh.close()

#  import material properties in JSON form from an external file 
#  { matprops: [ 
#          { 'vp': pval, 'vs': sval, 'density': dval },
#          ...
#          { 'vp': pval, 'vs': sval, 'density': dval } ] }
    def import_matprops(self, fname):
        properties=[]
        jblob=self.import_json(fname)
        mlist= jblob["matprops"]
        for item in mlist :
           mp=MaterialProperties.fromJSONOutput(item)
           properties.append(mp)
        return properties

#  export material properties in JSON form to an external file 
    def export_matprops(self,blob,fname):
        print("calling export_matprops")
        matpropsfile=fname
        if matpropsfile is None :
            matpropsfile="matprops.json"
        k = matpropsfile.rfind(".png")
        if( k != -1) : 
            matpropsfile = matpropsfile[:k] + "_matprops.json"
        try :
            fh = open(matpropsfile, 'w+') 
        except:
            print("ERROR: can not write the material property data.")
            exit(1)
        json.dump(blob, fh, indent=2, sort_keys=False)
        fh.close()


#  export material properties in csv form to an external file
    def export_matprops_csv(self,jblob,fname):
#        print("calling export_matprops_csv")
        matpropsfile=fname
        if matpropsfile is None :
            matpropsfile="matprops.csv"
        k = matpropsfile.rfind(".png")
        if( k != -1) :
            matpropsfile = matpropsfile[:k] + "_matprops.csv"
        try :
            fh = open(matpropsfile, 'w+')
        except:
            print("ERROR: can not write the material property data.")
            exit(1)

        mlist= jblob["matprops"]
        for item in mlist :
           vp=item['vp']
           vs=item['vs']
           density=item['density']
           aline = "%.3f,%.3f,%.3f\n" % (p, vs, density)
           fh.write(aline)
        fh.close()


#  export material properties in JSON form to an external file 
    def export_velocity(self,filename,vslist,vplist,rholist):
#        print("calling export_velocity")
        k = filename.rfind(".png")
        rawfile=filename
        if( k != -1) :
            rawfile= filename[:k] + "_data.json"
        try :
            fh = open(rawfile, 'w+')
        except:
            print("ERROR: can not write the material property data.")
            exit(1)
        raw={"vs":vslist, "vp":vplist, "rho":rholist};
        json.dump(raw, fh, indent=2, sort_keys=False)
        fh.close()

    #  make the proper bounds for colormap
    #  when all is True, then need to substep all the range
    def makebounds(self,minval=0.0,maxval=5.0,nstep=0,meanval=None, substep=5,all=True) :
        bounds=[]
        if(nstep == 0) :
          bounds = [0, 0.2, 0.4, 0.6, 0.8, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
          return bounds

        step=float(maxval - minval)/nstep

        l=0
        nsubstep=substep
        nnstep=float(step)/nsubstep
        if(meanval != None and step!= 0) :
          l =(meanval-minval) //step

        for i in range(0,nstep) :
          s= step*i+minval
          if (i == l or all == True) :
            for j in range(nsubstep) :
              bound= round(s+(j * nnstep),4)
              bounds.append(bound)
          
          else:
            bounds.append(round(s,4))

        bounds.append(round((step * nstep + minval),4))
#        print("bounds", bounds)
        return bounds

    ## 
    #  make the proper ticks for subplot
    def maketicks(self,minval=None,maxval=None,nstep=0) :
        ticks=[]

        if(nstep == 0) :
          ticks = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
          return ticks

        step=(maxval - minval)/nstep
        for i in range(nstep) :
            tick= round((step * i) + minval,4)
            ticks.append(tick)

        ticks.append(round((step * nstep + minval),4))
#        print("ticks "+ ticks)
        return ticks
