from Scripts.Tetisfunctioninputs import *

#pedotransferencia('sand_utm.tif','clay_utm.tif','OM_utm.tif')
CalcprofRaiz('cobveg.tif')
calalmcharcos('cobveg.tif')
rasterresolution(270,270)
Almac_Estatico("PAW_270.tif", "ProfRaices_270.tif","Hu.tif")

pedotransferencia('sand_utm.tif','clay_utm.tif','OM_utm.tif',6,'outSAT_band6.tif','outFC_band6.tif','outSatCond_band6.tif','outPAW_band6.tif')
rasterresolution2('outSatCond_band6.tif', 'outSatCond_band6_270.tif', 270,270)
RasterWarp('AT_270.tif','outSatCond_band6_270.tif','outSatCond_band6_270_clipped.tif')

RasterFormat('outSatCond_band6_270_clipped.tif', 'outSatCond_band6_270_clipped.asc')
RasterFormat('SatCond_270_clipped.tif', 'SatCond_270_clipped.asc')


