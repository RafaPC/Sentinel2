# -*- coding: utf-8 -*- 

import zipfile 
import os, sys
from osgeo import gdal


def unzip_transform(path_in, zip_name, folder = 'R10m',
                    format_in = '.jp2', format_out = '.tif',
                    outputSRS = 'EPSG:4326'):
    
    zip_name = zip_name.replace('SAFE', 'zip')
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
                
            # para que no de error en macOS, son archivos creados automaticamente
                
            bands_folder_path = os.path.join(base, 'bands.tif_folder')
            os.mkdir(bands_folder_path)
            
            n_band = 1
            bands_names_list = []
            bands_path_list = []
            
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
                        
                        gdal.UseExceptions() # Enable exceptions
                        gdal.Open(image_in_path)
                        gdal.Translate(image_out_path, image_in_path,
                                       format = format_gdal_out,
                                       outputSRS = outputSRS)
                        
                        print('\n...transformando formato de {0} > {1}...\n'\
                              .format(format_in, format_out))
                        
                        print('{} transformación realizada \n'.format(n_band))
                        n_band +=1

            print("Todas las transformaciones han sido completadas")
            print('\n Lista de elementos: \n')
            print(bands_names_list)

    return bands_names_list, bands_folder_path, bands_path_list


#****************PRUEBA****************

# bands_names_list, bands_folder_path, bands_path_list = unzip_transform(
#     '/Users/davidgabellamerino/Desktop/SENTINEL_PRUEBAS',
#      'S2A_MSIL2A_20210101T111451_N0214_R137_T30TUL_20210101T140201.zip')


if __name__ == "__main__":
    
    bands_names_list, bands_folder_path, bands_path_list = unzip_transform(
                                                    sys.argv[1], sys.argv[2])


