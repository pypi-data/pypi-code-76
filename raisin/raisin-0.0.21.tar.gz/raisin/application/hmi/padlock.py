#!/usr/bin/env python3

"""
|=======================|
| Gestion de l'antivol. |
|=======================|

Interagit avec l'utilisateur afin de lui demander ce qu'il shouaite.
"""

import time

from ..settings import settings
from ..hmi import tkinter, messagebox
from .theme import *
from .pathmanager import padding


def get_new_padlock(*, existing_window=None):
    """
    |==========================================================|
    | Interface pour recuperer les volontees de l'utilisateur. |
    |==========================================================|

    Utilise dans la mesure du possible, une jolie interface graphique.
    Les verifications sur les entrees sont effectuee ici.

    parametres
    ----------
    :param existing_window: Une fenetre tkinter presente par ailleur.

    sortie
    ------
    :return:
        -Le temps de pose "break_time".
        -Si il faut chiffrer "cipher".
        -Si il faut notifier par email "notify_by_email".
        -Les chemins concernes "paths".
    :rtype: (int, bool, bool, dict)
    """
    class DialogWindow:
        """
        Permet d'interragir graphiquement avec l'utilisateur.
        """
        def __init__(self, break_time, cipher, notify_by_email, paths, existing_window):
            self.existing_window = existing_window
            self.violently_closed = True        # permet de savoir si la fenetre a ete fermee violement ou via le bouton 'valider'
            self.answer = None                  # reponse de l'utilisateur

            # Preparation de la fenetre.
            if self.existing_window:                                    # si il y a deja une fenetre ouverte
                self.window = tkinter.Toplevel(self.existing_window)    # on est oblige d'utiliser un toplevel sinon ca plante
                self.window.grab_set()                                  # on fige la fenetre parente
                self.window.protocol("WM_DELETE_WINDOW", lambda : (self.window.destroy(), self.window.quit()))# il se trouve que ca semble fonctionner comme ca...
            else:                                                       # dans le cas ou aucune instance tkinter n'existe
                self.window = tkinter.Tk()                              # et bien on en cre une tout simplement

            # Configuration de la fenetre.
            self.window.title("Change padlock")
            self.window.configure(background=JAUNE)
            self.window.columnconfigure(0, weight=1)
            self.window.columnconfigure(1, weight=31)
            self.window.columnconfigure(2, weight=1)
            for i in range(3):
                self.window.rowconfigure(i, weight=1)
            self.window.rowconfigure(3, weight=29)                      # on donne en grand pouvoir d'etiration a la frame contenant les repertoires
            self.window.rowconfigure(4, weight=1)
            self.window.focus_force()
            # self.window.bind("<Return>", lambda event : self.quit())
            self.window.bind("<Escape>", lambda event : self.quit())

            # Initialisation des variables.
            self.cipher = tkinter.IntVar()                              # booleen pour dire si on chiffre ou non les donnees personelles
            self.cipher.set(int(cipher))                                # on y met la valeur par defaut
            self.paths_var = tkinter.StringVar()                        # 'dico' serialise
            self.paths_var.set(str(paths))                              # ce dico represente les repertoires
            self.break_time = tkinter.StringVar()                       # temps d'inactivite
            self.break_time.set(str(break_time))                        # on le charge avec une valeur par defaut d'une heure
            self.notify_by_email = tkinter.IntVar()                     # booleen qui dit si l'on doit ou non envoyer un mail
            self.notify_by_email.set(int(notify_by_email))              # dans le cas ou l'ip changerai

            # remplissage + ecoute
            self.create_widgets()
            self._show_reps(self.frame, self.cipher)
            self.window.mainloop()

        def create_widgets(self):
            """
            Initialisation des widgets.
            """
            theme(tkinter.Checkbutton(self.window,
                variable=self.notify_by_email,
                text="Me notifier par email")).grid(row=0, column=0, columnspan=2, sticky="ew")
            theme(tkinter.Button(self.window,
                image=icons.info(),
                command=lambda: messagebox.showinfo(
                    "Info email padlock",
                    "Si cette option est cochée, Un email vous sera envoyé à chaque fois "
                    "qu'une nouvelle ip est détéctée. Cet email contiendra le maximum "
                    "d'information sur l'environement au moment de l'envoi.\n"
                    "Cela à pour but de vous aider à localiser votre ordinateur et celui qui le possède...")
                )).grid(row=0, column=2)
            theme(tkinter.Label(self.window, text="Temps de repos (s) :")).grid(row=1, column=0)
            spinbox = theme(tkinter.Spinbox(self.window,
                textvariable=self.break_time, # variable 'str' pour recuperer ce qui y a dans le champs
                from_=0, # valeur minimum
                to=2678400, # valeur maximum de l'increment (1 mois)
                ))
            spinbox.bind("<Return>", lambda event : self._as_int(self.break_time, minimum=0, maximum=2678400))
            spinbox.bind("<FocusOut>", lambda event : self._as_int(self.break_time, minimum=0, maximum=2678400))
            spinbox.grid(row=1, column=1, sticky="ew")
            theme(tkinter.Button(self.window,
                image=icons.info(),
                command=lambda : messagebox.showinfo(
                    "Info time padlock",
                    "Le temps entré est le temps de pause. C'est la durée durant "
                    "laquelle raisin ne cherche rien a savoir. Une fois ce temps écoulé, "
                    "raisin regarde l'ip, et agit possiblement.")
                )).grid(row=1, column=2)
            self.frame = theme(tkinter.Frame(self.window))
            theme(tkinter.Checkbutton(self.window, 
                variable=self.cipher,
                text="Chiffrer mes donnees personelles",
                command=lambda : self._show_reps(self.frame, self.cipher), # affiche ou non les repertoires au moment de cocher / decocher la case
                )).grid(row=2, column=0, columnspan=2, sticky="ew")
            theme(tkinter.Button(self.window,
                image=icons.info(),
                command=lambda : messagebox.showinfo(
                    "Info cipher padlock",
                    "Si vous cochez cette case, raisin criptera les dossiers précisés ci-dessous. "
                    "Une fois le chiffrage terminé, une fenetre apparraitera vous demandant votre mot "
                    "de passe. L'orsque vous arriverez a entrez le bon mot de passe, toutes vos données seront déchiffrées. "
                    "Cette option permet au potentiel voleur de ne pas avoir acces à vos donnéess personelles.")
                )).grid(row=2, column=2)
            padding(self.frame, self.paths_var)
            self.frame.grid(row=3, column=0, columnspan=2, sticky="nesw")
            theme(tkinter.Button(self.window,
                image=icons.info(),
                command=lambda : messagebox.showinfo(
                    "Info path padlock",
                    "Les chemins present dans la liste des chemin principaux seront "
                    "chiffre recursivement. Si un sous repertoire ou un fichier "
                    "particulier ne doit pas etre affecté, il faut l'ajouter au chemins a exclure.")
                )).grid(row=3, column=2)
            theme(tkinter.Button(self.window, text="Valider", command=self.quit)).grid(row=4, column=0, columnspan=2)

        def _as_int(self, break_time, minimum, maximum):
            try:
                entier = int(eval(break_time.get()))
            except:
                entier = 3600
            break_time.set(str(min(maximum, max(minimum, entier))))

        def _show_reps(self, frame, cipher):
            if self.cipher.get():
                frame.grid(row=3, column=0, columnspan=2, sticky="nesw")            # active la zone ou il y a les chemins
            else:
                frame.grid_forget()  

        def quit(self):
            self.violently_closed = False                               # si on ferme la fenetre depuis cette methode, c'est que la fermeture est propre
            self.answer = (
                int(self.break_time.get()),
                bool(self.cipher.get()),
                bool(self.notify_by_email.get()),
                eval(self.paths_var.get()))                             # on peut allos recuperer la reponse
            self.window.destroy()                                       # selon qu'il y ai deja une fenetre en arriere plan
            if self.existing_window:                                    # on applique ou non la methode destroy
                self.window.quit() 

    with Printer("Configure the raisin padlock..."):
        break_time = settings["account"]["padlock"]["break_time"]
        cipher = settings["account"]["padlock"]["cipher"]
        notify_by_email = settings["account"]["padlock"]["notify_by_email"]
        paths = settings["account"]["padlock"]["paths"]
        
        if tkinter:
            g = DialogWindow(break_time, cipher, notify_by_email, paths, existing_window=existing_window)
            if g.violently_closed:
                raise KeyboardInterrupt("La fenetre a ete fermee violement!")
            return g.answer
        else:
            raise NotImplementedError("Il faut installer tkinter.")
