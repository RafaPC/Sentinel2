# -*- coding: utf-8 -*- 

from osgeo import ogr, osr 
import psycopg2, sys


def getAOI(mode = 0, fk_agri = None, bands_folder_path):
    
    """Se conecta a DB PostGIS y obtiene las AOI.shp de la tabla donde están,
    transforma la geometría de WKT >> lat/lon para ser usada posteriormente
    en el script sentinelsat como AOI para seleccionar la imagen-satelite 
    
    mode = 0 >> obtiene todas las AOI de la tabla AOI_SHP 
    mode = 1 >> obtiene las AOI para un agricultor, con su fk_agri"""

    dic_AOI = {}
    #Conecta con la DB
    
    try:
        conexion = psycopg2.connect(host='localhost', database='sentinel2_ap',
                                user='postgres', password='OrionyChimba0811')
        
        #Es necesario crear un cursor sobre el objeto que contiene la conexion
        cursor = conexion.cursor()

    except Exception as e:
        print (e)
        print('Could not connect to PostGIS database')
    
    query = "SELECT sid, st_astext(geom) FROM aoi_ejemplos"
    
    try:
        if mode == 0: 
            cursor.execute(query)
        
        elif mode == 1:
            query = query + " WHERE fk_agri = {}".format(fk_agri)
            cursor.execute(query)
        else:
            print ('The mode must be 0 or 1')
            sys.exit
    except Exception as e:
        print (e)
        print ('Could not execute the query')
        
    #recorre el resultado de la consulta
    #almacena geometría(x,y) en diccionario
    for sid, geom in cursor.fetchall():
        
        dic_AOI[sid] = geom

    conexion.commit()
    conexion.close()
    
    "************************************************************************"
    "************************************************************************"
    
def unzip_transform(path_in, zip_name, folder = 'R10m',
                format_in = '.jp2', format_out = '.tif',
                format_outclip = '.tif',
                outTransformSRS = 'EPSG:4326'):
    
    
    """Descomprime un archivo zip (path_zip = path_in + zip_name),
    busca la carpeta folder y tranforma los formatos de los archivos que contiene (.jp2) 
    a unos de salida (.tif) usando gdal.Translate().
    
    Los archivos creados los guarda en folder_elements, en el mismpo directorio del .zip
    
            
            path_in = ruta donde se encuentra el .zip
            zip_name = nombre del .zip
            folder = nombre de la carpeta donde se encuentran los archivos a transformar
            por defecto 'IMG_DATA' para descargas de imagenes Sentinel2 de Open Acess Hub
            
            
            Usar format_in y format_out en caso de querer tranformar
            diferentes formatos a los dados por defecto"""

    os.path.exists(path_in)
    
    path_zip = os.path.join(path_in, zip_name)
    
    file_zip = zipfile.ZipFile(path_zip, 'r')
    file_zip.extractall(path = path_in)
    file_zip.close()

    for base, dirs, files in os.walk(path_in):
        
        if base.endswith(folder):
   
            
            print('Directorio raiz \n {} \n'.format(base)) 
            dir = os.listdir(base)

            len_dir = len(dir)
            base_len = int(len(base))
            print('* path length * ',base_len)
            
            print('Este directorio tiene {} archivos \n'.format(len_dir))
            
            if '.DS_Store' in dir:
                dir.remove('.DS_Store')
                
            'para que no de error en macOS, son archivos creados automaticamente'
                
            bands_folder_path = os.path.join(base, 'bands.tif_folder')
            os.mkdir(bands_folder_path)
            
            n_band = 1
            bands_names_list = []
            bands_path_list = []
            
            imagesclip_pathlist = []
            
            bands_to_transform = ['B02_10m.jp2', 'B03_10m.jp2', 'B04_10m.jp2',
                              'B08_10m.jp2', 'TCI_10m.jp2']
            
            for band in dir:
                
                for selected in bands_to_transform:
                    
                    if band.endswith(selected):
                
                        image_in_path = os.path.join(base, band)
                        'image_.jp2' 
                        
                        image_out_name = band.replace(format_in, format_out)
                        bands_names_list.append(image_out_name)
                        
                        image_out_path = os.path.join(bands_folder_path,
                                                      image_out_name)
                        'image_.tif'
                        bands_path_list.append(image_out_path)
                        
                        if format_out == '.tif':
                            format_gdal_out = 'GTiff'
                        
                        print('\n...transformando formato de {0} > {1}...\n'\
                              .format(format_in, format_out))
                        
                        gdal.UseExceptions() # Enable exceptions
                        gdal.Open(image_in_path)
    
    "************************************************************************"
    
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
                        
                        #Fields defining for structure a layer #just needs field 'sid'
                        FieldDef_sid = ogr.FieldDefn('sid', ogr.OFTInteger)
                        layer.CreateField(FieldDef_sid) #Creates fields defined in layer
                        
                        #Define a new object (template) with the fields structure of layer
                        #This is necesary for define a feature_object (empty),
                        #for later introduce field values
                        feature_Defn = layer.GetLayerDefn()
                            
                        #Define an empty object with the structure of template new_FeatureDefn
                        feature = ogr.Feature(feature_Defn)
                        
                        
                        feature = ogr.Feature(layer.GetLayerDefn())
                        feature.SetField('sid', 3) # SID *** LO COGE DE FUERA ***
                        feature.SetGeometry((ogr.CreateGeometryFromWkt(AOI_clip)))
                        
                        #Creates a feature in new_layer
                        layer.CreateFeature(feature)
                    
                        print('*')
    
    
    return bands_names_list, bands_folder_path, bands_path_list, imagesclip_pathlist
    
    "************************************************************************"
    
    #CONSEGUIR LAS COORDENADAS CON .GetEnvelope() del rectángulo geográfico
    #el rectángulo geográfico se introducirá como input en .gdalTranslate()
    # outputBounds = [-180, 90, 180, -90]
    
    feature_count = layer.GetFeatureCount()
    
    src_field = src_feature.GetField(key)
    
    minLongitude , maxLongitude , minLatitude , maxLatitude = src_geom.GetEnvelope()

    
    src_geom = src_feature.GetGeometryRef()
                                                                -3.79167423530262, 42.7839343098834, 42.5, -5.7, 40.
    projWin --- subwindow in projected coordinates to extract: [ulx, uly, lrx, lry]
    
    
    
    
    
    
    
  projWinSRS --- SRS in which projWin is expressed
  strict --- strict mode
  unscale --- unscale values with scale and offset metadata
  scaleParams --- list of scale parameters, each of the form [src_min,src_max] or [src_min,src_max,dst_min,dst_max]
  exponents --- list of exponentiation parameters
  outputBounds --- assigned output bounds: [ulx, uly, lrx, lry]
  metadataOptions --- list of metadata options
  outputSRS --- assigned output SRS
    
    
    "************************************************************************"
    
    return dic_AOI

dic_AOI = getAOI(bands_folder_path = '/Users/davidgabellamerino/Desktop/SENTINEL_PRUEBAS/S2A_MSIL2A_20210101T111451_N0214_R137_T30TUL_20210101T140201.SAFE/GRANULE/L2A_T30TUL_A028877_20210101T111450/IMG_DATA/R10m/bands.tif_folder/')

print(dic_AOI)

"funcion >> crear shp temporal a cada vuelta de un bucle para hacer clip a las imagenes y luego borrarlo"

shp_temp = '/Users/davidgabellamerino/Documents/MASTER_TIG/PRUEBA_SENTINEL/shp_temporal.shp'


if __name__ == "__main__":
    getAOI(sys.argv[1], sys.argv[2])
