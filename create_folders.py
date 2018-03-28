#!/usr/bin/env python3
import os
import getpass
import pathlib
import sys

def create_folder(project_name):
    project_dir = os.path.join('.','docker_output',project_name)
    proj_directory = pathlib.Path(project_dir)
    if (proj_directory.exists()):
        #while (projec_directory.exists())
        #new_proj_check = input("Directory already exists. Enter another name or delete folder")
        print("Directory already exists. Enter another name or delete folder")
        sys.exit()
        return(1)
    else:
        pathlib.Path(project_dir).mkdir(parents=True, exist_ok=True)
        return(0)

def create_subfolders(project_name, plot_or_text):
    project_dir = os.path.join('.', 'docker_output', project_name)
    iter_folder = '{}_{}'.format(project_name , plot_or_text)
    subfolder = os.path.join(project_dir, iter_folder)
    pathlib.Path(subfolder).mkdir(parents=True, exist_ok=True)
    return(subfolder)

