#!/usr/bin/env python3
from read_pdb import read_pdb
from transform_coordinates import rotate
import operator
import transform_coordinates

def outer_function(a,b):
    return(a+b)

class Trieda(object):

    def __init__(self, a,b):
        self.a = a
        self.b = b
        self.seznam = [1,2,3]
    def add(self):
        #self.c = self.a + self.b
        self.c = outer_function(self.a,self.b)
        return(self.c)
    def mult(self):
        self.add()
        xyz = self.a * self.c
        self.d = xyz
        self.seznam.append(self.d)
        return(self.seznam)

trieda1 = Trieda(6,6)
#print(trieda1.add())
print(trieda1.mult())
