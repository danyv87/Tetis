#Script para calcular inputs requeridos para ejecución de modelo hidrológico Tetis
from Scripts.Tetisfunctioninputs import *

##################Cálculo profundidad de raiz###########################
    #CalcprofRaiz([input uso de suelo .tif])
    #genera salida ProfRaices.tif'
CalcprofRaiz('cobveg.tif')

##################Cálculo de almacenamiento en charcos##################
    #calalmcharcos([input uso de suelo .tif])
    #genera salida AlmCharcos.tif'
calalmcharcos('cobveg.tif') #input uso de suelo .tif

##################Función de pedotransferencia##########################
    #pedotransferencia([input arena],[input archilla],[input cantidad de materia organica],[número de bandas],[salida SAT],
                                    #[salida Capacidad de Campo],[salida Conductividad Saturada],[salida Contenido de Agua])
pedotransferencia('sand_utm.tif','clay_utm.tif','OM_utm.tif',6,'outSAT_band6.tif','outFC_band6.tif','outSatCond_band6.tif','outPAW_band6.tif')

##################Adecuar resolución raster#############################
# Adecuar todos los raster a resolución compatible con output de modelo ecohidrológico de Echeverria de 270 m x 270 m
    #rasterresolution([resolucion x,resolución y])
    #genera salida SAT_270.tif, FC_270.tif, SatCond_270.tif, PAW_270.tif, ProfRaices_270.tif, AlmCharcos_270.tif
rasterresolution(270,270)

##################Calcular almacenamiento estático######################
    #Almac_Estatico([input PAW_270.tif], [input ProfRaices_270.tif],[importar propiedades geográficas de raster Hu.tif])
    #genera salida AT_270.tif
Almac_Estatico("PAW_270.tif", "ProfRaices_270.tif","Hu.tif")

#Adecuación a outputs de la función de pedotransferencia a resolución compatible con modelo ecohidrológico de Echeverria de 270 m x 270 m
    #rasterresolution2('outSatCond_band6.tif', 'outSatCond_band6_270.tif', 270,270)

##################Clip to raster extent for tetis#######################
    #RasterWarp([RasterBase], [Raster2clip], [Outputname]):
RasterWarp('AT_270.tif','outSatCond_band6_270.tif','outSatCond_band6_270_clipped.tif') #

##################Convertir a formato input reconocible por Tetis#######
    #RasterFormat([rasterin], [rasterout])
RasterFormat('outSatCond_band6_270_clipped.tif', 'outSatCond_band6_270_clipped.asc') 
RasterFormat('SatCond_270_clipped.tif', 'SatCond_270_clipped.asc') 


