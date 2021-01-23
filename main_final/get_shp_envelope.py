from osgeo import ogr, osr
import os
def	get_shp_envelope(bands_folder_path, sid, geom):

	clipped_images_dir = 'clipped_images_' + str(sid)
	output_path = os.path.join(bands_folder_path, clipped_images_dir)
	os.mkdir(output_path)
	
	output_path_shp = os.path.join(output_path, 'shp_clip.shp')
	
	#Creates spatial ref object and sets it as WGS84
	spatialRef = osr.SpatialReference() 
	spatialRef.SetWellKnownGeogCS('WGS84')
	
	#Creates a new shp with a layer #Sets spatial_ref to new_layer
	driver = ogr.GetDriverByName('ESRI Shapefile')
	datasource = driver.CreateDataSource(output_path)
	layer = datasource.CreateLayer('shp_clip', srs = spatialRef,
								geom_type = ogr.wkbMultiPolygon)
	
	#Fields defining for structure a layer #just needs field 'sid'
	fieldDef_sid = ogr.FieldDefn('sid', ogr.OFTInteger)
	layer.CreateField(fieldDef_sid) #Creates fields defined in layer
	
	#Define a new object (template) with the fields structure of layer
	#This is necesary for define a feature_object (empty),
	#for later introduce field values
	feature_Defn = layer.GetLayerDefn()
		
	#Define an empty object with the structure of template new_FeatureDefn
	feature = ogr.Feature(feature_Defn)
	
	
	feature = ogr.Feature(layer.GetLayerDefn())
	feature.SetField('sid', 3) # SID *** LO COGE DE FUERA ***
	feature.SetGeometry((ogr.CreateGeometryFromWkt(geom)))
	
	#Creates a feature in new_layer
	layer.CreateFeature(feature)

	src_geom = feature.GetGeometryRef()
	envelope = src_geom.GetEnvelope()
	print('ENVELOPE CREADO')
	return envelope