from osgeo import gdal
import numpy as np
#Uso de suelo a profundidad de raiz

inDs = gdal.Open('C:\\Users\\ASUS\\OneDrive\\Documents\\CIH\\Tetis\\cobveg.tif')
driver = inDs.GetDriver()
S = inDs.GetRasterBand(1)
S = S.ReadAsArray()
S = S.astype(np.float)

Usosuelo = [1,'agua',0],\
           [2,'cultivo de regadio',1.5],\
           [3,'cultivo secano',1.3],\
           [4,'infraestructura urbana',0],\
           [5,'cobertura forestal',1]

S[S==1]=0
S[S==2]=1.5
S[S==3]=1.3
S[S==4]=0
S[S==5]=1
S[S<0]=np.nan

directory_path='C:\\Users\\ASUS\\OneDrive\\Documents\\CIH\\Tetis\\'

pathCobveg=str(directory_path)+'/ProfRaices.tif'
outDatasetCobveg = driver.Create(pathCobveg,inDs.RasterXSize,inDs.RasterYSize,1,gdal.GDT_Float32)

outDatasetCobveg.SetGeoTransform(inDs.GetGeoTransform())
outDatasetCobveg.SetProjection(inDs.GetProjection())

outbandCobveg = outDatasetCobveg.GetRasterBand(1)
#outbandCobveg.SetNoDataValue(-99)
outbandCobveg.WriteArray(S)
outbandCobveg.FlushCache()

del S
