#!/usr/bin/env python3
from read_pdb import read_pdb
from transform_coordinates import rotate
import operator
import transform_coordinates
import math

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

class PodTrieda(Trieda):

    def __init__(self,a,b,g):
        Trieda.__init__(self, a,b)
        self.g = g
        self.a = a+b
    def power(self):
        self.f = math.pow(self.a,self.g)
        return(self.f)



trieda1 = Trieda(2,3)
print(trieda1.a)
print(trieda1.add())

podtrieda1=PodTrieda(2,3,4)
print(podtrieda1.a)
print(podtrieda1.add())

#print(podtrieda1.add())
#a = podtrieda1.power()
#print(a)
#print(trieda1.mult())
