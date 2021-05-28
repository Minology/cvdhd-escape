from osgeo import gdal
from geoprep import GeoPrep
import datetime as dt
import os.path
from os import path
from os import walk
import csv
from addLandUse import copyReadtoWrite
from statistics import mean

def makeDictDPT(filenames):
    Dict = {}
    KeyNumDict = {}
    for i in range (0,366):
        k = str((dt.datetime(2019, 1, 1) + dt.timedelta(i - 1)).date()).replace('-', '')
        ValueList = []
        streak = 0
        for file in filenames:
            if(k in file): 
                streak = 1
                ValueList.append(GeoPrep("sample data/map/dewpoint temperature (dpt)/{}".format(file)))
            else:
                if not (streak == 0): break
        Dict[k] = ValueList
        KeyNumDict[k] = int(k)
    for key in Dict.copy():
        if len(Dict[key]) == 0:
            Dict.pop(key)
            KeyNumDict.pop(key)
    return Dict, KeyNumDict

def getAvgG(Dict, key, lat, lon, buffer):
    listAvg = []
    for solver in Dict[key]: 
        listAvg.append(solver.getsubavg(lat, lon, buffer))
    return mean(listAvg)

def addDPT(buffer, featurename, readfile, writefile, Dict, KeyNumDict):
        
    csvfile = open(readfile,'r')
    csvfile2 = open(writefile,'w')
    reader = csv.reader(csvfile)
    writer = csv.writer(csvfile2, lineterminator='\n')
    
    all = []
    row = next(reader)
    fixedfeaturename = featurename.replace(" ", "_")
    row.append('{}_{}'.format(fixedfeaturename, buffer))
    all.append(row)

    KeyNumList = []
    for key in KeyNumDict:
        KeyNumList.append(KeyNumDict[key])

    
    for row in reader:
        date = row[0].split("/")
        kkk = str(dt.datetime(int(date[2]), int(date[0]), int(date[1])).date()).replace('-', '')
        if kkk in Dict: row.append(getAvgG(Dict, kkk, float(row[1]), float(row[2]), buffer))
        else: 
            row.append(
               # Dict[list(KeyNumDict.keys())[list(KeyNumDict.values()).index((min(KeyNumList, key=lambda x:abs(x- int(kkk)))))]].getsubavg(float(row[1]),float(row[2]),buffer)
               getAvgG(Dict, list(KeyNumDict.keys())[list(KeyNumDict.values()).index((min(KeyNumList, key=lambda x:abs(x- int(kkk)))))], float(row[1]), float(row[2]), buffer)
            )
        all.append(row)
    
    writer.writerows(all)

def addDPTAllBuffer(featurename, file0, file1, file2, file3): 
    _, _, filenames = next(walk('sample data/map/{}'.format(featurename)))
    Dict, KeyNumDict = makeDictDPT(filenames)
    addDPT(3000, featurename, file0, file1, Dict, KeyNumDict)
    addDPT(6000, featurename, file1, file2, Dict, KeyNumDict)
    addDPT(9000, featurename, file2, file3, Dict, KeyNumDict)
    copyReadtoWrite(file3, file0)
    copyReadtoWrite(file3, file1)
    copyReadtoWrite(file3, file2)



def addDensity(name, readfile, writefile, buffer, pathToFile):
    csvfile = open(readfile,'r')
    csvfile2 = open(writefile,'w')
    reader = csv.reader(csvfile)
    writer = csv.writer(csvfile2, lineterminator='\n')
    all = []
    row = next(reader)
    featurename = name + str(buffer)
    row.append(featurename)
    all.append(row)
    m = GeoPrep(pathToFile)
    for row in reader:
        row.append(m.getsubavg(float(row[1]), float(row[2]), buffer))
        all.append(row)
    writer.writerows(all)
    

def addDensityAllBuffer(name, file0, file1, file2, file3, pathToFile):
    addDensity(name, file0, file1, 3000, pathToFile)
    addDensity(name, file1, file2, 6000, pathToFile)
    addDensity(name, file2, file3, 9000, pathToFile)
    copyReadtoWrite(file3, file0)
    copyReadtoWrite(file3, file1)
    copyReadtoWrite(file3, file2)



