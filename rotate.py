import random
import numpy as np
from transform_coordinates import rotate
from read_pdb import read_pdb
import random
#import align_matrices
from read_bcr_python import read_bcr_bin
import transform_coordinates
import math
import sys
#from surface3d_demo2 import surface
import linecache
import operator
import cv2
'''
def first_rot(x_rotations_count, y_rotations_count, z_rotations_count, pdb_file):
    coord_list = read_pdb(pdb_file)[1]
    y_turn_angle = (2*np.pi)/y_rotations_count
    x_turn_angle = (2*np.pi)/x_rotations_count
    z_turn_angle = (2*np.pi)/x_rotations_count
    list_of_all_rots=[]
    for i in range(0,x_rotations_count):
        coor_list_x_rot = rotate(x_turn_angle*i,"1,0,0", *coord_list)
        for j in range(0, y_rotations_count):
            coor_list_y_rot = rotate(y_turn_angle*j, "0,1,0", *coor_list_x_rot)
            for k in range(0, z_rotations_count):
                coor_list_final_rot = rotate(z_turn_angle*k, "0,0,1", *coor_list_y_rot)
                list_of_all_rots.append(coor_list_final_rot)

    return(list_of_all_rots)
'''
def ranvec(pi_mult):
    #coord_list = read_pdb(pdb_file)[1]
    #list_of_all_rots = []
    a = 2
    while(a > 1.0):
        xi1 = 1.0 - (2.0*random.random())
        xi2 = 1.0 - (2.0*random.random())
        a = (xi1*xi1) - (xi2*xi2)
    b = 2.0*math.sqrt(1-a)
    x_ranvec = xi1*b
    y_ranvec = xi2*b
    z_ranvec = 1.0 - (2.0*a)
    ran_angle = random.random()*(pi_mult*math.pi)
    return(x_ranvec, y_ranvec, z_ranvec, ran_angle)

def spiral_dist(points_count, main_ax):
    golden_angle = np.pi * (3 - np.sqrt(5))
    theta = golden_angle * np.arange(points_count)
    z = np.linspace(1 - 1.0 / points_count, 1.0 / points_count - 1, points_count)
    radius = np.sqrt(1 - z * z)
    points = np.zeros((points_count, 3)) #points equaly distributed on sphere
    points[:,0] = radius * np.cos(theta)
    points[:,1] = radius * np.sin(theta)
    points[:,2] = z
    #rot_axes = np.cross(points,main_ax)
    rot_axes = [[] for i in range(0, len(points))]
    for i in range(0, len(points)):
        rot_axes[i] = np.cross(points[i], main_ax)
    #print(rot_axes)
    rot_axes = np.array(rot_axes)
    #surface(points[:,0],points[:,1],points[:,2])
    #sys.exit()
    #print("these are rot axes")
    #print(rot_axes) 
    #print("eorotaxes")
    return(rot_axes, points, main_ax)

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    #print(vector)
    return vector / np.linalg.norm(vector)

def axisangle_regular(points_count, main_ax):
    rot_axes, points, main_ax= spiral_dist(points_count, main_ax)
    angle_list = []
    v2_u = unit_vector(main_ax)
    for i in range(0, points_count):
        v1_u = unit_vector(points[i])
        angle_list.append((np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))))
    #print(angle_list)
    return(rot_axes, angle_list)

class CreateRots(object):
    def __init__(self, rots_count,coor_list):
        self.rots_count = rots_count
        self.coor_list = coor_list
        self.z_axis = [0.0,0.0,1.0]
    def axisangle_regular(self):
        self.reg_axes, self.reg_angles = axisangle_regular(self.rots_count,[0.0,0.0,1.0])
        return()
    def create_rots(self):
        self.list_of_all_rots = []
        self.list_of_all_axisangles = []
        axisangle_regular(self.rots_count, self.z_axis)
        surface_xyz = []
        self.reg_axisangle = []
        for i in range(0, self.rots_count):
            reg_axisangle = np.append(self.reg_axes[i], self.reg_angles[i])
            rotation = rotate(reg_axisangle, self.coor_list)
            self.list_of_all_rots.append(rotation)
            self.list_of_all_axisangles.append(reg_axisangle)
            surface_xyz.append((rotation[0]))
        #x = np.array([item[0] for item in surface_xyz])
        #y = np.array([item[1] for item in surface_xyz])
        #z = np.array([item[2] for item in surface_xyz])
        #surface(x,y,z)
        #sys.exit()

        return(self.list_of_all_rots, self.list_of_all_axisangles)


class CreateRotsRefine(CreateRots):
    def __init__(self, rots_count, coor_list, ref_angle, docker_rough_output, ref_line_num):
       CreateRots.__init__(self, rots_count, coor_list) #rots_count = points count on cap
       self.ref_angle = ref_angle
       self.docker_rough_output = docker_rough_output
       self.ref_line_num = ref_line_num
       self.z_axis = [0.0,0.0,0.1]

    def rotate_to_rough_output(self):
        line = linecache.getline(self.docker_rough_output, self.ref_line_num)
        self.axisangle = operator.itemgetter(3,4,5,7)(line.split())
        self.axisangle = list(self.axisangle)
        for i in range(0,len(self.axisangle)):
            self.axisangle[i] = float(self.axisangle[i])
        #self.angle_z = operator.itemgetter(9)(line.split())
        #self.z_axisangle = [0.0,0.0,0.1,float(self.angle_z)]
        #print(self.z_axisangle, self.coor_list)
        #self.rot_global = transform_coordinates.rotate(self.axisangle, self.coor_list) pre pripad, zeby sa to posralo
        #self.coor_list = transform_coordinates.rotate(self.z_axisangle, self.rot_global)
        self.coor_list = transform_coordinates.rotate(self.axisangle, self.coor_list)
        return()

    def get_count_from_angle(self):
        self.whole_count = int((2*self.rots_count)/(1-np.cos(self.ref_angle))) # if I want x points in y degrees around wanted rotation, how many points will be on whole sphere?
        return()

    def axisangle_regular(self): #override parent method
        self.get_count_from_angle()
        golden_angle = np.pi * (3 - np.sqrt(5))
        theta = golden_angle * np.arange(self.whole_count)
        z = np.linspace(1 - 1.0 / self.whole_count, 1.0 / self.whole_count - 1, self.whole_count)
        radius = np.sqrt(1 - z * z)

        self.points = np.zeros((self.rots_count, 3)) #points equaly distributed on sphere
        self.rot_axes = [[] for i in range(0, self.rots_count)]
        self.reg_angles = []
        v2_u = self.z_axis / np.linalg.norm(self.z_axis)
        for i in range(0, self.rots_count):
            self.points[i,0] = radius[i] * np.cos(theta[i])
            self.points[i,1] = radius[i] * np.sin(theta[i])
            self.points[i,2] = z[i]
            self.rot_axes[i] = np.cross(self.points[i], self.z_axis)
            v1_u = self.points[i] / np.linalg.norm(self.points[i])
            self.reg_angles.append((np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))))
        self.reg_axes = np.array(self.rot_axes)
        return()


def rotate_image(img, angle):
    #print(img.dtype)
    #mat = img.astype(np.float32)
    mat = img

    #rotate:

    height, width = mat.shape[:2]
    image_center = (width / 2, height / 2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1)

    radians = math.radians(angle)
    sin = math.sin(radians)
    cos = math.cos(radians)
    bound_w = int((height * abs(sin)) + (width * abs(cos)))
    bound_h = int((height * abs(cos)) + (width * abs(sin)))

    rotation_mat[0, 2] += ((bound_w / 2) - image_center[0])
    rotation_mat[1, 2] += ((bound_h / 2) - image_center[1])

    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))

    #crop black frame:

    #rotated_mat_for_crop = (rotated_mat*1000000000).astype(np.uint8)
    #rotated_mat_for_crop = (rotated_mat).astype(np.uint8)
    #rotated_mat_for_crop = np.int8(rotated_mat*1000000000)
    mask = rotated_mat > 0.01# for zeroes true, for non zeroes false
    rotated_mat = rotated_mat[np.ix_(mask.any(1),mask.any(0))]
    return(rotated_mat)

def rotate_around_z(rots_count, matrix):
    angle = 360/rots_count
    rot_angles = [i*angle for i in range(1,rots_count)] # no rotation around z is default
    #print(rot_angles)
    new_pdb_mat_z_list = []
    angle_z_list = []
    matrix=np.array(matrix)
    for i in range(0, len(rot_angles)):
        new_pdb_mat_rot_z = rotate_image(matrix, rot_angles[i])
        new_pdb_mat_z_list.append(new_pdb_mat_rot_z)
        angle_z_list.append(rot_angles[i]*(np.pi/180))
    #print(len(new_pdb_mat_z_list))
    return(new_pdb_mat_z_list, angle_z_list)

