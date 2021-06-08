from osgeo import gdal
from geoprep import GeoPrep
import datetime as dt
import os.path
from os import path
from os import walk
import csv
from addLandUse import copyReadtoWrite

#add dict
def makeDict(filenames, path):
    print(path)
    Dict = {}
    KeyNumDict = {}
    for file in filenames:
        fixedfile = file.replace("_Ndvi","")
        k = fixedfile[-12:].replace(".tif", "")
        if "_Ndvi" in file: m = GeoPrep("{}{}_Ndvi.tif".format(path, k))
        else:
            print(k) 
            m = GeoPrep("{}{}.tif".format(path, k))
        Dict[k] = m
        KeyNumDict[k] = int(k)
    return Dict, KeyNumDict
# featurename = S5P NO2
# path = 'sample data/map/S5P NO2/S5P_NO2_'
# readfile = 'sample data/station/fixed0.csv'
# writefile = 'sample data/station/test1.csv'
def addOFeature(buffer, featurename, path, readfile, writefile, Dict, KeyNumDict):
        
    csvfile = open(readfile,'r')
    csvfile2 = open(writefile,'w')
    reader = csv.reader(csvfile)
    writer = csv.writer(csvfile2, lineterminator='\n')
    
    all = []
    row = next(reader)
    fixedfeaturename = featurename.replace(" ", "_")
    if "NDVI" in fixedfeaturename: row.append('NDVI_{}'.format(buffer))
    else: row.append('{}_{}'.format(fixedfeaturename, buffer))
    all.append(row)

    KeyNumList = []
    for key in KeyNumDict:
        KeyNumList.append(KeyNumDict[key])

    
    for row in reader:
        date = row[0].split("/")
        kkk = str(dt.datetime(int(date[2]), int(date[0]), int(date[1])).date()).replace('-', '')
        if kkk in Dict: row.append(Dict[kkk].getsubavg(float(row[1]),float(row[2]),buffer))
        else: 
            row.append(
                Dict[list(KeyNumDict.keys())[list(KeyNumDict.values()).index((min(KeyNumList, key=lambda x:abs(x- int(kkk)))))]].getsubavg(float(row[1]),float(row[2]),buffer)
            )
        all.append(row)
    
    writer.writerows(all)

def addOFeatureAllBuffer(featurename, path, file0, file1, file2, file3): 
    _, _, filenames = next(walk('sample data/map/{}'.format(featurename)))
    Dict, KeyNumDict = makeDict(filenames, path)
    addOFeature(3000, featurename, path, file0, file1, Dict, KeyNumDict)
    addOFeature(6000, featurename, path, file1, file2, Dict, KeyNumDict)
    addOFeature(9000, featurename, path, file2, file3, Dict, KeyNumDict)
    copyReadtoWrite(file3, file0)
    copyReadtoWrite(file3, file1)
    copyReadtoWrite(file3, file2)















    