def  pedotransferencia(sand,clay,OM,banda,outSAT,outFC,outSatCond,outPAW):
    from osgeo import gdal
    import numpy
    #funcion de pedotransferencia

    directory_path = 'C:\\Users\\ASUS\\OneDrive\\Documents\\CIH\\Tetis\\'
    pathsand= directory_path + str(sand) #sand_utm.tif
    inDs = gdal.Open(pathsand)
    driver = inDs.GetDriver()
    S = inDs.GetRasterBand(banda)
    S = S.ReadAsArray()
    S = S.astype(numpy.float)/1000

    pathclay= directory_path + str(clay) #clay_utm.tif
    inDs = gdal.Open(pathclay)
    driver = inDs.GetDriver()
    C = inDs.GetRasterBand(banda)
    C = C.ReadAsArray()
    C = C.astype(numpy.float)/1000

    pathOM = directory_path + str(OM)  # clay_utm.tif
    inDs = gdal.Open(pathOM)
    driver = inDs.GetDriver()
    OM = inDs.GetRasterBand(banda)
    OM = OM.ReadAsArray()
    OM = OM.astype(numpy.float)/10000

    DF = 1

    # MoistYre Regressions
    O1500t = -0.024 * S + 0.487 * C + 0.006 * OM + 0.005 * (S * OM) - 0.013 * (C * OM)
    O1500 = O1500t + 0.14 * O1500t - 0.02

    O33t = -0.251 * S + 0.195 * C + 0.011 * OM + 0.006 * (S * OM) - 0.027 * (C * OM) + 0.452 * (S * C) + 0.299
    O33 = O33t + 1.283 * numpy.power(O33t, 2) - 0.374 * O33t - 0.015

    OS33t = 0.278 * S + 0.034 * C + 0.022 * OM - 0.018 * (S * OM) - 0.027 * (C * OM) - 0.584 * (S * C) + 0.078
    OS33 = OS33t + 0.636 * OS33t - 0.107

    Yet = -21.67 * S - 27.93 * C - 81.97 * OS33 + 71.12 * (S * OS33) + 8.29 * (C * OS33) + 14.05 * (S * C) + 27.16
    Ye = Yet + 0.02 * numpy.power(Yet, 2) - 0.113 * Yet - 0.70

    OS = O33 + OS33 - 0.097 * S + 0.043

    pN = (1 - OS) * 2.65  # Normal density, g/cc

    # Density AdjYstments
    pDF = pN * DF  # Adjusted density, g/cc
    OSDF = 1 - (pDF / 2.65)
    O33DF = O33 - 0.2 * (OS - OSDF)
    OS33DF = OSDF - O33DF

    # tension - moistYre
    O = OS
    B = (numpy.log(1500) - numpy.log(33)) / (numpy.log(O33) - numpy.log(O1500))
    A = numpy.exp(numpy.log(33) + B * numpy.log(O33))
    YO = A * numpy.power(O, (-B))
    YO = 33.0 - ((O - O33) * (33.0 - Ye / (OS - O33)))

    # MoistYre - CondYctivity
    J = 1 / B
    KS = 1930 * numpy.power((OS - O33), (3 - J))  # Saturated conductivity
    # KO = KS*numpy.power((O/OS),(3+2/J)) #Unsaturated conductivity at moisture ?, mm/hr

    SAT = OS * 100
    FC = O33 * 100
    SatCond = KS
    WP=O1500 * 100
    PAW=(FC-WP)/100

    pathSAT=str(directory_path)+str(outSAT)
    outDatasetSAT = driver.Create(pathSAT,inDs.RasterXSize,inDs.RasterYSize,1,gdal.GDT_Float32)

    pathFC=str(directory_path)+str(outFC)
    outDatasetFC = driver.Create(pathFC,inDs.RasterXSize,inDs.RasterYSize,1,gdal.GDT_Float32)

    pathSatCond=str(directory_path)+str(outSatCond)
    outDatasetSatCond = driver.Create(pathSatCond,inDs.RasterXSize,inDs.RasterYSize,1,gdal.GDT_Float32)

    pathPAW=str(directory_path)+str(outPAW)
    outDatasetPAW = driver.Create(pathPAW,inDs.RasterXSize,inDs.RasterYSize,1,gdal.GDT_Float32)

    outDatasetSAT.SetGeoTransform(inDs.GetGeoTransform())
    outDatasetSAT.SetProjection(inDs.GetProjection())

    outDatasetFC.SetGeoTransform(inDs.GetGeoTransform())
    outDatasetFC.SetProjection(inDs.GetProjection())

    outDatasetSatCond.SetGeoTransform(inDs.GetGeoTransform())
    outDatasetSatCond.SetProjection(inDs.GetProjection())

    outDatasetPAW.SetGeoTransform(inDs.GetGeoTransform())
    outDatasetPAW.SetProjection(inDs.GetProjection())

    outbandSAT = outDatasetSAT.GetRasterBand(1)
    outbandSAT.SetNoDataValue(0)
    outbandSAT.WriteArray(SAT)
    outbandSAT.FlushCache()

    outbandFC = outDatasetFC.GetRasterBand(1)
    outbandFC.SetNoDataValue(0)
    outbandFC.WriteArray(FC)
    outbandFC.FlushCache()

    outbandSatCond = outDatasetSatCond.GetRasterBand(1)
    outbandSatCond.SetNoDataValue(0)
    outbandSatCond.WriteArray(SatCond)
    outbandSatCond.FlushCache()

    outbandPAW = outDatasetPAW.GetRasterBand(1)
    outbandPAW.SetNoDataValue(0)
    outbandPAW.WriteArray(PAW)
    outbandPAW.FlushCache()

    del FC
    del SAT
    del SatCond
    del PAW

def CalcprofRaiz(usodesuelo):
    from osgeo import gdal
    import numpy as np
    # Uso de suelo a profundidad de raiz

    directory_path = 'C:\\Users\\ASUS\\OneDrive\\Documents\\CIH\\Tetis\\'
    pathusodesuelo = directory_path + str(usodesuelo)  # nombre raster uso de suelo

    inDs = gdal.Open(pathusodesuelo)
    driver = inDs.GetDriver()
    S = inDs.GetRasterBand(1)
    S = S.ReadAsArray()
    S = S.astype(np.float)

    Usosuelo = [1, 'agua', 0], \
               [2, 'cultivo de regadio', 1.5], \
               [3, 'cultivo secano', 1.3], \
               [4, 'infraestructura urbana', 0], \
               [5, 'cobertura forestal', 1]

    S[S == 1] = 0
    S[S == 2] = 1.5
    S[S == 3] = 1.3
    S[S == 4] = 0
    S[S == 5] = 1
    S[S < 0] = np.nan

    pathCobveg = str(directory_path) + '/ProfRaices.tif'
    outDatasetCobveg = driver.Create(pathCobveg, inDs.RasterXSize, inDs.RasterYSize, 1, gdal.GDT_Float32)

    outDatasetCobveg.SetGeoTransform(inDs.GetGeoTransform())
    outDatasetCobveg.SetProjection(inDs.GetProjection())

    outbandCobveg = outDatasetCobveg.GetRasterBand(1)
    outbandCobveg.SetNoDataValue(-9999)
    outbandCobveg.WriteArray(S)
    outbandCobveg.FlushCache()

    del S

def calalmcharcos(usodesuelo):
    from osgeo import gdal
    import numpy as np
    # Uso de suelo a almacenamiento en charcos

    directory_path = 'C:\\Users\\ASUS\\OneDrive\\Documents\\CIH\\Tetis\\'
    pathusodesuelo = directory_path + str(usodesuelo)  # nombre raster uso de suelo

    inDs = gdal.Open(pathusodesuelo)
    driver = inDs.GetDriver()
    S = inDs.GetRasterBand(1)
    S = S.ReadAsArray()
    S = S.astype(np.float)

    Usosuelo = [1, 'agua', 0], \
               [2, 'cultivo de regadio', 6], \
               [3, 'cultivo secano', 6], \
               [4, 'infraestructura urbana', 0], \
               [5, 'cobertura forestal', 4]

    S[S == 1] = 0
    S[S == 2] = 6
    S[S == 3] = 6
    S[S == 4] = 0
    S[S == 5] = 4
    S[S < 0] = np.nan

    pathCobveg = str(directory_path) + '/AlmCharcos.tif'
    outDatasetCobveg = driver.Create(pathCobveg, inDs.RasterXSize, inDs.RasterYSize, 1, gdal.GDT_Float32)

    outDatasetCobveg.SetGeoTransform(inDs.GetGeoTransform())
    outDatasetCobveg.SetProjection(inDs.GetProjection())

    outbandCobveg = outDatasetCobveg.GetRasterBand(1)
    # outbandCobveg.SetNoDataValue(-99)
    outbandCobveg.WriteArray(S)
    outbandCobveg.FlushCache()

    del S

def rasterresolution(xRes,yRes):
    from osgeo import gdal
    import numpy
    # adecuar la resolucion espacial a 250m

    directory_path = 'C:\\Users\\ASUS\\OneDrive\\Documents\\CIH\\Tetis\\'
    pathSAT = str(directory_path) + 'SWAP-SAT.tif'
    pathFC = str(directory_path) + 'SWAP-FC.tif'
    pathaSatCond = str(directory_path) + 'SWAP-SatCond.tif'
    pathPAW = str(directory_path) + 'SWAP-PAW.tif'
    pathProfRaices = str(directory_path) + 'ProfRaices.tif'
    pathAlmCharcoss = str(directory_path) + 'AlmCharcos.tif'

    gdal.Warp(str(directory_path) + 'SAT_270.tif', pathSAT, xRes=xRes, yRes=yRes)
    gdal.Warp(str(directory_path) + 'FC_270.tif', pathFC, xRes=xRes, yRes=yRes)
    gdal.Warp(str(directory_path) + 'SatCond_270.tif', pathaSatCond, xRes=xRes, yRes=yRes)
    gdal.Warp(str(directory_path) + 'PAW_270.tif', pathPAW, xRes=xRes, yRes=yRes)
    gdal.Warp(str(directory_path) + 'ProfRaices_270.tif', pathProfRaices, xRes=xRes, yRes=yRes)
    gdal.Warp(str(directory_path) + 'AlmCharcos_270.tif', pathAlmCharcoss, xRes=xRes, yRes=yRes)

def rasterresolution2(Rasterin, Rasterout, xRes,yRes):
    from osgeo import gdal
    import numpy
    # adecuar la resolucion espacial a 270m

    directory_path = 'C:\\Users\\ASUS\\OneDrive\\Documents\\CIH\\Tetis\\'
    path = str(directory_path) + str(Rasterin)

    gdal.Warp(str(directory_path) + str(Rasterout), path, xRes=xRes, yRes=yRes)


def Almac_Estatico(PAW_270, ProfRaices_270,Hu):
    from osgeo import gdal
    import numpy
    import os
    #𝐻𝑢 = 𝐴𝑆 + 𝐴𝑇 ∙ 𝑚𝑖𝑛(𝑃𝑅; 𝑅𝑂𝑂)
    #𝐴𝑆 = 𝐴𝐶 + 𝐴𝐷

    directory_path = 'C:\\Users\\ASUS\\OneDrive\\Documents\\CIH\\Tetis\\'
    pathHu = directory_path + str(Hu)
    pathPAW = directory_path + str(PAW_270)
    pathProfRaices = directory_path + str(ProfRaices_270)

    gdalSrc = gdal.Open(pathHu)

    xmin = gdalSrc.GetGeoTransform()[0]
    ymin = gdalSrc.GetGeoTransform()[3] + gdalSrc.RasterYSize*gdalSrc.GetGeoTransform()[5]
    xmax = gdalSrc.GetGeoTransform()[0] + gdalSrc.RasterXSize*gdalSrc.GetGeoTransform()[1]
    ymax = gdalSrc.GetGeoTransform()[3]

    os.system("gdalwarp -te " + str(xmin) + " " + str(ymin) + " " + str(xmax) + " " + str(ymax) + " " + str(
        pathPAW) + " " + str(directory_path) + "PAW_cutted.tif" )
    os.system("gdalwarp -te " + str(xmin) + " " + str(ymin) + " " + str(xmax) + " " + str(ymax) + " " + str(
        pathProfRaices) + " " + str(directory_path) + "ProfRaices_cutted.tif")


    #AT = PAW * ProfRaices_270 * 100 * 10 #[cm/cm]*[m]*100*10 -> [mm]
    os.system("gdal_calc.py -A " + str(directory_path+"PAW_cutted.tif") + " -B " +str(
        directory_path+"ProfRaices_cutted.tif") + " --outfile=" +str(
        directory_path+"AT_270.tif") + " --calc=" + '"A*B*100*10"')

    #gdal_translate - of GTiff C:/Users/ASUS/OneDrive/Documents/CIH/Tetis/AT_270.tif C:/Users/ASUS/AppData/Local/Temp/processing_eZSKXw/8d9c2be1aa404618bdcc9588a7876fa4/OUTPUT.tif

def RasterWarp(RasterBase, Raster2clip, Outputname):
    from osgeo import gdal
    import numpy
    import os
    #Clip to raster extent for tetis

    directory_path = 'C:\\Users\\ASUS\\OneDrive\\Documents\\CIH\\Tetis\\'
    pathRasterBase = directory_path + str(RasterBase)
    pathRaster2clip = directory_path + str(Raster2clip)

    gdalSrc = gdal.Open(pathRasterBase)
    xmin = gdalSrc.GetGeoTransform()[0]
    ymin = gdalSrc.GetGeoTransform()[3] + gdalSrc.RasterYSize*gdalSrc.GetGeoTransform()[5]
    xmax = gdalSrc.GetGeoTransform()[0] + gdalSrc.RasterXSize*gdalSrc.GetGeoTransform()[1]
    ymax = gdalSrc.GetGeoTransform()[3]

    os.system("gdalwarp -te " + str(xmin) + " " + str(ymin) + " " + str(xmax) + " " + str(ymax) + " " + str(
        pathRaster2clip) + " " + str(directory_path) + str(Outputname))

def RasterFormat(rasterin, rasterout):
    from osgeo import gdal
    import numpy
    import os


    directory_path = 'C:\\Users\\ASUS\\OneDrive\\Documents\\CIH\\Tetis\\'
    pathsand= directory_path + str(rasterin)
    inDs = gdal.Open(pathsand)
    driver = inDs.GetDriver()
    S = inDs.GetRasterBand(1)
    S = S.ReadAsArray()
    S = S.astype(numpy.float)
    S1 = numpy.nan_to_num(S)

    path=str(directory_path)+rasterin[0:-4]+'_nonan.tif'
    outDataset = driver.Create(path,inDs.RasterXSize,inDs.RasterYSize,1,gdal.GDT_Float32)

    outDataset.SetGeoTransform(inDs.GetGeoTransform())
    outDataset.SetProjection(inDs.GetProjection())

    outband = outDataset.GetRasterBand(1)
    outband.WriteArray(S1)
    outband.FlushCache()

    del S1
    os.system('gdal_translate -of AAIGrid ' + str(directory_path)+rasterin[0:-4]+'_nonan.tif' + ' ' + directory_path+ str(rasterout))