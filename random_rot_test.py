#/usr/bin/env python3
from rotate import ranvec, create_rots

x,y,z,ang = ranvec(2)
rots, axisangles = create_rots(1000, 2, [[1.0,0.0,0.0]] )
print("1000")
print("sadfs")
print(axisangles)
print(rots)
#for i in range(0, len(rots)):
#   print("{} {} {}".format(rots[i][0][0],rots[i][0][1],rots[i][0][2]))

