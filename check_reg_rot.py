#/usr/bin/env python3

import numpy as np
from rotate import axisangle_regular
from transform_coordinates import rotate_vec, normalize
from surface3d_demo2 import surface
rot_axes, angle_list = axisangle_regular(100, [0,0,1])

#print(rot_axes)
rots = []
for i in range(0,len(rot_axes)):
    rot_axes[i] = normalize(rot_axes[i])
for i in range(0, len(rot_axes)):
    rot_axisangle = np.append(normalize(rot_axes[i]),angle_list[i])
    print(rot_axisangle)
    new_xyz = rotate_vec(rot_axisangle,normalize((0,0,100)))
    rots.append(new_xyz)
rots = np.array(rots)
rots_x = rots[:,0]
rots_y = rots[:,1]
rots_z = rots[:,2]
surface(rot_axes[:,0], rot_axes[:,1], rot_axes[:,2])
surface(rots_x, rots_y, rots_z)

