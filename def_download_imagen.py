# Sentinel Web Login:
# user: gonzalogis
# pass: iwc.w6mEMp84Fj4

# -*- coding: utf-8 -*-

import os
import sentinelsat
from datetime import date
import time


dic_AOI = {7: 'MULTIPOLYGON(((-4.50559645530908 40.7086153317464,-4.47387022241673 40.7135866470223,-4.46411461075216 40.7124681334455,-4.4620651125033 40.7098581953612,-4.4656722294213 40.6961854197893,-4.47075498507847 40.6909020048112,-4.47255854353747 40.6905912026476,-4.47526388122596 40.694134261375,-4.50092359930168 40.6918344026038,-4.51133505040589 40.7019656173812,-4.50559645530908 40.7086153317464)))', 8: 'MULTIPOLYGON(((-4.5310102335949 40.7418384155896,-4.505760415169 40.7435775497543,-4.50756397362799 40.7361237974477,-4.52641935751747 40.7285449597278,-4.54347118294795 40.7309056738799,-4.54150366462905 40.7391053985976,-4.5310102335949 40.7418384155896)))', 5: 'MULTIPOLYGON(((-4.32647030835908 40.7261220344342,-4.28843162086032 40.7231398514352,-4.27597067150727 40.7082269321096,-4.34483381266883 40.6868459225951,-4.36582067473712 40.7057411207912,-4.36778819305602 40.722145760741,-4.32647030835908 40.7261220344342)))', 6: 'MULTIPOLYGON(((-1.99795336790392 42.5048112687524,-1.96975227199967 42.508679135872,-1.96057051984479 42.4982837003202,-1.9645055564826 42.485226519035,-1.97860610443472 42.4707153429042,-2.00123256510209 42.481115360785,-2.01008639753715 42.4973165951864,-1.99795336790392 42.5048112687524)))', 3: 'MULTIPOLYGON(((-1.95171668740973 42.4893374071352,-1.94810957049175 42.4987672472783,-1.92745062814328 42.4941734002052,-1.92187599290639 42.481599040483,-1.929746066182 42.4702315790789,-1.9549958846079 42.4673289176097,-1.95860300152589 42.4704734614589,-1.95171668740973 42.4893374071352)))', 4: 'MULTIPOLYGON(((-3.80216766633676 42.7781580335008,-3.78216456342793 42.7827309634102,-3.76937569435507 42.7716590784327,-3.77560616903159 42.7608259710666,-3.79626511138006 42.7586591222595,-3.81298901709072 42.7639557300081,-3.80216766633676 42.7781580335008)))', 1: 'MULTIPOLYGON(((-3.79167423530262 42.7839343098834,-3.75494722668312 42.7796021531174,-3.75789850416147 42.7608259710666,-3.77593408875141 42.7564921976755,-3.79790470997914 42.7682889813751,-3.80446310437548 42.7774359610623,-3.79167423530262 42.7839343098834)))', 2: 'MULTIPOLYGON(((-3.78037045350324 42.7835826393944,-3.78145154646088 42.7849864030543,-3.76922687993987 42.7845591740057,-3.77030797289751 42.7819957377979,-3.78037045350324 42.7835826393944)))'}


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

	# Iteracion de cada geometria, contiene en su interior la query, conexion a servidor, comprobacion de id y descarga
	print (dic_AOI)
	for sid in dic_AOI:
		geom = dic_AOI[sid]
		print (geom)


	# Intentamos conexion de llamada al servidor de la API
	# Establecemos intentos (que podemos espaciar con time.sleep()) 
	# Porque en ocasiones si el servidor esta muy solicitado, da problema de conexion
		tries = 0
		responseOK = False
		while responseOK is False and tries < 3:

	# area_relation ({'Intersects', 'Contains', 'IsWithin'}, optional) --
	# What relation to use for testing the AOI. Case insensitive.
	# Intersects: true if the AOI and the footprint intersect (default)
	# Contains: true if the AOI is inside the footprint
	# IsWithin: true if the footprint is inside the AOI
	# Hay que tener cuidado en el futuro para parcelas que cumplan Intersects con dos 'tiles' 
	# O incluso mas, aunque improbable

	# search by polygon, time, and SciHub query keywords
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
			except sentinelsat.SentinelAPIError as errorX:
				tries += 1
				mesgError = errorX.response.json()['feed']['error']['message']
				print (errorX.msg , mesgError)
			if tries < 3 and responseOK is False:
					time.sleep(3.0)
			# Seleccionamos el primer producto por su 
			#sid, si su id ya ha sido descargada, continuamos con la iteracion general
			if responseOK is True:	
				print "Total de imagenes validas para la parcela ", sid,\
					"encontrados: ", len(products_list)
				id = list(products_list.keys())[0]
				filename = products_list[id]["filename"]
				if id in idList:
					print ("para la parcela %s la id %s esta repetida") %(sid, id)
					dic_SidZip[sid] = filename
					continue
			# Si el id de descarga no existia, append a la lista y descargamos
				else:
					idList.append(id)
					dic_SidZip[sid] = filename
				print ('ID: ', id)

				#	# La descarga esta comentada porque tarda mucho, en su lugar ponemos prints para simular descargas completadas
				respuesta = api.download(id, os.path.join(workspace, 'descargas'))
				print (respuesta)
				
				print ('Descarga Completada del archivo con ID %s \npara la parcela %s') %(id, sid)
			else:
				print ("La parcela %s no se ha podido descargar") %(sid)
				continue


	return	dic_SidZip
	dic_SidZip = download_sentinel2_images(dic_AOI)

print 	(dic_SidZip)