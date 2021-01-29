# -*- coding: utf-8 -*- 

# Filename: unzip_transform.py
# Authors: David Gabella Merino & Gonzalo Prieto Ciprian
# Date: January 27, 2021
# Description: Sentinel-2 downloaded product unzip and format transformation (default .jp2 >> .tif)

try:
	import zipfile 
	import os
	from osgeo import gdal

except ImportError:
	import zipfile 
	import os
	from osgeo import gdal

def unzip_transform(workspace, zip_name, folder = 'R10m',
					format_in = '.jp2', format_out = '.tif',
					format_outclip = '.tif'):
	
	"""
	File unzip (path_zip = path_in + zip_name), folder search
	and format transformation of those containing '.jp2' to 'tif'
	format using gdal.Translate()
	
	Created files are saved into 'bands.tif_folder',
	in the same directory as  '.jp2' files
	
	zip_name = name of the .zip
	folder = folder where the .jp2 files to be transformed are located
	*default 'R10m' for Sentinel-2 image downloads
	
	Please, do use 'format_in' and 'format_out' in case different formats
	from default ones are desired
	
	"""
	# Path creation and '.zip' extraction
	path_zip = os.path.join(workspace, 'Downloads', zip_name)
	print('PATH ZIP \n {} \n'.format(path_zip)) 
	file_zip = zipfile.ZipFile(path_zip.replace('SAFE', 'zip'), 'r')
	file_zip.extractall(path = os.path.join(workspace, 'Downloads'))
	file_zip.close()

	# Variables declaration
	bands_names_list = []
	bands_path_list = []
	bands_folder_path = ""

	# Matching directories search
	for base, dirs, files in os.walk(path_zip):
		
		if base.endswith(folder):

			print('Root directory \n {} \n'.format(base)) 
			dir = os.listdir(base)
			print('This directory has {} files \n'.format(len(dir)))
			
			# macOS automatically created files removal
			if '.DS_Store' in dir:
				dir.remove('.DS_Store')

			try:
				# Folder creation
				bands_folder_path = os.path.join(base, 'bands.tif_folder')
				os.mkdir(bands_folder_path)
			except:
				print('The folder {} had already been created \n'.format(
														bands_folder_path)) 

			n_band = 1
			
			bands_to_transform = ['B02_10m.jp2', 'B03_10m.jp2',
								 'B04_10m.jp2', 'B08_10m.jp2', 'TCI_10m.jp2']

			# GDAL exceptions enabling
			gdal.UseExceptions()
			
			# Bands finding and transformation
			for band in dir:
				
				for selected in bands_to_transform:
					
					# If path ends with in one of bands which wants transform
					if band.endswith(selected):

						# creates image_.jp2 path
						image_in_path = os.path.join(base, band)
						
						# creates image out name and append to list
						image_out_name = band.replace(format_in, format_out)
						bands_names_list.append(image_out_name)
						
						# creates new image_.tif path 
						image_out_path = os.path.join(bands_folder_path,
													image_out_name)
						
						bands_path_list.append(image_out_path)
						
						if format_out == '.tif':
							format_gdal_out = 'GTiff'
						
						msg = '\n...transforming format of {0} to {1}...\n'
						
						print(msg.format(format_in, format_out))
						
						try:
							# File transformation using gdal.Translate()
							if os.path.exists(image_out_path) is False:
								gdal.Open(image_in_path)
								gdal.Translate(image_out_path,
											image_in_path,
											format = format_gdal_out)
								
								print('{} transformation done \n'.format(n_band))
								n_band += 1
						except Exception as e:
							print('Transformated band already existed')
				bands_names_list.sort()
			print('All transformations have been completed')
			print('\n List of items: \n')
			print(bands_names_list)
			
			
			
	return bands_names_list, bands_folder_path, bands_path_list