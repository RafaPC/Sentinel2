# -*- coding: utf-8 -*- 

# Filename: clip_bands.py
# Authors: David Gabella Merino & Gonzalo Prieto Ciprian
# Date: January 27, 2021
# Description: Band clipping with AOI envelope by using gdal.Translate


from osgeo import gdal
import os

def image_clipped_AOI(band_list, bands_folder_path, sid, AOI_clip):
    
    
    """Clip a list of bands that have in a folder with an area of interest
    
    band_list = list of bands to clip with AOI
    bands_folder_path = folder where are the bands
    sid = area of interes identifier 
    AOI_clip = envelope object or list that containts:
            minLongitude, maxLongitude, minLatitude, maxLatitude
    
    - raster and shp (AOI) have to be in the same projection  """
    
    try:
    
        for band_name in band_list:
            
            # Clip name creation
            image_outclip_name = band_name[:-4] + '_clip' + band_name[-4:]
            
            # Clip path creation
            imageclip_outpath = os.path.join(bands_folder_path,
                                            'clipped_images_' + str(sid),
                                             image_outclip_name)
            
            # Projection and clipping raster image with Shp envelope using Translate
            gdal.Translate(imageclip_outpath, # output folder path
                os.path.join(bands_folder_path, band_name), # output file path
                format = 'GTiff',
                # projWin sets boundary raster image will be clipped to
                projWin = [AOI_clip[0], AOI_clip[3], AOI_clip[1], AOI_clip[2]],
                projWinSRS = 'EPSG:4326')
            
    except Exception as e:
        print(e)
        