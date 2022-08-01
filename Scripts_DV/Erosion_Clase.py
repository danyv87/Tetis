import os, re
from Scripts_DV.BulkDensity import ErosionClase

# set paths
ouput_path = "C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\ErosionRate\\"
tif = "C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Tetis_InputsRecalculados\\bulk_UTM.tif"
shp = "C:\\Users\\danielal\\OneDrive - ITAIP Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Varios\\Ottopfasteter nivel 10.shp"

list = os. listdir('C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Tetis_Outputs')

for i in list:
    añostr = re.search(r'(?<=_)\w+', i)
    año = añostr[0][0:4]
    variable = i[0][0:3]
    ErosionClase(tif,shp,output_path,año,variable)