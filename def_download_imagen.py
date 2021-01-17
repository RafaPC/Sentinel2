# Sentinel Web Login:
# user: gonzalogis
# pass: iwc.w6mEMp84Fj4

# -*- coding: utf-8 -*-

import os
import sentinelsat
from datetime import date
import time




def download_sentinel2_images(dic_AOI):
	workspace = r'C:\Users\rafit\Desktop\Sentinel\SHP'
	os.chdir(workspace)

	# Llamada a la API, logging
	api = sentinelsat.SentinelAPI('gonzalogis', 'iwc.w6mEMp84Fj4', 'https://scihub.copernicus.eu/dhus')
	idList = []
	dic_SidZip={}
	# Comprobamos si existe una carpeta de descargas, para crearla en caso negativo
	if os.path.exists(os.path.join(workspace, 'descargas')) is False:
		os.mkdir(os.path.join(workspace, 'descargas'))

	# Iteramos sobre cada clave (parcela) de diccionario, asignando su geometría a la variable
	for sid in dic_AOI:
		geom = dic_AOI[sid]
		print (geom)


	# Intentamos conexion de llamada al servidor de la API
	# Establecemos intentos (que podemos espaciar con time.sleep()) 
	# Porque en ocasiones si el servidor esta muy solicitado, da problema de conexion
		tries = 0
		responseOK = False
		while responseOK is False and tries < 3:
	# Lista de predicados espaciales utilizables:

	# # area_relation ({'Intersects', 'Contains', 'IsWithin'}, optional) --
	# # What relation to use for testing the AOI. Case insensitive.
	# # Intersects: true if the AOI and the footprint intersect (default)
	# # Contains: true if the AOI is inside the footprint
	# # IsWithin: true if the footprint is inside the AOI

	# Busqueda por geometria, fecha y  SciHub query keywords
	# La busqueda (que devuelve una lista) es generalista (20 dias y 0-90 % nubes) porque solo seleccionamos
	# el producto deseado mas adelante, independientemente de que obtengamos una lista de 20-40
	# hacemos order_by por atributo (indicando +(default) o - delante para ordenar ascending o descending)
			try: 
				products_list = api.query(geom,
										date=('NOW-20DAY', 'NOW'),
										platformname='Sentinel-2',
										cloudcoverpercentage=(0, 90),
										order_by= ('size, cloudcoverpercentage')) #Aqui descargo la imagen de menor tamano
				responseOK = True

			# Capturamos el error de conexion al servidor
			except sentinelsat.SentinelAPIError as exception:
				tries += 1
				mesgError = exception.response.json()['feed']['error']['message']
				print (exception.msg , mesgError)
			if tries < 3 and responseOK is False:
					time.sleep(3.0)
			# Seleccionamos el primer producto por su ID
			# Si su ID ya ha sido descargada, continuamos con la iteracion general
			if responseOK is True:	
				print "Total de imagenes validas para la parcela ", sid,\
					"encontrados: ", len(products_list)
				id = list(products_list.keys())[0]
				filename = products_list[id]["filename"]
				if id in idList:
					print ("para la parcela %s la id %s esta repetida") %(sid, id)
					dic_SidZip[sid] = filename
					continue
				# Si el ID de descarga no existia, append a la lista y descargamos
				else:
					idList.append(id)
					dic_SidZip[sid] = filename
				print ('ID: ', id)
				
				respuesta = api.download(id, os.path.join(workspace, 'descargas'))
				print (respuesta)
				
				print ('Descarga Completada del archivo con ID %s \npara la parcela %s') %(id, sid)
			else:
				print ("La parcela %s no se ha podido descargar") %(sid)
				continue


	return	dic_SidZip