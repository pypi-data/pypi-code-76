#!/usr/bin/env python3

"""
Permet de poser de simples petites question a l'utilisateur.
"""

import getpass

from ...tools import Printer
from .theme import theme as _theme
from .theme import (JAUNE, POURPRE, VERT_CLAIR, VERT_FONCE)
from ..hmi import tkinter


def question_binaire(question, *, default=None, existing_window=None):
    """
    pose une question a l'utilisateur ou la reponse ne peut etre que oui ou non
    'default' doit etre True pour oui ou False pour non
    retourne True ou False en fonction de la reponse
    leve un KeyboardInterrupt si l'utilisateur se rebelle
    """
    class DialogWindow:
        """
        permet repondre a une question fermee
        """
        def __init__(self, question, default, existing_window):
            self.question = question
            self.default = default
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
            self.window.configure(background=JAUNE)
            self.window.columnconfigure(0, weight=1)
            self.window.columnconfigure(1, weight=1)
            self.window.rowconfigure(0, weight=2)
            self.window.rowconfigure(1, weight=1)

            # remplissage + ecoute
            self.create_widgets()
            self.window.bind("<Return>", lambda event : self.quit(self.default))
            self.window.focus_force()
            self.window.mainloop()

        def create_widgets(self):
            text = self.question + ("\n('%s' par defaut)" % {True:"yes", False:"no"}[self.default] if type(self.default) is bool else "")
            _theme(tkinter.Label(self.window, text=text, wraplength=300)).grid(row=0, column=0, columnspan=2, sticky="ew")
            _theme(tkinter.Button(self.window, text="Yes", command=lambda : self.quit(True))).grid(row=1, column=0, sticky="ew")
            _theme(tkinter.Button(self.window, text="No", command=lambda : self.quit(False))).grid(row=1, column=1, sticky="ew")

        def quit(self, option):
            if option is None:
                Printer().show("Il n'y a pas de valeur par defaut!")
                return
            self.violently_closed = False                                                   # si on ferme la fenetre depuis cette methode, c'est que la fermeture est propre
            self.answer = option                                                            # on peut allos recuperer la reponse
            self.window.destroy()                                                           # selon qu'il y ai deja une fenetre en arriere plan
            if self.existing_window:                                                        # on applique ou non la methode destroy
                self.window.quit() 

    assert type(question) is str,\
        "type(question) must be 'str', %s is not 'str': it is %s" % (question, type(question))
    assert default in [True, False, None],\
        "La valeur par defaut ne peut etre que True, False ou None, pas %s." % default
    
    if tkinter:                     # si il y a une possibilite d'avoir une interface graphique
        try:
            g = DialogWindow(question, default=default, existing_window=existing_window)
        except tkinter.TclError:
            pass
        else:
            if g.violently_closed:
                raise KeyboardInterrupt("La fenetre a ete fermee violement!")
            return g.answer
    
    # dans le cas ou l'on doit tout faire dans le terminal
    aide = "y/n" if default is None else \
          ("Y/n" if default == True else "y/N")
    p = Printer()
    while 1:                    # tant que l'utilisateur n'a pas donne une reponsse satisfaisante
        reponse = input(p.indent(question + " [%s] " % aide))
        if not reponse:         # si l'utilisateur n'a rien repondu
            if default is None:
                p.show("\tVous etes oblige de fournir une reponse car il n'y a pas de valeur par defaut.")
                continue
            return default# on renvoi la valeur par defaut
        elif reponse.lower() == "y":# si l'utilisateur a dit oui
            return True         # on retourne positivement
        elif reponse.lower() == "n":# si il a dit non
            return False        # on retourne False
        else:                   # si la reponse n'est pas comprehenssible
            p.show("\tVous ne pouvez repondre que 'y' or 'n', no %s." % reponse)

def question_choix_multiples(question, choix, default=None, indentation=0):
    """
    pose une question et propose une multitude de reponses parmis
    la liste choix
    la liste des choix est une liste de str, chaque chaine est depourvue de point d'interrogation
    mis a part la question principale
    retourne une liste de bouleens
    """
    if default is None:
        default = {}

    class Graphic:
        """
        representation graphique avec tkinter
        """
        def __init__(self, question, choix, default):
            self.question = question
            self.choix = choix
            self.resultats = []
            self.default = default
            self.fenetre = tkinter.Tk()
            self.checkvars = [tkinter.IntVar() for i in range(len(choix))]
            for i in range(len(self.checkvars)): # on met les valeurs par defaut
                self.checkvars[i].set({None:-1, True:1, False:0}[self.default.get(i, None)])

        def show(self):
            self.fenetre.title("raisin")
            label = tkinter.Label(self.fenetre, text=self.question)
            label.grid(row=0, column=0)
            questions = [tkinter.Label(self.fenetre, text="%d) %s ?" % (i+1, text)) for i,text in enumerate(self.choix)]
            [q.grid(row=i+1, column=0) for i,q in enumerate(questions)]
            for column, affirmation in zip((1, 2), ("yes", "no")):
                radio_boutons = [tkinter.Radiobutton(self.fenetre, 
                                    variable=v,
                                    text=affirmation,
                                    value=(1 if affirmation == "yes" else 0))
                                for v,c in zip(self.checkvars, self.choix)]
                [b.grid(row=i+1, column=column) for i,b in enumerate(radio_boutons)]

            valideur = tkinter.Button(self.fenetre, text="Valider", command=self.valider)
            valideur.grid(row=0, column=2)
            self.fenetre.mainloop()

        def valider(self):
            for i, v in enumerate(self.checkvars):
                if v.get() == -1:
                    tkinter.messagebox.showerror("Reponse incomplette", "Vous devez choisir une option pour la reponse n°%d." % (i+1))
                    return
            self.resultats = [bool(v.get()) for v in self.checkvars]
            self.fenetre.destroy() 

    def terminal(question, choix, default, indentation):
        """
        pose les questions dans le terminal
        """
        print("\t"*indentation + question)
        print("\t"*indentation + "\tchoix possibles (inclusif):")
        for i,c in enumerate(choix):
            print("\t"*indentation + "\t\t" + str(i+1) + ": " + c)
        return [question_binaire(q + " ?", default.get(i, None), indentation=indentation+1) for i, q in enumerate(choix)]

    # verification des entrees
    assert type(question) is str, "type(question) must be 'str', %s is not 'str': it is %s." % (question, type(question))
    assert type(default) is dict, "type(default) must be 'dict', %s is not a 'dict': it is %s." % (default, type(default))
    for clef, value in default.items():
        assert type(clef) is int, "Les clef des 'default' doiventent etre de type int, pas %s." % type(clef)
        assert 0 <= clef < len(choix), "Les clefs representent le rang de la question, %d n'est pas compris entre 0 et %d" % (clef, len(choix)-1)
        assert value in [True, False, None], "Les valeurs par defaut ne peuvent etre que True, False ou None, pas %s." % value
    assert type(choix) is list, "'choix' doit etre une liste, pas un %s." % type(choix)
    for c in choix:
        assert type(c) is str, "type(choix) must be 'str', %s is not 'str': it is %s" % (c, type(c))

    if tkinter:                     # si il y a de quoi faire une interface graphique
        try:
            g = Graphic(question, choix, default)
            g.show()
        except tkinter.TclError:
            return terminal(question, choix, default, indentation)
        else:
            res = g.resultats
            if not res:
                raise KeyboardInterrupt
            return res
    else:
        return terminal(question, choix, default, indentation)

def question_choix_exclusif(question, choix, *, default=None, existing_window=None):
    """
    pose une question avec un nombre limite de reponses
    retourne le rang de la reponse en partant de 0, leve KeyboardInterrupt si l'utilisateur refuse de cooperer
    'default' et le rang de la reponse selectionne par defaut
    'existing_window' vaut soit None, si il n'y a aucune autre fenetre ailleur, ou vaut vaut l'instance de la fenetre existante si il y en a deja une
    """
    class DialogWindow:
        """
        permet de demander une reponse parmis une liste de choix possible
        """
        def __init__(self, question, choix, default, existing_window):
            self.question = question
            self.choix = choix
            self.default = default
            self.existing_window = existing_window
            self.violently_closed = True        # permet de savoir si la fenetre a ete fermee violement ou via le bouton 'valider'
            self.answer = None                  # reponsse de l'utilisateur

            # preparation de la fenetre
            if self.existing_window:                                                        # si il y a deja une fenetre ouverte
                self.window = tkinter.Toplevel(self.existing_window)                        # on est oblige d'utiliser un toplevel sinon ca plante
                self.window.grab_set()                                                      # on fige la fenetre parente
                self.window.protocol("WM_DELETE_WINDOW", lambda : (self.window.destroy(), self.window.quit()))# il se trouve que ca semble fonctionner comme ca...
            else:                                                                           # dans le cas ou aucune instance tkinter n'existe
                self.window = tkinter.Tk()                                                  # et bien on en cre une tout simplement

            # configuration
            self.window.configure(background=JAUNE)
            self.window.columnconfigure(0, weight=1)
            for i in range(len(self.choix) + 2):
                self.window.rowconfigure(i, weight=1)

            # remplissage + ecoute
            self.initializing_variables()
            self.create_widgets()
            self.window.bind("<Return>", lambda event : self.quit())
            self.window.focus_force()
            self.window.mainloop()

        def initializing_variables(self):
            """
            prepare les variables qui cont etre utiles
            """
            self.answer_var = tkinter.IntVar()                                              # variable qui contient le champ de reponse
            self.answer_var.set(self.default if self.default is not None else -1)               # on l'initialise avec la valeur par defaut si il y en a une

        def create_widgets(self):
            """
            met les widgets dans la fanetre
            """
            _theme(tkinter.Label(self.window, text=self.question)).grid(row=0, column=0, sticky="ew")
            for i, text in enumerate(self.choix):
                _theme(tkinter.Radiobutton(self.window, variable=self.answer_var, text=text, value=i)).grid(row=i+1, column=0, sticky="ew")
            _theme(tkinter.Button(self.window, text="Validate", command=self.quit)).grid(row=len(self.choix)+1, column=0, sticky="ew")

        def quit(self):
            """
            detruit la fenetre si la reponsse et bonne
            et enregistre la reponse
            """
            if self.answer_var.get() == -1:
                Printer().show("Il faut saisir une reponse!")
                return
            self.violently_closed = False                                                   # si on ferme la fenetre depuis cette methode, c'est que la fermeture est propre
            self.answer = self.answer_var.get()                                             # on peut allos recuperer la reponse
            self.window.destroy()                                                           # selon qu'il y ai deja une fenetre en arriere plan
            if self.existing_window:                                                        # on applique ou non la methode destroy
                self.window.quit()  

    # verification des entrees
    assert type(question) is str, "type(question) must be 'str', %s is not 'str': it is %s." % (question, type(question))
    assert type(choix) is list, "'choix' doit etre une liste, pas un %s." % type(choix)
    for c in choix:
        assert type(c) is str, "type(choix) must be 'str', %s is not 'str': it is %s" % (c, type(c))
    assert default is None or type(default) is int, "'default' doit etre un entier, pas: %s." % type(default)
    if type(default) is int:
        assert 0 <= default < len(choix), "'default' doit etre compris entre 0 et %d. Or il vaut %s." % (len(choix)-1, default)

    if tkinter:
        try:
            g = DialogWindow(question, choix, default=default, existing_window=existing_window)
        except tkinter.TclError:
            pass
        else:
            if g.violently_closed:
                raise KeyboardInterrupt("La fenetre a ete fermee violement!")
            return g.answer

    # Si l'interface graphique a echouee.
    p = Printer()
    while 1:
        p.show(question)
        p.show("\tchoix possibles (exclusif):")
        for i, c in enumerate(choix):
            p.show("\t\t" + str(i+1) + ": " + c + (" (par default)" if i == default else ""))
        rep = input(p.indent("reponse n° "))
        if not rep:
            if default:
                return default
            p.show("\tVous etes oblige de fournir une reponse car il n'y a pas de valeur par defaut.")
            continue
        if not rep.isdigit():
            p.show("\tVous devez entrer un nombre entre nombre entier, pas '%s'." % rep)
            continue
        rep = int(rep)
        if  rep > len(choix) or rep < 1:
            p.show("\tLe resultat doit etre compris entre %s et %d." % (1, len(choix)))
            continue
        return rep - 1

def question_reponse(question, *, default=None, validatecommand=lambda answer : True, existing_window=None, show=None):
    """
    Pose une question qui appelle a une reponse ecrite.
    Retourne la reponse de l'utilisateur, ou leve KeyboardInterrupt, si l'utilisateur refuse de cooperer.
    'default' est la valeur par defaut (str ou None)
    'existing_window' vaut soit None, si il n'y a aucune autre fenetre ailleur, ou vaut vaut l'instance de la fenetre existante si il y en a deja une
    """
    class DialogWindow:
        """
        Permet de poser graphiquement une question a choix ouvert a l'utilisateur
        """
        def __init__(self, question, default, validatecommand, existing_window, show):
            self.question = question
            self.default = default
            self.validatecommand = validatecommand
            self.existing_window = existing_window
            self.show = show
            self.violently_closed = True        # permet de savoir si la fenetre a ete fermee violement ou via le bouton 'valider'
            self.answer = None                  # reponsse de l'utilisateur

            # preparation de la fenetre
            if self.existing_window:                                      # si il y a deja une fenetre ouverte
                self.window = tkinter.Toplevel(self.existing_window)      # on est oblige d'utiliser un toplevel sinon ca plante
                self.window.grab_set()                                    # on fige la fenetre parente
                self.window.protocol(
                    "WM_DELETE_WINDOW",
                    lambda : (self.window.destroy(), self.window.quit())) # il se trouve que ca semble fonctionner comme ca...
            else:                                                         # dans le cas ou aucune instance tkinter n'existe
                self.window = tkinter.Tk()                                # et bien on en cre une tout simplement

            # configuration
            self.window.configure(background=JAUNE)
            self.window.columnconfigure(0, weight=1)
            self.window.rowconfigure(0, weight=1)
            self.window.rowconfigure(1, weight=1)
            self.window.rowconfigure(2, weight=1)
            
            # remplissage + ecoute
            self.initializing_variables()
            self.create_widgets()
            self.window.bind(
                "<Return>",
                lambda event : self.quit() if self.validate_button["state"] == "normal" else None)
            self.window.focus_force()
            self.window.mainloop()

        def quit(self):
            """
            detruit la fenetre
            et enregistre la reponse
            """
            self.violently_closed = False                                                   # si on ferme la fenetre depuis cette methode, c'est que la fermeture est propre
            self.answer = self.answer_var.get()                                             # on peut allos recuperer la reponse
            self.window.destroy()                                                           # selon qu'il y ai deja une fenetre en arriere plan
            if self.existing_window:                                                        # on applique ou non la methode destroy
                self.window.quit()  

        def initializing_variables(self):
            """
            prepare les variables qui cont etre utiles
            """
            self.answer_var = tkinter.StringVar()                                           # variable qui contient le champ de reponse
            self.answer_var.set(self.default if self.default is not None else "")               # on l'initialise avec la valeur par defaut si il y en a une

        def create_widgets(self):
            """
            rempli la fenetre avec les widgets
            """
            _theme(tkinter.Label(self.window, text=self.question)).grid(row=0, column=0, sticky="ew")
            self.validate_button = _theme(tkinter.Button(
                self.window,
                text="Validate",
                command=self.quit,
                state="normal" if self.validatecommand(self.answer_var.get()) else "disable"
            ))
            self.validate_button.grid(row=2, column=0)
            entry = _theme(tkinter.Entry(self.window, show=self.show, textvariable=self.answer_var))
            entry.bind(
                "<KeyRelease>",
                lambda event : self.validate_button.config(
                    state="normal"
                    if self.validatecommand(self.answer_var.get())
                    else self.validate_button.config(state="disable")))
            entry.focus()                               # on force le focus
            entry.grid(row=1, column=0, sticky="ew")

    # verification des entrees
    assert type(question) is str, "type(question) must be 'str', %s is not 'str': it is %s." % (question, type(question))
    assert type(default) is str or default is None, "type(default) must be 'str: it is %s." % type(default)

    if tkinter:
        try:
            g = DialogWindow(question, default=default, validatecommand=validatecommand, existing_window=existing_window, show=show)
        except tkinter.TclError:
            pass
        else:
            if g.violently_closed:
                raise KeyboardInterrupt("La fenetre a ete fermee violement!")
            return g.answer

    # Si on doit se rabatre sur une interaction dans le terminal.
    p = Printer()
    while 1:
        p.show(question)
        if default:
            p.show("Reponse par default: %s" % default)
        if show == "" or show == "*":
            rep = getpass.getpass(p.indent("Votre Reponse: "))
        else:
            rep = input(p.indent("Votre Reponse: "))
        if not rep and default is not None:
            return default
        if not validatecommand(rep):
            continue
        return rep
