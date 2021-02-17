#!/usr/bin/env python3

"""
|==========================================|
| Demande et modification du mot de passe. |
|==========================================|

Interagit avec l'utilisateur afin de lui demander le mot de passe.
C'est aussi ici qu'il y a l'interface qui permet de changer
le mot de passe.
"""

from ...tools import Printer
from ...security import request_psw
from ..hmi import tkinter, messagebox
from ..settings import settings
from .theme import *
import raisin.application.hmi.dialog as dialog


def get_new_psw(*, existing_window=None):
    """
    |===================================================|
    | Interface pour changer le mot de passe de raisin. |
    |===================================================|

    Utilise dans la mesure du possible, une jolie interface graphique.
    Les verifications sont faites ici.

    parametres
    ----------
    :param existing_window: Une fenetre tkinter presente par ailleur.

    sortie
    ------
    :return:
        -Le nouveau mot de passe.
        -La nouvelle sentence memory.
        -Si il faut enregistrer le mot de passe en clair.
    :rtype: (str, str, bool)
    """
    class DialogWindow:
        """
        Permet d'interragir graphiquement avec l'utilisateur.
        """
        def __init__(self, old_psw, sentence_memory, clair, existing_window):
            self.sentence_memory = sentence_memory
            self.clair = clair
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
            self.window.title("Change password")
            self.window.configure(background=JAUNE)
            self.window.columnconfigure(0, weight=1)                                         # numero de colone, etirement relatif: On rend l'onglet redimenssionable sur la largeur
            self.window.columnconfigure(1, weight=31)
            self.window.columnconfigure(2, weight=1)
            for i in range(6):
                self.window.rowconfigure(i, weight=1)
            self.window.focus_force()
            self.window.bind("<Return>", lambda event: self.quit())
            self.window.bind("<Escape>", lambda event: self.quit())

            # initialisation des variables
            self.psw1 = tkinter.StringVar()
            self.psw1.set(old_psw if old_psw is not None else "")
            self.psw2 = tkinter.StringVar()
            self.psw2.set(old_psw if old_psw is not None else "")
            self.ok_var = tkinter.StringVar()
            self.en_clair = tkinter.IntVar()
            self.en_clair.set(clair)
            self.memory = tkinter.StringVar()
            self.memory.set(sentence_memory)

            # remplissage + ecoute
            self.create_widgets()
            self.compare()
            self.window.mainloop()

        def create_widgets(self):
            """
            Initialisation des widgets.
            """
            theme(tkinter.Label(self.window, text="New Password :")).grid(row=0, column=0, sticky="w")
            entre1 = theme(tkinter.Entry(self.window, show="*", textvariable=self.psw1))
            entre1.bind("<KeyRelease>", lambda event : self.compare())
            entre1.grid(row=0, column=1, sticky="ew")
            theme(tkinter.Label(self.window, text="Confirmation :")).grid(row=1, column=0, sticky="w")
            entre2 = theme(tkinter.Entry(self.window, show="*", textvariable=self.psw2))
            entre2.bind("<KeyRelease>", lambda event : self.compare())
            entre2.grid(row=1, column=1, sticky="ew")
            self.canvas_ok = theme(tkinter.Canvas(self.window))
            self.canvas_ok.grid(row=2, column=0)
            theme(tkinter.Label(self.window, textvariable=self.ok_var)).grid(row=2, column=1)
            theme(tkinter.Checkbutton(self.window, variable=self.en_clair, text="Enregistrer le mot de passe en clair")).grid(row=3, column=0, columnspan=2, sticky="ew")
            theme(tkinter.Button(self.window,
                image=icons.info(),
                command=lambda: messagebox.showinfo(
                    "Info psw",
                    "Enregistrer le mot de passe en clair permet de donner de l'autonomie a l'application. "
                    "En effet, raisin sera capable tous seul d'aller chercher le mot de passe "
                    "sans avoir a vous le demander a tous bout de champs. Mais comme vous pouvez "
                    "vous en douter, cette option n'est pas ultra sécure!")
                )).grid(row=3, column=3)
            theme(tkinter.Label(self.window, text="sentence_memory :")).grid(row=4, column=0, sticky="w")
            theme(tkinter.Entry(self.window, textvariable=self.memory)).grid(row=4, column=1, sticky="ew")
            self.valider = theme(tkinter.Button(self.window, text="Valider", command=lambda: self.quit()))
            self.valider.grid(row=5, column=0, columnspan=2)

        def compare(self):
            """
            Compare les 2 mots de passes et fait apparaitre
            le bouton de validation.
            """
            self.canvas_ok.delete("all")
            if self.psw1.get() == self.psw2.get():
                self.canvas_ok.create_image(8, 8, image=icons.ok())
                self.ok_var.set("Passwords are the same.")
                self.valider.config(state="normal")
            else:
                self.canvas_ok.create_image(8, 8, image=icons.error())
                self.ok_var.set("Passwords do not match.")
                self.valider.config(state="disable")

        def quit(self):
            if self.psw1.get() != self.psw2.get():
                Printer().show("Passwords do not match.")
            else:
                self.violently_closed = False                                                   # si on ferme la fenetre depuis cette methode, c'est que la fermeture est propre
                self.answer = (self.psw1.get(), self.memory.get(), self.en_clair.get())                                                            # on peut allos recuperer la reponse
                self.window.destroy()                                                           # selon qu'il y ai deja une fenetre en arriere plan
                if self.existing_window:                                                        # on applique ou non la methode destroy
                    self.window.quit() 

    class DialogTerminal:
        """
        Permet d'interagir avec l'utilisateur dans le terminal.
        """
        def __init__(self, psw, sentence_memory, clair):
            self.psw = psw
            self.sentence_memory = sentence_memory
            self.clair = clair
            self.menu()

        def menu(self):
            """
            Choisi entre les differentes options.
            """
            choix1 = "Change / Delete the password." if self.psw else "Add a password."
            choix2 = "Change / Delete the mnemonic frase." if self.sentence_memory else "Add mnemonic frase."
            choix3 = "Do not save the password in clear text." if self.clair else "Save the password in clear text."
            rep = dialog.question_choix_exclusif(
                "What do you want to do?",
                choix=[
                    choix1,
                    choix2,
                    choix3,
                    "Apply changes and exit."
                ],
                default=3)
            if rep == 0:
                return self.get_psw()
            elif rep == 1:
                return self.get_mnemonic()
            elif rep == 2:
                self.clair = not self.clair
                return self.menu()

        def get_psw(self):
            """
            Supprime, change ou ajoute un mot de passe.
            """
            def get():
                psw = dialog.question_reponse("New password:", show="")
                dialog.question_reponse("Confirmation:", show="", validatecommand=lambda answer: answer == psw)
                return psw

            if not self.psw:
                psw = get()
                if psw:
                    self.psw = psw
                elif psw == "":
                    self.psw = None
            else:
                self.psw = None
                if dialog.question_choix_exclusif("Do you want to delete or change the password?", ["Delete.", "Change"]):
                    return self.get_psw()
            return self.menu()

        def get_mnemonic(self):
            """
            Demande une phrase mnemonique.
            """
            self.sentence_memory = dialog.question_reponse("mnemonic frase:")
            return self.menu()

    with Printer("Configure the raisin psw..."):
        old_psw = request_psw(force=True, message="Change the raisin psw.")
        sentence_memory = settings["account"]["security"]["sentence_memory"]
        clair = True if settings["account"]["security"]["psw"] else False
        
        if tkinter:
            try:
                g = DialogWindow(old_psw, sentence_memory, clair, existing_window=existing_window)
            except tkinter.TclError:
                pass
            else:
                if g.violently_closed:
                    raise KeyboardInterrupt("La fenetre a ete fermee violement!")
                return g.answer
        g = DialogTerminal(old_psw, sentence_memory, clair)
        return g.psw, g.sentence_memory, g.clair
