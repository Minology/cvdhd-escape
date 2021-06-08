import os
from train.addLandUse import addLandcoverFeatures, copyReadtoWrite
from geoprep import GeoPrep
import csv
from testadd import find_nearest, findnearestDPT, fixedate
import shutil

# change the date here
Date = 20191231


# handle all solvers
solverNDVI = GeoPrep("sample data/map/normalized difference vegetation index[NDVI]/MOD13Q1_{}_Ndvi.tif".format(find_nearest("normalized difference vegetation index[NDVI]",Date)))
solverS5P = GeoPrep("sample data/map/S5P NO2/S5P_NO2_{}.tif".format(find_nearest("S5P NO2",Date)))
solverTemp = GeoPrep("sample data/map/temperature/TMPCombine_{}.tif".format(find_nearest("temperature", Date)))
solverWind = GeoPrep("sample data/map/wind speed/WSPDCombine_{}.tif".format(find_nearest("wind speed", Date)))
solverHumid = GeoPrep("sample data/map/relative humidity/RHCombine_{}.tif".format(find_nearest("relative humidity", Date)))
solverPressure = GeoPrep("sample data/map/pressure/PRESSCombine_{}.tif".format(find_nearest("pressure", Date)))
solverpblh = GeoPrep("sample data/map/planetary boundary layer height[pblh]/HPBLCombine_{}.tif".format(find_nearest("planetary boundary layer height[pblh]", Date)))
solverRoadDen = GeoPrep("sample data/map/road density/road_dens.tif")
solverPopulationDen = GeoPrep("sample data/map/population density/vnm_ppp_2019_resampled3km.tif")

feature_names = ["NDVI_","S5P_NO2_","temperature_","wind_speed_","relative_humidity_","pressure_","planetary_boundary_layer_height[pblh]_","dewpoint_temperature_(dpt)_","road_density_","population_density_"]
DictFeatures = {
        "NDVI_": solverNDVI,
        "S5P_NO2_": solverS5P,
        "temperature_": solverTemp,
        "wind_speed_": solverWind,
        "relative_humidity_": solverHumid,
        "pressure_": solverPressure,
        "planetary_boundary_layer_height[pblh]_": solverpblh,
        "road_density_": solverRoadDen,
        "population_density_": solverPopulationDen
}

def addFeatureTest(name, readfile, writefile, buffer):
    csvfile = open(readfile,'r')
    csvfile2 = open(writefile,'w')
    reader = csv.reader(csvfile)
    writer = csv.writer(csvfile2, lineterminator='\n')
    all = []
    row = next(reader)
    featurename = name + str(buffer)
    row.append(featurename)
    all.append(row)
    if name == "dewpoint_temperature_(dpt)_":
        listDPTdates = findnearestDPT(Date)
        listofsolver = []
        
        for filenumber in listDPTdates:
            solver = GeoPrep("sample data/map/dewpoint temperature (dpt)/DPT_{}.tif".format(filenumber))
            listofsolver.append(solver)

        
        for row in reader:
            listofsubavg = []
            for sv in listofsolver:
                m = sv.getsubavg(float(row[1]), float(row[2]), buffer)
                listofsubavg.append(m)
            row.append(sum(listofsubavg)/len(listofsubavg))
            all.append(row)
        writer.writerows(all)
    else:
        for row in reader:
            row.append(DictFeatures[name].getsubavg(float(row[1]), float(row[2]), buffer))
            all.append(row)
        writer.writerows(all)

def addFeatureTestAllBuffer(name):
    print(name)
    addFeatureTest(name,'sample data/station/test{}.csv'.format(Date), 'sample data/station/test1.csv',3000)
    copyReadtoWrite('sample data/station/test1.csv', 'sample data/station/test{}.csv'.format(Date))
    
    addFeatureTest(name,'sample data/station/test{}.csv'.format(Date), 'sample data/station/test1.csv',6000)
    copyReadtoWrite('sample data/station/test1.csv', 'sample data/station/test{}.csv'.format(Date))

    addFeatureTest(name,'sample data/station/test{}.csv'.format(Date), 'sample data/station/test1.csv',9000)
    copyReadtoWrite('sample data/station/test1.csv', 'sample data/station/test{}.csv'.format(Date))

if __name__ == '__main__':
    
    mpath = 'sample data/station'
    with open(os.path.join(mpath, 'test{}.csv'.format(Date)), 'w') as fp:
        testWriter = csv.writer(fp, lineterminator='\n')
        testWriter.writerow(["time","lat", "lon"])
        for m in range (0,768):
            for n in range (0,468):
                testWriter.writerow([fixedate(Date),25.6 - m*0.025, 100.1 + n*0.025]) #fix
    
    for i in range (1,4):
        path = '../sample data/station'
        with open(os.path.join(path, 'test{}.csv'.format(i)), 'w') as fp:
            pass
    
    addLandcoverFeatures('sample data/station/test{}.csv'.format(Date), 'sample data/station/test1.csv', 'sample data/station/test2.csv', 'sample data/station/test3.csv')
    addFeatureTestAllBuffer("NDVI_")
    addFeatureTestAllBuffer("S5P_NO2_")
    addFeatureTestAllBuffer("temperature_")
    addFeatureTestAllBuffer("wind_speed_")
    addFeatureTestAllBuffer("relative_humidity_")
    addFeatureTestAllBuffer("pressure_")
    addFeatureTestAllBuffer("planetary_boundary_layer_height[pblh]_")
    addFeatureTestAllBuffer("dewpoint_temperature_(dpt)_")
    addFeatureTestAllBuffer("road_density_")
    addFeatureTestAllBuffer("population_density_")

    
    with open("sample data/station/test1.csv", "r") as source:
        print("ending . . .")
        reader = csv.reader(source)
        with open("sample data/station/test{}.csv".format(Date), "w") as result:
            writer = csv.writer(result, lineterminator='\n')
            for r in reader:
                writer.writerow((r[1:]))
    
    original = "sample data/station/test{}.csv".format(Date)
    target = "data/test/test{}.csv".format(Date)
    shutil.move(original,target)    


    



































