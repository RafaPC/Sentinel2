# Sentinel Web Login:
# user: gonzalogis
# pass: iwc.w6mEMp84Fj4

from osgeo import ogr
import os
import sentinelsat
from datetime import date
import time

workspace = r'C:\Users\rafit\Desktop\Sentinel\SHP'
os.chdir(workspace)

driver = ogr.GetDriverByName('ESRI Shapefile')
datasource = driver.Open(r'C:\Users\rafit\Desktop\Sentinel\SHP', 0)

# layer = GetLayer()

# for shp in range(datasource.GetLayerCount()):
#     layer = datasource.GetLayer(shp)
#     for feature in layer:
#         # por defecto, exporta a Wkt, de modo que no hace falta poner geom.ExportToWkt
#         geom = feature.GetGeometryRef()

# geom = datasource.GetLayer(0)[0].GetGeometryRef()



# AQUI ESTA EL PROBLEMA DE QUE LAS GEOMETRIAS ESTAN EN METROS Y HACEN FALTA EN LAT/LONG
Parcela_1 = 'POLYGON ((-420245.946554843 4793717.38835783,-419261.69458634 4793299.953473,-419064.844192639 4792616.8785073,-419337.894738745 4791813.63342289,-419903.045869041 4791668.16389583,-421541.349145651 4791902.18009981,-422284.300631557 4792971.06548,-422049.350161653 4793957.72971833,-420347.546758044 4794311.91707057,-420245.946554843 4793717.38835783))'
Parcela_1_rect = 'POLYGON ((-422397.490107098 4794482.71540755,-418838.860969346 4794513.59952112,-418758.3527074 4791505.46930436,-422315.910883079 4791474.63690589,-422397.490107098 4794482.71540755))'
ParcelaSENT_rect = 'POLYGON ((-4.805397020191035 38.24605276891404,-2.239841508018477 38.24605276891404,-2.239841508018477 39.81259892014185,-4.805397020191035 39.81259892014185,-4.805397020191035 38.24605276891404))'
# Sentinel Web Login:
# user: gonzalogis
# pass: iwc.w6mEMp84Fj4

api = sentinelsat.SentinelAPI('gonzalogis', 'iwc.w6mEMp84Fj4', 'https://scihub.copernicus.eu/dhus')

# download single scene by known product id

# search by polygon, time, and SciHub query keywords
#footprint = geojson_to_wkt(read_geojson('/path/to/map.geojson'))
geom = ParcelaSENT_rect
tries = 0
responseOK = False
while responseOK is False and tries < 3:

# area_relation ({'Intersects', 'Contains', 'IsWithin'}, optional) --
# What relation to use for testing the AOI. Case insensitive.

# Intersects: true if the AOI and the footprint intersect (default)
# Contains: true if the AOI is inside the footprint
# IsWithin: true if the footprint is inside the AOI
	try:
		products_list = api.query(geom,
							date=('NOW-20DAY', 'NOW'),
							platformname='Sentinel-2',
							cloudcoverpercentage=(0, 90),
							order_by='size, cloudcoverpercentage')

		responseOK = True
	except sentinelsat.SentinelAPIError as errorX:
		tries += 1
		mesgError = errorX.response.json()['feed']['error']['message']
		print errorX.msg , mesgError
		if tries < 3:
			time.sleep(3.0)
	else:
		print len(products_list)
		id = list(products_list.keys())[0]
		print 'ID: ', id
		if os.path.exists(os.path.join(workspace, 'descargas')) is False:
			os.mkdir(os.path.join(workspace, 'descargas'))

		respuesta = api.download(id, os.path.join(workspace, 'descargas'))
		print respuesta
		
	finally:
		print 'final'