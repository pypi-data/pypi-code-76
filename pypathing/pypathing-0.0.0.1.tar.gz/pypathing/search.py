
from .scr import cy_searchers

import numpy as np
from typing import Tuple, Set

class PathfindingError(Exception):
    "error calles when no path solution was found"

def Dijkstra(maze: np.ndarray, start: Tuple[int, int], end: Set[Tuple[int, int]], timeout: float=None, getScanned=False):
    """A* pathifinding system

        an interface with a c++ A* pathfinder on a maze saved in a np.ndarray

        @param maze: a numpy array containing the maze where the 1 values are the walkable positions
        @type maze: 2d numpy.ndarray

        @param start: the starting position of the maze. the positions must be greater 0 and within the bounds of the maze
        @type start:  tuple<int,int>
        @param start: the end position of the maze. the positions must be greater 0 and within the bounds of the maze
        @type start:  tuple<int,int>
        """

    if not (isinstance(timeout, float) or timeout is None): raise TypeError(f"timeout must be float not {type(timeout).__name__}")
    
    if not isinstance(maze, np.ndarray): raise TypeError(f"the maze must be an numpy array not {type(maze).__name__}")
    if not len(maze.shape) == 2: raise ValueError(f"the maze must be 2 dimentional")
    if not isinstance(start, (tuple, list)): raise TypeError(f"start must be a tuple not {type(start).__name__}")
    if not len(start) == 2: raise ValueError(f"start must have a length of 2")

    if not isinstance(start[0], int): raise TypeError(f"start x pos must be int not {type(start[0]).__name__}")
    if not isinstance(start[1], int): raise TypeError(f"start x pos must be int not {type(start[1]).__name__}")

    if not maze.shape[0] > start[0] >= 0: raise ValueError(f"start x pos is out of range must be greater equal 0 and les than the size of the maze")
    if not maze.shape[1] > start[1] >= 0: raise ValueError(f"start y pos is out of range must be greater equal 0 and les than the size of the maze")
    
    if not isinstance(end, (list, tuple, set)): raise TypeError(f"end must be tuple or list not {type(end).__name__}")
    for end_val in end:
        if not isinstance(end_val, (tuple, list, set)): raise TypeError(f"end must be a tuple not {type(end_val).__name__}")
        if not len(end_val) == 2: raise ValueError(f"end must have a length of 2")

        if not isinstance(end_val[0],   int): raise TypeError(f"end x pos must be int not {type(end_val[0]).__name__}")
        if not isinstance(end_val[1],   int): raise TypeError(f"end x pos must be int not {type(end_val[1]).__name__}")
    
        if not maze.shape[0] > end_val[0]   >= 0: raise ValueError(f"end x pos is out of range must be greater equal 0 and les than the size of the maze")
        if not maze.shape[1] > end_val[1]   >= 0: raise ValueError(f"end x pos is out of range must be greater equal 0 and les than the size of the maze")

    res = cy_searchers.Dijkstra_cy(maze, list(start), list(end), getScanned)
    if res[0,0] == -1:
        raise PathfindingError("no pathfinding solution was found")
    return res

def Astar(maze: np.ndarray, start: Tuple[int, int], end: Set[Tuple[int, int]], timeout: float=None, getScanned=False, fast=True):
    """A* pathifinding system

        an interface with a c++ A* pathfinder on a maze saved in a np.ndarray

        @param maze: a numpy array containing the maze where the 1 values are the walkable positions
        @type maze: 2d numpy.ndarray

        @param start: the starting position of the maze. the positions must be greater 0 and within the bounds of the maze
        @type start:  tuple<int,int>
        @param start: the end position of the maze. the positions must be greater 0 and within the bounds of the maze
        @type start:  tuple<int,int>
        @param timeout: dosnt do anything
        @param getScanned: weather or not the scanned positions schould be returned
        @type getScanned: bool
        @param fast: wheather to use a weanrd c++ change that makes it 100 times faster but less acurate
        @type fast: bool
        """
    if not  isinstance(fast, bool): return TypeError(f"param fast must be bool not {type(fast).__name__}")
    if not (isinstance(timeout, float) or timeout is None): raise TypeError(f"timeout must be float not {type(timeout).__name__}")
    
    if not isinstance(maze, np.ndarray): raise TypeError(f"the maze must be an numpy array not {type(maze).__name__}")
    if not len(maze.shape) == 2: raise ValueError(f"the maze must be 2 dimentional")
    if not isinstance(start, (tuple, list)): raise TypeError(f"start must be a tuple not {type(start).__name__}")
    if not len(start) == 2: raise ValueError(f"start must have a length of 2")

    if not isinstance(start[0], int): raise TypeError(f"start x pos must be int not {type(start[0]).__name__}")
    if not isinstance(start[1], int): raise TypeError(f"start x pos must be int not {type(start[1]).__name__}")

    if not maze.shape[0] > start[0] >= 0: raise ValueError(f"start x pos is out of range must be greater equal 0 and les than the size of the maze")
    if not maze.shape[1] > start[1] >= 0: raise ValueError(f"start y pos is out of range must be greater equal 0 and les than the size of the maze")
    
    if not isinstance(end, (list, tuple, set)): raise TypeError(f"end must be tuple or list not {type(end).__name__}")
    for end_val in end:
        if not isinstance(end_val, (tuple, list, set)): raise TypeError(f"end must be a tuple not {type(end_val).__name__}")
        if not len(end_val) == 2: raise ValueError(f"end must have a length of 2")

        if not isinstance(end_val[0],   int): raise TypeError(f"end x pos must be int not {type(end_val[0]).__name__}")
        if not isinstance(end_val[1],   int): raise TypeError(f"end x pos must be int not {type(end_val[1]).__name__}")
    
        if not maze.shape[0] > end_val[0]   >= 0: raise ValueError(f"end x pos is out of range must be greater equal 0 and les than the size of the maze")
        if not maze.shape[1] > end_val[1]   >= 0: raise ValueError(f"end x pos is out of range must be greater equal 0 and les than the size of the maze")

    res = cy_searchers.Astar_cy(maze, list(start), list(end), getScanned, fast)
    if res[0,0] == -1:
        raise PathfindingError("no pathfinding solution was found")
    return res