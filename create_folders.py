#!/usr/bin/env python3
import os
import getpass
import pathlib
import sys

class CreateFolder(object):

    def __init__(self, infilename_pdb, infilename_bcr, project_name):
        self.infilename_pdb = infilename_pdb.split(".")[0]
        self.infilename_bcr = infilename_bcr.split(".")[0]
        self.project_name = "{}_in_{}_{}".format(self.infilename_pdb,self.infilename_bcr,project_name)

    def create_folder(self):
        self.project_dir = os.path.join('pydocker_output',self.project_name)
        proj_directory = pathlib.Path(self.project_dir)
        if (proj_directory.exists()):
            print("Directory already exists. Enter another name or delete folder")
            sys.exit()
            return(1)
        else:
            pathlib.Path(self.project_dir).mkdir(parents=True, exist_ok=True)
            print(proj_directory)
            print(type(proj_directory))
            return(proj_directory)

    #def create_subfolders(self):
        #text_or_graph_folder = '{}_{}'.format(self.project_name , self.plot_or_text)
        #self.subfolder = os.path.join(self.project_dir, text_or_graph_folder)
        #pathlib.Path(self.subfolder).mkdir(parents=True, exist_ok=True)
        #return(self.subfolder)

class CreateFolderRefine(CreateFolder):
    def __init__(self, infilename_pdb, infilename_bcr, project_name, line_num_to_refine):
        CreateFolder.__init__(self,infilename_pdb,infilename_bcr, project_name)
        self.line_num = line_num_to_refine
        self.project_name = "{}_in_{}_refinement_{}_{}".format(self.infilename_pdb,self.infilename_bcr,str(self.line_num),project_name)

