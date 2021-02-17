#!/usr/bin/env python3

"""
|===================|
| Gere les chemins. |
|===================|

-Decore une frame pour interagir elegament avec un utilisateur.
-Genere un arbre a partir d'une variable decrivant les chemins.
"""

import os
import sys
import threading
import time
import unidecode

from ...tools import Printer # 'tkinter' est importe que la ou il y en a besoin.
from ...errors import *


def load(root="/", *, validate=(lambda absfilename: True), ignoreaccent=False, depth=-1):
    r"""
    |=====================================|
    | Recherche les chemins satifaisants. |
    |=====================================|

    parametres
    ----------
    :param root: Repertoire a partir du-quel on effectue la recherche.
    :type root: str
    :param validate: Callable qui prend en entree un chemin
        de fichier et retourne un booleen. Le fichier
        est accepte si True est retourne. Par contre,
        le fichier n'est pas charge si la fonction renvoi False.
    :type validate: callable
    :param ignoreaccent: Considere les caracteres accentues
        comme des caracteres sans accent si True.
    :type ignoreaccent: bool
    :param depth: Profondeur de recherche.
        -1, recursivite sans limite.
        0, pas de recursivite.
        n, descend au plus de n repertoires.
    :type depth: int

    sortie
    ------
    :return: L'arborecence complete.
    :rtype: dict

    exemple
    -------
    :Example:
    >>> from os.path import basename
    >>> import re
    >>> from raisin.application.hmi import pathmanager
    >>>
    >>> val = lambda f: re.search(r"^\S{3,5}2\.jpg$", basename(f))
    >>> pathmanager.load("/home/robin/images", validate=val)
    {'dirs': {'fractale': {'dirs': {}, 'files': ['julia2.jpg']}},
    'files': []}
    >>>
    """
    def listdir(path):
        try:
            yield from os.listdir(path)
        except (PermissionError, OSError):
            pass

    assert isinstance(root, str), \
        "'root' doit etre de type str, pas %s." % type(root).__name__
    assert os.path.isdir(root), \
        "'root' doit etre un repertoire. %s n'en est pas un." % repr(root)
    assert hasattr(validate, "__call__"), "'validate' doit etre un callable."
    assert isinstance(ignoreaccent, bool), \
        "'ignoreaccent' doit etre un booleen, pas un %s." % type(ignoreaccent).__name__
    assert isinstance(depth, int), "'depth' doit etre un entier, pas un %s." % type(depth).__name__

    with Printer("Load tree from %s..." % repr(root)):
        tree = {"dirs": {}, "files": []} # La racine ou une branche de l'arbre final.
        for path in listdir(root):
            abspath = os.path.join(root, path)
            if os.path.isdir(abspath):
                if depth:
                    branch = load(abspath,
                        validate=validate,
                        ignoreaccent=ignoreaccent,
                        depth=depth-1)
                    if branch != {"dirs": {}, "files": []}:
                        tree["dirs"][path] = branch
            elif validate(unidecode.unidecode(abspath) if ignoreaccent else abspath):
                tree["files"].append(path)
        return tree

def predict(current, *, isdir=False, isfile=False, validate=(lambda abspath: True), depth=5):
    """
    |=================================|
    | Gere la completion automatique. |
    |=================================|

    parametres
    ----------
    :param current: La phrase telle qu'elle est tapee par l'utilisateur.
    :type current: str
    :param isdir: Rechercher seulement un dossier si True.
    :type isdir: bool
    :param isfile: Rechercher seulement les fichiers si True.
    :type isfile: bool
    :param validate: Callable qui prend en entree un chemin complet
        et retourne un booleen. Le repertoire ou le fichier
        est accepte si True est retourne. Par contre,
        le chemin n'est pas charge si la fonction renvoi False.
    :type validate: callable
    :param depth: Profondeur de recherche. Pris en compte si 'isfile' == True.
        -1, recursivite sans limite.
        0, pas de recursivite.
        n, descend au plus de n repertoires.
    :type depth: int

    sortie
    ------
    :return: les caracteres certains.
    :rtype: str

    exemple
    -------
    :Example:
    >>> from raisin.application.hmi import pathmanager
    >>> pathmanager.predict("/h")
    'ome'
    >>> 
    """
    # def common(candidats):
    #     """
    #     Retourne la plus grande partie commune
    #     parmis tous les candidats.
    #     """
    #     if len(candidats) == 0:
    #         return ""
    #     if len(candidats) == 1:
    #         return candidats[0]
        
    #     area = "" # Portion commune.
    #     for lettres in zip(*candidats): # On parcours simultanement tous les candidats
    #         if len(set(lettres)) == 1: # Si la racine est identique
    #             area += lettres[0]
    #         else:
    #             break
    #     return area

    def ravel(root, tree):
        """
        Defait l'arbre pour le metre a plat dans une liste.
        """
        paths = [os.path.join(root, c) for c in tree["files"]]
        for rep, subtree in tree["dirs"].items():
            paths.append(os.path.join(root, rep))
            paths.extend(ravel(paths[-1], subtree))
        return paths

    def merge(trees):
        """
        Agence des branches en les faisant
        partir d'un seul meme noeud.
        """
        return {
            "files": sum([t["files"] for t in trees], start=[]),
            "dirs": {k: v for t in trees for k, v in t["dirs"].items()}
        }

    assert isinstance(current, str), \
        "'current' doit etre str, pas %s." % type(current).__name__
    assert isinstance(isdir, bool), \
        "'isdir' doit etre un boolee, pas un %s." % type(isdir).__name__
    assert isinstance(isfile, bool), \
        "'isfile' doit etre un boolee, pas un %s." % type(isfile).__name__
    assert (not isdir) or (not isfile), \
        "'isdir' et 'isfile' ne peuvent pas etre True tous d'eux!"
    assert hasattr(validate, "__call__"), "'validate' doit etre un callable."
    assert isinstance(depth, int), "'depth' doit etre un entier, pas un %s." % type(depth).__name__

    with Printer("Prediction of %s..." % repr(current)) as p:
        father = os.path.dirname(os.path.abspath(current)) # Repertoire parent.
        if not os.path.isdir(father):
            return ""
        end = os.path.basename(os.path.abspath(current)) # Attention /home/robin/
        p.show("Father: %s" % repr(father))
        p.show("Curent: %s" % repr(end))

        if isdir:
            candidats = [
                e for e in os.listdir(father)
                if e[:len(end)] == end
                and os.path.isdir(os.path.join(father, e))
                and validate(os.path.join(father, e))]
        elif isfile:
            candidats = ravel(
                "",
                merge([
                    {"files": [],
                     "dirs": {p: load(
                        os.path.join(father, p),
                        validate=validate,
                        depth=depth)}}
                    for p in os.listdir(father)
                    if p[:len(end)] == end
                    and os.path.isdir(os.path.join(father, p))]
                    + [{"files": [p for p in os.listdir(father)
                        if p[:len(end)] == end
                        and os.path.isfile(os.path.join(father, p))
                        and validate(os.path.join(father, p))],
                        "dirs": {}}]))
            if candidats:
                candidats.sort(key=lambda p: len(p))
                candidats = [c for c in candidats if candidats[-1][:len(c)] != c] + [candidats[-1]]
        else:
            candidats = [
                e for e in os.listdir(father)
                if e[:len(end)] == end
                and validate(os.path.join(father, e))]
        prediction = os.path.commonprefix([c[len(end):] for c in candidats])
        if isdir and prediction and os.path.isdir(os.path.join(father, end + prediction)):
            prediction += "/"
        p.show("Result: %s" % repr(prediction))
        return prediction

def complete(entry, *, isdir=False, isfile=False, validate=(lambda abspath: True)):
    """
    |====================================|
    | Decore un wiget entry pour gerer   |
    | la saisie des chemins de fichiers. |
    |====================================|

    parametres
    ----------
    :param entry: Widjet de saisie tkinter.
    :type entry: tkinter.Entry
    :param isdir: Rechercher seulement un dossier si True.
    :type isdir: bool
    :param isfile: Rechercher seulement les fichiers si True.
    :type isfile: bool
    :param validate: Callable qui prend en entree un chemin complet
        et retourne un booleen. Le repertoire ou le fichier
        est accepte si True est retourne. Par contre,
        le chemin n'est pas charge si la fonction renvoi False.
    :type validate: callable

    sortie
    ------
    :return: L'entree ammelioree.
    :rtype: tkinter.Entry

    exemple
    -------
    :Example:
    >>> import tkinter
    >>> from raisin.application.hmi import pathmanager
    >>> master = tkinter.Tk()
    >>> pathmanager.complete(tkinter.Entry(master)).pack()
    >>> master.mainloop()
    """
    class Predictor(threading.Thread):
        """
        Recherche une completion.
        """
        def __init__(self, entry, **kwargs):
            """
            :param entry: Widget de saisie tkinter.
            :type entry: tkinter.Entry
            :param lock: Verrou.
            :type lock: threading.Lock
            """
            threading.Thread.__init__(self)
            self.entry = entry
            self.kwargs = kwargs
            self.must_die = False

        def run(self):
            """
            Recalcule la fin a partir du curseur.
            Qu'il y ai une selection ou non.
            """
            try:
                for depth in [1, 2, 5]:
                    current = self.entry.get()[:self.entry.index("insert")] # Partie avant le curseur.
                    threading.settrace(self.trace) # Mise en place de la fonction de tracage.
                    prediction = predict(current, **self.kwargs, depth=depth) # Ce qu'il va y avoir apres le curseur.
                    threading.settrace(None) # Ca fonctione mal avec sys.sttrace
                    # On remplace la fin par le nouveau resultat.
                    if self.entry.get()[:self.entry.index("insert")] == current:
                        self.entry.delete(0, "end")
                        self.entry.insert(0, current + prediction)
                        self.entry.icursor(len(current))
                        self.entry.select_range(len(current), "end")
            except SucidalError:
                threading.settrace(None)
            else:
                threading.settrace(None)

        def trace(self, frame, event, arg):
            """
            Surveille la sante mentale du thread en permanence.
            Si il commence a deprimer, il est extermine sur le champs.
            """
            if event == "line":
                if self.must_die:
                    raise SucidalError("Succide du thread demande.")
            return self.trace

        def kill(self):
            """
            Arrete le thread.
            """
            self.must_die = True

    class Calculator:
        """
        Permet de gerer la recherche de chemins
        en fonction des evenements.
        """
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.threads = []

        def __call__(self, event):
            """
            Methode appelee des que l'utilisateur
            presse une touche.
            """
            [t.join(timeout=0) if t.must_die else t.kill()
             for t in self.threads if t.is_alive()] # On demande aux threads de se sucider. On assasine les recalcitrants.
            self.threads = [t for t in self.threads if t.is_alive()] # On netoie les cadavres.

            if event.keysym in ("Return", "Tab"):
                event.widget.icursor("end")
                event.widget.select_clear()
            elif event.keysym in ("Escape", "BackSpace", "Delete"):
                if event.widget.select_present():
                    event.widget.delete("insert", "end")
            elif event.keysym in ("Left", "Right"):
                event.widget.select_range("insert", "end")
            else:
                self.threads.append(Predictor(event.widget, **self.kwargs))
                self.threads[-1].start()

    from . import tkinter # On l'importe ici pour ne pas freiner.

    assert isinstance(entry, tkinter.Entry),\
        "'entry' doit etre un widget tkinter.Entry, pas %s." % type(entry).__name__
    assert isinstance(isdir, bool), \
        "'isdir' doit etre un boolee, pas un %s." % type(isdir).__name__
    assert isinstance(isfile, bool), \
        "'isfile' doit etre un boolee, pas un %s." % type(isfile).__name__
    assert (not isdir) or (not isfile), \
        "'isdir' et 'isfile' ne peuvent pas etre True tous d'eux!"
    assert hasattr(validate, "__call__"), "'validate' doit etre un callable."

    calculator = Calculator(isdir=isdir, isfile=isfile, validate=validate)
    entry.bind("<KeyRelease>", calculator)
    return entry

def make_tree(paths):
    """
    |===============================|
    | Construit un arbre qui permet |
    | de parcourir les chemins.     |
    |===============================|

    parametres
    ----------
    :param paths: Le dictionaire qui contient les liste des
        chemins inclus et des chemins a exclure.
        Par example:
        {'paths': ['/chemin1', '/chemin2'], 'excluded_paths': ['/chemin1/enfant1']}
    :type paths: dict

    sortie
    ------
    :return: L'arbre des chemins.
    :rtype: Tree
    """
    import raisin.application.hmi.checks as checks
    assert checks.paths_verification(paths), "L'entree n'est pas correcte."

    class Tree:
        """
        Gestion plus naturelle des chemins.
        """
        def __init__(self, path, genre):
            self.path = os.path.normcase(os.path.abspath(path)) # Le chemin racine de cette branche.
            self.genre = genre # Etat 'included' ou 'excluded'.
            self.branches = [] # Les arbres enfants.

        def __str__(self):
            """
            Affichage pas trop degaulasse.
            """
            return "<Tree(path=%s, genre=%s)>" % (repr(self.path), repr(self.genre))

        def __repr__(self):
            """
            Representation en profondeur.
            """
            def indent(chaine):
                return "\t" + "\n\t".join(chaine.split("\n"))

            if self.branches:
                return "Tree(paths=%s, genre=%s, branches=[\n%s])" % (
                    repr(self.path),
                    repr(self.genre),
                    "\n".join([
                        "\n\t".join(repr(t).split("\n"))
                        for t in self.branches]))
            return "Tree(paths=%s, genre=%s, branches=[])" % (
                    repr(self.path),
                    repr(self.genre))

        def __contains__(self, other):
            """
            Retourne True l'abre 'other'
            est contenu dans self.
            Retourne False sinon.
            """
            return len(other.path) >= len(self.path) \
                and os.path.commonpath([other.path, self.path]) == self.path

        def __eq__(self, other):
            return self.path == other.path

        def __len__(self):
            """
            Retourne le nombre d'enfant et de sous-enfants.
            """
            return sum(len(t) for t in self.branches)

        def walk(self, *, root=None):
            """
            Cede recursivement tous les fichiers
            enfants a prendre en consieration.
            Contrairement a os.walk, ne cede pas
            3 choses mais seulement un chemin absolu.
            """
            if self.genre == "included":
                real_root = root if root else self.path
                if os.path.isdir(real_root):
                    for element in os.listdir(real_root):
                        total = os.path.join(real_root, element)
                        if any(os.path.commonpath([total, b.path]) == b.path for b in self.branches):
                            continue
                        if os.path.isdir(total):
                            yield from self.walk(root=total)
                        else:
                            yield total
                elif os.path.isfile(real_root):
                    yield real_root
            if not root:
                for branch in self.branches:
                    yield from branch.walk()

        def append(self, other):
            """
            Tente d'ajouter l'abre 'other'
            dans la bonne sous branche de self.
            Si 'other' n'est pas un sous-arbre de self,
            leve une exception ValueError.
            """
            if other not in self:
                raise ValueError("'other' n'est pas contenu dans self.")
            for branche in self.branches:
                if other == branche:
                    raise ValueError("'other' est deja ajoute.")
                try:
                    branche.append(other)
                    return
                except ValueError:
                    continue
            self.branches.append(other)

    with Printer("Making path tree..."):
        trees = [Tree(p, "included") for p in paths["paths"]] \
            + [Tree(p, "excluded") for p in paths["excluded_paths"]]
        trees.sort(key=lambda tree: len(tree.path)) # On trie les chemins par taille croissante de facon a faire moin de calculs

        commun = os.path.commonpath([t.path for t in trees]) if trees else "/"
        tree = Tree(os.path.dirname(commun), "excluded") # Racine de l'arbre
        for t in trees:
            tree.append(t)
        return tree

def padding(frame, paths_var, *, isdir=False, isfile=False, validate=(lambda abspath: True)):
    """
    |===================================|
    | Complete graphiquement un         |
    | espace qui permet de selectionner |
    | un arbre de repertoire.           |
    |===================================|

    Plus precisement, l'utilisateur peux selectionner
    plusieurs arborecences/fichiers a considerer tout
    en excluant des sous arborecences/fichiers.

    parametres
    ----------
    :param frame: Frame tkinter vierge a habiller.
    :type frame: tkinter.Frame
    :param paths_var: Variable tkinter dans laquel on y
        lit et y ecrit les resultats. Son contenu doit prendre
        la forme suivante:
        "{'paths': ['/chemin1', '/chemin2'], 'excluded_paths': ['/chemin1/enfant1']}"
    :type paths_var: tkinter.StringVar
    :param isdir: Rechercher seulement un dossier si True.
    :type isdir: bool
    :param isfile: Rechercher seulement les fichiers si True.
    :type isfile: bool
    :param validate: Callable qui prend en entree un chemin complet
        et retourne un booleen. Le repertoire ou le fichier
        est accepte si True est retourne. Par contre,
        le chemin n'est pas charge si la fonction renvoi False.
    :type validate: callable

    sortie
    ------
    :return: La frame habillee.
    :rtype: tkinter.Frame

    exemple
    -------
    :Example:
    >>> import tkinter
    >>> from raisin.application.hmi import pathmanager
    >>> master = tkinter.Tk()
    >>> var = tkinter.StringVar()
    >>> var.set(str({"paths":[], "excluded_paths":[]}))
    >>> pathmanager.padding(tkinter.Frame(master), var).pack(fill="both", expand=True)
    >>> master.mainloop()
    >>> var.get()
    "{'paths': ['/home'], 'excluded_paths': []}"
    """
    global paths

    class Trash:
        """
        Supprime tout une arborescence.
        """
        def __init__(self, racine):
            self.racine = racine

        def __call__(self):
            global paths
            paths = {
                "paths": [p for p in paths["paths"]
                    if os.path.commonpath([p, self.racine]) != self.racine],
                "excluded_paths": [p for p in paths["excluded_paths"]
                    if os.path.commonpath([p, self.racine]) != self.racine]}
            entry_path_var.set("")
            entry_excluded_path_var.set("")
            valider()

    def inter(current, refs):
        """
        S'assure que 'current' soit contenu dans
        l'une des references 'refs'.
        """
        commun = os.path.commonprefix(refs) if refs else "/"
        return current[:len(commun)] == commun

    def ravel(tree, depth=0):
        """
        Deplie recursivement l'arbre.
        Cede dans l'ordre:
        (path_de_la_branche,
        son_genre,
        sa_profondeur)
        """
        if depth:
            yield tree.path, tree.genre, depth-1
        for branche in tree.branches:
            yield from ravel(branche, depth+1)

    def valider():
        """
        Si les chemins saisis sont corrects,
        l'entree est ajoute au 'paths' et 'paths_var'.
        Met a jour l'affichage des chemins deja saisis.
        """
        # Ajout du chemin.
        if entry_path_var.get():
            paths["paths"].append(os.path.abspath(entry_path_var.get()))
            entry_path_var.set("")
        elif entry_excluded_path_var.get():
            paths["excluded_paths"].append(os.path.abspath(entry_excluded_path_var.get()))
            entry_excluded_path_var.set("")
        paths_var.set(repr(paths))
        tree = make_tree(paths)

        # Initialisation de la zonne d'ecriture.
        for widget in disp_frame.winfo_children():
            widget.grid_forget()
        
        # Reecriture des widjets.
        for i, (path, genre, depth) in enumerate(ravel(tree)):
            text = "%s(%s) %s" % (
                "|   "*depth,
                "+" if genre == "included" else "-",
                repr(path))
            disp_frame.rowconfigure(i, weight=1)
            theme.theme(tkinter.Label(disp_frame,
                text=text,
                # font="-overstrike %d" % (genre == "excluded")
                )).grid(row=i, column=0, sticky="w")
            theme.theme(tkinter.Button(disp_frame,
                image=theme.icons.trash(),
                command=Trash(path)
                )).grid(row=i, column=1)

    def unblock():
        """
        Active ou desactive le bouton de validation selon
        que les donnee soient corectes.
        Si l'entree est incorecte, la raison de cette incorrectitude
        est explicite dans la bonne zonne.
        """        
        # Verfifications
        if entry_path_var.get() and entry_excluded_path_var.get():
            error_var.set("Only one thing at a time!")
            button_valider.config(state="disable")
        elif not entry_path_var.get() and not entry_excluded_path_var.get():
            error_var.set("Fields are empty.")
            button_valider.config(state="disable")
        else:
            import raisin.application.hmi.checks as checks
            paths_copy = {"paths": paths["paths"].copy(), "excluded_paths": paths["excluded_paths"].copy()}
            if entry_path_var.get():
                paths_copy["paths"].append(os.path.abspath(entry_path_var.get()))
            else:
                paths_copy["excluded_paths"].append(os.path.abspath(entry_excluded_path_var.get()))
            message = checks.paths_verification(paths_copy, revert=True)
            if message == True:
                error_var.set("Ok.")
                button_valider.config(state="normal")
            else:
                error_var.set(message)
                button_valider.config(state="disable")

    # Imports.
    import raisin.application.hmi.theme as theme
    from . import tkinter, messagebox # On importe ici pour ne pas gener ailleur.

    assert isinstance(frame, tkinter.Frame), \
        "'frame' doit etre de type tkinter.Frame, pas %s." % type(frame).__name__
    assert isinstance(paths_var, tkinter.StringVar), \
        "'paths_var' doit etre de type tkinter.StringVar, pas %s." % type(paths_var).__name__
    assert isinstance(isdir, bool), \
        "'isdir' doit etre un boolee, pas un %s." % type(isdir).__name__
    assert isinstance(isfile, bool), \
        "'isfile' doit etre un boolee, pas un %s." % type(isfile).__name__
    assert (not isdir) or (not isfile), \
        "'isdir' et 'isfile' ne peuvent pas etre True tous d'eux!"
    assert hasattr(validate, "__call__"), "'validate' doit etre un callable."

    # Declaration des variables.
    entry_path_var = tkinter.StringVar()        # Pour recuperer facilement le contenu de la premiere zonne de saisie.
    entry_excluded_path_var = tkinter.StringVar() # De meme pour la zonne exclusive.
    try:
        paths = eval(paths_var.get())
    except (SyntaxError, TypeError) as e:
        raise ValueError(
            "'paths_var' n'a pas un contenu qui represente une variable python.") from e
    assert isinstance(paths, dict), \
        "'paths_var' doit contenir un dictionaire, pas un %s." % type(paths).__name__
    assert "paths" in paths, "'paths_var' doit avoir une clef 'paths'."
    assert "excluded_paths" in paths, "'paths_var' doit avoir une clef 'excluded_paths'."
    assert isinstance(paths["paths"], list), \
        "'paths_var['paths'] doit etre une liste, pas %s." % type(paths["paths"]).__name__
    assert isinstance(paths["excluded_paths"], list), \
        "'paths_var['excluded_paths'] doit etre une liste, pas %s." % type(paths["excluded_paths"]).__name__

    with Printer("Path padding..."):
        # Initialisation des widgets.
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=9)
        frame.columnconfigure(3, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        theme.theme(frame)

        theme.theme(tkinter.Label(frame, text="Included :")).grid(row=0, column=0, sticky="w")
        entry_path = theme.theme(complete(
            tkinter.Entry(
                frame,
                textvariable=entry_path_var),
            isdir=isdir,
            isfile=isfile,
            validate=validate
            ))
        entry_path.grid(row=0, column=1, columnspan=2, sticky="ew")
        entry_path.bind("<Leave>", lambda event: unblock())
        theme.theme(tkinter.Button(frame,
                    image=theme.icons.info(),
                    command=lambda : messagebox.showinfo(
                        "Info input path",
                        "Les dossiers ou le fichiers entre ici seront "
                        "pris en compte. Si le chemin correspond a un "
                        "dossiers, tout les dossiers enfants sont consideres.")
                    )).grid(row=0, column=3)
        
        theme.theme(tkinter.Label(frame, text="Excluded :")).grid(row=1, column=0, sticky="w")
        entry_excluded_path = theme.theme(complete(
            tkinter.Entry(frame, textvariable=entry_excluded_path_var),
            isdir=isdir,
            isfile=isfile,
            validate=lambda p: inter(p, paths["paths"])
            ))
        entry_excluded_path.grid(row=1, column=1, columnspan=2, sticky="ew")
        entry_excluded_path.bind("<Leave>", lambda event: unblock())
        theme.theme(tkinter.Button(frame,
                    image=theme.icons.info(),
                    command=lambda : messagebox.showinfo(
                        "Info excluded path",
                        "Les dossiers ou le fichiers entre ici seront "
                        "exclus des chemins saisis au dessus.")
                    )).grid(row=1, column=3)

        button_valider = theme.theme(tkinter.Button(frame, text="Valider", state="disable", command=valider))
        button_valider.grid(row=2, column=1, sticky="ew")
        error_var = tkinter.StringVar()
        theme.theme(tkinter.Label(frame, textvariable=error_var)).grid(row=2, column=2, sticky="w")
        theme.theme(tkinter.Button(frame,
                    image=theme.icons.info(),
                    command=lambda : messagebox.showinfo(
                        "Info validation",
                        "Ce bouton permet de valider le chemin.\n"
                        "Il n'est actif que quand la saisie est "
                        "correcte. Si ce n'est pas le cas, il "
                        "faut faire passer la souris sur le bouton "
                        "pour faire apparaitre le message d'erreur.")
                    )).grid(row=2, column=3)

        disp_frame = theme.theme(tkinter.Frame(frame))
        disp_frame.grid(row=3, column=1, columnspan=2, sticky="ewsn")
        disp_frame.columnconfigure(0, weight=10)
        disp_frame.columnconfigure(1, weight=1)
        theme.theme(tkinter.Button(frame,
                    image=theme.icons.info(),
                    command=lambda : messagebox.showinfo(
                        "Info displayed paths",
                        "L'affichage et la suppression des "
                        "fichiers existant se fait ici.")
                    )).grid(row=3, column=3)

        valider()

        return frame
