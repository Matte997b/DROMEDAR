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
import var_remap_options as vrmpo

cdo = Cdo()

def main():
    
    print('Do you want to calculate SPI, SPEI or OTHER?')
    cond = str(input()).upper()
    
    if cond == 'SPI':
        
        folder_path_tp = '/work_big/users/dromedar/bordoni/home/datasets/tp_ERA5/tp_tseries'
        folder_path_SPI_tmp = '/work_big/users/dromedar/bordoni/home/datasets/tp_ERA5/tmp_SPI'

        # FILE SELECTION
        files = ftl.list_files(folder_path_tp)
        print()
        file = os.path.join(folder_path_tp, ftl.choose_file(files))
        print()
        print(f'File selected: {file}')
        model_name = os.path.basename(file).split('_')[0]
        model_res = os.path.basename(file).split('_')[4]
        print(model_name)
        print(model_res)
        
        folder_path_SPI = f'/work_big/users/dromedar/bordoni/home/datasets/tp_ERA5/SPI_{model_name}'
        SPI_period = 1
        domain = 'indom'
        #domain = 'med'
        drops.SPI_len(file, model_name, model_res, folder_path_SPI, folder_path_SPI_tmp, SPI_period, domain)
        
    elif cond == 'SPEI':
        folder_path_tp_min_PET = '/work_big/users/dromedar/bordoni/home/datasets/tp_min_PET_ERA5'
        folder_path_SPEI_tmp = '/work_big/users/dromedar/bordoni/home/datasets/tp_min_PET_ERA5/tmp_SPEI'
        # FILE SELECTION
        files_tp_min_PET = ftl.list_files(folder_path_tp_min_PET)
        print()
        file_tp_min_PET = os.path.join(folder_path_tp_min_PET, ftl.choose_file(files_tp_min_PET))
        print()
        print(f'File selected: {file_tp_min_PET}')
        model_name = os.path.basename(file_tp_min_PET).split('_')[0]
        model_res = os.path.basename(file_tp_min_PET).split('_')[4]
        print(model_name)
        print(model_res)
        
        
        
        folder_path_SPEI = f'/work_big/users/dromedar/bordoni/home/datasets/tp_min_PET_ERA5/SPEI_{model_name}'
        SPEI_period = 12
        domain = 'indom'
        #domain = 'med'
        #domain = 'hres'
        drops.SPEI_len(file, model_name, model_res, folder_path_SPEI, folder_path_SPEI_tmp, SPEI_period, domain)
    
    else:
        
        vrmpo.variables_remapping()
        
        

if __name__ == '__main__':
    
    main()


