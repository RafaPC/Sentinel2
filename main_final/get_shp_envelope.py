# -*- coding: utf-8 -*- 

# Filename: get_shp_envelope.py
# Authors: David Gabella Merino & Gonzalo Prieto Ciprian
# Date: January 27, 2021
# Description: AOI-based envelope shapefile creation


from osgeo import ogr, osr
import os

def	get_shp_envelope(bands_folder_path, sid, geom):

	# Directory creation
	clipped_images_dir = 'clipped_images_' + str(sid)
	output_path = os.path.join(bands_folder_path, clipped_images_dir)
	os.mkdir(output_path)
	
	output_path_shp = os.path.join(output_path, 'shp_clip.shp')
	
	# Spatial reference creation and WGS84 setting
	spatialRef = osr.SpatialReference() 
	spatialRef.SetWellKnownGeogCS('WGS84')
	
	# New empty Shp with layer creation. Spatial reference setting
	driver = ogr.GetDriverByName('ESRI Shapefile')
	datasource = driver.CreateDataSource(output_path)
	layer = datasource.CreateLayer('shp_clip', srs = spatialRef,
								geom_type = ogr.wkbMultiPolygon)
	
	# Field definition and creation
	fieldDef_sid = ogr.FieldDefn('sid', ogr.OFTInteger)
	layer.CreateField(fieldDef_sid) # Defined in layer
	
	# Feature definition
	feature_Defn = layer.GetLayerDefn()

	feature = ogr.Feature(feature_Defn)
	
	
	feature = ogr.Feature(layer.GetLayerDefn())
	feature.SetField('sid', sid)
	feature.SetGeometry((ogr.CreateGeometryFromWkt(geom)))
	
	# Feature creation in new layer
	layer.CreateFeature(feature)

	src_geom = feature.GetGeometryRef()
	envelope = src_geom.GetEnvelope()
	return envelope