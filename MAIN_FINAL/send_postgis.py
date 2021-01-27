# -*- coding: utf-8 -*-

import subprocess

def send_postgis(sid, ndvi_path, tci_path):
    
    
    """Utilizando raster2pgsql, carga un raster dataset en una DB postgis
    cada raster de la bands_path_list se guarda en una tabla,
    tipo AOI_raster_Bn, dependiendo del nombre de la banda.
    
    
    bands_path_list = lista con las rutas del dateset devuelta por la
    función 
    
    """
    
    path_raster2pgsql = '/Library/PostgreSQL/13/bin/raster2pgsql' 
    #Cambiar por el propio path donde se encuentre
    
    table_name = 'AOI_raster_{}'.format(sid)
            
    files = [ndvi_path, tci_path]
    
    try:
        for file in files:
        
            cmd_send ='{0} -I -C -s 32629 -a {1} -F {2}'\
            .format(path_raster2pgsql,file,table_name)
            subprocess.run(cmd_send, shell = True)
        print ('Files uploaded to {}'.format(table_name))
        
    except Exception as e:
        print (e)