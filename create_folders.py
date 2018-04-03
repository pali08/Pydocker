#!/usr/bin/env python3
import os
import getpass
import pathlib
import sys

class CreateFolder(object)

    def __init__(self, project_name, plot_or_text):
        self.project_name = project_name
        self.plot_or_text = plot_or_text

    def create_folder(self):
        project_dir = os.path.join('.','docker_output',self.project_name)
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
    
    def create_subfolders(self):
        project_dir = os.path.join('.', 'docker_output', self.project_name)
        iter_folder = '{}_{}'.format(self.project_name , self.plot_or_text)
        self.subfolder = os.path.join(project_dir, iter_folder)
        pathlib.Path(self.subfolder).mkdir(parents=True, exist_ok=True)
        return(self.subfolder)

class CreateFolderRefine(CreateFolder)
    def __init__(self, project_name, plot_or_text, line_num_to_refine):
        CreateFolder.__init__(project_name, plot_or_text)
        self.project_name = project_name + "_ref_" + line_num_to_refine

