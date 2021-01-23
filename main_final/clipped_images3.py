# -*- coding: utf-8 -*- 

from osgeo import gdal, ogr, osr
import os, sys

def image_clipped_AOI(band_list, bands_folder_path, sid, AOI_clip):
	
	#los raster y los shp (AOI) tienen que estar en la misma proyección
	#TODO: Debería crear la carpeta clipped_images

	for band_name in band_list:
		#CREA NOMBRE DE LOS CLIPS
		image_outclip_name = band_name[:-4] + '_clip' + band_name[-4:]

		imageclip_outpath = os.path.join(bands_folder_path, 'clipped_images_' + str(sid), image_outclip_name)
		print ('Banda en %s clipeada a %s\n') %(os.path.join(bands_folder_path, band_name), os.path.join(bands_folder_path, 'clipped_images_' + str(sid), image_outclip_name))

		# imagesclip_pathlist.append(imageclip_outpath)

		# if format_out == '.tif':
		format_gdal_out = 'GTiff'
		print ('Envelope:\n')
		print (AOI_clip)
		#CLIPEA LOS .TIF
		gdal.Translate(imageclip_outpath, os.path.join(bands_folder_path, band_name),
			format = format_gdal_out,
			#TODO:
			# projWin =[ -3.798980, 43.042195, -3.404507, 42.898601],
			projWin = [AOI_clip[0], AOI_clip[3], AOI_clip[1], AOI_clip[2]],
			# projWin = [AOI_clip[0], AOI_clip[2], AOI_clip[1], AOI_clip[3]],
			projWinSRS = 'EPSG:4326')