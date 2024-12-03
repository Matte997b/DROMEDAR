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
	
    cond = str('SPEI')
    
    if cond == 'SPI': 
        
        #Domain can be: indom or med
        indom = 'indom'
        med = 'med'
        domain = [indom, med]
        
        for dom in domain:
            file = f'/work_big/users/dromedar/bordoni/home/datasets/tp_ERA5/tp_tseries/ERA5_total_precipitation_day_1.0x1.0_sfc_1940-2023_{dom}.nc'
            folder_path_SPI_tmp = '/work_big/users/dromedar/bordoni/home/datasets/tp_ERA5/tmp_SPI_1_0'
		
            model_name = os.path.basename(file).split('_')[0]
            model_res = os.path.basename(file).split('_')[4]
            print(model_name)
            print(model_res)
		
            folder_path_SPI = f'/work_big/users/dromedar/bordoni/home/datasets/tp_ERA5/SPI_{model_name}'   
            SPI_periods = [1, 3, 6, 12]
            
            for SPI_period in SPI_periods:
                drops.SPI_len(file, model_name, model_res, folder_path_SPI, folder_path_SPI_tmp, SPI_period, dom)

    elif cond == 'SPEI':
        
        #Domain can be: indom or med
        indom = 'indom'
        med = 'med'
        domain = [indom, med]
        
        for dom in domain:
            file = f'/work_big/users/dromedar/bordoni/home/datasets/tp_minus_PET_ERA5/tp_m_PET_tseries/ERA5_P-PET_day_1.0x1.0_sfc_1940-2023_{dom}.nc'
            folder_path_SPEI_tmp = '/work_big/users/dromedar/bordoni/home/datasets/tp_minus_PET_ERA5/tmp_SPEI_1_0'

            model_name = os.path.basename(file).split('_')[0]
            model_res = os.path.basename(file).split('_')[3]
            print(model_name)
            print(model_res)
		
            folder_path_SPEI = f'/work_big/users/dromedar/bordoni/home/datasets/tp_minus_PET_ERA5/SPEI_{model_name}'
            SPEI_periods = [1, 3, 6, 12]
            
            for SPEI_period in SPEI_periods:
                drops.SPEI_len(file, model_name, model_res, folder_path_SPEI, folder_path_SPEI_tmp, SPEI_period, dom)
	
    elif cond == 'RDI':
        
        #Domain can be: indom or med
        indom = 'indom'
        med = 'med'
        domain = [indom, med]
        
        for dom in domain:
            file_tp = f'/work_big/users/dromedar/bordoni/home/datasets/tp_ERA5/tp_tseries/ERA5_total_precipitation_day_1.0x1.0_sfc_1940-2023_{dom}.nc'
            file_PET = f'/work_big/users/dromedar/bordoni/home/datasets/PET_ERA5/PET_tseries/ERA5_PET_day_1.0x1.0_sfc_1940-2023_{dom}.nc'
            folder_path_RDI_tmp = '/work_big/users/dromedar/bordoni/home/datasets/tp_div_PET_ERA5/tmp_RDI_1_0'

            model_name = os.path.basename(file_tp).split('_')[0]
            model_res = os.path.basename(file_tp).split('_')[3]
            print(model_name)
            print(model_res)
		
            folder_path_RDI = f'/work_big/users/dromedar/bordoni/home/datasets/tp_div_PET_{model_name}'
            RDI_periods = [1, 3, 6, 12]
            
            for RDI_period in RDI_periods:
                drops.RDI_len(file_tp, file_PET, model_name, model_res, folder_path_RDI, folder_path_RDI_tmp, int(RDI_period), dom)
                
    else:		
        vrmpo.variables_remapping()
		
if __name__ == '__main__':
	main()


