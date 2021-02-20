import json
from browser import window, document, html, bind
from visualife.utils.text_utils import substitute_template


class StructureViewer:
    """Represents a viewer for biological molecules.

    It contains NGL viewer inside. It may display .pdb or .mol formats.
    See full documentation here http://nglviewer.org

    The following example shows how to load a PDB file from a local directory:

    .. raw:: html

      <script src="https://cdn.rawgit.com/arose/ngl/v2.0.0-dev.32/dist/ngl.js"></script>
      <style> .d {width:200px; overflow: hidden; display: inline-block;} </style>
      <div id="show_3d_A" class="d"></div> <div id="show_3d_B" class="d"></div> <div id="show_3d_C" class="d"></div>
      <script type="text/python">
        from visualife.widget import StructureViewer

        panel3d_A = StructureViewer("show_3d_A",backgroundColor="white", width=200, height=200, menu_buttons={})
        panel3d_A.add_model("1", "../_static/2q9f.pdb")
        panel3d_B = StructureViewer("show_3d_B",backgroundColor="white", width=200, height=200, menu_buttons={})
        panel3d_B.add_model("1", "2gb1")
        pdb_txt = "ATOM    408  N   LYS A  28      -2.867   6.554  -3.724  1.00  0.17           N"
        pdb_txt += "\\n" + "ATOM    409  CA  LYS A  28      -2.011   7.699  -3.277  1.00  0.21           C"
        pdb_txt += "\\n" + "ATOM    410  C   LYS A  28      -1.865   7.707  -1.749  1.00  0.19           C"
        pdb_txt += "\\n" + "ATOM    411  O   LYS A  28      -0.810   8.013  -1.230  1.00  0.23           O"
        panel3d_C = StructureViewer("show_3d_C",backgroundColor="white", width=200, height=200, menu_buttons={})
        panel3d_C.add_model("1", pdb_txt)
        panel3d_C.as_sticks()
      </script>

    It has been created by the following code:

    .. code-block:: Python

        from visualife.widget import StructureViewer

        panel3d_A = StructureViewer("show_3d_A",backgroundColor="white", width=200, height=200, menu_buttons={})
        panel3d_A.add_model("1", "../_static/2q9f.pdb")
        panel3d_B = StructureViewer("show_3d_B",backgroundColor="white", width=200, height=200, menu_buttons={})
        panel3d_B.add_model("1", "2gb1")
        pdb_txt = "ATOM    408  N   LYS A  28      -2.867   6.554  -3.724  1.00  0.17           N"
        pdb_txt += "\\n" + "ATOM    409  CA  LYS A  28      -2.011   7.699  -3.277  1.00  0.21           C"
        pdb_txt += "\\n" + "ATOM    410  C   LYS A  28      -1.865   7.707  -1.749  1.00  0.19           C"
        pdb_txt += "\\n" + "ATOM    411  O   LYS A  28      -0.810   8.013  -1.230  1.00  0.23           O"
        panel3d_C = StructureViewer("show_3d_C",backgroundColor="white", width=200, height=200, menu_buttons={})
        panel3d_C.add_model("1", pdb_txt)
        panel3d_C.as_sticks()
    """

    def __init__(self, div_id, **kwargs):

        self.__div_id = div_id
        self.__pdbs = {}
        self.__models = {}
        self.__active_selection_dict = {}
        stage = window.NGL.Stage
        background_color = kwargs.get('backgroundColor',"black")
        
        self.__on_clear = []

        self.__to_write = """
        <div id="viewer-{%ID%}" style="height:{%height%}px; width:{%width%}px;"></div>
        <div id="buttons-{%ID%}" style="display: flex; flex-direction: row; width:{%width%}px; flex-wrap:wrap;">
        </div>
        """

        replacement = {"{%ID%}": div_id, "{%width%}": kwargs.get("width", 500),
                       "{%height%}": kwargs.get("height", 500)
                       }

        document[div_id].innerHTML = substitute_template(self.__to_write, replacement)
        self.__stage = stage.new("viewer-"+div_id, { 'backgroundColor': background_color } )
        
        # Definition of the default menu
        default_menu = {"sticks": "as_sticks", "cartoon": "as_cartoon", "center": "center",
                         "zoom ligand" : "zoom_heteroatom","clear all": "clear",}
        # --- Here we create the menu based on **kwargs; if not provided: a default menu will be made
        menu_def = kwargs.get("menu_buttons", default_menu)
        for name, func in menu_def.items():
            self.add_to_menu(name,func)

    def add_to_menu(self, button_name, callback):
        """Adds a button to the menu, binds a callback to the button_name

        :param button_name: ``string`` name for button
        :param callback: function or ``string`` to bind on click
        """
        button_id = button_name + "-" + self.__div_id
        button_el = html.INPUT(button_name, id=button_id, Class="GLViewerWidget-button", type="button", value=button_name)
        document["buttons-" + self.__div_id] <= button_el
        if callable(callback):
            button_el.bind("click",callback)
        else:
            button_el.bind("click", getattr(self, callback))

    def replace_bfactors(self, model_id, bf_values):
        """ Replaces B-factor values with given values

        Every atom of an i-th residue gets bf_values[i]
        :param model_id: ``string`` id that define a model to be affected
        :param bf_values: ``list`` list of values to be used
        """
        def process_component(component):
            N = len(bf_values)

            def bf_action(atom):
                atom.bfactor = bf_values[atom.residueIndex % N]

            component.structure.eachAtom(bf_action)

        self.__models[model_id].then(process_component)

    def as_sticks(self, evt=None):
        """Displays a molecule or its fragment as sticks

        The method will be applied to residues (chains, atoms) that have been recently selected
        by ``active_selection()`` method. By default the whole structure is selected

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :param kwargs: see below
        :return: None
        """

        def color(o):
            o.removeAllRepresentations()
            o.addRepresentation('licorice', { 'color': 'element' })

        for i in self.__models:
            self.__models[i].then(color)

    def as_lines(self, evt=None):
        """Displays a molecule or its fragment as lines

        The method will be applied to residues (chains, atoms) that have been recently selected
        by ``active_selection()`` method. By default the whole structure is selected

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :param kwargs: see below
        :return: None
        """
        def color(o):
            o.removeAllRepresentations()
            o.addRepresentation('lines', { 'color': 'element' })

        for i in self.__models:
            self.__models[i].then(color)

    def as_spheres(self, evt=None):
        """Displays a molecule or its fragment as spheres

        The method will be applied to residues (chains, atoms) that have been recently selected
        by ``active_selection()`` method. By default the whole structure is selected

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :param kwargs: see below
        :return: None
        """
        def color(o):
            o.removeAllRepresentations()
            o.addRepresentation('spacefill', { 'color': 'element'})

        for i in self.__models:
            self.__models[i].then(color)

    def as_cartoon(self, evt=None):
        """Displays a molecule or its fragment as cartoon

        The method will be applied to residues (chains, atoms) that have been recently selected
        by ``active_selection()`` method. By default the whole structure is selected

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        """
        def color(o):
            o.removeAllRepresentations()
            o.addRepresentation('cartoon', { 'sele':'not hetero','color': 'atomindex' })
            o.addRepresentation('licorice', { 'sele':'hetero','color': 'element' })

        for i in self.__models:
            self.__models[i].then(color)

    def center(self, evt=None):
        """Centers the scene"""
        self.__stage.autoView()

    def add_model(self, model_id, URL, **kwargs):
        """Adds a new structure to this viewer.

        :param model_id: ``string`` ID used to identify that molecule
        :param URL: ``string`` | ``File`` | ``Blob`` either a URL or an object containing the file data:

            * a four character string is assumed to be a PDB code of a protein to be downloaded from the PDB website
            * a string that contains multiple lines is assumed to be a PDB-formatted text
            * other strings are recognized as local file names
            * blob and file objects are handled by NGL instance directly

        :param kwargs: see below
        :return: Promise object of StructureComponent or a SurfaceComponent
        """

        params = {"ext": "pdb", 'defaultRepresentation': True}
        if "as_trajectory" in kwargs:
            params["asTrajectory"] = kwargs["as_trajectory"]
        if len(URL.split()) > 1:
            print("loading PDB text")
            stringBlob = window.Blob.new([URL], {"type": 'text/plain'})
            m = self.__stage.loadFile(stringBlob, params)
        else:
            if len(URL) == 4 and URL[0].isdigit():
                print("fetching: rcsb://" + URL + ".pdb")
                m = self.__stage.loadFile("rcsb://" + URL + ".pdb")
            else:
                m = self.__stage.loadFile(URL, params)

        self.__pdbs[model_id] = URL
        self.__models[model_id] = m
        self.as_cartoon()
        return m

    def remove_model(self, model_id):
        """Removes a model from this widget and from the NGL viewer

        :param model_id: ``string`` ID of a model to be removed
        :return: True if the structure was actually removed
        """

        def rem(o):
        	self.__stage.removeComponent(o)

        if model_id in self.__models:
            self.__models[model_id].then(rem)
            return True
        return False

    def add_style(self, model_id, style, representation_parameters={}):
        """Modify a style used to display a structure
        
        :param model_id: ``string`` ID of a model to apply the style
        :param style: ``string`` name of the representation to be set, e.g. ``"cartoon"`` or ``"licorice"``
        :param representation_parameters: dictionary used to create a ``NGL.StructureRepresentationType`` object
        :return: None
        """

        def add_styl(o):
            
            reprs = o.addRepresentation(style, representation_parameters)
            return reprs

        return self.__models[model_id].then(add_styl)

    def remove_style(self, model_id, rep=None):
        """Remove a style used to structure

        :param model_id: ``string`` ID of a model to apply the style
        :param rep: ``NGL.StructureRepresentationType`` object
        :return: None
        """

        def rem_styl(o):
            if rep is None:
                o.removeAllRepresentations()
            else:
                o.setVisibility(not o.visible)

        if rep is None:
            self.__models[model_id].then(rem_styl)
        else:
            rep.then(rem_styl)
        
    def show_model(self, model_id):
        """Makes visible a requested structure (i.e. a model).

        The structure must have been already added to this Widget

        :param structure_id: ``string`` ID of a model to show
        :return: True if shown successfully, false if this called failed
          (e.g. when the requested structure has not been registered in this Widget)
        """
        def set_vis(o):
            o.setVisibility(True)
        if model_id in self.__models:
            self.__models[model_id].then(set_vis)
            return True
        return False

    def hide_model(self, model_id):
        """Hides a requested structure (i.e. a model).

        This method does not remove the structure, it just make it invisible. You can always show the structure again
        by calling ``show()`` method. The structure must have been already added to this Widget

        :param model_id: ``string`` ID of a model to show
        :return: True if shown successfully, false if this called failed
          (e.g. when the requested structure has not been registered in this Widget)
        """
        def set_vis(o):
            o.setVisibility(False)

        if model_id in self.__models:
            self.__models[model_id].then(set_vis)
            return True
        return False

    def color_ss(self,model_id):
        """Color given model by secondary structure

        :param model_id: ``string`` with model id
        """

        def color(o):
            o.addRepresentation('backbone', { 'color': 'sstruc' })
            o.addRepresentation('rocket', { 'sele': 'helix', 'color': 'sstruc' })
            o.addRepresentation('cartoon', { 'sele': 'sheet', 'color': 'sstruc' })
            o.addRepresentation('tube', { 'sele': 'turn', 'color': 'sstruc' })

        if model_id in self.__models:
            self.__models[model_id].then(color)
            return True
        return False

    def show_distance(self,model_id,atom_pairs_list):
        """Show distance between pair of atom in a given model

        :param model_id: id of model to mark the distances
        :param atom_pairs_list: ``list`` of tuples of atom pairs eg. [(13,31),(5,43)] 
        """

        def distance(o):
            o.addRepresentation("distance", {
            'atomPair': atom_pairs_list,
            'labelColor': "skyblue",
            'color': "skyblue"})

        if model_id in self.__models:
            self.__models[model_id].then(distance)
            return True
        return False

    def zoom_to(self, model_id, selection):
        """Zooms to the active selection

        The method will zoom and center the view on residues (chains, atoms) that have been recently selected
        by ``active_selection()`` method. By default the whole structure is selected

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :param kwargs: see below
        :return: None
        """
        def zoom(o):
            o.autoView(selection, 1000)
        if model_id in self.__models:
            self.__models[model_id].then(zoom)
            return True
        return False

    def zoom_heteroatom(self, evt):
        """Zooms to the heteroatoms group

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :param kwargs: see below
        :return: None
        """
        def zoom(o):
            o.autoView("hetero and not water and not GOL",100)
        for i in self.__models:
            self.__models[i].then(zoom)
            
    def clear(self, evt=None):
        """Clears the scene"""
        self.__stage.removeAllComponents()


