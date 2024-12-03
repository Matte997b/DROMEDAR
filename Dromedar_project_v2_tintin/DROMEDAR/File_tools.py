import os
import subprocess
# CDO, DATA AND NUMERICAL LIBRARY
from cdo import *
import xarray as xr
import numpy as np
import netCDF4 as ncdf

cdo = Cdo()

def list_files(directory):
    '''
    It gives a list of the file/folder content

    Parameters
    ----------
    directory : FOLDER PATH

    Returns
    -------
    files : list of element inside the folder (often netCDF files)

    '''
    # List of file in the directory
    files = os.listdir(directory)
    for i, file in enumerate(files):
        print('Files list:')
        print(f"{i + 1}. {file}")
    return files

def choose_file(files):
    '''
    It allows to chose a file/folder inside the list. Remember to select a file
    and not a folder, in that case you need to modify the filepath

    Parameters
    ----------
    files : list of files

    Returns
    -------
    The chosen file of the list that allows to works on it

    '''
    # Ask the use for the file
    while True:
        try:
            choice = int(input("Chose the desired file: ")) - 1
            if 0 <= choice < len(files):
                return files[choice]
            else:
                print("Scelta non valida. Riprova.")
        except ValueError:
            print("Per favore, inserisci un numero valido.")

def infos(file):
    '''
    Just a function that collect the command to obtain file informations

    Parameters
    ----------
    file : selected file

    Returns
    -------
    None.

    '''
    info_file_content = cdo.sinfon(input = file)
    # info_variable = cdo.infon(input=file)
    print(info_file_content)
    # print(info_variable)
    

def delater(folder_path, file):
    '''
    Delate file and give less intermediate file

    Parameters
    ----------
    file : filepath

    Returns
    -------
    None.
    
    '''
    item = os.path.join(folder_path, f'{file}')
    command_rm_item = f"rm -f {item}"
    subprocess.run(command_rm_item, shell=True, capture_output=True, text=True)
    
def command_run_tested(command):
    '''
    Run command and rise Error just in case

    Parameters
    ----------
    command : command line str

    Returns
    -------
    None.

    '''
    print(f'Command run: {" ".join(command)}')     
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        print(f'Output: {result.stdout}')
        
        if result.stderr:
            print(f'Error: {result.stderr}')
    
    except subprocess.CalledProcessError as e:
        print(f'Error in the command execution: {e}')
    
