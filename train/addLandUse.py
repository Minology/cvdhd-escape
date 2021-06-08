from osgeo import gdal
from geoprep import GeoPrep
import csv

def addFeature(name, readfile, writefile, num, buffer):
    csvfile = open(readfile,'r')
    csvfile2 = open(writefile,'w')
    reader = csv.reader(csvfile)
    writer = csv.writer(csvfile2, lineterminator='\n')
    all = []
    row = next(reader)
    featurename = name + str(buffer)
    row.append(featurename)
    all.append(row)
    m = GeoPrep('sample data/map/landCover2019wgs84.tif', doclass= num)
    for row in reader:
        row.append(m.getsubcnt(float(row[1]), float(row[2]), buffer))
        all.append(row)
    writer.writerows(all)

def copyReadtoWrite(readfile, writefile):
    csvfile = open(readfile,'r')
    csvfile2 = open(writefile,'w')
    reader = csv.reader(csvfile)
    writer = csv.writer(csvfile2, lineterminator='\n')
    all = []
    for row in reader:
        all.append(row)
    writer.writerows(all)
    

def addFeatureAllBuffer(name, num, file0, file1, file2, file3):
    print(name)
    addFeature(name, file0, file1, num, 3000)
    addFeature(name, file1, file2, num, 6000)
    addFeature(name, file2, file3, num, 9000)
    copyReadtoWrite(file3, file0)
    copyReadtoWrite(file3, file1)
    copyReadtoWrite(file3, file2)

def addLandcoverFeatures(file0, file1, file2, file3):
    mydict = {
        "Shrubs_": [20],
        "Herbaceous_vegetation_": [30],
        "Cultivated_and_managed_vegetation/agriculture_": [40],
        "Urban/built_up_": [50],
        "Bare/sparse_vegetation_": [60],
        "Snow_and_ice_": [70],
        "Permanent_water_bodies_": [80],
        "Herbaceous_wetland_": [90],
        "Moss_and_lichen_": [100],
        "Close_forest_": [111,112,113,114,115,116],
        "Open_forest_": [121,122,123,124,125,126],
        "Oceans,seas_": [200]
    }
    for i in list(mydict.keys()):
        addFeatureAllBuffer(i, mydict.get(i), file0, file1, file2, file3)

if __name__ == '__main__':
    for m in range (0,5):
            for n in range (0,5):
                print(m,n)