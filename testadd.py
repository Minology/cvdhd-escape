from os import path
from os import walk
import numpy as np
from osgeo import gdal
from geoprep import GeoPrep

def callList(featurename):
    """
    _, _, filenames = next(walk('sample data/map/{}'.format(featurename)))
    fixedfilenames = []
    """
    fileNames = []
    for (dirpath, dirnames, filenames) in walk('sample data/map/{}'.format(featurename)):
        fileNames.extend(filenames)
        break 

    fixedfilenames = []
    for file in fileNames:
        if featurename == "dewpoint temperature (dpt)":
            file = int((file[-15:].replace(".tif", ""))[:8])
        elif featurename == "normalized difference vegetation index[NDVI]":
            file = int(file[-17:].replace("_Ndvi.tif", ""))
        else:
            file = int(file[-12:].replace(".tif", ""))
        fixedfilenames.append(file)
    
    return fixedfilenames

def find_nearest(featurename, value):
    array = np.asarray(callList(featurename))
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def findnearestDPT(value):
    fileNames = []
    for (dirpath, dirnames, filenames) in walk('sample data/map/dewpoint temperature (dpt)'):
        fileNames.extend(filenames)
        break 

    trueValue = str(find_nearest("dewpoint temperature (dpt)", value))
    valuelist = []
    for v in fileNames:
        if trueValue in v: valuelist.append(v[4:15])
    return valuelist 

def fixedate(date):
    date = str(date)
    y, m, d = date[:4], date[4:6], date[6:8]
    return d + "/" + m + "/" + y

