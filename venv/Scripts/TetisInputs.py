from Scripts.Tetisfunctioninputs import *

# Uso de suelo a profundidad de raiz
CalcprofRaiz('cobveg.tif')


calalmcharcos('cobveg.tif')
rasterresolution(270,270)
Almac_Estatico("PAW_270.tif", "ProfRaices_270.tif","Hu.tif")

#Función de pedotransferencia
pedotransferencia('sand_utm.tif','clay_utm.tif','OM_utm.tif',6,'outSAT_band6.tif','outFC_band6.tif','outSatCond_band6.tif','outPAW_band6.tif')

#Adecuación a outputs de la función de pedotransferencia a resolución compatible con modelo ecohidrológico de Echeverria de 270 x 270 m
rasterresolution2('outSatCond_band6.tif', 'outSatCond_band6_270.tif', 270,270)

#Clip to raster extent for tetis
RasterWarp('AT_270.tif','outSatCond_band6_270.tif','outSatCond_band6_270_clipped.tif') #

#tif 2 asc
RasterFormat('outSatCond_band6_270_clipped.tif', 'outSatCond_band6_270_clipped.asc') 
RasterFormat('SatCond_270_clipped.tif', 'SatCond_270_clipped.asc') 


