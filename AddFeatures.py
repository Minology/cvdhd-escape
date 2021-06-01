import os
from osgeo import gdal
from addLandUse import addLandcoverFeatures 
from addOthers import addOFeatureAllBuffer
from addDPTandDen import addDPTAllBuffer, addDensityAllBuffer
import csv
import shutil

if __name__ == '__main__': 
    
    for i in range (1,4):
        path = 'sample data/station'
        with open(os.path.join(path, 'fixed{}.csv'.format(i)), 'w') as fp:
            pass
    
    
    addLandcoverFeatures('sample data/station/station_no2_2019_daily_formated.csv', 'sample data/station/fixed1.csv', 'sample data/station/fixed2.csv', 'sample data/station/fixed3.csv')
    
    addOFeatureAllBuffer("normalized difference vegetation index[NDVI]", "sample data/map/normalized difference vegetation index[NDVI]/MOD13Q1_", 
                          'sample data/station/station_no2_2019_daily_formated.csv', 
                          'sample data/station/fixed1.csv', 
                          'sample data/station/fixed2.csv', 
                          'sample data/station/fixed3.csv'
                        )
    
    addOFeatureAllBuffer("S5P NO2", "sample data/map/S5P NO2/S5P_NO2_", 
                          'sample data/station/station_no2_2019_daily_formated.csv', 
                          'sample data/station/fixed1.csv', 
                          'sample data/station/fixed2.csv', 
                          'sample data/station/fixed3.csv'
                        )
    
    addOFeatureAllBuffer("temperature", "sample data/map/temperature/TMPCombine_", 
                          'sample data/station/station_no2_2019_daily_formated.csv', 
                          'sample data/station/fixed1.csv', 
                          'sample data/station/fixed2.csv', 
                          'sample data/station/fixed3.csv'
                        )
    
    addOFeatureAllBuffer("wind speed", "sample data/map/wind speed/WSPDCombine_", 
                          'sample data/station/station_no2_2019_daily_formated.csv', 
                          'sample data/station/fixed1.csv', 
                          'sample data/station/fixed2.csv', 
                          'sample data/station/fixed3.csv'
                        )
    
    addOFeatureAllBuffer("relative humidity", "sample data/map/relative humidity/RHCombine_", 
                          'sample data/station/station_no2_2019_daily_formated.csv', 
                          'sample data/station/fixed1.csv', 
                          'sample data/station/fixed2.csv', 
                          'sample data/station/fixed3.csv'
                        )
    
    addOFeatureAllBuffer("pressure", "sample data/map/pressure/PRESSCombine_", 
                          'sample data/station/station_no2_2019_daily_formated.csv', 
                          'sample data/station/fixed1.csv', 
                          'sample data/station/fixed2.csv', 
                          'sample data/station/fixed3.csv'
                        )
    
    addOFeatureAllBuffer("planetary boundary layer height[pblh]", "sample data/map/planetary boundary layer height[pblh]/HPBLCombine_", 
                          'sample data/station/station_no2_2019_daily_formated.csv', 
                          'sample data/station/fixed1.csv', 
                          'sample data/station/fixed2.csv', 
                          'sample data/station/fixed3.csv'
                        )
    
    addDPTAllBuffer("dewpoint temperature (dpt)",
                    'sample data/station/station_no2_2019_daily_formated.csv', 
                    'sample data/station/fixed1.csv', 
                    'sample data/station/fixed2.csv', 
                    'sample data/station/fixed3.csv'
                   )
    
    addDensityAllBuffer("road_density_", 
                        'sample data/station/station_no2_2019_daily_formated.csv', 
                        'sample data/station/fixed1.csv', 
                        'sample data/station/fixed2.csv', 
                        'sample data/station/fixed3.csv',
                        'sample data/map/road density/road_dens.tif')
    
    addDensityAllBuffer("population_density_", 
                        'sample data/station/station_no2_2019_daily_formated.csv', 
                        'sample data/station/fixed1.csv', 
                        'sample data/station/fixed2.csv', 
                        'sample data/station/fixed3.csv',
                        'sample data/map/population density/vnm_ppp_2019_resampled3km.tif')
    
    
    original = "sample data/station/fixed3.csv".format()
    target = "data/train.csv".format()
    shutil.move(original,target)















    
          