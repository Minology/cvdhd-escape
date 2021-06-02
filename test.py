from osgeo import gdal
from osgeo import osr
from osgeo.gdalconst import *
import pandas as pd
import numpy as np
import pickle
import sys
import getopt

MODEL = "Linear Regression"
CLIPPING_MODE = 0

def lat_to_x(lat):
    return (25.6 - lat) / 0.025

def lon_to_y(lon):
    return (lon - 100.1) / 0.025

# Function to read the original file's projection:
def GetGeoInfo(FileName):
    SourceDS = gdal.Open(FileName, GA_ReadOnly)
    NDV = SourceDS.GetRasterBand(1).GetNoDataValue()
    xsize = SourceDS.RasterXSize
    ysize = SourceDS.RasterYSize
    GeoT = SourceDS.GetGeoTransform()
    Projection = osr.SpatialReference()
    Projection.ImportFromWkt(SourceDS.GetProjectionRef())
    DataType = SourceDS.GetRasterBand(1).DataType
    DataType = gdal.GetDataTypeName(DataType)
    return NDV, xsize, ysize, GeoT, Projection, DataType

def ReadGeoTiff(FilePath):
    dataset = gdal.Open(FilePath, GA_ReadOnly)
    # Get the first (and only) band.
    band = dataset.GetRasterBand(1)
    # Open as an array.
    return band.ReadAsArray()

# Function to write a new file.
def CreateGeoTiff(NewFilePath, Array, driver, NDV, 
                  xsize, ysize, GeoT, Projection, DataType):
    if DataType == 'Float32':
        DataType = gdal.GDT_Float32
    elif DataType == 'Float64':
        DataType = gdal.GDT_Float64
    elif DataType == 'Byte':
        DataType = gdal.GDT_Byte
    # Set nans to the original No Data Value
    if NDV is None:
        NDV = np.nan
    Array[np.isnan(Array)] = NDV
    # Set up the dataset
    DataSet = driver.Create( NewFilePath, xsize, ysize, 1, DataType )
            # the '1' is for band 1.
    DataSet.SetGeoTransform(GeoT)
    DataSet.SetProjection( Projection.ExportToWkt() )
    # Write the array
    DataSet.GetRasterBand(1).WriteArray( Array )
    DataSet.GetRasterBand(1).SetNoDataValue(NDV)
    return NewFilePath

def test_date(date):
    templateFilePath = r'data/template.tif'
    array = ReadGeoTiff(templateFilePath)
    
    array = np.full(array.shape, np.nan)
    test_data = pd.read_csv(f'data/test/test{date}.csv')
    no2 = model.predict(test_data[features])
    test_locations = test_data[['lat', 'lon']].to_numpy()
    for i in range(len(no2)):
        lat, lon = test_locations[i]
        x, y = lat_to_x(lat), lon_to_y(lon)
        if CLIPPING_MODE == 0:
            array[round(x)][round(y)] = no2[i]
        else:
            array[round(x)][round(y)] = max(no2[i], 0)
        
    NDV, xsize, ysize, GeoT, Projection, DataType = GetGeoInfo(templateFilePath)
    # Set up the GTiff driver
    driver = gdal.GetDriverByName('GTiff')
    if CLIPPING_MODE == 0:
        outputFile = CreateGeoTiff(f'output/NO2_{date}.tif',
                                   array, driver, NDV, xsize, ysize, GeoT, Projection, DataType)
    else:
        outputFile = CreateGeoTiff(f'output/NO2_{date}_clipped.tif',
                                   array, driver, NDV, xsize, ysize, GeoT, Projection, DataType)
    return array

if __name__ == "__main__":
    model_name = "linear_regression"
    
    argv = sys.argv[1:]
    date = argv[0]
    if not date.startswith("-"):
        argv = argv[1:]
    
    try:
        opts, args = getopt.getopt(argv,'hcm:', ['model='])
    except getopt.GetoptError:
        print('Usage: test.py <yyyyMMdd> -c -m <modelname>')
        print('Use -c option for clipping')
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: test.py <yyyyMMdd> -c -m <modelname>')
            print('Use -c option for clipping')
            sys.exit()
        elif opt == '-c':
            CLIPPING_MODE = 1
        elif opt in ("-m", "--model"):
            MODEL = arg
    
    if MODEL == "Linear Regression":
        model_name = "linear_regression"
    else:
        model_name = "linear_regression"
    
    with open(f'models/{model_name}.pkl', 'rb') as model_file:
        model_info = pickle.load(model_file)
        
    features = model_info['features']
    model = model_info['model']
    output = test_date(date)
    
    #import matplotlib.pyplot as plt
    #plt.imshow(output)
    #plt.show(block=True)