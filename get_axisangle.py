#!/usr/bin/env python3
import sys
import transform_coordinates
import numpy as np

in_axisangle = sys.argv[2]
in_axisangle = in_axisangle.split(",")
for i in range(0,len(in_axisangle)):
    in_axisangle[i] = float(in_axisangle[i])
in_quat_glob = transform_coordinates.axisangle_to_q(in_axisangle[3],transform_coordinates.normalize(in_axisangle[0:3]))
#print(in_axisangle[0:3])
in_quat_z = transform_coordinates.axisangle_to_q(float(in_axisangle[4]),[0,0,1])
q_designed = transform_coordinates.q_mult(in_quat_z, in_quat_glob)
in_axisangle = transform_coordinates.q_to_axisangle(q_designed)

with open (sys.argv[1]) as textfile:
    lines = textfile.readlines()
    for line in lines:
        vecs_split = line.split()
        glob_rot = vecs_split[0].split(",")
        for i in range(0,len(glob_rot)):
            glob_rot[i] = float(glob_rot[i])
        z_rot = vecs_split[1].split(",")
        for i in range(0,len(glob_rot)):
            z_rot[i] = float(z_rot[i])
        quat_glob = transform_coordinates.axisangle_to_q(glob_rot[3],glob_rot[0:3])
        quat_z = transform_coordinates.axisangle_to_q(z_rot[3],z_rot[0:3])
        quat_glob_z = transform_coordinates.q_mult(quat_z,quat_glob)
        axisangle_glob_z = transform_coordinates.q_to_axisangle(quat_glob_z)
        #rel_rot = transform_coordinates.relative_rot(in_axisangle, axisangle_glob_z)[3]
        rel_rot = transform_coordinates.relative_rot(in_axisangle,axisangle_glob_z)
        #if(abs(rel_rot) < np.pi):
        print(rel_rot)
        #else:
            #print(2*np.pi-abs(rel_rot))
