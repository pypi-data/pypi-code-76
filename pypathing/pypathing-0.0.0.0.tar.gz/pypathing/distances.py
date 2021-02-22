from numpy import array

class __PathfindingDistances:
    @property
    def diagonal(self):
        """diagonal distance key
            
            sqrt(dx**2+dy**2+dz**2)"""
        return 0

    @property
    def fastDiagonal(self):
        """fast diagonal distance key
            
            dx**2+dy**2+dz**2"""
        return 1

    @property
    def manhattan(self):
        """manhattan distance key
            dx+dy+dz"""
        return 2
    
    @property
    def dijkara(self):
        """dont use any distance aproximantion
        
            well actualy all estimations are 1"""
        return -1


class __directions:
    "the directions"
    @property
    def noDiagonal(self):
        return 0
    
    @property
    def fullDiagonal(self):
        return 4
    
    @property
    def oneObstacleBlock(self):
        return 1
    
    @property
    def towObstacleBlock(self):
        return 2
    
    @property
    def threeObstacleBlock(self):
        return 3

distance = __PathfindingDistances()
directions= __directions()