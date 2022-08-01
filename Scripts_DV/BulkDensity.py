def  ErosionClase(input_bulkdensity,input_OttonivelX,output_path,año,variable):

    #Convertir tif de densidad aparente de soilgrids a polygono Pfastetter
    import rasterio
    from affine import Affine
    from rasterstats import zonal_stats
    import numpy as np
    import geopandas as gpd
    import pandas as pd

    #importar archivos
    tif = rasterio.open(input_bulkdensity)
    shp = gpd.read_file(input_OttonivelX)

    #adecuar raster a numpy
    tif_array = tif.read(1)
    tif_array_flipped = np.flipud(tif_array)
    affine=tif.transform #usar este affine
    new_affine2 = Affine(affine.a, affine.b, affine.c,affine.d, affine.e*-1, affine.f + (affine.e * (tif.read(1).shape[0]-1))) # leer https://github.com/perrygeo/python-rasterstats/issues/98

    #zonal statistics
    stats=zonal_stats(shp, tif_array_flipped , affine=affine, stats=["max"],all_touched=True) #se asignan los valores maximos en la intersección con el shapefile
    stats = pd.DataFrame(stats)
    shp['max'] = stats['max']
    shp.to_file(filename=output_path + variable + '_ErosionRate_' + año + '.shp')
    #shp2=shp[["fid", "nunivotcda","cocursodag","cocdadesag", "max"]]
    #shp2.to_csv(path2 + años[i] + Param_label_ODS632[j] + '_zonal.csv')

    #importar erosión material parental
    shp2 = gpd.read_file(output_path + "ErosionRate.shp")

    #operación
    bulkdensity = shp['max']
    ErosionTNperHa =bulkdensity * 1/(270*270/1000) * shp2['_max']
    shp['ErosionTNperHa']= ErosionTNperHa*-1
    shp.to_file(filename=output_path + variable + '_ErosionRate_' + año + '.shp')

    Clasificacion = {'Class': ['Muy leve', 'Ligero', 'Moderado', 'Alto', 'Severo', 'Muy severo', 'Catastrófico'],
                    'Erosion rate (t/ha)': ['<2','2–5','5–10','10–50','50–100','100–500','>500']}

    df3 = pd.DataFrame()
    shp.loc[shp['ErosionTNperHa'].le(2), 'Ratio Erosion'] = 'Muy leve'
    shp.loc[shp['ErosionTNperHa'].ge(2) & shp['ErosionTNperHa'].le(5), 'Ratio Erosion'] = 'Ligero'
    shp.loc[shp['ErosionTNperHa'].ge(5) & shp['ErosionTNperHa'].le(10), 'Ratio Erosion'] = 'Moderado'
    shp.loc[shp['ErosionTNperHa'].ge(10) & shp['ErosionTNperHa'].le(50), 'Ratio Erosion'] = 'Alto'
    shp.loc[shp['ErosionTNperHa'].ge(50) & shp['ErosionTNperHa'].le(100), 'Ratio Erosion'] = 'Severo'
    shp.loc[shp['ErosionTNperHa'].ge(100) & shp['ErosionTNperHa'].le(500), 'Ratio Erosion'] = 'Muy severo'
    shp.loc[shp['ErosionTNperHa'].ge(500), 'Ratio Erosion'] = 'Catastrófico'
    shp.to_file(filename=output_path + variable + '_ErosionRate_' + año + '.shp')

