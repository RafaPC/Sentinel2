# Sentinel Web Login:
# user: gonzalogis
# pass: iwc.w6mEMp84Fj4

from osgeo import ogr, osr
import os
import sentinelsat
from datetime import date
import time
import pyproj

# #Establecer directorio mediante 'os'
workspace = r'C:\Users\rafit\Desktop\Sentinel\SHP'
os.chdir(workspace)

#Seleccion de driver y apertura de 'shp' en modo lectura
driver = ogr.GetDriverByName('ESRI Shapefile')
datasource = driver.Open(r'C:\Users\rafit\Desktop\Sentinel\SHP', 0)


# Iteracion sobre los 'shp', obtencion de geometria de sus features (parcelas)
# Aun hay que almacenarlos en un diccionario o asi.
# Se produce una transformacion a 4326 (WGS84) independientemente cual sea su SRC origen
for shp in range(datasource.GetLayerCount()):
	layer = datasource.GetLayer(shp)
	sourceSR = layer.GetSpatialRef()
	targetSR = osr.SpatialReference()
	targetSR.ImportFromEPSG(4326)
	coordTrans = osr.CoordinateTransformation(sourceSR,targetSR)
	print sourceSR
	for feature in layer:
        # por defecto, exporta a Wkt, de modo que no hace falta poner geom.ExportToWkt
		geom = feature.GetGeometryRef()
		print ("La geometria original, previo reproyeccion es, expresada en  metros")
		print geom
		geom.Transform(coordTrans)
		print ("La geometria reproyectada a WGS84 es, expresada en grados decimales")
		print geom

		
# AQUI ESTA EL PROBLEMA DE QUE LAS GEOMETRIAS ESTAN EN METROS Y HACEN FALTA EN LAT/LONG
#Estan establecidas a mano para poder continuar el proceso de descarga
#Parcela_1 Contiene una parcela de 9 vertices al sur de Aranjuez
#Parcela_1_rect Contiene misma zona pero en parcela rectangular
#ParcelaSENT_rect Contiene lo mismo que la anterior pero las coordenadas son lat/long

# Parcela_1 = 'POLYGON ((-420245.946554843 4793717.38835783,-419261.69458634 4793299.953473,-419064.844192639 4792616.8785073,-419337.894738745 4791813.63342289,-419903.045869041 4791668.16389583,-421541.349145651 4791902.18009981,-422284.300631557 4792971.06548,-422049.350161653 4793957.72971833,-420347.546758044 4794311.91707057,-420245.946554843 4793717.38835783))'
# Parcela_1_rect = 'POLYGON ((-422397.490107098 4794482.71540755,-418838.860969346 4794513.59952112,-418758.3527074 4791505.46930436,-422315.910883079 4791474.63690589,-422397.490107098 4794482.71540755))'
# ParcelaSENT_rect = 'POLYGON ((-4.805397020191035 38.24605276891404,-2.239841508018477 38.24605276891404,-2.239841508018477 39.81259892014185,-4.805397020191035 39.81259892014185,-4.805397020191035 38.24605276891404))'

#Llamada a la API, logging
api = sentinelsat.SentinelAPI('gonzalogis', 'iwc.w6mEMp84Fj4', 'https://scihub.copernicus.eu/dhus')



#Establecemos la geometria deseada
# geom = ParcelaSENT_rect

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
							order_by='size, cloudcoverpercentage')

		responseOK = True

#Capturamos el error de conexion al servidor
	except sentinelsat.SentinelAPIError as errorX:
		tries += 1
		mesgError = errorX.response.json()['feed']['error']['message']
		print errorX.msg , mesgError
		if tries < 3:
			time.sleep(3.0)

# Seleccionamos el primer producto por su clave
	else:
		print len(products_list)
		id = list(products_list.keys())[0]

# Vigilar este print, por el cambio de 2x a 3x
# Comprobamos si existe una carpeta de descargas, para crearla en caso negativo
		print 'ID: ', id
		if os.path.exists(os.path.join(workspace, 'descargas')) is False:
			os.mkdir(os.path.join(workspace, 'descargas'))

# Descarga de un solo producto en base a su 'id', a su vez, obtenido de la consulta del producto
# Para descargas de varios elementos futuros usar download_all
		respuesta = api.download(id, os.path.join(workspace, 'descargas'))
		print respuesta

# Aviso del final de la descarga
	finally:
		print ('Descarga Completada')
