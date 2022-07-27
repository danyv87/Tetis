from osgeo import gdal
import numpy as np

RasterXSize=270
RasterYSize=270

# Uso de suelo a profundidad de raiz

directory_path = 'C:\\Users\\ASUS\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Inputs_Recalculados\\'
pathusodesuelo = directory_path + 'SatCond_270_clipped.asc'  # nombre raster uso de suelo

inDs = gdal.Open(pathusodesuelo)
driver = inDs.GetDriver()
S = inDs.GetRasterBand(1)
S = S.ReadAsArray()
S = S.astype(np.float)

pathCobveg = str(directory_path) + 'SatCond_270_clipped2.asc'
outDatasetCobveg = driver.Create(pathCobveg, inDs.RasterXSize, inDs.RasterYSize, 1, gdal.GDT_Float32)

outDatasetCobveg.SetGeoTransform(inDs.GetGeoTransform())
outDatasetCobveg.SetProjection(inDs.GetProjection())

outbandCobveg = outDatasetCobveg.GetRasterBand(1)
outbandCobveg.SetNoDataValue(-9999)
outbandCobveg.WriteArray(S)
outbandCobveg.FlushCache()

del S