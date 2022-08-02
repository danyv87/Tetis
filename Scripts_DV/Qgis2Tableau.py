#######################################################
# convertir asc to csv point
# from osgeo import gdal
# import os
#
# path_asc='C:/Users/ASUS/Downloads/Proyecto_QGIS/Tetis_Incremental/layers/Validacion 2017-2020/'
#
# filename=path_asc + 'P4_201712312359.asc'
# inDs = gdal.Open(filename)
# outDs = gdal.Translate('{}.xyz'.format(filename), inDs, format='XYZ', creationOptions=["ADD_HEADER_LINE=YES"])
# outDs = None
# try:
#     os.remove('{}.csv'.format(filename))
# except OSError:
#     pass
# os.rename('{}.xyz'.format(filename), '{}.csv'.format(filename))
#os.system('ogr2ogr -f "ESRI Shapefile" -oo X_POSSIBLE_NAMES=X* -oo Y_POSSIBLE_NAMES=Y* -oo KEEP_GEOM_COLUMNS=NO {0}.shp {0}.csv'.format(filename))


########################################################
## convertir outputs de qgis en excel para tableau
import csv
import pandas as pd
import glob, re
from collections import Counter

path_asc='C:/Users/ASUS/Downloads/Proyecto_QGIS/Tetis_Incremental/layers/2_Ascii_Out_Tetis/'
path_out= 'C:/Users/ASUS/Downloads/Proyecto_QGIS/Tetis_Incremental/layers/3_Zonal_Statistics/'
path_tableau= 'C:/Users/ASUS/Downloads/Proyecto_QGIS/Tetis_Incremental/layers/4_Tableau/'

list_=glob.glob(path_out + '*.xlsx')
#list_2=glob.glob(path_asc + '*.asc')

WS1 = pd.read_excel(list_[0])
WS1['anho']=list_[0][-9:-5]
WS1['variable']=list_[0][list_[0].find('csv_zonal_')+10:-9]
for x in range(1,len(list_)):
    WS2 = pd.read_excel(list_[x])
    WS2['anho'] = list_[x][-9:-5]
    WS2['variable'] = list_[x][list_[0].find('csv_zonal_') + 10:-9]
    print(x)
    WS1 = WS1.append(WS2,ignore_index=True)
    #WS1 = WS1.append(WS2, ignore_index=True)

WS1.to_csv(path_tableau+'P4_tableau.csv')

import os, shutil
folder = path_out
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))