# -*- coding: utf-8 -*- 

from osgeo import ogr, osr 
import psycopg2, sys


def getAOI(mode = 0, fk_agri = None):
    
    """Se conecta a DB PostGIS y obtiene las AOI.shp de la tabla donde están,
    transforma la geometría de WKT >> lat/lon para ser usada posteriormente
    en el script sentinelsat como AOI para seleccionar la imagen-satelite 
    
    mode = 0 >> obtiene todas las AOI de la tabla AOI_SHP 
    mode = 1 >> obtiene las AOI para un agricultor, con su fk_agri"""

    dic_AOI = {}
    #Conecta con la DB
    
    try:
        conexion = psycopg2.connect(host='localhost', database='sentinel2_ap',
                                user='postgres', password='*************')
        
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
    
    return dic_AOI

# dic_AOI = getAOI()

# print(dic_AOI)

# "funcion >> crear shp temporal a cada vuelta de un bucle para hacer clip a las imagenes y luego borrarlo"

# shp_temp = '/Users/davidgabellamerino/Documents/MASTER_TIG/PRUEBA_SENTINEL/shp_temporal.shp'


if __name__ == "__main__":
    getAOI(sys.argv[1], sys.argv[2])
