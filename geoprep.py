from osgeo import gdal
import numpy as np
from measure import latlonDistance

class GeoPrep:
    def __init__(self, data_path, doclass=-1):
        ds = gdal.Open(data_path, gdal.GA_ReadOnly)
        band = ds.GetRasterBand(1)

        data = band.ReadAsArray()
        # print(len(data), len(data[0]))
        self.nodataValue = band.GetNoDataValue()
        # print(nodata)

        transform = ds.GetGeoTransform()
        # print(transform)

        self.xOrigin = transform[0]
        self.yOrigin = transform[3]
        self.pixelWidth = transform[1]
        self.pixelHeight = -transform[5]
        self.subsum = np.zeros((len(data),len(data[0])), dtype=float)
        self.cntdata = np.zeros((len(data),len(data[0])), dtype=int)
        self.data = data
        self.doclass=doclass

        # print(data[0][1])
        # print(data[0][2])
        # print(data[0][3])
        # print(data[1][1])
        # print(data[1][2])
        # print(data[1][3])
        if doclass == -1:
            for i in range(self.subsum.shape[0]):
                for j in range(self.subsum.shape[1]):
                    self.cntdata[i][j]=self.getCnt(i,j-1)+self.getCnt(i-1,j)-self.getCnt(i-1,j-1)
                    self.subsum[i][j]=self.getSum(i,j-1)+self.getSum(i-1,j)-self.getSum(i-1,j-1)
                    if self.isData(i,j):
                        self.cntdata[i][j] += 1
                        self.subsum[i][j] += data[i][j]
        else:
            for i in range(self.subsum.shape[0]):
                for j in range(self.subsum.shape[1]):
                    self.cntdata[i][j]=self.getCnt(i,j-1)+self.getCnt(i-1,j)-self.getCnt(i-1,j-1)
                    if self.isData(i,j) and (data[i][j] in self.doclass):
                        self.cntdata[i][j] += 1

    def eq(self, a, b):
        if type(b) == int or type(b) == float:
            return abs(a-b)<1e-4
        else:
            return False


    def isData(self, i, j):
        return not np.isnan(self.data[i][j]) and not self.eq(self.data[i][j], self.nodataValue)

    def getProperCell(self,i,j):
        ii = i
        jj = j
        if self.outboundLow(i,j): 
            return 0
        if i > self.cntdata.shape[0]:
            ii = self.cntdata.shape[0] - 1
        if j > self.cntdata.shape[1]:
            jj = self.cntdata.shape[1] - 1  
        return ii, jj

    def outboundLow(self,i,j):
        return i<0 or j<0

    def outboundHigh(self,i,j):
        return i>=self.cntdata.shape[0] or j>=self.cntdata.shape[1]

    def outbound(self,i,j):
        return self.outboundLow(i,j) or self.outboundHigh(i,j)

    def getCnt(self,i,j):
        if self.outboundLow(i,j):
            return 0
        if i > self.cntdata.shape[0]:
            i = self.cntdata.shape[0]
        if j > self.cntdata.shape[1]:
            j = self.cntdata.shape[1]
        return self.cntdata[i][j]

    def getSum(self,i,j):
        if self.outboundLow(i,j):
            return 0
        if i > self.subsum.shape[0]:
            i = self.subsum.shape[0]
        if j > self.subsum.shape[1]:
            j = self.subsum.shape[1]
        return self.subsum[i][j]

    def toLatLon(self,x,y):
        lon=y*self.pixelWidth+self.xOrigin
        lat=self.yOrigin-x*self.pixelHeight
        return lat,lon

    def calculateDistance(self,x,y,xx,yy):
        lat1,lon1=self.toLatLon(x,y)
        lat2,lon2=self.toLatLon(xx,yy)
        # print(lat1,lon1,lat2,lon2)
        return latlonDistance(lat1,lon1,lat2,lon2)

    def find(self,x,y,xd,yd,radius):
        l=0
        r=800
        while (l<=r):
            md=(l+r)//2
            xx=x+xd*md
            yy=y+yd*md
            if self.outbound(xx,yy):
                r=md-1
            else:
                distance=self.calculateDistance(x,y,xx,yy)
                # print("HAHA", md, distance)
                if distance>radius:
                    r=md-1
                else: 
                    l=md+1
        return x+xd*r, y+yd*r

    def findAroundRadius(self, lat, lon, radius):
        col = int((lat - self.xOrigin) / self.pixelWidth)
        row = int((self.yOrigin - lon) / self.pixelHeight)
        # print(row, col)

        tlx=self.find(row, col, -1, 0, radius)[0]
        tly=self.find(row, col, 0, -1, radius)[1]
        brx=self.find(row, col, 1, 0, radius)[0]
        bry=self.find(row, col, 0, 1, radius)[1]
        return tlx,tly,brx,bry

    def getsubavg(self, lat, lon, radius):
        tlx,tly,brx,bry=self.findAroundRadius(lat,lon,radius)
        
        # print(tlx, tly, brx, bry)
        return (self.getSum(brx,bry)+self.getSum(tlx-1,tly-1)-self.getSum(tlx-1,bry)-self.getSum(brx,tly-1))/   \
                (max(1,self.getCnt(brx,bry)+self.getCnt(tlx-1,tly-1)-self.getCnt(tlx-1,bry)-self.getCnt(brx,tly-1)))

    def getsubcnt(self, lat, lon, radius):
        tlx,tly,brx,bry=self.findAroundRadius(lat,lon,radius)
        
        # print(tlx, tly, brx, bry)
        return self.getCnt(brx,bry)+self.getCnt(tlx-1,tly-1)-self.getCnt(tlx-1,bry)-self.getCnt(brx,tly-1)

if __name__ == '__main__':
    # ----- land cover use case for a list of classes. any cell that has value in doclass will be counted
    solver = GeoPrep('../sample data/map/landCover2019wgs84.tif', doclass=[40,50])
    # getsubcnt(lat,lon,rad)
    # get count of something in a radius of rad (meters), around position at (lat,lon)
    print(solver.getsubcnt(100.10001+0.025*2, 25.60001, 5000))

    # ----- other feature use case
    solver = GeoPrep('../sample data/map/S5P_NO2_20190101.tif')
    # getsubavg(lat,lon,rad)
    # get average of something in a radius of rad (meters), around position at (lat,lon)
    print(solver.getsubavg(100.10001+0.025*2, 25.60001, 5000))
    # print(solver.calculateDistance(0,0,1,0))
