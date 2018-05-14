#!/usr/bin/env python3
import sys
import transform_coordinates
import numpy as np
import linecache
import argparse
import os

def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z

def qv_mult(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)

def read_docker_output(textfiles, linenums):
    if(len(textfiles) != len(linenums)):
        print("Count of textfiles and linenums must equal")
        sys.exit()
    axis_angles = []
    for i in range(0,len(textfiles)):
        line = linecache.getline(textfiles[i],linenums[i]).split()
        #print(line)
        axis_angles.append([float(line[3]),float(line[4]),float(line[5]),float(line[7])])
    #print(axis_angles)
    return(axis_angles)

def relative_rot(axis_angle_1, axis_angle_2):
    def inverse_quat(quat):
        q_conj = np.array(q_conjugate(quat))
        q_inv =  np.array(q_conjugate(quat))/np.sqrt(quat[0]**2+quat[1]**2+quat[2]**2+quat[3]**2)
        return(q_inv)
    quat1 = axisangle_to_q(axis_angle_1[3], axis_angle_1[:3])
    inverse_quat1 = inverse_quat(quat1)
    quat2 = axisangle_to_q(axis_angle_2[3], axis_angle_2[:3])
    q_result = q_mult(quat2, inverse_quat1)
    axis_angle = q_to_axisangle(q_result)
    return(axis_angle)

def normalize(xyz, tolerance=0.00001):
    #print(xyz)
    xyz = [i*100 for i in xyz]
    mag2 = sum(n * n for n in xyz)
    if abs(mag2 - 1.0) > tolerance:
        mag = np.sqrt(mag2)
        xyz = tuple(n / mag for n in xyz)
    return xyz

def q_to_axisangle(q):
    imag = q[1:4]
    real = q[0]
    quat_abs = np.sqrt((imag[0]**2)+(imag[1]**2)+(imag[2]**2))
    axis = np.array(imag)/quat_abs
    angle = 2*np.arctan2(quat_abs, real)
    axis = list(axis)
    axis.append(angle)
    return(axis) # axis+angle

def axisangle_to_q(phi, axis):
    axis = normalize(axis)
    x, y, z = axis
    phi = phi/2
    w = np.cos(phi)
    x = x * np.sin(phi)
    y = y * np.sin(phi)
    z = z * np.sin(phi)
    return w, x, y, z

def get_output(textfiles, linenums, outputfile):
    relative_rots = []
    axis_angles = read_docker_output(textfiles, linenums)
    #print(axis_angles)
    for j in range(0,len(axis_angles)-1):
        #try:
        relative_rots.append(relative_rot(axis_angles[j], axis_angles[j+1]))
        #except IndexError:
            #print("The last rotation reached")

    if (os.path.isfile(outputfile) == True):
        print("Output file already exists, enter another name.")
        sys.exit()
    with open (outputfile,mode="w") as textfile:
        textfile.write("Rotation from default to first position:\n axis:{0:.5f} {1:.5f} {2:.5f} angle: {3:.5f} \n Rotation between positions: \n".format(axis_angles[0][0],axis_angles[0][1], axis_angles[0][2], axis_angles[0][3]))
        for k in range(0,len(relative_rots)):
            textfile.write("{0:.0f} and {1:.0f}: axis: {2:.5f} {3:.5f} {4:.5f} angle: {5:.5f}".format(k+1,k+2,relative_rots[k][0], relative_rots[k][1], relative_rots[k][2], relative_rots[k][3]))
        #lines = textfile.readlines()
    return(0)

def Main():
    parser = argparse.ArgumentParser(description='Get relative rotations between 2 or more rotations of pdb file. The input is output text file of docker. The output of the program is textfile with default rotation (rotation from default pdb to position 1) and then relative rotation from position 1 to 2, 2 to 3 etc.', epilog="Example: \n I want to combine rotaion 2 (2nd line) from a.txt (position 1), rotation 3 from b.txt (position 2) and rotation 5 from c.txt (position 3): \n ./combine_rots.py --files a.txt b.txt c.txt --line_nums 2 3 5 -o outputfile.txt")
    parser.add_argument('-f','--files', nargs='+', help="Docker output files")
    parser.add_argument('-l','--line_nums', nargs='+', type=int, help="Number of line")
    parser.add_argument('-o','--output', help = "Name of output file", type=str)
    args = parser.parse_args()
    get_output(args.files, args.line_nums, args.output)

    return()
if __name__  == '__main__' :
            Main()
