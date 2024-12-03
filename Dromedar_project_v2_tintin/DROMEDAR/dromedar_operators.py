import os
import subprocess
# CDO, DATA AND NUMERICAL LIBRARY
from cdo import *
import numpy as np
import netCDF4 as ncdf

#MY MODULES
import File_tools as ftl

cdo = Cdo()

def complete_timeseries(model_name, out_mon, SPI_period):
    '''
    It allows to maintain a complete time series also applying the runmean 
    or runsum

    Parameters
    ----------
    out_mon : filepath

    Returns
    -------
    filepath

    '''
    folder_path = '/home/mattia/Documents/Final_thesis/DATASET'
    
    cdo.seltimestep(f'2/{SPI_period}', input=out_mon,
                    output=os.path.join(folder_path, f'step2{SPI_period}.nc'))
    
    cdo.shifttime(-1*SPI_period, input=os.path.join(folder_path, f'step2{SPI_period}.nc'),
                  output=os.path.join(folder_path, f'step2{SPI_period}shft.nc'))
    
    cdo.mergetime(input=[os.path.join(folder_path, f'step2{SPI_period}shft.nc'),
                         os.path.join(folder_path, f'{model_name}_tp_mon.nc')],
                  output=os.path.join(folder_path, f'long_{model_name}_tp_mon.nc'))
    
    return os.path.join(folder_path, f'long_{model_name}_tp_mon.nc')

def mon_sum(file, model_name, folder_path, var):
    '''
    Just a function to pass from a daily total variable to the total monthly of
    the variable

    Parameters
    ----------
    file : FILE PATH
    model_name : NAME OF THE MODEL str
    folder_path : FOLDER PATH

    Returns
    -------
    None.

    '''
    cdo.monsum(options='-b f64 -P 25', input=file,
               output=os.path.join(folder_path, f'{model_name}_tp_mon.nc'))
    
    dataset = ncdf.Dataset(os.path.join(folder_path, f'{model_name}_tp_mon.nc'), 'a')
    precipitation = dataset.variables[var]
    precipitation.setncattr('units', 'mm/month')
    precipitation.setncattr('long_name', 'total monthly precipitation')
    dataset.close()
    
def mon_sum_test(file, model_name, folder_path, var):
    '''
    Just a function to pass from a daily total variable to the total monthly of
    the variable

    Parameters
    ----------
    file : FILE PATH
    model_name : NAME OF THE MODEL str
    folder_path : FOLDER PATH

    Returns
    -------
    None.

    '''
    cdo.monsum(options='-b f64 -P 25', input=file,
               output=os.path.join(folder_path, f'{model_name}_mon_{var}.nc'))
    
def magnitude(infile1, infile2, folder_path, outname):
    '''
    Calculate the vectorial sum

    Parameters
    ----------
    file1 : FILE PATH
    file2 : FILE PATH

    Returns
    -------
    None.

    '''
    outfile = os.path.join(folder_path, f'{outname}.nc')
    command = [
        'cdo', 'sqrt', '-add',
        '-sqr', infile1, 
        '-sqr', infile2,
        outfile
        ]
    ftl.command_run_tested(command)
    
def SPI_len(file, model_name, model_res, folder_path_SPI, folder_path_SPI_tmp, SPI_period, domain):
    '''
    Calculate the SPI from critical percentile values

    Parameters
    ----------
    file : FILE PATH
    model_name : MODEL NAME str
    folder_path : FOLDER PATH
    SPI_period : SPI length int

    Returns
    -------
    None.

    '''
    
    crit=np.array([2.275,6.681,15.866,84.134,93.319,97.725])
        
    var = 'tp'
    str(var)
    
    ###########################################################################
    # Monsum it is necessary if we are working on daily or subdaily dataset
    mon_sum(file, model_name, folder_path_SPI_tmp, var)
    ###########################################################################
    mon_tp = os.path.join(folder_path_SPI_tmp, f'{model_name}_tp_mon.nc')
    
    cdo.runsum(SPI_period, options='--timestat_date last -b f64 -P 25', 
               input=mon_tp, 
               output=os.path.join(folder_path_SPI_tmp, 'runsum.nc'))
    
    out_runsum = os.path.join(folder_path_SPI_tmp, 'runsum.nc')
    
    dataset = ncdf.Dataset(out_runsum, 'a')
    precipitation = dataset.variables[var]
    precipitation.setncattr('units', f'mm/{SPI_len}mon')
    precipitation.setncattr('long_name', f'total of {SPI_len} months')
    #time_len = len(dataset['time'])
    mon_len = len(dataset['valid_time'])
    dataset.close()
    
    years = ((mon_len//12)+1)

    for percen in crit:
        out_perc = os.path.join(folder_path_SPI_tmp, f'percen_{percen}.nc')
        
        # Command structure
        command_perc = [
            'cdo',
            '-P', '30',
            '-L',
            '-b', 'f64',
            f'ymonpctl,{percen}',
            out_runsum,
            '-ymonmin', out_runsum,
            '-ymonmax', out_runsum,
            out_perc
        ]
        ftl.command_run_tested(command_perc)
        
        # Extend percintile to the length of the time dimension (i.e. 22 years)
        command_extend_perc = [
        'cdo',
        '-P', '30',
        '-b', 'f64',
        'cat'
        ] + [out_perc] * years + [
        os.path.join(folder_path_SPI_tmp, f'percen_{percen}_ext.nc')
        ]
            
        ftl.command_run_tested(command_perc)
        ftl.command_run_tested(command_extend_perc)
        
        dataset = ncdf.Dataset(os.path.join(folder_path_SPI_tmp, f'percen_{percen}.nc'), 'a')
        precipitation = dataset.variables[var]
        precipitation.setncattr('units', f'mm/{SPI_len}mon')
        precipitation.setncattr('long_name', f'Percentile {percen}% {SPI_len} months')
        dataset.close()
        
            
    out_perc = os.path.join(folder_path_SPI_tmp, f'percen_{percen}.nc')
    months = [f'{month:02}' for month in range(1, 13)]
    
    for mon in months:
        for percen in crit:
            
            if model_name == 'IMERG':

                command_algn_perc = [
                    'cdo', 'settaxis,2000-07-01,00:00:00,1mon', 
                    os.path.join(folder_path_SPI_tmp, f'percen_{percen}_ext.nc'),
                    os.path.join(folder_path_SPI_tmp, f'percen_{percen}_algn.nc')
                ]
            
            else:
                command_algn_perc = [
                    'cdo','settaxis,1940-01-01,00:00:00,1mon', 
                    os.path.join(folder_path_SPI_tmp, f'percen_{percen}_ext.nc'),
                    os.path.join(folder_path_SPI_tmp, f'percen_{percen}_algn.nc')
                ]

            
            command_ge_perc = [
                'cdo',
                '-P', '30',
                'ge',
                f'-selmon,{mon}', out_runsum,
                f'-selmon,{mon}', os.path.join(folder_path_SPI_tmp, f'percen_{percen}_algn.nc'),
                os.path.join(folder_path_SPI_tmp, f'ge_{percen}_mon{mon}.nc')
                ]
            
            ftl.command_run_tested(command_algn_perc)
            ftl.command_run_tested(command_ge_perc)
            
            dataset = ncdf.Dataset(os.path.join(folder_path_SPI_tmp, f'ge_{percen}_mon{mon}.nc'), 'a')
            precipitation = dataset.variables[var]
            precipitation.setncattr('units', '-')
            precipitation.setncattr('long_name', 'Conditional Masking where runsum larger that the threshold')
            dataset.close()

        ftl.delater(folder_path_SPI_tmp, f'SPI_{mon}.nc')
        
        command_ge_SPI = [
            'cdo',
            '-P', '30',
            'enssum',
            os.path.join(folder_path_SPI_tmp, f'ge_*_mon{mon}.nc'),
            os.path.join(folder_path_SPI_tmp, f'SPI_{mon}.nc')
            ]
     
        ftl.command_run_tested(command_ge_SPI)
        ftl.delater(folder_path_SPI_tmp, 'ge_*_mon*.nc')
        
    ftl.delater(folder_path_SPI_tmp, 'percen_*.nc')
    ftl.delater(folder_path_SPI_tmp, 'offset_SPI.nc')
    
    cdo.mergetime(input = os.path.join(folder_path_SPI_tmp, 'SPI_??.nc'),
                  output = os.path.join(folder_path_SPI_tmp, 'offset_SPI.nc'))
    
    cdo.subc(3, input = os.path.join(folder_path_SPI_tmp, 'offset_SPI.nc'),
             output=os.path.join(folder_path_SPI, f'{model_name}_SPI_{SPI_period}_{domain}_{model_res}.nc'))
    
    dataset_SPI = ncdf.Dataset(os.path.join(folder_path_SPI, f'{model_name}_SPI_{SPI_period}_{domain}_{model_res}.nc'), 'a')
    precipitation = dataset_SPI.variables[var]
    precipitation.setncattr('units', '-')
    precipitation.setncattr('long_name', f'SPI period of {SPI_period}')
    dataset.close()
    
    ftl.delater(folder_path_SPI_tmp, 'SPI_*.nc')
    ftl.delater(folder_path_SPI_tmp, 'offset_SPI.nc')
    ftl.delater(folder_path_SPI_tmp, 'runsum.nc')
    ftl.delater(folder_path_SPI_tmp, f'long_{model_name}_tp_mon.nc')
    ftl.delater(folder_path_SPI_tmp, f'{model_name}_tp_mon.nc')
    
    """SPI = xr.open_dataset(os.path.join(folder_path, f'{model_name}_SPI.nc'))
    SPI_var = SPI['pr']
    
    max_value = SPI_var.max().values
    min_value = SPI_var.min().values
    
    print(f"Valore massimo: {max_value}")
    print(f"Valore minimo: {min_value}")"""
    
def SPEI_len(file, model_name, model_res, folder_path_SPEI, folder_path_SPEI_tmp, SPEI_period, domain):
    '''
    Calculate the SPEI from critical percentile values

    Parameters
    ----------
    file : FILE PATH
    model_name : MODEL NAME str
    folder_path : FOLDER PATH
    SPEI_period : SPEI length int

    Returns
    -------
    None.

    '''
    
    crit=np.array([2.275,6.681,15.866,84.134,93.319,97.725])
        
    var = 'tp'
    str(var)
    
    ###########################################################################
    # Monsum it is necessary if we are working on daily or subdaily dataset
    mon_sum(file, model_name, folder_path_SPEI_tmp, var)
    ###########################################################################
    mon_tp = os.path.join(folder_path_SPEI_tmp, f'{model_name}_tp_mon.nc')
    
    cdo.runsum(SPEI_period, options='--timestat_date last -b f64 -P 25', 
               input=mon_tp, 
               output=os.path.join(folder_path_SPEI_tmp, 'runsum.nc'))
    
    out_runsum = os.path.join(folder_path_SPEI_tmp, 'runsum.nc')
    
    dataset = ncdf.Dataset(out_runsum, 'a')
    precipitation = dataset.variables[var]
    precipitation.setncattr('units', f'mm/{SPEI_len}mon')
    precipitation.setncattr('long_name', f'total of {SPEI_len} months')
    #time_len = len(dataset['time'])
    mon_len = len(dataset['valid_time'])
    dataset.close()
    
    years = ((mon_len//12)+1)

    for percen in crit:
        out_perc = os.path.join(folder_path_SPEI_tmp, f'percen_{percen}.nc')
        
        # Command structure
        command_perc = [
            'cdo',
            '-P', '30',
            '-L',
            '-b', 'f64',
            f'ymonpctl,{percen}',
            out_runsum,
            '-ymonmin', out_runsum,
            '-ymonmax', out_runsum,
            out_perc
        ]
        ftl.command_run_tested(command_perc)
        
        # Extend percintile to the length of the time dimension (i.e. 22 years)
        command_extend_perc = [
        'cdo',
        '-P', '30',
        '-b', 'f64',
        'cat'
        ] + [out_perc] * years + [
        os.path.join(folder_path_SPEI_tmp, f'percen_{percen}_ext.nc')
        ]
            
        ftl.command_run_tested(command_perc)
        ftl.command_run_tested(command_extend_perc)
        
        dataset = ncdf.Dataset(os.path.join(folder_path_SPEI_tmp, f'percen_{percen}.nc'), 'a')
        precipitation = dataset.variables[var]
        precipitation.setncattr('units', f'mm/{SPEI_len}mon')
        precipitation.setncattr('long_name', f'Percentile {percen}% {SPEI_len} months')
        dataset.close()
        
            
    out_perc = os.path.join(folder_path_SPEI_tmp, f'percen_{percen}.nc')
    months = [f'{month:02}' for month in range(1, 13)]
    
    for mon in months:
        for percen in crit:
            
            if model_name == 'IMERG':

                command_algn_perc = [
                    'cdo', 'settaxis,2000-07-01,00:00:00,1mon', 
                    os.path.join(folder_path_SPEI_tmp, f'percen_{percen}_ext.nc'),
                    os.path.join(folder_path_SPEI_tmp, f'percen_{percen}_algn.nc')
                ]
            
            else:
                command_algn_perc = [
                    'cdo','settaxis,1940-01-01,00:00:00,1mon', 
                    os.path.join(folder_path_SPEI_tmp, f'percen_{percen}_ext.nc'),
                    os.path.join(folder_path_SPEI_tmp, f'percen_{percen}_algn.nc')
                ]

            
            command_ge_perc = [
                'cdo',
                '-P', '30',
                'ge',
                f'-selmon,{mon}', out_runsum,
                f'-selmon,{mon}', os.path.join(folder_path_SPEI_tmp, f'percen_{percen}_algn.nc'),
                os.path.join(folder_path_SPEI_tmp, f'ge_{percen}_mon{mon}.nc')
                ]
            
            ftl.command_run_tested(command_algn_perc)
            ftl.command_run_tested(command_ge_perc)
            
            dataset = ncdf.Dataset(os.path.join(folder_path_SPEI_tmp, f'ge_{percen}_mon{mon}.nc'), 'a')
            precipitation = dataset.variables[var]
            precipitation.setncattr('units', '-')
            precipitation.setncattr('long_name', 'Conditional Masking where runsum larger that the threshold')
            dataset.close()

        ftl.delater(folder_path_SPEI_tmp, f'SPEI_{mon}.nc')
        
        command_ge_SPEI = [
            'cdo',
            '-P', '30',
            'enssum',
            os.path.join(folder_path_SPEI_tmp, f'ge_*_mon{mon}.nc'),
            os.path.join(folder_path_SPEI_tmp, f'SPEI_{mon}.nc')
            ]
     
        ftl.command_run_tested(command_ge_SPEI)
        ftl.delater(folder_path_SPEI_tmp, 'ge_*_mon*.nc')
        
    ftl.delater(folder_path_SPEI_tmp, 'percen_*.nc')
    ftl.delater(folder_path_SPEI_tmp, 'offset_SPEI.nc')
    
    cdo.mergetime(input = os.path.join(folder_path_SPEI_tmp, 'SPEI_??.nc'),
                  output = os.path.join(folder_path_SPEI_tmp, 'offset_SPEI.nc'))
    
    cdo.subc(3, input = os.path.join(folder_path_SPEI_tmp, 'offset_SPEI.nc'),
             output=os.path.join(folder_path_SPEI, f'{model_name}_SPEI_{SPEI_period}_{domain}_{model_res}.nc'))
    
    dataset_SPEI = ncdf.Dataset(os.path.join(folder_path_SPEI, f'{model_name}_SPEI_{SPEI_period}_{domain}_{model_res}.nc'), 'a')
    precipitation = dataset_SPEI.variables[var]
    precipitation.setncattr('units', '-')
    precipitation.setncattr('long_name', f'SPEI period of {SPEI_period}')
    dataset.close()
    
    ftl.delater(folder_path_SPEI_tmp, 'SPEI_*.nc')
    ftl.delater(folder_path_SPEI_tmp, 'offset_SPEI.nc')
    ftl.delater(folder_path_SPEI_tmp, 'runsum.nc')
    ftl.delater(folder_path_SPEI_tmp, f'long_{model_name}_tp_mon.nc')
    ftl.delater(folder_path_SPEI_tmp, f'{model_name}_tp_mon.nc')
    
def RDI_len(file_tp, file_PET, model_name, model_res, folder_path_RDI, folder_path_RDI_tmp, RDI_period, domain):
    '''
    ................

    Parameters
    ----------
    file : FILE PATH
    model_name : MODEL NAME str
    folder_path : FOLDER PATH
    RDI_period : RDI length int

    Returns
    -------
    None.

    '''
    
    crit=np.array([2.275,6.681,15.866,84.134,93.319,97.725])
    
    var_tp = 'tp'
    var_PET = 'pev'
    str(var_tp)
    str(var_PET)
    
    ###########################################################################
    # Monsum it is necessary if we are working on daily or subdaily dataset
    mon_sum_test(file_tp, model_name, folder_path_RDI_tmp, var_tp)
    mon_sum_test(file_PET, model_name, folder_path_RDI_tmp, var_PET)
    ###########################################################################
    mon_tp = os.path.join(folder_path_RDI_tmp, f'{model_name}_mon_{var_tp}.nc')
    mon_PET = os.path.join(folder_path_RDI_tmp, f'{model_name}_mon_{var_PET}.nc')
    out_run_RDI = os.path.join(folder_path_RDI_tmp, f'{model_name}_run_RDI.nc')
    
    
    command_mean_tp = [
        'cdo',
        '-P', '30',
        '-b', 'f64',
        f'runmean,{RDI_period}',
        mon_tp,
        '/work_big/users/dromedar/bordoni/home/datasets/tp_div_PET_ERA5/tmp_RDI_2_5/ERA5_tp_mon_window.nc'
        ]
    
    subprocess.run(command_mean_tp)
    
    command_mean_PET = [
        'cdo',
        '-P', '30',
        '-b', 'f64',
        f'runmean,{RDI_period}',
        mon_PET,
        '/work_big/users/dromedar/bordoni/home/datasets/tp_div_PET_ERA5/tmp_RDI_2_5/ERA5_pev_mon_window.nc'
        ]
    
    subprocess.run(command_mean_PET)

    command_runratio = [
        'cdo',
        '-P', '30',
        '-b', 'f64',
        'div',
        '/work_big/users/dromedar/bordoni/home/datasets/tp_div_PET_ERA5/tmp_RDI_2_5/ERA5_tp_mon_window.nc',
        '/work_big/users/dromedar/bordoni/home/datasets/tp_div_PET_ERA5/tmp_RDI_2_5/ERA5_pev_mon_window.nc',
        out_run_RDI
        ]
    
    ftl.command_run_tested(command_runratio)
    
    dataset = ncdf.Dataset(mon_tp, 'a')
    #precipitation = dataset.variables[var_tp]
    #precipitation.setncattr('units', f'-')
    #precipitation.setncattr('long_name', f'total of {RDI_len} months')
    #time_len = len(dataset['time'])
    mon_len = len(dataset['valid_time'])
    dataset.close()
    
    years = ((mon_len//12)+1)
    
    for percen in crit:
        out_perc = os.path.join(folder_path_RDI_tmp, f'percen_{percen}.nc')
        
        # Command structure
        command_perc = [
            'cdo',
            '-P', '30',
            '-L',
            '-b', 'f64',
            f'ymonpctl,{percen}',
            out_run_RDI,
            '-ymonmin', out_run_RDI,
            '-ymonmax', out_run_RDI,
            out_perc
        ]
        ftl.command_run_tested(command_perc)
        
        # Extend percintile to the length of the time dimension (i.e. 22 years)
        command_extend_perc = [
        'cdo',
        '-P', '30',
        '-b', 'f64',
        'cat'
        ] + [out_perc] * years + [
        os.path.join(folder_path_RDI_tmp, f'percen_{percen}_ext.nc')
        ]
            
        ftl.command_run_tested(command_perc)
        ftl.command_run_tested(command_extend_perc)
        
        '''dataset = ncdf.Dataset(os.path.join(folder_path_RDI_tmp, f'percen_{percen}.nc'), 'a')
        precipitation = dataset.variables[var]
        precipitation.setncattr('units', f'mm/{RDI_len}mon')
        precipitation.setncattr('long_name', f'Percentile {percen}% {RDI_len} months')
        dataset.close()'''
        
            
    out_perc = os.path.join(folder_path_RDI_tmp, f'percen_{percen}.nc')
    months = [f'{month:02}' for month in range(1, 13)]
    
    for mon in months:
        for percen in crit:
            
            command_algn_perc = [
                'cdo','settaxis,1940-01-01,00:00:00,1mon', 
                os.path.join(folder_path_RDI_tmp, f'percen_{percen}_ext.nc'),
                os.path.join(folder_path_RDI_tmp, f'percen_{percen}_algn.nc')
                ]
            
            command_ge_perc = [
                'cdo',
                '-P', '30',
                'ge',
                f'-selmon,{mon}', out_run_RDI,
                f'-selmon,{mon}', os.path.join(folder_path_RDI_tmp, f'percen_{percen}_algn.nc'),
                os.path.join(folder_path_RDI_tmp, f'ge_{percen}_mon{mon}.nc')
                ]
            
            ftl.command_run_tested(command_algn_perc)
            ftl.command_run_tested(command_ge_perc)
            
            '''dataset = ncdf.Dataset(os.path.join(folder_path_RDI_tmp, f'ge_{percen}_mon{mon}.nc'), 'a')
            precipitation = dataset.variables[var]
            precipitation.setncattr('units', '-')
            precipitation.setncattr('long_name', 'Conditional Masking where runsum larger that the threshold')
            dataset.close()'''

        ftl.delater(folder_path_RDI_tmp, f'RDI_{mon}.nc')
        
        command_ge_RDI = [
            'cdo',
            '-P', '30',
            'enssum',
            os.path.join(folder_path_RDI_tmp, f'ge_*_mon{mon}.nc'),
            os.path.join(folder_path_RDI_tmp, f'RDI_{mon}.nc')
            ]
     
        ftl.command_run_tested(command_ge_RDI)
        ftl.delater(folder_path_RDI_tmp, 'ge_*_mon*.nc')
        
    ftl.delater(folder_path_RDI_tmp, 'percen_*.nc')
    ftl.delater(folder_path_RDI_tmp, 'offset_RDI.nc')
    
    cdo.mergetime(input = os.path.join(folder_path_RDI_tmp, 'RDI_??.nc'),
                  output = os.path.join(folder_path_RDI_tmp, 'offset_RDI.nc'))
    
    cdo.subc(3, input = os.path.join(folder_path_RDI_tmp, 'offset_RDI.nc'),
             output=os.path.join(folder_path_RDI, f'{model_name}_RDI_{RDI_period}_{domain}_{model_res}.nc'))
    
    '''dataset_RDI = ncdf.Dataset(os.path.join(folder_path_RDI, f'{model_name}_RDI_{RDI_period}_{domain}_{model_res}.nc'), 'a')
    precipitation = dataset_RDI.variables[var]
    precipitation.setncattr('units', '-')
    precipitation.setncattr('long_name', f'RDI period of {RDI_period}')
    dataset.close()'''
    
    ftl.delater(folder_path_RDI_tmp, 'RDI_*.nc')
    ftl.delater(folder_path_RDI_tmp, 'offset_RDI.nc')
    ftl.delater(folder_path_RDI_tmp, 'runsum.nc')
    ftl.delater(folder_path_RDI_tmp, f'long_{model_name}_tp_mon.nc')
    ftl.delater(folder_path_RDI_tmp, f'{model_name}_tp_mon.nc')
    
def remapping(model_name, folder_path, template, infile, outname):
    '''
    It allows to remap the selected file with the variable of interest

    Parameters
    ----------
    model_name : name of the model (i.e. ERA5)
    folder_path : folder_path where to find the template and where python save
        the remapped variable
    template : name of the template
    infile : the template file
    outname : the mame of the file.nc of the var remapped

    Returns
    -------
    It creates the remapped variable as file.nc

    '''
    outfile = os.path.join(folder_path, f'{outname}.nc')
    command_rmap = [
        'cdo',
        '-f', 'nc',
        f'-remapcon,{template}',
        f'{infile}',
        outfile
        ]
    ftl.command_run_tested(command_rmap)     
    
    
    
    
    
