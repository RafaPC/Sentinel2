# -*- coding: utf-8 -*- 

# Filename: getAOI.py
# Authors: David Gabella Merino & Gonzalo Prieto Ciprian
# Date: January 27, 2021
# Description: connects to a PostGis DB, takes the geometries,
# transform them in wkt and stores them in a dictionary (sid:geom)

try:
    import sys
    from osgeo import ogr, osr 
    import psycopg2
except ImportError:
    import sys
    from osgeo import ogr, osr 
    import psycopg2


def getAOI(mode = 0, fk_agri = None):
    
    """It connects to DB PostGIS and gets the AOI.shp from the table
       where they are, transforms the geometry of WKT >> lat / lon
       to be used later in the sentinelsat script as AOI
       to select the satellite-image
    
      mode = 0 >> gets all AOIs from table AOI_SHP
      mode = 1 >> gets the AOIs for a farmer, with his fk_agri
      fk_agri = id of the farmer who wants to look at the plot"""

    dic_AOI = {} #sid:geom
    
    # Connects to a PostGis DB
    try:
        connection = psycopg2.connect(host='localhost', database='sentinel2_ap',
                                user='postgres', password='OrionyChimba0811')
        
        # It is necessary to create a cursor on the object
        # that contains the connection 
        cursor = connection.cursor()

    except Exception as e:
        print (e)
        print('Could not connect to PostGIS database')
    
    query = "SELECT sid, st_astext(geom) FROM aoi_ejemplos"
    
    #creates and execute query
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
        
    # Run through the query result and store geometry to dictionary 
    for sid, geom in cursor.fetchall():
        
        dic_AOI[sid] = geom

    # Close connection
    connection.commit()
    connection.close()
    
    return dic_AOI

#if __name__ == "__main__":
#    getAOI(sys.argv[1], sys.argv[2])