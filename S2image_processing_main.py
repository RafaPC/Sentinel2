# -*- coding: utf-8 -*- 

# Filename: S2image_processing_main.py
# Date: January 27, 2021
# Description:
# 1. Gets Areas of Interest (AOI) from PostGIS DB and store in dic{sid:geom}
# 2. Downloads Sentinel2 images of AOI using sentinelsat API from SCIHUB
# 3. Unzip file and tranform its format (default .jp2 >> .tif)
# 4. Creates shp from AOI and gets envelope (minLon, maxLon, minLat, maxLat)
# 5. Clip images.tif with envelope
# 6. Calculates NDVI  from clipped images
# 7. Sends to PostGIS DB the NDVI and other images ***NOT FUNCTIONAL YET***

# Way to get to the folder with the images (example):

# Downloads >> S2A_MSIL2A_...01.SAFE >> S2A_MSIL2A_...01.SAFE >> GRANULE >>
# L2A_T30...47 >> IMG_DATA >> R10m >> bands.fit_folder >> clipped_images_1
# A new 'clipped_images_X' will be created for each AOI using a same Sentinel-2 product

import os
from getAOI import getAOI
from download_sentinel2_images import download_sentinel2_images
from unzip_transform import unzip_transform
from get_shp_envelope import get_shp_envelope
from clip_bands import image_clipped_AOI
from calculate_NDVI import calculate_NDVI
from send_postgis import send_postgis


# Workspace should be read from input
workspace = 'F:/Sentinel/SHP'


# 1. Area of Interest (AOI) taking from postGIS DB and Dictionary storing {sid:geom}
dic_AOI = getAOI()

# Same Dictionary that should be returned by getAOI is down below, 
# commented, so no connection with DB is needed
# dic_AOI = {7: 'MULTIPOLYGON(((-4.50559645530908 40.7086153317464,-4.47387022241673 40.7135866470223,-4.46411461075216 40.7124681334455,-4.4620651125033 40.7098581953612,-4.4656722294213 40.6961854197893,-4.47075498507847 40.6909020048112,-4.47255854353747 40.6905912026476,-4.47526388122596 40.694134261375,-4.50092359930168 40.6918344026038,-4.51133505040589 40.7019656173812,-4.50559645530908 40.7086153317464)))', 8: 'MULTIPOLYGON(((-4.5310102335949 40.7418384155896,-4.505760415169 40.7435775497543,-4.50756397362799 40.7361237974477,-4.52641935751747 40.7285449597278,-4.54347118294795 40.7309056738799,-4.54150366462905 40.7391053985976,-4.5310102335949 40.7418384155896)))', 5: 'MULTIPOLYGON(((-4.32647030835908 40.7261220344342,-4.28843162086032 40.7231398514352,-4.27597067150727 40.7082269321096,-4.34483381266883 40.6868459225951,-4.36582067473712 40.7057411207912,-4.36778819305602 40.722145760741,-4.32647030835908 40.7261220344342)))', 6: 'MULTIPOLYGON(((-1.99795336790392 42.5048112687524,-1.96975227199967 42.508679135872,-1.96057051984479 42.4982837003202,-1.9645055564826 42.485226519035,-1.97860610443472 42.4707153429042,-2.00123256510209 42.481115360785,-2.01008639753715 42.4973165951864,-1.99795336790392 42.5048112687524)))', 3: 'MULTIPOLYGON(((-1.95171668740973 42.4893374071352,-1.94810957049175 42.4987672472783,-1.92745062814328 42.4941734002052,-1.92187599290639 42.481599040483,-1.929746066182 42.4702315790789,-1.9549958846079 42.4673289176097,-1.95860300152589 42.4704734614589,-1.95171668740973 42.4893374071352)))', 4: 'MULTIPOLYGON(((-3.80216766633676 42.7781580335008,-3.78216456342793 42.7827309634102,-3.76937569435507 42.7716590784327,-3.77560616903159 42.7608259710666,-3.79626511138006 42.7586591222595,-3.81298901709072 42.7639557300081,-3.80216766633676 42.7781580335008)))', 1: 'MULTIPOLYGON(((-3.79167423530262 42.7839343098834,-3.75494722668312 42.7796021531174,-3.75789850416147 42.7608259710666,-3.77593408875141 42.7564921976755,-3.79790470997914 42.7682889813751,-3.80446310437548 42.7774359610623,-3.79167423530262 42.7839343098834)))', 2: 'MULTIPOLYGON(((-3.78037045350324 42.7835826393944,-3.78145154646088 42.7849864030543,-3.76922687993987 42.7845591740057,-3.77030797289751 42.7819957377979,-3.78037045350324 42.7835826393944)))'}


# 2. Sentinel-2 imagery download for AOI using sentinelsat API from SCIHUB
zip_path_list = download_sentinel2_images(workspace, dic_AOI)

for sid in zip_path_list:

	# 3. Downloaded products unzip and bands format transformation (default .jp2 >> .tif)
	bands_names_list, bands_folder_path, bands_path_list = unzip_transform(
															workspace,
															zip_path_list[sid])

	# 4. Envelope Shapefile creation based on AOI
	envelope = get_shp_envelope(bands_folder_path, sid, dic_AOI[sid])

	# 5. Envelope based clipping of '.tif' imagery
	image_clipped_AOI(bands_names_list, bands_folder_path, sid, envelope)

	print ("SID {} clips created in {}".format(sid, bands_folder_path))

	# Folder creation for clipped images storing
	clipped_folder = os.path.join(bands_folder_path,
									'clipped_images_'+ str(sid))
	# 6. NDVI Calculation based on '.tif' clipped imagery
	ndvi_path = calculate_NDVI(clipped_folder, bands_names_list[2],
												bands_names_list[3])
	# 7. Result bands sending to PostGIS DB *** NOT FUNCTIONAL YET ***
	#send_postgis(sid, ndvi_path)			***  WORK IN PROGRESS  ***

	print('\n *** IMAGE PROCESSING FINISHED FOR SID {0} *** \n'.format(sid))