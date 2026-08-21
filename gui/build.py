"""
A unified build script to create executable versions of the gui. 
Currently only usable for mac and windows. Further support for linux may be added in future versions.
"""

import PyInstaller.__main__
import shutil
import os
from sys import platform
import fnmatch
from importlib.metadata import version

_GENERATE_EXE_GUI = True

def create_gui_exe(os_name:str) -> str:
    '''
    Runs pyinstaller with the appropriate icon and flags for the chosen distribution. 

    Parameters
    ----------
    os_name
        name of operating system of choice [mac, win]

    Returns
    -------
        path of output file
    '''

    if os.path.exists(f'pybis2spice_gui_v{version("pybis2spice")}'):
        os.remove(f'pybis2spice_gui_v{version("pybis2spice")}')

    PyInstaller.__main__.run([
        'pybis2spice_gui.py',
        '-iicon.icns' if os_name == 'mac' else '-iicon.ico',
        '--onefile',
        '--collect-all', 
        'ecdtools',
        '--collect-all', 
        'textparser'
    ])

    file_type = '' if os_name == 'mac' else '.exe'

    shutil.copy(os.path.join('dist', 'pybis2spice_gui'+file_type), os.getcwd())

    path = os.path.join(os.getcwd(), 'pybis2spice_gui'+file_type)
    return path


def recursively_delete_files_with_pattern(directory_path, pattern):
    # Get a list of all files in directory
    for root_dir, subdirs, filenames in os.walk(directory_path):
        # Find the files that matches the given pattern
        for filename in fnmatch.filter(filenames, pattern):
            try:
                os.remove(os.path.join(root_dir, filename))
            except OSError:
                print("Error while deleting file")


def folder_mopup(os_name:str):
    '''
    Sets up distribution folders and creates versioned and platform specific zip files of the 
    gui with example LTSPICE models packaged together with the executable for end users. 

    Parameters
    ----------
    os_name 
        name of operating system of choice [mac, win]
    '''

    file_type = '' if os_name == 'mac' else '.exe'

    bin_path = os.path.join(os.path.dirname(os.getcwd()), "bin")
    if not os.path.exists(bin_path):
        os.mkdir(bin_path)

    # Check if version folder already exists within bin and delete it
    folder_path = os.path.join(os.path.dirname(os.getcwd()), "bin", f"pybis2spice_v{version("pybis2spice")}-{os_name}")
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    # Create the version number folder (pybis2spice_vX.Y)
    os.mkdir(folder_path)

    # Check if zip exists and delete
    zip_path = os.path.join(os.path.dirname(os.getcwd()), "bin", f"pybis2spice_v{version("pybis2spice")}-{os_name}.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    # Copy the executable and the examples directory into the version number folder
    src_gui_filepath = os.path.join(os.getcwd(), 'pybis2spice_gui')
    shutil.copy(src_gui_filepath, folder_path)

    src_examples_dir = os.path.join(os.path.dirname(os.getcwd()), "examples")
    dest_examples_dir = os.path.join(folder_path, "examples")
    shutil.copytree(src_examples_dir, dest_examples_dir)

    # Remove all SPICE generated .log and .raw files
    recursively_delete_files_with_pattern(dest_examples_dir, "*.raw")
    recursively_delete_files_with_pattern(dest_examples_dir, "*.log")


if __name__ == '__main__':

    if platform == "darwin":
        os_name = 'mac'
    elif platform in ["win32", "cygwin"]:
        os_name = 'win'
    else:
        raise NotImplementedError()

    if _GENERATE_EXE_GUI:
        gui_filepath = create_gui_exe(os_name)
    else:
        gui_filepath = os.path.join(os.getcwd(), 'pybis2spice_gui')

    # Rename the GUI file to include the version number
    if os.path.exists(gui_filepath):
        try:
            os.rename(gui_filepath, os.path.join(os.getcwd(), f'pybis2spice_gui'))
        except:
            pass

    # Creates folder in bin directory and copies executable and example files
    folder_mopup(os_name)

    # Zip up the contents
    base_path = os.path.join(os.path.dirname(os.getcwd()), "bin", f"pybis2spice_v{version("pybis2spice")}-{os_name}")
    shutil.make_archive(base_name=base_path,
                        format='zip',
                        root_dir=os.path.dirname(base_path),
                        base_dir=f"pybis2spice_v{version("pybis2spice")}-{os_name}")