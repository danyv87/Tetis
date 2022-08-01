import os, re
from Scripts_DV.BulkDensity import ErosionClase

# set paths
output_path = "C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Tetis_ErosionRate\\"
tif = "C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Tetis_InputsRecalculados\\bulk_UTM.tif"
shp = "C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Varios\\Ottopfasteter nivel 10.shp"
path1 = "C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\3_Zonal_Statistics_backup\\"

list = os. listdir('C:\\Users\\danielal\\OneDrive - ITAIPU Binacional\\CIH\\Proyectos\\Modelacion Ecohidrologica\\Proyecto_QGIS\\Tetis_Incremental\\layers\\Tetis_Outputs')

for i in list:
    año = re.search(r'(?<=_)\w+', i)[0][0:4]
    variable = i.rpartition('_')[0]
    if variable == "P4":
        ErosionClase(tif,shp,output_path,año,variable,path1)
