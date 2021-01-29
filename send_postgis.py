# -*- coding: utf-8 -*- 

# Filename: send_postgis.py
# Authors: David Gabella Merino & Gonzalo Prieto Ciprian
# Date: January 27, 2021
# Description: Result bands and NDVI storing in PostGIS Database

try:
	import subprocess

except ImportError:
	import subprocess

def send_postgis(sid, ndvi_path, tci_path):
    
    
    """
	Using raster2pgsql, saves into a PostGIS DB
	every raster dataset from 'bands_path_list' as table

	sid = Unicode acting as primary key in original DB
	ndvi_path = List of paths leading to all different NDVI images
	tci_path  = List of paths leading to all different TCI band images
    bands_path_list = Returned list of raster dataset paths

    """
    
	# Change to where 'path' lives if applies
    path_raster2pgsql = '/Library/PostgreSQL/13/bin/raster2pgsql' 
    
    
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