#Convertir tif de densidad aparente de soilgrids a polygono Pfastetter
import rasterio
from affine import Affine
from rasterstats import zonal_stats
import os
import numpy as np
import geopandas as gpd
import pandas as pd

#importar archivos
path= "C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\"
tif = rasterio.open(path + "Inputs_Recalculados\\bulk_UTM.tif")
shp = gpd.read_file(path + "Varios\\Ottopfasteter nivel 10.shp")

#adecuar raster a numpy
tif_array = tif.read(1)
tif_array_flipped = np.flipud(tif_array)
affine=tif.transform #usar este affine
new_affine2 = Affine(affine.a, affine.b, affine.c,affine.d, affine.e*-1, affine.f + (affine.e * (tif.read(1).shape[0]-1))) # leer https://github.com/perrygeo/python-rasterstats/issues/98

#zonal statistics
stats=zonal_stats(shp, tif_array_flipped , affine=affine, stats=["max"],all_touched=True) #se asignan los valores maximos en la intersección con el shapefile
stats = pd.DataFrame(stats)
shp['max'] = stats['max']
shp.to_file(filename=path + 'Varios\\Bulk_zonal.shp')
#shp2=shp[["fid", "nunivotcda","cocursodag","cocdadesag", "max"]]
#shp2.to_csv(path2 + años[i] + Param_label_ODS632[j] + '_zonal.csv')

#importar erosión material parental
shp2 = gpd.read_file(path + "3_Zonal_Statistics_backup\\Zonal_P4_2014.shp")

#operación
bulkdensity = shp['max']
ErosionTNperHa =bulkdensity * 1/(270*270/1000) * shp2['_max']
shp['ErosionTNperHa']= ErosionTNperHa
shp.to_file(filename=path + 'Varios\\Bulk_zonal.shp')
