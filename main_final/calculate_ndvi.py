# -*- coding: utf-8 -*- 

# Archivo: ejercicio1P6_p2.py
# Autor: David Gabella Merino
# Fecha: 16 de enero de 2021
# Descripcion: calcula el índice NDVI a partir de las bandas 4 y 8 de Sentinel2


try:
	import os, sys, time
	from osgeo import ogr, gdal 
	from gdalconst import *
	import numpy as np

except ImportError:
	import os, sys, time
	import ogr, gdal
	from gdalconst import *
	import numpy as np




def calculate_NDVI(workspace, red_band_name, nir_band_name,
				   output_filename='NDVI.tif'):

	try:
		os.path.exists(workspace)
		os.chdir(workspace)

		red_band_path = os.path.join(workspace, red_band_name[:-4] + '_clip.tif')
		nir_band_path = os.path.join(workspace, nir_band_name[:-4] + '_clip.tif')
		
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
		
		#creates an output image
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
		mask = np.greater(red_data + nir_data, 0)
		ndvi = np.choose(mask, (-99, (nir_data-red_data)
								/ (nir_data+red_data)))
		#NDVI = (NIR — RED)/(NIR + RED)
		#LANDSAT8: RED - B4 ; NIR - B5
		
		#writes data on the out-band
		ndvi_band.WriteArray(ndvi)
		print('_' * 15) 
	
	except IOError as ioe:
		print("Directory doesn't exist") 
		print(ioe)
	except Exception as e:
		print(e)