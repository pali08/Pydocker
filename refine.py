#!/usr/bin/env python3
from read_pdb import read_pdb
from transform_coordinates import rotate
import operator
import transform_coordinates

class Refine(object)

    def __init__(self, angle_refin, points_count_refin, res_num_to_refine, pdb, bcr, docker_rough_output):
        self.angle_refin = angle_refin
        self.res_num_to_refine = res_num_to_refine
        self.pdb = pdb
        self.bcr = bcr
        self.docker_rough_output = docker_rough_output
    
    def read_pdb(self):
        self.pdb_list = read_pdb(self.pdb)[1]
    
    def rotate_cl(self,self.docker_rough_output, self.res_num_to_refine, self.pdb_list):
        line = linecache.getline(self.docker_rough_output, self.res_num_to_refine)
        self.axisangle = operator.itemgetter(3,4,5,7)(line)
        self.angle_z = operator.itemgetter(9)(line)
        self.z_axis = [0,0,1]
        self.z_axisangle = self.z_axis.append(self.z_angle)
        self.rot = transform_coordinates.rotate(self.axisangle, self.pdb_list)
        self.rot_whole = transform_coordinates.axisangle_to_q(self.axisangle_z,self.rot1) 
        self.new_xyz = transform_coordinates.rotate(self.axisangle, self.angle_z)


    def get_count_from_angle(self):
        self.whole_count = int((2*self.points_count_refin)/(1-np.cos(self.angle_ref)))
        return(self.whole_count)
    
    def dist_point_on_cap(self):
        self.get_count_from_angle()
        golden_angle = np.pi * (3 - np.sqrt(5))
        theta = golden_angle * np.arange(self.whole_count)
        z = np.linspace(1 - 1.0 / whole_count, 1.0 / whole_count - 1, whole_count)
        radius = np.sqrt(1 - z * z)
        
        self.points = np.zeros((points_count_refin, 3)) #points equaly distributed on sphere
        self.rot_axes = [[] for i in range(0, len(points_count_refin))]
        self.agle_list = []
        v2_u = self.z_axis / np.linalg.norm(self.z_axis)
        for i in range(0, points_count_refin):
            self.points[i,0] = radius[i] * np.cos(theta[i])
            self.points[i,1] = radius[i] * np.sin(theta[i])
            self.points[i,2] = z[i]
            self.rot_axes[i] = np.cross(points[i], main_ax)
            v1_u = self.points[i] / np.linalg.norm(self.points[i])
            self.angle_list.append((np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))))
            self.rot_axes = np.array(rot_axes)

        return(self.rot_axes, self.angle_list)


