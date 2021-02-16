# /usr/bin/python3

import pandas as pd

if not __package__:
    from cytolysis.fibers import Fiber_set
    from cytolysis.couples import Couple_set
    from cytolysis.objects import Object_set
    from cytolysis import read_config as rc
    from cytolysis import anutils as an
else:
    from .fibers  import Fiber_set
    from .couples import Couple_set
    from .objects import Object_set
    from . import read_config as rc
    from . import anutils as an

__IPV__ = False
try:
    import ipyvolume as ipv
    from ipywidgets import widgets, interact
    __IPV__ = True
except:
    print("Unable to import Ipyvolume")

__VERSION__ = "0.0.21"

"""
    A module to analyze cytosim simulations

    see README.txt for operation
"""

########## TODO :
# - have yaml config ? at least a default conf ! e.g. for dimension=2 or =3

##### General architecture :
# Objects (fibers, couples...) are stored in objects sets, one object set by frame and by name
#   Each object_set contains methods to analyze its components : object_set.analyze(object, ... )
#   Simulation is a set of frame
#   Analysis are passed through dictionaries of functions { 'object_name' : { 'property' :  function } }




export_analysis=an.export_analysis

# Each frame contains a fibers, couples, and stuff
class Frame():
    """
    A frame is a data structure containing several Fibers, Couples, Space, etc.
        frame.fibers is a dictionary, e.g. {'microtubules' : list_MT] }
        where list_MT = [MT1, MT2, ... ], with MT1, MT2, ... being instances of class Fiber

    """
    def __init__(self, *args, number=None, **kwargs):
        self.fibers = {}
        self.couples = {}
        #self.spaces = {}
        self.objects = {}

        self.analysis = None
        self.id = number
        self.initialize(*args, **kwargs)

        self.all_sets = [self.fibers, self.couples, self.objects]

    def initialize(self, *args,
                   fibers_lines={}, couples_lines={}, objects_lines={},
                   config=None, options={}, **kwargs):

        # Fibers factory :
        for name, lines_dict in fibers_lines.items():
            opt = an.get_options(options, name)
            self.fibers[name] = Fiber_set(name=name, reports=lines_dict, config=config, **opt)

        # Couples factory
        for name, lines_dict in couples_lines.items():
            opt = an.get_options(options, name)
            self.couples[name] = Couple_set(name=name, reports=lines_dict, config=config, **opt)

        # Custom objects factory
        for name, lines_dict in objects_lines.items():
            opt = an.get_options(options, name)
            self.objects[name] = Object_set(name=name, reports=lines_dict, config=config, **opt)

        # and so on...


    def make_analysis(self, *args, **kwargs):

        self.fibers_analysis = an.make_analysis(self.fibers,*args,**kwargs)
        self.couples_analysis = an.make_analysis(self.couples,*args,**kwargs)
        self.objects_analysis = an.make_analysis(self.objects, *args, **kwargs)

    def plot(self,*args, options=None, **kwargs):
        for set in self.all_sets:
            for name, set in set.items():
                opts={}
                if options is not None:
                    try:
                        opts = options[name]
                    except:
                        opts = {}
                set.plot(*args, **opts,  **kwargs)

        return None

    def hide(self):
        for set in self.all_sets:
            for name, set in set.items():
                for plot in set.plots:
                    plot.visible=False

    def show(self):
        for set in self.all_sets:
            for name, set in set.items():
                for plot in set.plots:
                    plot.visible = True


class Simulation(list):
    """
    Simulation is the main class
        it is a list of frames  initiated with reports and config files,
        eg : config=config.cym, fibers_reports={ "microtubule" : { "points" : "fiber_points.txt" } }
        ...
    """
    def __init__(self,*args, **kwargs):
        list.__init__(self)
        self.config=None
        self.analysis=None
        self.frames_analysis=None
        self.properties={}
        self.name='frame'
        self.id = 0
        self.n_frames=0
        self.shown = False
        # Actual initialization
        self.initialize(*args,**kwargs)

    # Initialization step
    def initialize(self, *args,
                   fibers_report={}, couples_report={}, objects_report={},
                   config=None, **kwargs):

        """
            We actually build the simulation here
            We will make the frames from the report files using iterators over these files

            x_iter is a dictionary of dictiionaries of iterators :
            e.g.
            fibers_iter = { "microtubule" : { "points" : iterator_to_fiber_points } }
        """

        if config is not None:
            self.read_config(config, *args, **kwargs)

        fibers_iter = an.make_iter_dict(fibers_report)
        objects_iter = an.make_iter_dict(objects_report)
        couples_iter = an.make_iter_dict(couples_report)



        # We skip the first lines until "% frames"
        # Treat this as a dirty hack if you want.
        fibers_block, f_flag = an.make_block_dict(fibers_iter)
        couples_block, c_flag = an.make_block_dict(couples_iter)
        objects_block, o_flag = an.make_block_dict(objects_iter)

        # Now we iterate upon the config files
        keep = True
        while keep:

            fibers_block, f_flag = an.make_block_dict(fibers_iter)
            couples_block, c_flag = an.make_block_dict(couples_iter)
            objects_block, o_flag = an.make_block_dict(objects_iter)

            if not f_flag and not c_flag and not o_flag:
                keep = False
            else:
                self.append(Frame(*args, number=len(self),
                                  fibers_lines=fibers_block, couples_lines=couples_block, objects_lines=objects_block,
                                  config=self.config, **kwargs))

        self.n_frames = len(self)


    def read_config(self, config, simul_props={}, **kwargs ):

        self.config = rc.parse(config)
        com = ['set', 'simul', '*']
        props = an.get_dict_from_pile(self.config, com)
        self.properties = {**self.properties, **props, **simul_props}


    def analyze(self, frame, *args, analyzer=None, **kwargs):

        analysis = {'id': frame.id}
        if analyzer is not None:
            for name,func in analyzer.items():
                analysis[name] = func(frame)

        return analysis


    def make_analysis(self,*args, analyzer=None, **kwargs):
        for frame in self:
            frame.make_analysis(*args, analyzer=analyzer, **kwargs)

        self.frames_analysis = an.objects_analysis(self, *args, analyzer=analyzer, **kwargs)

        try:
            analyzer = analyzer['simulation']
        except:
            analyzer = None

        analysis = {}
        if analyzer is not None:
            for name, func in analyzer.items():
                analysis[name] = func(self)

        if analysis:
            keys = analysis.keys()
            datas = pd.DataFrame(columns=keys)
            datas.loc[self.id] = [analysis[key] for key in keys]
            self.analysis = datas

    def show(self, *args, **kwargs):
        if not __IPV__:
            raise ValueError("Could not import module iPyVolume")
        else:

            if len(args) == 0:
                ipv.show()
                self.shown=True
            else:
                number=args[0]
                if len(args)>1:
                    args = args[1:]
                else:
                    args = []

                self[number].plot(*args, **kwargs)

    def plot(self, number, *args, **kwargs):
        if not __IPV__:
            raise ValueError("Could not import module iPyVolume")
        else:
            self[number].plot(*args, **kwargs)

    def plot_all(self, *args, **kwargs):
        if not __IPV__:
            raise ValueError("Could not import module iPyVolume")
        else:
            for frame in self:
                frame.plot(*args, **kwargs)

    def show_frame(self, number, *args, **kwargs):
        for frame in self:
            if frame.id == number:
                frame.show()
            else:
                frame.hide()

    def frame_player(self, interval=2000, *args, **kwargs):
        if not __IPV__:
            raise ValueError("Could not import module iPyVolume")
        else:
            self.plot_all(*args, **kwargs)
            self.show_frame(0)

            #play = widgets.Play( interval=interval, value=0, min=0, max=len(self)-1, step=1 )
            slider = widgets.IntSlider(value=0, min=0, max=len(self)-1,step=1)

            #widgets.jslink((play, 'value'), (slider, 'value'))
            interact(self.show_frame, number=slider)
            self.show()
            #widgets.HBox([play, slider])

    def figure(self):
        if not __IPV__:
            raise ValueError("Could not import module iPyVolume")
        else:
            ipv.figure()
