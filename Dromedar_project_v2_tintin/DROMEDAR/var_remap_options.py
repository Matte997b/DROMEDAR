import os
import subprocess
# CDO, DATA AND NUMERICAL LIBRARY
from cdo import *
import xarray as xr
import numpy as np
import netCDF4 as ncdf

#MY MODULES
import dromedar_operators as drops
import File_tools as ftl

cdo = Cdo()

def variables_remapping():
    '''
    It allows to choose what variables remap and this function just contains the
    variables that you want remap. The real function of the template used in the
    remapping and the effective remapping variable can be found in
    dromedar_operators.py module

    Returns
    -------
    It creates the template and remapped variable file

    '''
    model_name ='ERA5'
    folder_path = '/home/mattia/Documents/Final_thesis/VARIABLES'
    #Z500##################################################################
    
    folder_path_Z500 = os.path.join(folder_path, 'Z500')
    # REMAP TEMPLATE Z500
    lon1 = -85
    lon2 = 60
    lat1 = 70   
    lat2 = 15
    drops.remapping_tmpl(model_name, folder_path_Z500, lon1, lon2, lat1, lat2)
    
    # REMAP Z500
    '''template = os.path.join(folder_path_IVT, 'ERA5_template.nc')
    in1 = os.path.join(folder_path_IVT, 'east_flux_scaled.nc')
    in2 = os.path.join(folder_path_IVT, 'north_flux_scaled.nc')
    outname1 = 'east_flux_scaled_rmap'
    outname2 = 'north_flux_scaled_rmap'
    drops.remapping(model_name, folder_path_IVT, template, in1, outname1)
    drops.remapping(model_name, folder_path_IVT, template, in2, outname2)'''
    
    #IVT###################################################################
    
    folder_path_IVT = '/home/mattia/Documents/Final_thesis/VARIABLES/IVT'
    # REMAP TEMPLATE IVT
    lon1 = -85
    lon2 = 60
    lat1 = 70   
    lat2 = 15
    drops.remapping_tmpl(model_name, folder_path_IVT, lon1, lon2, lat1, lat2)
    
    # REMAP IVT
    '''template = os.path.join(folder_path_IVT, 'ERA5_template.nc')
    in1 = os.path.join(folder_path_IVT, 'east_flux_scaled.nc')
    in2 = os.path.join(folder_path_IVT, 'north_flux_scaled.nc')
    outname1 = 'east_flux_scaled_rmap'
    outname2 = 'north_flux_scaled_rmap'
    drops.remapping(model_name, folder_path_IVT, template, in1, outname1)
    drops.remapping(model_name, folder_path_IVT, template, in2, outname2)'''
    
    
    # VECTORIAL MAGNITUDE IVT
    infile1 = os.path.join(folder_path_IVT, 'IVT_EW_rmap.nc')
    infile2 = os.path.join(folder_path_IVT, 'IVT_NW_rmap.nc')
    outname = 'ERA5_IVT_rmap'
    drops.magnitude(infile1, infile2, folder_path_IVT, outname)
    
    #HORIZONTAL WIND#######################################################
    
    folder_path_wind = '/home/mattia/Documents/Final_thesis/VARIABLES/Wind'
    
    # REMAP TEMPLATE WIND
    model_name ='ERA5'
    lon1 = -85
    lon2 = 60
    lat1 = 70   
    lat2 = 15
    drops.remapping_tmpl(model_name, folder_path_wind, lon1, lon2, lat1, lat2)
    
    # REMAP WIND
    '''template = os.path.join(folder_path_wind, 'template_ERA5.nc')
    in1 = os.path.join(folder_path_wind, 'u300_corr.nc')
    in2 = os.path.join(folder_path_wind, 'v300_corr.nc')
    outname1 = 'u300_scaled_rmap'
    outname2 = 'v300_scaled_rmap'
    drops.remapping(model_name, folder_path_wind, template, in1, outname1)
    drops.remapping(model_name, folder_path_wind, template, in2, outname2)'''
    
    # VECTORIAL MAGNITUDE WIND
    
    infile3 = os.path.join(folder_path_wind, 'u300_rmap.nc')
    infile4 = os.path.join(folder_path_wind, 'v300_rmap.nc')
    outname = 'ERA5_U_scaled_magnitude_rmap'
    drops.magnitude(infile3, infile4, folder_path_wind, outname)
    
    #PV300#################################################################
    
    folder_path_PV = '/home/mattia/Documents/Final_thesis/VARIABLES/PV'
    
    # REMAP TEMPLATE PV
    model_name ='ERA5'
    lon1 = -85
    lon2 = 60
    lat1 = 70   
    lat2 = 15
    drops.remapping_tmpl(model_name, folder_path_PV, lon1, lon2, lat1, lat2)
    
    # REMAP WIND
    '''template = os.path.join(folder_path_wind, 'template_ERA5.nc')
    in1 = os.path.join(folder_path_wind, 'u300_corr.nc')
    in2 = os.path.join(folder_path_wind, 'v300_corr.nc')
    outname1 = 'u300_scaled_rmap'
    outname2 = 'v300_scaled_rmap'
    drops.remapping(model_name, folder_path_wind, template, in1, outname1)
    drops.remapping(model_name, folder_path_wind, template, in2, outname2)'''
    
    # VECTORIAL MAGNITUDE WIND
    
    '''infile3 = os.path.join(folder_path_wind, 'u300_rmap.nc')
    infile4 = os.path.join(folder_path_wind, 'v300_rmap.nc')
    outname = 'ERA5_U_scaled_magnitude_rmap'
    drops.magnitude(infile3, infile4, folder_path_wind, outname)'''