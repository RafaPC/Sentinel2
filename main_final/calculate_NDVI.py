# -*- coding: utf-8 -*- 

# Filename: calculate_NDVI.py
# Authors: David Gabella Merino & Gonzalo Prieto Ciprian
# Date: January 27, 2021
# Description: calculate NDVI index from Sentinel 2 bands 4(red) 8(nir)


try:
    import os
    import sys
    from osgeo import ogr, gdal 
    from gdalconst import *
    import numpy as np

except ImportError:
    import os
    import sys
    import ogr, gdal
    from gdalconst import *
    import numpy as np

def calculate_NDVI(workspace, red_band_name, nir_band_name,
                   output_filename='NDVI.tif'):

    try:
        os.path.exists(workspace)
        os.chdir(workspace)
        
        #path where will be stored the ndvi image
        ndvi_path = os.path.join(workspace, output_filename)

        #build nir and red paths from workspace + bands_name_list + clip-end
        red_band_path = os.path.join(workspace,
                                    red_band_name[:-4] + '_clip.tif')
        nir_band_path = os.path.join(workspace,
                                     nir_band_name[:-4] + '_clip.tif')
        
        if not output_filename.endswith('.tif'):
            print('Output_filename must end with .tif')
            sys.exit(1)

        #open red and nir bands
        red_band = gdal.Open(red_band_path, GA_ReadOnly)
        nir_band = gdal.Open(nir_band_path, GA_ReadOnly)
        #nir and red bands have the same characteristics
        
        #gets transform and projection to setting ndvi image
        transform = red_band.GetGeoTransform()
        proj = red_band.GetProjection()

        #gets image size
        rows = red_band.RasterYSize
        columns = red_band.RasterXSize
        
        print ('Rows: {} Columns: {}'.format(rows, columns))
        
        #creates an output image with red band charts and 1 band, 
        driver = gdal.GetDriverByName('GTiff')
        NDVI = driver.Create(output_filename, columns, rows, 1, GDT_CFloat64)
        ndvi_band = NDVI.GetRasterBand(1)
        NDVI.SetGeoTransform(transform)
        NDVI.SetProjection(proj)
        ndvi_band.SetNoDataValue(-99)

        #read data
        red_data = red_band.ReadAsArray(0, 0, columns,
                                        rows).astype(np.float64)

        nir_data = nir_band.ReadAsArray(0, 0, columns,
                                        rows).astype(np.float64)
        
        #calculates NDVI
        #NDVI = (NIR — RED)/(NIR + RED) #SENTINEL2: RED - B4 ; NIR - B8
        #if you want use LANDSAT8: RED - B4 ; NIR - B5
        mask = np.greater(red_data + nir_data, 0)
        ndvi = np.choose(mask, (-99, (nir_data-red_data)
                                / (nir_data+red_data)))
        
        #writes data on the out-band
        ndvi_band.WriteArray(ndvi)
        print('_' * 15) 
        
        return ndvi_path
    
    except IOError as ioe:
        print("Directory doesn't exist") 
        print(ioe)
    except Exception as e:
        print(e)