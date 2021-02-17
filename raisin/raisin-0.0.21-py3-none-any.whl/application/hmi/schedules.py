#!/usr/bin/env python3

"""
|==============================|
| Gere la saisie des horaires. |
|==============================|

-Decore une frame pour interagir elegament avec un utilisateur.
"""

import copy
import datetime
import re
import time

from ...tools import Printer
from . import theme, checks
from . import tkinter, messagebox

class Schedules:
    """
    |========================================|
    | Permet de voir la variable 'schedules' |
    | comme une fonction continue.           |
    |========================================|

    exemple
    -------
    :Example:
    >>> from raisin.application.hmi.schedules import Schedules
    >>> s = Schedules({
        'friday': {'22:00': True, '8:00': False}, 
        'monday': {'22:00': True, '8:00': False},
        'saturday': {'10:00': False, '23:00': True},
        'sunday': {'10:00': False, '23:00': True},
        'thursday': {'22:00': True, '8:00': False},
        'tuesday': {'22:00': True, '8:00': False},
        'wednesday': {'22:00': True, '8:00': False}})
    >>>
    """
    def __init__(self, schedules):
        """
        parametres
        ----------
        :param schedules: Dictionaire qui contient les horaires et les valeurs.
        :type schedules: dict
        """
        import raisin.application.hmi.checks as checks
        assert checks.schedules_verification(schedules), \
            "'schedules' n'est pas correcte"
        
        self.schedules = schedules
        self.days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        # self.next_day = {self.days[i]: self.days[(i+1)%len(self.days)] for i in range(len(self.days))}
        # self.previous_day = {v:c for c,v in self.next_day.items()}
        self.values = {self._to_min(d, *map(int, date.split(":"))): value
            for d, dic in self.schedules.items()
            for date, value in dic.items()} # Associ la valeur sur une echelle lineaire en minute.
        self.keys = sorted(self.values.keys()) # Met les clefs dans l'ordre.

    def __call__(self, date=None, *, day=None):
        """
        |============================|
        | Calcul l'interpolation     |
        | d'orde 0 au point demande. |
        |============================|

        parametres
        ----------
        :param date: Moment de l'interpolation. Peut etre:
            -None, Interpole avec l'heure actuelle.
            -float, int, The current time in seconds since the Epoch.
            -time.struct_time, Prend l'heure donee.
            -str, format %H:%M. Il faut preciser le jour.
        :type date: None
        :param day: Le jour en anglais. seulement si type(date) == str.
        :type day: str

        sortie
        ------
        :return: La valeur au point demande.
        :rtype: bool, int, float

        exemple
        -------
        :Example:
        >>> s()
        True
        >>> s(1608547486.959979)
        False
        >>> s("22:15", day="monday")
        True
        """
        with Printer("Search value for %s schedules..." % repr(date)) as p:
            # Parsing de la date.
            if date == None:
                date = time.gmtime()
            elif isinstance(date, float) or isinstance(date, int):
                date = time.gmtime(date)
            elif isinstance(date, str):
                assert isinstance(day, str), \
                    "'day' doit etre str, pas %s." % type(day).__name__
                assert day.lower() in self.days
                assert re.fullmatch(r"\d{1,2}:\d{1,2}", date)
                date = time.strptime("{}:{}".format(day.lower(), date), "%A:%H:%M")
            elif isinstance(date, time.struct_time):
                pass
            else:
                raise ValueError("'date' n'est pas correcte.")
            d, h, m = self.days[date.tm_wday], date.tm_hour, date.tm_min
            p.show("date: %s %02dh%02d" % (d, h, m))

            # Recherche de la date a gauche la plus proche
            # Il y a moyen d'optimiser pour etre en log(n) au lieu de n.
            # La variable nex, est la si on veut faire une interpolation d'odre 1.
            minute = self._to_min(d, h, m)
            rang = len(self.keys)
            for i, key in enumerate(self.keys):
                if key > minute: # Inegalite stricte pour tomber bien quand on fait rang-1.
                    rang = i
                    break
            if rang == 0 or rang == len(self.keys):
                pre, nex = len(self.keys)-1, 0
            else:
                pre, nex = rang-1, rang

            # Valeur de retour
            value = self.values[self.keys[pre]]
            p.show("value: %s" % value)
            return value

    def _to_min(self, d, h, m):
        """
        Retourne une date en minute relative au debut de la semaine.
        """
        return m + 60*h + 24*60*self.days.index(d)

def padding(frame, schedules_var, *, ylabel="value", converter=eval):
    """
    |===========================================|
    | Complete graphiquement un                 |
    | espace qui permet de choisir les horaires |
    | et les valeurs associees.                 |
    |===========================================|

    parametres
    ----------
    :param frame: Frame tkinter vierge a habiller.
    :type frame: tkinter.Frame
    :param paths_var: Variable tkinter dans la quelle on y
        lit et y ecrit les resultats. Son contenu doit prendre
        la forme suivante:
        ("{'friday': {'22:00': True, '8:00': False}, 'monday': {'22:00': True, '8:00': "
         "False}, 'saturday': {'10:00': False, '23:00': True}, 'sunday': {'10:00': "
         "False, '23:00': True}, 'thursday': {'22:00': True, '8:00': False}, "
         "'tuesday': {'22:00': True, '8:00': False}, 'wednesday': {'22:00': True, "
         "'8:00': False}}")
    :type paths_var: tkinter.StringVar
    :param ylabel: Nom de l'axe des ordonees.
    :type ylabel: str
    :param converter: Fonction de validation qui permet de forcer l'utilisateur a
        saisir une donne correcte. Cette fonction prend en entree la chaine de caractere
        saisie par l'utilisateur. Renvoi la donnee refletee par cette chaine.
        Leve une exception si les donnee d'entree sont incorrectes.
    :type converter: callable

    sortie
    ------
    :return: La frame habillee.
    :rtype: tkinter.Frame

    exemple
    -------
    :Example:
    >>> import tkinter
    >>> from raisin.application.hmi import schedules
    >>> master = tkinter.Tk()
    >>> var = tkinter.StringVar()
    >>> var.set(str({
        'friday': {'22:00': True, '8:00': False}, 
        'monday': {'22:00': True, '8:00': False},
        'saturday': {'10:00': False, '23:00': True},
        'sunday': {'10:00': False, '23:00': True},
        'thursday': {'22:00': True, '8:00': False},
        'tuesday': {'22:00': True, '8:00': False},
        'wednesday': {'22:00': True, '8:00': False}}))
    >>> schedules.padding(tkinter.Frame(master), var).pack(fill="both", expand=True)
    >>> master.mainloop()
    """
    global schedules, schedules_manager

    def graph(day):
        """
        Genere un canevas qui contient
        le graphique pour ce jour.
        """
        # Calcul des points
        dates = sorted({time.strptime("%s:%s" % (day, d), "%A:%H:%M") for d in list(schedules[day].keys()) + ["00:00", "23:59"]})
        values = [schedules_manager(d) for d in dates]
        for i in range(len(dates)-1): # Fonction escalier. Pour ne pas faire d'interpolation lineaire.
            dates.insert(2*i + 1, dates[2*i + 1])
            values.insert(2*i + 1, values[2*i])

        # Affichage
        import matplotlib
        import matplotlib.figure
        import matplotlib.backends.backend_tkagg
        fig = matplotlib.figure.Figure(facecolor=theme.JAUNE)                   # couleur de fond autour du graph
        ax = fig.add_subplot()
        ax.set_facecolor(theme.JAUNE)                                           # couleur de fond dans le graph
        ax.set_xlabel("time (hour)")
        ax.set_ylabel(ylabel)
        xfmt = matplotlib.dates.DateFormatter("%H:%M")                          # format de l'heure a afficher
        ax.xaxis.set_major_formatter(xfmt)
        ax.plot([datetime.datetime(*d[:6]) for d in dates], values, "o-", color=theme.POURPRE)

        return matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=frames[day]).get_tk_widget()

    def disp_entry(day):
        """
        Ecrit dans la barre de saisie du jour correspondant,
        le nouveau contenu associe a la variable schedules[day]
        """
        keys = sorted(schedules[day].keys(), key=lambda h: 60*int(h.split(":")[0]) + int(h.split(":")[1]))
        entrees[day].delete(0, "end")
        entrees[day].insert(0, ", ".join(
            "%s: %s" % (d.replace(":", "h"), schedules[day][d])
            for d in keys))

    def validate(event):
        """
        Tente de comprendre ce qu'il y a dans la zonne de saisie.
        Si ce qui est saisi est correcte, Les graphiques sont mis a jour.
        Et le contenu de la variable 'schedules_var' est mise a jour.
        """
        global schedules, schedules_manager

        with Printer("Check the input...") as p:
            # Verifications
            bloc = r"(\s*\d{1,2}[h:]\d{1,2}(?:(?:\s*:\s*)|\s+)[a-zA-Z0-9\.]+)"
            patern = bloc + r"(?:\s*[,;]" + bloc + r")*" # Model regex d'une saisie corecte.
            if not re.fullmatch(patern, event.widget.get()): # On tente de recuperer les groupes.
                p.show("Syntaxe incorrecte.") # Si la saisie n'est pas corecte,
                return # On ne va pas plus loin.
            p.show("Syntaxe correct.")

            # Recuperation du jour.
            for day, entry in entrees.items():
                if event.widget is entry:
                    break
            p.show("Day: %s." % day)
            canvas_entree[day].delete("all")
            canvas_entree[day].create_image(8, 8, image=theme.icons.refresh())
            
            # Extraction des informations.
            nouv_schedules = copy.copy(schedules)
            nouv_schedules[day] = {}
            for group in re.compile(bloc).findall(event.widget.get()):
                decomposition = re.search(
                    r"(?P<heures>\d+)[h:](?P<minutes>\d+).+?(?P<value>[a-zA-Z0-9\.]+)",
                    group)
                heures = int(decomposition.group("heures"))
                minutes = int(decomposition.group("minutes"))
                try:
                    value = converter(decomposition.group("value"))
                except KeyboardInterrupt as e:
                    raise e from e
                except Exception as e:
                    p.show("La valeur %s n'est pas pythonisable." \
                        % repr(decomposition.group("value")))
                    p.show(" and ".join(e.args))
                    canvas_entree[day].delete("all")
                    canvas_entree[day].create_image(8, 8, image=theme.icons.error())
                    return
                p.show("%02dh%02d: %s" % (heures, minutes, value))
                nouv_schedules[day]["%02d:%02d" % (heures, minutes)] = value

            # Deuxieme verification.
            if nouv_schedules == schedules:
                p.show("Nothing change.")
                canvas_entree[day].delete("all")
                canvas_entree[day].create_image(8, 8, image=theme.icons.ok())
                return
            if not checks.schedules_verification(nouv_schedules):
                o.show("Invalid data.")
                canvas_entree[day].delete("all")
                canvas_entree[day].create_image(8, 8, image=theme.icons.error())
                return

            # Enregistrement des changements.
            schedules = nouv_schedules
            schedules_manager = Schedules(schedules)
            schedules_var.set(str(schedules))

            # Visualisation des changements.
            disp_entry(day)
            for day_ in canvas_graph: # Un changement sur un jour,
                canvas_graph[day_].delete("all") # peut impacter le graphique des jours suivants.
                canvas_graph[day_] = graph(day_) # Donc dans le doute, on les met tous a jour.
                canvas_graph[day_].grid(row=0, column=0, columnspan=2, sticky="nesw")
            canvas_entree[day].delete("all")
            canvas_entree[day].create_image(8, 8, image=theme.icons.ok())

    # Verifications.
    assert isinstance(frame, tkinter.Frame), \
        "'frame' doit etre de type tkinter.Frame, pas %s." % type(frame).__name__
    assert isinstance(schedules_var, tkinter.StringVar), \
        "'schedules_var' doit etre de type tkinter.StringVar, pas %s." % type(schedules_var).__name__
    assert isinstance(ylabel, str), \
        "'ylabel' doit etre de type str, pas %s." % type(ylabel).__name__
    assert ylabel, "'ylabel' ne doit pas etre une chaine vide."
    assert hasattr(converter, "__call__"), "'converter' doit etre un callable."

    # Declaration des variables.
    frames = {} # Contient les frames pour chaque jour.
    try:
        schedules = eval(schedules_var.get())
    except (SyntaxError, TypeError) as e:
        raise ValueError(
            "'schedules' n'a pas un contenu qui represente une variable python.") from e
    assert checks.schedules_verification(schedules), \
        "'schedules' ne respecte pas les conventions."
    canvas_graph = {}
    canvas_entree = {}
    entrees = {}
    schedules_manager = Schedules(schedules)

    with Printer("Schedules padding..."):
        # Initialisation des widgets.
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        theme.theme(frame)

        notebook = theme.theme(tkinter.ttk.Notebook(frame))
        notebook.grid(row=0, column=0, sticky="nesw")

        for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
            frames[day] = theme.theme(tkinter.Frame(frame))
            notebook.add(frames[day], text=day)
            frames[day].rowconfigure(0, weight=31)
            frames[day].rowconfigure(1, weight=1)
            frames[day].rowconfigure(2, weight=1)
            frames[day].columnconfigure(0, weight=1)
            frames[day].columnconfigure(1, weight=32)
            canvas_graph[day] = graph(day)
            canvas_graph[day].grid(row=0, column=0, columnspan=2, sticky="nesw")
            canvas_entree[day] = theme.theme(tkinter.Canvas(frames[day]))
            canvas_entree[day].grid(row=1, column=0)

            entrees[day] = theme.theme(tkinter.Entry(frames[day]))
            entrees[day].grid(row=1, column=1, sticky="ew")
            entrees[day].bind("<KeyRelease>", validate)
            disp_entry(day)

        return frame

def get_schedules(schedules, *, existing_window=None, ylabel="value", converter=eval):
    """
    |======================================|
    | Interface pour changer les horaires. |
    |======================================|

    Utilise dans la mesure du possible, une jolie interface graphique.
    Les verifications sont faites ici.
    Ne modifie pas le contenu de 'schedules', fait une copie veritable.

    parametres
    ----------
    :param schedules: Les horaires deja existantes.
    :type schedules: dict
    :param existing_window: Une fenetre tkinter presente par ailleur.
    :param ylabel: Nom de l'axe des ordonees.
    :type ylabel: str
    :param converter: Fonction de validation qui permet de forcer l'utilisateur a
        saisir une donne correcte. Cette fonction prend en entree la chaine de caractere
        saisie par l'utilisateur. Renvoi la donnee refletee par cette chaine.
        Leve une exception si les donnee d'entree sont incorrectes.
    :type converter: callable

    sortie
    ------
    :return: Les nouvelles horaires.
    :rtype: dict

    exemple
    -------
    :Example:
    >>> from raisin.application.hmi import schedules
    >>> s = {
        'friday': {'22:00': True, '8:00': False}, 
        'monday': {'22:00': True, '8:00': False},
        'saturday': {'10:00': False, '23:00': True},
        'sunday': {'10:00': False, '23:00': True},
        'thursday': {'22:00': True, '8:00': False},
        'tuesday': {'22:00': True, '8:00': False},
        'wednesday': {'22:00': True, '8:00': False}}
    >>> schedules.get_schedules(s)
    {'friday': {'22:00': True, '8:00': False}, 
    'monday': {'22:00': True, '8:00': False},
    'saturday': {'10:00': False, '23:00': True},
    'sunday': {'10:00': False, '23:00': True},
    'thursday': {'22:00': True, '8:00': False},
    'tuesday': {'22:00': True, '8:00': False},
    'wednesday': {'22:00': True, '8:00': False}}
    >>>
    """
    class DialogWindow:
        """
        Permet d'interragir graphiquement avec l'utilisateur.
        """
        def __init__(self, schedules, ylabel, converter, existing_window):
            self.schedules = copy.copy(schedules)
            self.ylabel = ylabel
            self.converter = converter
            self.existing_window = existing_window
            self.violently_closed = True        # permet de savoir si la fenetre a ete fermee violement ou via le bouton 'valider'
            self.answer = None                  # reponse de l'utilisateur

            # preparation de la fenetre
            if self.existing_window:                                                        # si il y a deja une fenetre ouverte
                self.window = tkinter.Toplevel(self.existing_window)                        # on est oblige d'utiliser un toplevel sinon ca plante
                self.window.grab_set()                                                      # on fige la fenetre parente
                self.window.protocol("WM_DELETE_WINDOW", lambda : (self.window.destroy(), self.window.quit()))# il se trouve que ca semble fonctionner comme ca...
            else:                                                                           # dans le cas ou aucune instance tkinter n'existe
                self.window = tkinter.Tk()                                                  # et bien on en cre une tout simplement

            # configuration
            self.window.title("Change schedules")
            self.window.configure(background=theme.JAUNE)
            self.window.columnconfigure(0, weight=1)                                         # numero de colone, etirement relatif: On rend l'onglet redimenssionable sur la largeur
            self.window.rowconfigure(0, weight=30)
            self.window.rowconfigure(1, weight=1)
            self.window.focus_force()
            self.window.bind("<Return>", lambda event: self.quit())
            self.window.bind("<Escape>", lambda event: self.quit())

            # initialisation des variables
            self.schedules_var = tkinter.StringVar()
            self.schedules_var.set(str(self.schedules))

            # remplissage + ecoute
            padding(
                tkinter.Frame(self.window),
                self.schedules_var,
                ylabel=self.ylabel,
                converter=self.converter
                ).grid(row=0, column=0, sticky="ewsn")
            theme.theme(
                tkinter.Button(self.window, text="Valider", command=lambda: self.quit())
                ).grid(row=1, column=0)
            self.window.mainloop()

        def quit(self):
            self.violently_closed = False                                                   # si on ferme la fenetre depuis cette methode, c'est que la fermeture est propre
            self.answer = eval(self.schedules_var.get())                                    # on peut allos recuperer la reponse
            self.window.destroy()                                                           # selon qu'il y ai deja une fenetre en arriere plan
            if self.existing_window:                                                        # on applique ou non la methode destroy
                self.window.quit() 

    with Printer("Configure the raisin schedules..."):
        if tkinter:
            try:
                import matplotlib
            except ImportError as e:
                raise NotImplementedError("Il faut installer matplotlib.") from e
            
            # Avec fenetre graphique.
            g = DialogWindow(schedules, ylabel, converter, existing_window=existing_window)
            if g.violently_closed:
                raise KeyboardInterrupt("La fenetre a ete fermee violement!")
            return g.answer
        
        else:
            raise NotImplementedError("Il faut installer tkinter.")
