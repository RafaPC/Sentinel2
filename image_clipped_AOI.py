# -*- coding: utf-8 -*- 

from osgeo import gdal
import os, sys

def image_clipped_AOI(band_list, AOI_clip, bands_folder_path):
    
    """ los raster y los shp (AOI) tienen que estar en la misma proyección"""
    
    output_path = os.path.join(bands_folder_path,'clipped_images')
    os.mkdir(output_path)
    
    bands_clip_list = []
    
    for band in band_list:
        
        band_out_name = band[:-4] +'_clip' + band[-4:]
        band_out_path = os.path.join(output_path, band_out_name)
        bands_clip_list.append(band_out_path)
        
        options = gdal.WarpOptions(cutlineDSName = AOI_clip,
                                   #cutline dataset name
        cropToCutline = True)
        #Crop the extent of the target dataset to the extent of the cutline.
        # whether to use cutline extent for output bounds,
        clip_band = gdal.Warp(srcDSOrSrcDSTab = bands_folder_path + band,
        #an array of Dataset objects or filenames, or a Dataset object or a filename
                        destNameOrDestDS = band_out_path, 
                        #Output dataset name or object
                        options = options)
        clip_band = None
    
    return bands_clip_list

if __name__ == "__main__" :
    image_clipped_AOI(sys.argv[1], sys.argv[2], sys.argv[3])
