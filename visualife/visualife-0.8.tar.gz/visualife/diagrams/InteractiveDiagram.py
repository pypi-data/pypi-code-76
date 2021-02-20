#! /usr/bin/env python

import copy
from visualife.diagrams.Diagram import *


class InteractiveNode(NodeBase):

    def __init__(self, node, code_snippet, **params):
        """Extends :class:`InteractiveNode` with a code snipped.
        
        This class both contains and extends a :class:`NodeBase`, calls to the base class
        are delegated to the node instance
        """

        self.__code_snippet = code_snippet
        self.next_command = None
        self.__node = node
        self.__lines = []
        if "lines" in params:
            self.__lines.append(int(params["lines"]))

    def __str__(self):
        """Returns the code snippet assigned to this node

        :return: (``string``) code snippet that will be executed by this node
        """
        return self.__code_snippet

    @property
    def id(self):
        return self.__node.id

    @property
    def left(self):
        return self.__node.left

    @property
    def right(self):
        return self.__node.right

    @property
    def top(self):
        return self.__node.top

    @property
    def bottom(self):
        return self.__node.bottom

    @property
    def height(self):
        return self.__node.height

    @property
    def width(self):
        return self.__node.width

    @property
    def x(self): return self.__node.x

    @x.setter
    def x(self, x): self.__node.x = x

    @property
    def y(self): return self.__node.y

    @y.setter
    def y(self, y): self.__node.y = y

    @property
    def code_snippet(self):
        """Returns the code snippet assigned to this node

        :return: (``string``) code snippet that will be executed by this node
        """
        return self.__code_snippet

    @property
    def node(self):
        """Returns the node object used to display this :class:`InteractiveNode`

        :return: (:class:`NodeBase`) node object
        """
        return self.__node

    def execute(self, global_variables, local_variables):
        print("CODE to run: ", self.__code_snippet, global_variables, local_variables)
        exec(self.__code_snippet, global_variables, local_variables)
        return self.next_command

    def draw(self, viewport, **kwargs):
        self.__node.draw(viewport)

    def highlight(self, state=True):
        self.__node.highlight(state)


class InteractiveCondition(InteractiveNode):

    def __init__(self, node, code_snippet, **params):
        super().__init__(node, code_snippet, **params)
        self.__true_command = None
        self.__false_command = None

    @property
    def true_command(self):
        return self.__true_command

    @true_command.setter
    def true_command(self, true_command):
        self.__true_command = true_command

    @property
    def false_command(self):
        return self.__false_command

    @false_command.setter
    def false_command(self, false_command):
        self.__false_command = false_command

    def execute(self, global_attrs):
        result = eval(self.code_snippet, global_attrs)
        self.next_command = self.__true_command if result else self.__false_command
        return self.next_command


class InteractiveDiagram(Diagram):

    def __init__(self, viewport, id):
        """Diagram that can execute code snippets

        This class is devised to draw interactive algorithm diagrams on a web page.

        :param viewport: where to actually draw the line
        :param id: (``string``) unique ID of this diagram
        """
        super().__init__(viewport, id)
        self.__globals = {}
        self.__locals = {}
        self.__next_cmd = None
        self.__start_cmd = None
        self.__stop_cmd = None
        self.__i_stop = 0

    @property
    def next_command(self):
        """Returns the text command that will be executed by this diagram

        :return: (:class:`InteractiveNode`) a node that will be executed by the incomming
            :meth:`next` method call
        """
        return self.__next_cmd

    def add_start(self, *location, **attrs):
        """ Add a START node of a block diagram

        :param xc: (``number``) x coordinate
        :param yc: (``number``) y coordinate
        :param attrs: see below
        :return: :class:`InteractiveNode`

        :Keyword Arguments:
            * *text_style* (``string``) --
              a dictionary holding style settings for text
            * *node_style* (``string``) --
              a style for drawing
        """

        if len(location) == 2:
            xc, yc = location[0], location[1]
        else:
            xc, yc = 0, 0
        start = InteractiveNode(RectNode("start", "start", xc, yc, 80, 30, **dict(node_style={"rx": 20, "ry": 20}, **attrs)), "True", **attrs)
        super(InteractiveDiagram, self).add_node(start, **attrs)
        self.__start_cmd = start
        return start

    def add_stop(self, *location, **attrs):
        """ Add a STOP node of a block diagram

        :param location: (``number, number``) x and y coordinates of the middle of the stop node
        :param attrs: see below
        :return: :class:`InteractiveNode`

        :Keyword Arguments:
            * *text_style* (``string``) --
              a dictionary holding style settings for text
            * *node_style* (``string``) --
              a style for drawing
        """
        if len(location) == 2:
            xc, yc = location[0], location[1]
        else:
            xc, yc = 0, 0
        stop = InteractiveNode(RectNode("stop-"+str(self.__i_stop), "stop", xc, yc, 80, 30,
                                        **dict(node_style={"rx": 20, "ry": 20}, **attrs)), "True", **attrs)
        self.__i_stop += 1
        super(InteractiveDiagram, self).add_node(stop, **attrs)
        self.__stop_cmd = stop
        return stop

    def add_node(self, node, **attrs):
        c = super().add_node(node, **attrs)
        if "follows" in attrs:
            attrs["follows"].next_command = node
        return c

    def start(self):
        self.highlight(False)
        self.__next_cmd = self.__start_cmd
        self.__next_cmd.highlight(True)

    def next(self, if_debug=False):
        """Executes the next node of this diagram

        The executed node will be highlighted, the previous node will be turned back
        to its normal color and the code snippet that is associated to the entered node 
        will be executed by a Python interpreter
        
        :param: if_debug (``boolean``) if true, this method will print debug info on the console
        :return: (``boolean``) ``True`` when the algorithm reached its end
        """

        self.__next_cmd.highlight(False)
        if if_debug: print("entering next", self.__next_cmd, self.__globals, self.__locals)
        if self.__next_cmd == self.__stop_cmd: return True
        self.__next_cmd = self.__next_cmd.execute(self.__globals, self.__locals)
        self.__next_cmd.highlight(True)
        return False

    def has_next(self):
        """``True`` if there is more commands to be executed

        :return: (``boolean``)
        """
        return not self.__next_cmd == self.__stop_cmd

    def declare_variables(self, **kwargs):
        for n, v in kwargs.items():
            self.__locals[n] = v

    def list_variables(self):
        return self.__globals.keys()

    def set_value(self, name, value):
        self.__globals[name] = value

    def get_value(self, name):
        return self.__globals.get(name, "")

    def globals_copy(self):
        return copy.deepcopy(self.__globals)

    def locals_copy(self):
        return copy.deepcopy(self.__globals)
