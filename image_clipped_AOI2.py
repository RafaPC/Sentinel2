# -*- coding: utf-8 -*- 

from osgeo import gdal, ogr, osr
import os, sys

def image_clipped_AOI(band_list, AOI_clip, bands_folder_path):
    
    """ los raster y los shp (AOI) tienen que estar en la misma proyección"""
    
    
    output_path = os.path.join(bands_folder_path,'clipped_images')
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
    datasource.SyncToDisk()
    # datasource.CreateLayer('shp_clip', srs = spatialRef,
    #                             geom_type = ogr.wkbMultiPolygon)
    # layer = driver.Open(output_path).GetLayer(0)

    #Fields defining for structure a layer #just needs field 'sid'
    FieldDef_sid = ogr.FieldDefn('sid', ogr.OFTInteger)
    layer.CreateField(FieldDef_sid) #Creates fields defined in layer
    
    #Define a new object (template) with the fields structure of layer
    #This is necesary for define a feature_object (empty),
    #for later introduce field values
    feature_Defn = layer.GetLayerDefn()
        
    #Define an empty object with the structure of template new_FeatureDefn
    feature = ogr.Feature(feature_Defn)
    
    #FIXME:
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField('sid', 3) # SID *** LO COGE DE FUERA ***
    feature.SetGeometry((ogr.CreateGeometryFromWkt(AOI_clip)))
    
    #Creates a feature in new_layer
    layer.CreateFeature(feature)

    print('*')
    
    
    
    
    bands_clip_list = []
    
    for band in band_list:
        
        band_out_name = band[:-4] + '_clip' + band[-4:]
        band_out_path = os.path.join(output_path, band_out_name)
        bands_clip_list.append(band_out_path)
        
        options = gdal.WarpOptions(cutlineDSName = output_path_shp,
                                   #cutline dataset name
        cropToCutline = True)
        #Crop the extent of the target dataset to the extent of the cutline.
        # whether to use cutline extent for output bounds,
        clip_band = gdal.Warp(srcDSOrSrcDSTab = bands_folder_path + '\\' + band,
        #an array of Dataset objects or filenames, or a Dataset object or a filename
                        destNameOrDestDS = band_out_path, 
                        #Output dataset name or object
                        options = options)
        # FIXME:
		# clip_band = None
        print ('Una banda hecha---------------')
    return bands_clip_list


# band_list_1 = ['T30TUL_20210101T111451_B02_10m.tif',
#                'T30TUL_20210101T111451_B03_10m.tif',
#                'T30TUL_20210101T111451_B04_10m.tif',
#                'T30TUL_20210101T111451_B08_10m.tif',
#                'T30TUL_20210101T111451_TCI_10m.tif']

# AOI7 = 'MULTIPOLYGON(((-4.50559645530908 40.7086153317464,-4.47387022241673 40.7135866470223,-4.46411461075216 40.7124681334455,-4.4620651125033 40.7098581953612,-4.4656722294213 40.6961854197893,-4.47075498507847 40.6909020048112,-4.47255854353747 40.6905912026476,-4.47526388122596 40.694134261375,-4.50092359930168 40.6918344026038,-4.51133505040589 40.7019656173812,-4.50559645530908 40.7086153317464)))'

# AOI1 = 'MULTIPOLYGON(((-3.79167423530262 42.7839343098834,-3.75494722668312 42.7796021531174,-3.75789850416147 42.7608259710666,-3.77593408875141 42.7564921976755,-3.79790470997914 42.7682889813751,-3.80446310437548 42.7774359610623,-3.79167423530262 42.7839343098834)))'
# AOI2 = 'MULTIPOLYGON(((-3.78037045350324 42.7835826393944,-3.78145154646088 42.7849864030543,-3.76922687993987 42.7845591740057,-3.77030797289751 42.7819957377979,-3.78037045350324 42.7835826393944)))'
# AOI3 = 'MULTIPOLYGON(((-1.95171668740973 42.4893374071352,-1.94810957049175 42.4987672472783,-1.92745062814328 42.4941734002052,-1.92187599290639 42.481599040483,-1.929746066182 42.4702315790789,-1.9549958846079 42.4673289176097,-1.95860300152589 42.4704734614589,-1.95171668740973 42.4893374071352)))'
# AOI4 = 'MULTIPOLYGON(((-3.80216766633676 42.7781580335008,-3.78216456342793 42.7827309634102,-3.76937569435507 42.7716590784327,-3.77560616903159 42.7608259710666,-3.79626511138006 42.7586591222595,-3.81298901709072 42.7639557300081,-3.80216766633676 42.7781580335008)))'
# AOI5 = 'MULTIPOLYGON(((-4.32647030835908 40.7261220344342,-4.28843162086032 40.7231398514352,-4.27597067150727 40.7082269321096,-4.34483381266883 40.6868459225951,-4.36582067473712 40.7057411207912,-4.36778819305602 40.722145760741,-4.32647030835908 40.7261220344342)))'
# AOI6 = 'MULTIPOLYGON(((-1.99795336790392 42.5048112687524,-1.96975227199967 42.508679135872,-1.96057051984479 42.4982837003202,-1.9645055564826 42.485226519035,-1.97860610443472 42.4707153429042,-2.00123256510209 42.481115360785,-2.01008639753715 42.4973165951864,-1.99795336790392 42.5048112687524)))'
# image_clipped_AOI(band_list_1, AOI6,
#                   '/Users/davidgabellamerino/Desktop/SENTINEL_PRUEBAS/S2A_MSIL2A_20210101T111451_N0214_R137_T30TUL_20210101T140201.SAFE/GRANULE/L2A_T30TUL_A028877_20210101T111450/IMG_DATA/R10m/bands_folder_tif/')

if __name__ == "__main__" :
    image_clipped_AOI(sys.argv[1], sys.argv[2], sys.argv[3])
