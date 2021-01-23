# -*- coding: utf-8 -*- 

from osgeo import gdal
import os

def image_clipped_AOI(band_list, bands_folder_path, sid, AOI_clip):
	
	#los raster y los shp (AOI) tienen que estar en la misma proyección
	for band_name in band_list:
		#CREA NOMBRE DE LOS CLIPS
		image_outclip_name = band_name[:-4] + '_clip' + band_name[-4:]

		imageclip_outpath = os.path.join(bands_folder_path, 'clipped_images_' + str(sid), image_outclip_name)

		print ('Envelope:\n')
		print (AOI_clip)
		#CLIPEA LOS .TIF
		gdal.Translate(imageclip_outpath, os.path.join(bands_folder_path, band_name),
			format = 'GTiff',
			projWin = [AOI_clip[0], AOI_clip[3], AOI_clip[1], AOI_clip[2]],
			projWinSRS = 'EPSG:4326')