# -*- coding: utf-8 -*- 

import zipfile  
import os
from osgeo import gdal
import subprocess


def desc_zip_transform(path_in, zip_name, folder = 'IMG_DATA', format_in = '.jp2', format_out = '.tif' ):
    
    
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
    
    
    try: 
        
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
                
                print('Este directorio tiene {} archivos \n'.format(len_dir))
                
                if '.DS_Store' in dir:
                    dir.remove('.DS_Store')
                    
                'para que no de error en macOS, son archivos creados automaticamente'
                    
                path_elements = os.path.join(base, 'folder_elements')
                os.mkdir(path_elements)
                
                list_path_elements = []
                
                n_band = 1
                
                
                for band in dir:
                    image_in = os.path.join(base,band)
                    'image_.jp2' 
                    
                    image_out = image_in.replace(format_in, format_out)
                    'image_.tif'
                    
                    list_path_elements.append(image_out)
                    
                    print (image_out)
                    
                    if format_out == '.tif':
                        format_gdal_out = 'GTiff'
                    
                    gdal.Open(image_in)
                    gdal.Translate(image_out, image_in, format= format_gdal_out)
                    print('\n...transformando formato de {0} > {1}...\n'.format(format_in, format_out))
                    
                    print('{} transformación realizada \n'.format(n_band))
                    n_band +=1
                    
        return list_path_elements

    except Exception as e:
        
        print(e)
        print(type(e))
        

desc_zip_transform('/Users/davidgabellamerino/Documents/MASTER_TIG/PRUEBA_SENTINEL/', 'S2A_MSIL1C_20201102T111231_N0209_R137_T29SQC_20201102T132329.zip')


def send_postgis(list_path_elements):
    
    
    """Utilizando raster2pgsql, carga un raster dataset en una DB postgis
    cada raster de la list_path_elements se guarda en una tabla,
    tipo AOI_raster_Bn, dependiendo del nombre de la banda.
    
    
    list_path_elements = lista con las rutas del dateset devuelta por la
    función desc_zip_transform
    
    """
    
    path_raster2pgsql = '/Library/PostgreSQL/13/bin/raster2pgsql'
    
    
    for file in list_path_elements:
        
        n_band = file[-7,-4]
        
        if file.endswith(str(n_file)):
            
            table_name = 'AOI_raster_{}'.format(n_band)
            
            cmd_send = '{0} -I -C -s 32629 -a {1} -F {2}'.format(path_raster2pgsql,
                                                                file, table_name)
    
            
            subprocess.run(cmd_send, shell = True)
            "mirar argumentos para hacer más robusta la funcion \
            timeout > para excesos de tiempo, \
            "
        

def main():
    
    desc_zip(os.argv(1), os.argv(2))
    
    send_postgis(list_path_elements)

if __name__ == "__main__":
    
    main()
    
