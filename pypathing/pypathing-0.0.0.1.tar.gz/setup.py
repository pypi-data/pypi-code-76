from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
from numpy import get_include
from os import system


extensions = [Extension( "pypathing.scr.cy_generators", 
                        ["pypathing/scr/cy_generators.pyx"]),
                        
              Extension( "pypathing.scr.cy_searchers",
                        ["pypathing/scr/cy_searchers.pyx"],
                        include_dirs=[get_include()]),

              Extension( "pypathing.scr.cy_nodeGraph",
                        [   "pypathing/scr/cy_nodeGraph.pyx",
                            "pypathing/scr/pathfinding/node_Graph.cpp",
                            "pypathing/scr/pathfinding/node.cpp",
                            "pypathing/scr/pathfinding/Edge.cpp",
                            "pypathing/scr/pathfinding/Cluster.cpp",
                            "pypathing/scr/pathfinding/Astar.cpp",
                            "pypathing/scr/pathfinding/distance.cpp",
                            "pypathing/scr/pathfinding/pathfinders.cpp",
                            "pypathing/scr/pathfinding/hpA_builders.cpp",
                            "pypathing/scr/pathfinding/GoalPathing.cpp",
                            #"pathing/scr/pathfinding/node_Graph.cpp",
                        ],
                        include_dirs=[get_include()])]


#with open("README.rst") as readmeFile:
#    readme = readmeFile.read()



setup(
    name = "pypathing",
    packages = ["pypathing"],
    version="0.0.0.1",
    license="apache-2.0",

    include_package_data = True,

    author = 'Julian Wandhoven',
    author_email = 'julian.wandhoven@gmail.com',

    url="https://github.com/JulianWww/pyPathing",
    
    keywords=["pathfinding"],

    install_requires=[
        "numpy"
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: C++",
        "Programming Language :: Cython",
        "Typing :: Typed",
        'Programming Language :: Python :: 3'
    ],

    ext_modules=cythonize(extensions, annotate=False)
)
