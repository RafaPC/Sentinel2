# -*- coding: utf-8 -*- 

# Filename: unzip_transform.py
# Authors: David Gabella Merino & Gonzalo Prieto Ciprian
# Date: January 27, 2021
# Description: gets envelope minLon, maxLon, minLat, maxLat
# of shapefile from WKTgeom using OGR and OSR


try:
    import os
    from osgeo import ogr, osr

except ImportError:
    import os
    from osgeo import ogr, osr


def get_shp_envelope(bands_folder_path, sid, geom):
    
    """It goes through the whole process to create a vector file (shp)
    and get its envelope (minLon, maxLon, minLat, maxLat) using OGR & OSR
    Creates a folder inside the folder where are the bands
    that will be cut with the envelope of the vector file (shp) 
    
    bands_folder_path = folder where are the bands
    sid = area of interes identifier 
    geom = geometry of area of interest in WKT geom"""
    
    try: 
        #Creates new folder 
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
        
        # Fields defining for structure a layer #just needs field 'sid'
        fieldDef_sid = ogr.FieldDefn('sid', ogr.OFTInteger)
        layer.CreateField(fieldDef_sid) #Creates fields defined in layer
        
        # Define a new object (template) with the fields structure of layer
        # This is necesary for define a feature_object (empty),
        # for later introduce field values
        feature_Defn = layer.GetLayerDefn()
            
        # Define an empty object with the structure of template new_FeatureDefn
        feature = ogr.Feature(feature_Defn)
        
        # Define a feature with input sid and input geom in a layer
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetField('sid', sid)
        feature.SetGeometry((ogr.CreateGeometryFromWkt(geom)))
        
        # Creates a feature in new_layer
        layer.CreateFeature(feature)
    
        src_geom = feature.GetGeometryRef()
        # envelope: minLongitude, maxLongitude, minLatitude, maxLatitude
        envelope = src_geom.GetEnvelope()
        
    except Exception as e:
        print(e)
        
    return envelope