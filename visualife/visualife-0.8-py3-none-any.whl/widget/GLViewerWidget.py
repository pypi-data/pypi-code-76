import json
from browser import window, document, html, bind
from visualife.utils.text_utils import substitute_template


class GLViewerWidget:
    """Represents a viewer for biological molecules.

    It contains 3DMol viewer inside. It may display .pdb or .mol formats.
    See full documentation here https://3dmol.csb.pitt.edu/index.html

    """

    def __init__(self, div_id, **kwargs):

        self.__div_id = div_id
        self.__pdbs = {}
        self.__models = {}
        self.__active_selection_dict = {}
        self.__style = """
        .GLViewerWidget-button {
            flex: 1;
            display: inline;
            margin: 2px;
            font-size: 13px;
        }
        """
        self.__to_write = """
        <div id="viewer-{%ID%}" style="height:{%height%}px; width:{%width%}px;"></div>
        <div id="buttons-{%ID%}" style="display: flex; flex-direction: row; width:{%width%}px; flex-wrap:wrap;">
        </div>
        """

        document <= html.STYLE(self.__style)

        replacement = {"{%ID%}": div_id, "{%width%}": kwargs.get("width", 500),
                       "{%height%}": kwargs.get("height", 500)
                       }

        document[div_id].innerHTML = substitute_template(self.__to_write, replacement)
        self.__glviewer = \
            getattr(window, '$3Dmol').createViewer(document["viewer-"+div_id], {'backgroundColor': 'white'})
        self.__on_clear = []

        # Definition of the default menu
        default_menu = {"sticks": "as_sticks", "clear all": "clear_all",
                       "cartoon": "as_cartoon", "center": "center",
                        "zoom to selection": "zoom_to", "zoom ligand" : "zoom_heteroatom"}
        # --- Here we create the menu based on **kwargs; if not provided: a default menu will be made
        menu_def = kwargs.get("menu_buttons", default_menu)
        for name, func in menu_def.items():
            self.add_to_menu(name,func)

    def add_to_menu(self, button_name, callback):
        button_id = button_name + "-" + self.__div_id
        button_el = html.INPUT(button_name, id=button_id, Class="GLViewerWidget-button", type="button", value=button_name)
        document["buttons-" + self.__div_id] <= button_el
        if callable(callback):
            button_el.bind("click",callback)
        else:
            button_el.bind("click", getattr(self, callback))

    def active_selection(self, selection_dict):
        """Defines an active selection.

        The selected residues will be subjected to ``as_sticks()``, ``as_lines()``, ``as_spheres()``, ``as_cartoon()``
        and ``zoom_to()`` methods. By default the whole molecule is selected.

        :param selection_dict: selection as JSON-like dictionary; must a valid argument
        for ``3DMol.AtomSelectionSpec`` object. A few examples are given below:

        - ``{chain:'B'}`` : selects chain B
        - ``resi:["91-95","42-50"]`` : selects two ranges of residues
        - ``{resn:'PMP', byres:true,expand:5}`` : selects residue PMP and then extends the selection to any residue whose
            atom is within 5A
        - ``{chain:'B', invert: True}`` : selects everything but chain B
        :return: None
        """
        self.__active_selection_dict = selection_dict

    def as_sticks(self, evt):
        """Displays a molecule or its fragment as sticks

        The method will be applied to residues (chains, atoms) that have been recently selected
        by ``active_selection()`` method. By default the whole structure is selected

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :param kwargs: see below
        :return: None
        """
        self.__glviewer.setStyle(self.__active_selection_dict, {"stick": {}})
        self.__glviewer.render()

    def as_lines(self, evt):
        """Displays a molecule or its fragment as lines

        The method will be applied to residues (chains, atoms) that have been recently selected
        by ``active_selection()`` method. By default the whole structure is selected

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :param kwargs: see below
        :return: None
        """
        self.__glviewer.setStyle(self.__active_selection_dict, {"line": {}})
        self.__glviewer.render()

    def as_spheres(self, evt):
        """Displays a molecule or its fragment as spheres

        The method will be applied to residues (chains, atoms) that have been recently selected
        by ``active_selection()`` method. By default the whole structure is selected

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :param kwargs: see below
        :return: None
        """
        self.__glviewer.setStyle(self.__active_selection_dict, {"sphere": {}})
        self.__glviewer.render()

    def as_cartoon(self, evt, **kwargs):
        """Displays a molecule or its fragment as cartoon

        The method will be applied to residues (chains, atoms) that have been recently selected
        by ``active_selection()`` method. By default the whole structure is selected

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :param kwargs: see below
        :return: None
        """
        self.__glviewer.setStyle({"hetflag": False}, {"cartoon": {"color": 'spectrum'}})
        self.__glviewer.render()

    def clear_all(self, evt):
        self.clear()

    def zoom_to(self, evt):
        """Zooms to the active selection

        The method will zoom and center the view on residues (chains, atoms) that have been recently selected
        by ``active_selection()`` method. By default the whole structure is selected

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :param kwargs: see below
        :return: None
        """
        self.__glviewer.zoomTo(self.__active_selection_dict, 1000)

    def zoom_heteroatom(self, evt):
        """Zooms to the heteroatoms group

        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :param kwargs: see below
        :return: None
        """
        self.__glviewer.zoomTo({"hetflag": True},1000)

    def center(self, evt):
        """
        Zooms out so the whole structure is visible
        :param evt: event object; its not used by this method must must appear
            in the method definition so it can be used as a callback for an HTML event
        :return:
        """
        self.__glviewer.zoomTo()

    def save_as_png(self,evt):
        png = self.__glviewer.pngURI()
        document["Download-"+self.__div_id].href = png

    def add_on_clear(self, callback):
        """Add a callback function to be called when this viewer is cleared, e.g. by calling ``clear()`` method

        :param callback: a function to be called
        :return: None
        """
        self.__on_clear.append(callback)

    def atomcallback(self, atom, viewer, b, a):
        """Function to run on atom click
        """
        res = viewer.selectedAtoms({'resi': atom.resi})
        for at in res:
            if 'clickLabel' not in at.to_dict() or at.clickLabel == None:

                self.__glviewer.addStyle({'resi': atom.resi}, {'stick': {'color': 'spectrum'}})
                self.__glviewer.render();

                for a in res:
                    a.clicked = True
                    if a.atom == "CA":
                        a.clickLabel = viewer.addLabel(str(atom.resn) + str(atom.rescode),
                                                       {'fontSize': 14,
                                                        'position': {'x': a.x, 'y': a.y, 'z': a.z}})
                self.__glviewer.render();
            else:
                for a in res:
                    if a.atom == "CA":
                        viewer.removeLabel(a.clickLabel)
                        a.clickLabel = None;
                    a.clicked = False

    def clear(self):
        """Clears this panel and removes all structures from memory

        This call also triggers all ``on_clear`` callbacks functions
        """
        self.__glviewer.clear()
        for callback in self.__on_clear:
            callback()
        self.__pdbs = {}
        self.finalize()

    def remove_model(self, structure_id):
        """Removes a model from this widget and from the 3Dmol viewer

        :param structure_id: ``string`` ID of a model to be removed
        :return: True if the structure was actually removed
        """

        if structure_id in self.__models:
            self.__glviewer.removeModel(self.__models[structure_id])
            self.finalize()
            return True
        return False

    def add_model(self, name, pdb_text, if_show=True):
        """Adds a new structure to this viewer.

        :param name: ``string`` ID used to identify that molecule
        :param pdb_text: ``string`` biomalecule structure as PDB data (text)
        :param if_show: ``bool`` if True, the structure will be immediately visible in the viewer
        :return: ``$3Dmol.GLModel`` object
        """

        self.__pdbs[name.split(".")[0]] = pdb_text
        m = self.__glviewer.addModel(pdb_text, "pdb")
        self.__models[name] = m
        atoms = m.selectedAtoms();
        for a in atoms:
            a.clickable = True
            a.callback = self.atomcallback

        self.__glviewer.setStyle({'hetflag': False}, {'cartoon': {'color': 'spectrum'}})
        self.__glviewer.setStyle({'hetflag': True}, {'stick': {'color': 'spectrum'}})
        if not if_show: m.hide()
        self.finalize()
        return m

    def add_style(self, selection, style):
        """Modify a style used to display a fragment of a model
        :param selection: dictionary used to create a ``3DMol.AtomSelectionSpec`` object
        :param style: dictionary used to create a ``3DMol.AtomStyleSpec`` object
        :return: None
        """

        self.__glviewer.setStyle(selection, style)
        self.finalize()

    def show_structure(self, structure_id):
        """Makes visible a requested structure (i.e. a model).

        The structure must have been already added to this Widget
        :param structure_id: ``string`` ID of a model to show
        :return: True if shown successfully, false if this called failed
          (e.g. when the requested structure has not been registered in this Widget)
        """
        if structure_id in self.__models:
            self.__models[structure_id].show()
            return True
        return False

    def hide_structure(self, structure_id):
        """Hides a requested structure (i.e. a model).

        This method does not remove the structure, it just make it invisible. You can always show the structure again
        by calling ``show()`` method. The structure must have been already added to this Widget

        :param structure_id: ``string`` ID of a model to show
        :return: True if shown successfully, false if this called failed
          (e.g. when the requested structure has not been registered in this Widget)
        """
        if structure_id in self.__models:
            self.__models[structure_id].hide()
            return True
        return False

    def finalize(self):
        """Force the viewer to refresh"""
        self.__glviewer.render()
        self.__glviewer.zoomTo()

    def check_clicked_atoms(self, ev):
        """Returns a list of atoms that are clicked 

        Returns a list of clicked atoms ``serial`` number 
        """
        clicked_atoms = []
        model = self.__glviewer.getModel()
        atoms = model.selectedAtoms()
        for i in atoms:
            if 'clicked' in i.to_dict() and i.clicked == True:
                clicked_atoms.append(int(i.serial))
        print(clicked_atoms)
        clicked_atoms = json.dumps(clicked_atoms)
        return clicked_atoms

    def update_viewer(self, decoys):
        """Shows decoys from a given list
        """
        self.__glviewer.clear()
        print(self.__pdbs)
        for d in decoys:
            self.show_decoy(self.__pdbs[d])
        self.finalize()

    def show_ligand_contacts(self, ligand_code, ligand_atom, rcptr_resi, rcptr_atoms):
        """Show contacts between ligand and receptor 
        """
        ligand_atom = self.__glviewer.selectedAtoms({'hetflag': True, 'resn': ligand_code, 'atom': ligand_atom})

        for i in range(len(rcptr_atoms)):
            receptor_atom = self.__glviewer.selectedAtoms({'resi': rcptr_resi, 'atom': rcptr_atoms[i].strip()})
            self.__glviewer.addCylinder({
                'start': {'x': ligand_atom[0].x, 'y': ligand_atom[0].y, 'z': ligand_atom[0].z},
                'end': {'x': receptor_atom[0].x, 'y': receptor_atom[0].y, 'z': receptor_atom[0].z},
                'radius': 0.1, 'color': 'grey', 'dashed': True})
            self.__glviewer.addStyle({'resi': rcptr_resi}, {'stick': {'color': 'spectrum'}})
        self.__glviewer.zoomTo({'chain': 'X'}, 400);
        self.__glviewer.render()

    def add_atom(self, a, cor, model=0):
        """Adds an atom to a viewer
        """

        self.__glviewer.getModel(model).addAtoms(
            [{'hetflag': False, 'serial': a, 'x': cor[a][0], 'y': cor[a][1], 'z': cor[a][2]}])
        self.__glviewer.setStyle({'hetflag': False, 'serial': a, }, {'sphere': {'color': 'white', 'radius': 0.3}})
        self.__glviewer.addCylinder({
            'start': {'x': cor[a][0], 'y': cor[a][1], 'z': cor[a][2]},
            'end': {'x': cor[a][3], 'y': cor[a][4], 'z': cor[a][5]},
            'radius': 0.3, 'color': 'grey'})
