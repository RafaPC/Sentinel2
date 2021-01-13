# -*- coding: utf-8 -*- 

# Archivo: ejercicio1P6_p2.py
# Autor: David Gabella Merino
# Fecha: 13 de diciembre de 2020
# Descripcion: calcula el índice NDVI a partir de un raster.tif

import os, sys, time
from osgeo._gdal import GetDriverByName

try:
    from osgeo import ogr, gdal 
    from gdalconst import *
    import numpy as np

except ImportError:
    import ogr, gdal
    from gdalconst import *
    import numpy as np

"paquete utils para obtener el tamaño"
"HACER UN IF banda.GetSizeBlock > size > leer por bloque; sino leer linea"



def calculate_NDVI(workspace, file_raster, output_filename='NDVI.tif',
                   red_band = 4, nir_band = 5):

    try:
        os.path.exists(workspace)
        os.chdir(workspace)
        
        if not os.path.exists(file_raster):
            print ("Doesn't exist this file: {} ".format(file_raster))
            sys.exit(1)
        
        if not output_filename.endswith('.tif'):
            print('Output_filename must end with .tif')
            sys.exit(1)
        
        if not type(red_band) and type(nir_band) == int:
            print('red_band and nir_band must be integer')
            print("They're the band number that matches red and nir in {}"
                  .format(file_raster))
            sys.exit(1)
            
        raster_dataset = gdal.Open(file_raster, GA_ReadOnly)
        transform = raster_dataset.GetGeoTransform()
        proj = raster_dataset.GetProjection()
    
        if raster_dataset is None:
            print ('Cannot open file {}'.format(file_raster))
            sys.exit(1)
            
        #gets image size
        rows = raster_dataset.RasterYSize
        columns = raster_dataset.RasterXSize
        n_bands = raster_dataset.RasterCount
        
        print ('Rows: {} Columns: {} Number of bands: {}'.format(rows, columns,
                                                                n_bands))
        
        #creates an output image
        driver = GetDriverByName('GTiff')
        NDVI = driver.Create(output_filename, columns, rows, 1, GDT_CFloat64)
        ndvi_band = NDVI.GetRasterBand(1)
        NDVI.SetGeoTransform(transform)
        NDVI.SetProjection(proj)
        ndvi_band.SetNoDataValue(-99)
        
        print('****')
        
        red_band_n = raster_dataset.GetRasterBand(int(red_band)) #bands indexed from 1
        nir_band_n = raster_dataset.GetRasterBand(int(nir_band))
        
        block_Xsize, block_Ysize = red_band_n.GetBlockSize()
        print('Block size: x {} y {}'.format(1, block_Xsize, block_Ysize))
        
        input('*')
        for i in range(0, rows, block_Ysize):
            
            if i + block_Ysize < rows:
                rows_to_read = block_Ysize
            else:
                rows_to_read = rows - i 
                
            for j in range(0, columns, block_Xsize):
                
                if j + block_Xsize < columns:
                    columns_to_read = block_Xsize
                    
                else:
                    columns_to_read = columns - j
        
                #read data
                red_data = red_band_n.ReadAsArray(j, i, columns_to_read,
                                        rows_to_read).astype(np.float64)
                
                nir_data = nir_band_n.ReadAsArray(j, i, columns_to_read,
                                        rows_to_read).astype(np.float64)
                
                #calculates NDVI
                mask = np.greater(red_data + nir_data, 0)
                ndvi = np.choose(mask, (-99, (nir_data-red_data)
                                        / (nir_data+red_data)))
                #NDVI = (NIR — RED)/(NIR + RED)
                #LANDSAT8: RED - B4 ; NIR - B5
                
                #writes data on the out-band
                ndvi_band.WriteArray(ndvi, j, i)
                print('#'*10, i, j) 
        
        NoData = ndvi_band.GetNoDataValue()
        print ('NDVI NoData values = {}'.format(NoData))
    
    except IOError as ioe:
        print("Directory doesn't exist") 
        print(ioe)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    calculate_NDVI(sys.argv[1], sys.argv[2], sys.argv[3],
               sys.argv[4], sys.argv[5])
