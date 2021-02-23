import math
from math import *


class Vectors:
    # x,y,z=float(0),float(0),float(0)
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, *args):
        '''
        For adding two vectors
        v1=Vectors(1,2,5)
        v2=Vectors(1,22,2)
        v3=v1+v2
        '''
        x, y, z = float(0), float(0), float(0)
        x = self.x
        y = self.y
        z = self.z
        for value in args:
            x = x + value.x
            y = y + value.y
            z = z + value.z
        obj = Vectors(x, y, z)
        return obj

    def __sub__(self, *args):
        x, y, z = float(0), float(0), float(0)
        x = self.x
        y = self.y
        z = self.z
        for value in args:
            x = x - value.x
            y = y - value.y
            z = z - value.z
        obj = Vectors(x, y, z)
        return obj

    def __mul__(self, *args):
        x, y, z = float(0), float(0), float(0)
        x = self.x
        y = self.y
        z = self.z
        for value in args:
            x = x * value.x
            y = y * value.y
            z = z * value.z
        sum = x + y + z
        return sum

    def magnitude(self):
        value = math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))
        return value

    def angleBetweenVectorsInRadians(self, another):
        c = self * another
        d = self.magnitude() * another.magnitude()
        angle = math.acos(c / d)
        return angle

    def angleBetweenVectorsInDegrees(self, another):
        c = self * another
        d = self.magnitude() * another.magnitude()
        angle = math.acos(c / d)
        return ((180 / math.pi) * angle)

    def printVector(self):
        print(self.x, "i", self.y, "j", self.z, "k")

    def __str__(self):
        return '({}) i+ ({}) j + ({}) k'.format(self.x, self.y, self.z)

    def __ne__(self, object):
        if self.x != object.x or self.y != object.y or self.z != object.z:
            return True
        else:
            return False

    def __eq__(self, object):
        if self.x != object.x or self.y != object.y or self.z != object.z:
            return False
        else:
            return True

    def __ge__(self, object):
        if (self.magnitude() >= object.magnitude()):
            return True
        else:
            return False

    def __gt__(self, object):
        if (self.magnitude() > object.magnitude()):
            return True
        else:
            return False

    def __le__(self, object):
        if (self.magnitude() <= object.magnitude()):
            return True
        else:
            return False

    def __lt__(self, object):
        if (self.magnitude() < object.magnitude()):
            return True
        else:
            return False

    def __pow__(self, object):
        '''
        This function finds the cross product of two vectors 
        Syntax:
                v1=Vectors(x,y,z)
                v2=Vectors(x1,y1,z1)
                v3=v1**v2 --> Finds cross product of v1 with v2
        '''
        x = ((self.y * object.z) - (object.y * self.z))
        y = -((self.x * object.z) - (object.x * self.z))
        z = ((self.x * object.y) - (object.x * self.y))
        crossProduct = Vectors(x, y, z)
        return crossProduct
    
    def unit(self):
        x=self.x/self.magnitude()
        y=self.y/self.magnitude()
        z=self.z/self.magnitude()
        v=Vectors(x,y,z)
        return v
        
    
    def X(self):
        return self.x
    
    def Y(self):
        return self.y
    
    def Z(self):
        return self.z

    def isParallel(self,other):
        if self.unit()==other.unit():
            return True
        else:
            return False
    def isPerpendicular(self,other):
        if self.angleBetweenVectorsInDegrees(other)==90:
            return True
        else:
            return False
        
       





