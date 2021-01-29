# -*- coding: utf-8 -*- 

# Filename: download_sentinel2_images.py
# Authors: David Gabella Merino & Gonzalo Prieto Ciprian
# Date: January 27, 2021
# Description: Sentinel-2 imagery download through sentinelsat API from SCIHUB

try:
	import os
	import time
	from datetime import date
	import sentinelsat

except ImportError:
	import os
	import time
	from datetime import date
	import sentinelsat


def download_sentinel2_images(workspace, dic_AOI):
	
	"""   
	Sentinel-2 API connection, query based URI construction for selected product downloading
	through OData and OpenSearch API's usage.
	
	dic_AOI = AOI's 'SID' will be keys
	 		  Database AOI's geometry will be values
	
	"""
	
	os.chdir(workspace)

	# API calling, logging
	api = sentinelsat.SentinelAPI('gonzalogis', 'iwc.w6mEMp84Fj4', 'https://scihub.copernicus.eu/dhus')
	idList = []
	dic_SidZip={}
	# 'Downloads'folder existance checking, creation if false
	if os.path.exists(os.path.join(workspace, 'Downloads')) is False:
		os.mkdir(os.path.join(workspace, 'Downloads'))
		
	# Main iteration in which the rest will be based
	# Geometry assignment through dictionary key's iteration
	for sid in dic_AOI:
		geom = dic_AOI[sid]
		print (geom)


	# API server connection trial
	# Attempts spaced by time.sleep() due to server error
		tries = 0
		responseOK = False
		while responseOK is False and tries < 3:

	# List of spatial relationships to use:

	# # area_relation ({'Intersects', 'Contains', 'IsWithin'}, optional) --
	# # What relation to use for testing the AOI. Case insensitive.
	# # Intersects: true if the AOI and the footprint intersect (default)
	# # Contains: true if the AOI is inside the footprint
	# # IsWithin: true if the footprint is inside the AOI

	# Search based on geometry, date and SciHub query keywords
	# Order_by attribute, indicating '+' (by default) or '-' for ascending/descending ordering
			try: 
				# OpenSearch API query-based URI creation
				products_list = api.query(geom,
										date=('NOW-20DAY', 'NOW'),
										platformname='Sentinel-2',
										cloudcoverpercentage=(0, 90),
										# Smallest size product ordering for processing efficiency management
										order_by= ('size, cloudcoverpercentage'))
				responseOK = True		
										# Search returns list (of dictionaries) of available matching products

			# SentinelSat API Server connection error catching
			except sentinelsat.SentinelAPIError as exception:
				tries += 1
				mesgError = exception.response.json()['feed']['error']['message']
				print (exception.msg , mesgError)

			if tries < 3 and responseOK is False:
					time.sleep(3.0)

			# First product 'ID' selection from returned list
			if responseOK is True:    
				print ("Total de imagenes validas para la parcela ", sid,\
					"encontrados: ", len(products_list))
				# First list product (dictionary of a product) selection (most recent date)
				id = list(products_list.keys())[0]
				# "filename" will be value taken from product key 'filename'
				filename = products_list[id]["filename"]

				# If 'ID' has already been downloaded redundant process is avoided
				# New 'ID' + Already Dowloaded Image adding as new pair in dic_SidZip
				if id in idList:
					print ("para la parcela {} la id {} esta repetida".format(sid, id))
					dic_SidZip[sid] = filename
					continue

				# Non preexisting 'ID', and 'SID' will be saved as new pair in dic_SidZip
				else:
					idList.append(id)
					dic_SidZip[sid] = filename
				print ('ID: ', id)
				
				# OData API product downloading
				respuesta = api.download(id, os.path.join(workspace, 'Downloads'))
				print (respuesta)
				
				print ('Descarga Completada del archivo con ID {} \npara la parcela {}'.format(id, sid))
			else:
				print ("La parcela {} no se ha podido descargar".format(sid))
				continue

	# Dictionary returned will be 'SID' (keys) and 'filename' (values) obtained from OpenSearch API dictionary
	return    dic_SidZip