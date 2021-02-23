#!/usr/bin/env python

from pathlib import Path

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from declatravaux import __version__
from declatravaux.archives import Archives, Declaration
from declatravaux.configuration import Configuration
from declatravaux.ui_main_window import Ui_Main_Window
from declatravaux import images_rc
from declatravaux.workers import TransmissionWorker, ProgressWorker


class MainWindow(QMainWindow, Ui_Main_Window):

    declaration_signal = QtCore.pyqtSignal(Declaration, bool)

    def __init__(self, parent=None, fake_emailing=False):
        super().__init__(parent)
        self.setupUi(self)

        # Chargement du fichier de configuration
        self.cfg = Configuration()

        # Initialisation de variables
        self.archives_list = []
        self.declaration = None
        self.fake_emailing = fake_emailing
        self.mails_count = 0

        # Affichage de la version
        self.labelVersion.setText(f'version {__version__}')

        # Masquage de la fenêtre « À Propos »
        fix_about = self.textBrowserAbout.sizePolicy()
        fix_about.setRetainSizeWhenHidden(True)
        self.textBrowserAbout.setSizePolicy(fix_about)
        self.textBrowserAbout.setProperty('visible', False)

        # Masquage du bouton « Précédent » au démarrage
        self.pushButtonPrevious.setProperty('visible', False)

        # Remplissage du formulaire « Paramètres »
        self.fill_parameters()

        # Ajout d'un validator sur lineEditFileSelection
        validator = QtGui.QRegExpValidator(
            QtCore.QRegExp('(.:)?.*/[0-9]{13}[A-Z]{1}([0-9][0-9])?_(DT|DICT|DDC|ATU).zip'), self.lineEditFile)
        self.lineEditFile.setValidator(validator)

        # Masquage de la ligne d'erreur
        fix_file_error = self.labelFileError.sizePolicy()
        fix_file_error.setRetainSizeWhenHidden(True)
        self.labelFileError.setSizePolicy(fix_file_error)
        self.labelFileError.setProperty('visible', False)

        # S'il s'agit du premier lancement du logiciel,
        # le bouton « Démarrer » est désactivé
        if int(self.cfg['PremierLancement']):
            self.pushButtonNext.setEnabled(False)

        # Initialisation des threads
        self.tr_worker = TransmissionWorker()
        self.tr_thread = QtCore.QThread()
        self.declaration_signal.connect(self.tr_worker.run)
        self.tr_worker.step_signal.connect(self.tr_progress)
        self.tr_worker.moveToThread(self.tr_thread)

        self.pr_worker = ProgressWorker()
        self.pr_thread = QtCore.QThread()
        self.pr_thread.started.connect(self.pr_worker.run)
        self.pr_worker.progress_signal.connect(self.pr_progress)
        self.pr_worker.moveToThread(self.pr_thread)

        # Initialisation de la barre de progression
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(5)

        # Initialisation des icones de fin
        self.icon_checked = QtGui.QPixmap(":/images/checked.svg")
        self.icon_error = QtGui.QPixmap(":/images/cancel.svg")

        # Connexion des signaux des widgets vers les slots
        self.pushButtonAbout.toggled.connect(self.toggle_about)

        self.pushButtonQuit.clicked.connect(self.close)
        self.pushButtonParameters.clicked.connect(self.show_parameters)
        self.pushButtonPrevious.clicked.connect(self.go_previous)
        self.pushButtonNext.clicked.connect(self.go_next)

        self.pushButtonSearchDir.clicked.connect(self.browse_parameters)
        self.pushButtonWorkDir.clicked.connect(self.browse_parameters)
        self.pushButtonParamCancel.clicked.connect(self.quit_parameters)
        self.pushButtonParamValidate.clicked.connect(self.quit_parameters)

        self.pushButtonBrowse.clicked.connect(self.browse)
        self.lineEditFile.textEdited.connect(self.check_file_format)
        self.listWidget.itemSelectionChanged.connect(lambda: self.activate_button_next(True))

    # Méthode assignant les icônes
    def set_win_icon(self, push_button, icon_name):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f':/icons/icons/{icon_name}.svg'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        push_button.setIcon(icon)

    # Méthode affichant la page suivante
    def go_next(self):

        current_page = self.stackedWidget.currentWidget()

        # Si la page actuelle est la page d'accueil
        # On lance la recherche d'archives
        # La page suivante dépend du résultat de la recherche
        if current_page is self.pageStart:

            archives = Archives()
            self.archives_list = archives.search(self.cfg['RepertoireRecherche'])

            # S'il n'y a aucune archive trouvée,
            # la page suivante est pageFileSelection
            if len(self.archives_list) == 0:
                self.pushButtonNext.setEnabled(False)
                self.lineEditFile.setText('')
                self.stackedWidget.setCurrentWidget(self.pageFileSelection)

            # Si une seule archive est trouvée,
            # la page suivante est pageConfirmation
            elif len(self.archives_list) == 1:
                self.declaration = self.archives_list[0]
                self.set_label_confirmation(self.declaration.dType, self.declaration.numero, self.declaration.date)
                self.stackedWidget.setCurrentWidget(self.pageConfirmation)

            # Si plusieurs archives sont trouvées,
            # le widget Liste est rempli
            # la page suivante est pageArchiveChoose
            else:

                # La liste est remplie selon les archives trouvées
                self.listWidget.clear()

                for declaration in self.archives_list:
                    self.listWidget.addItem(declaration.name)

                self.pushButtonNext.setEnabled(False)
                self.stackedWidget.setCurrentWidget(self.pageArchiveChoose)

            # Dans tous les cas, on masque le bouton « Paramètres »,
            # on affiche le bouton « Précédent »
            # et le bouton « Démarrer » est modifié en « Suivant »
            self.pushButtonParameters.setProperty('visible', False)
            self.pushButtonPrevious.setProperty('visible', True)
            self.pushButtonNext.setText('Suivant')

        elif current_page in (self.pageFileSelection, self.pageArchiveChoose):

            # Si la page actuelle est pageFileSelection,
            # la page suivante est pageConfirmation
            if current_page is self.pageFileSelection:
                if self.lineEditFile.hasAcceptableInput():
                    self.declaration = Declaration(self.lineEditFile.text())
                    self.stackedWidget.setCurrentWidget(self.pageConfirmation)
                else:
                    return 0

            # Si la page actuelle est pageArchiveChoose
            # la page suivante est pageConfirmation
            elif current_page is self.pageArchiveChoose:
                self.declaration = self.archives_list[self.listWidget.currentRow()]
                self.stackedWidget.setCurrentWidget(self.pageConfirmation)

            self.set_label_confirmation(self.declaration.dType, self.declaration.numero, self.declaration.date)

        # Si la page actuelle est pageConfirmation,
        # la page suivante est pageProgress
        elif current_page is self.pageConfirmation:
            self.stackedWidget.setCurrentWidget(self.pageProgress)

            # Les différents boutons sont masqués
            self.pushButtonQuit.setProperty('visible', False)
            self.pushButtonPrevious.setProperty('visible', False)
            self.pushButtonNext.setProperty('visible', False)

            # Lancement des threads
            self.tr_thread.start()
            self.declaration_to_thread(self.declaration, self.fake_emailing)
            self.pr_thread.start()

        elif current_page is self.pageProgress:
            self.stackedWidget.setCurrentWidget(self.pageEnd)
            self.pushButtonQuit.setProperty('visible', True)
            self.pushButtonNext.setProperty('visible', True)

        # Si la page actuelle est pageEnd,
        # la page d'accueil est affichée
        elif current_page is self.pageEnd:
            self.stackedWidget.setCurrentWidget(self.pageStart)
            self.pushButtonNext.setText('Démarrer')
            icon = QtGui.QIcon.fromTheme('go-next')
            self.pushButtonNext.setIcon(icon)
            self.pushButtonParameters.setProperty('visible', True)

        else:
            self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() + 1) % self.stackedWidget.count())

    #  Méthode affichant la page précédente
    def go_previous(self):

        current_page = self.stackedWidget.currentWidget()

        # Si la page actuelle est pageSelection ou pageArchiveChoose,
        # la page précédente est pageStart
        if current_page in (self.pageFileSelection, self.pageArchiveChoose):

            self.stackedWidget.setCurrentWidget(self.pageStart)
            self.pushButtonNext.setEnabled(True)
            self.lineEditFile.setText('')
            self.listWidget.clear()

            # Masquage bouton Précédent / Affichage bouton Paramètres
            # Bouton Suivant renommé en Démarrer
            self.pushButtonPrevious.setProperty('visible', False)
            self.pushButtonParameters.setProperty('visible', True)
            self.pushButtonNext.setText('Démarrer')

        # Si la page actuelle est pageConfirmation,
        # la page précédente dépend du nombre d'archives qui avaient été trouvées
        elif current_page is self.pageConfirmation:
            pages = {0: self.pageFileSelection, 1: self.pageStart, 2: self.pageArchiveChoose}
            self.stackedWidget.setCurrentWidget(pages.get(len(self.archives_list), self.pageArchiveChoose))

            if len(self.archives_list) == 1:
                self.pushButtonPrevious.setProperty('visible', False)
                self.pushButtonParameters.setProperty('visible', True)

        else:
            self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() - 1) % self.stackedWidget.count())

    # Affichage des paramètres
    def show_parameters(self):
        self.stackedWidget.setCurrentWidget(self.pageParameters)
        self.stackedWidgetButtons.setCurrentWidget(self.stackedWidgetButtonsParameters)

    # Validation ou annulation des paramètres
    def quit_parameters(self):

        # Si le bouton Valider est appelé,
        # on enregistre les paramètres
        if self.sender().objectName() == 'pushButtonParamValidate':

            self.cfg.parameters = {'RepertoireRecherche': self.lineEditSearchDir.text(),
                                   'RepertoireDeclarations': self.lineEditWorkDir.text(),
                                   'AdresseElectronique': self.lineEditMail.text(),
                                   'ServeurSMTP': self.lineEditSmtpServer.text(),
                                   'PortServeurSMTP': self.lineEditSmtpPort.text(),
                                   'NomExpediteur': self.lineEditExpeditorName.text(),
                                   }
            self.cfg.password = self.lineEditPassword.text()

            self.pushButtonNext.setEnabled(True)

        # Si le bouton Annuler est appelé,
        # les anciens paramètres sont restaurés dans le formulaire
        else:
            self.fill_parameters()

        self.stackedWidget.setCurrentWidget(self.pageStart)
        self.stackedWidgetButtons.setCurrentWidget(self.stackedWidgetButtonsDefault)

    def toggle_about(self):
        state = self.textBrowserAbout.property('visible')
        self.textBrowserAbout.setProperty('visible', not state)

    def browse(self):
        # noinspection PyTypeChecker,PyCallByClass
        (fileUrl, f) = QFileDialog.getOpenFileName(self, 'Choisir une archive', '~/',
                                                   'Archives (*.zip);;Tous les fichiers (*)')
        if fileUrl:
            self.lineEditFile.setText(fileUrl)
            self.check_file_format()

    def browse_parameters(self):
        # noinspection PyTypeChecker,PyCallByClass
        directory_url = QFileDialog.getExistingDirectory(self, 'Choisir un répertoire', str(Path().home()),
                                                         QFileDialog.ShowDirsOnly)
        if directory_url:
            if self.sender().objectName() == 'pushButtonSearchDir':
                self.lineEditSearchDir.setText(directory_url)
            else:
                self.lineEditWorkDir.setText(directory_url)

    def activate_button_next(self, boolean):
        self.pushButtonNext.setEnabled(boolean)

    def check_file_format(self):
        if not self.lineEditFile.hasAcceptableInput() or not Path(self.lineEditFile.text()).exists():
            self.lineEditFile.setStyleSheet('color: rgb(226,87,76);')
            self.labelFileError.setProperty('visible', True)
            self.activate_button_next(False)

            if not self.lineEditFile.hasAcceptableInput():
                self.labelFileError.setText('Le format de l’archive sélectionnée est incorrect.')
            else:
                self.labelFileError.setText('Le fichier indiqué n’existe pas.')

        else:
            self.lineEditFile.setStyleSheet('')
            self.labelFileError.setProperty('visible', False)
            self.activate_button_next(True)

    def fill_parameters(self):
        self.lineEditSearchDir.setText(self.cfg['RepertoireRecherche'])
        self.lineEditWorkDir.setText(self.cfg['RepertoireDeclarations'])
        self.lineEditMail.setText(self.cfg['AdresseElectronique'])
        self.lineEditPassword.setText(self.cfg.password)
        self.lineEditSmtpServer.setText(self.cfg['ServeurSMTP'])
        self.lineEditSmtpPort.setText(self.cfg['PortServeurSMTP'])
        self.lineEditExpeditorName.setText(self.cfg['NomExpediteur'])

    def set_label_confirmation(self, dType, numero, date):

        det = 'L’' if dType == 'ATU' else 'La '

        self.labelConfirmation.setText(f"""
                    <style>
                    p {{margin: 15px; line-height: 125%; font-size: 14pt; text-align: center}};
                    b {{white-space: nowrap;}}
                    </style>
                    <p>
                        {det}<b>{dType}</b> n<span style="vertical-align: super;">o</span>
                        <b>{numero}</b> du <b>{date.replace(' ', '&nbsp;')}</b> a été sélectionnée.
                    </p>
                    <p>
                        Souhaitez-vous procéder à sa télétransmission ?
                    </p>""")

    def tr_progress(self, step_num, step_text, step_add):

        if step_num in range(0, 5):
            # L'étape 2 contient le nombre de courriels à envoyer en 3e item
            if step_num == 2:
                self.mails_count = step_add

            # Pour l'étape 4, le label comprend l'information sur le nombre de courriels envoyés
            if step_num == 3:
                self.labelStep.setText(f'{step_text} ({step_add} sur {self.mails_count})')

            # Pour toutes les autres étapes, le label reprend uniquement "step_text"
            else:
                self.labelStep.setText(f'{step_text}')

            # Dans tous les cas, on incrémente la barre de progression
            self.progressBar.setValue(step_num)

        # Une fois le traitement terminé,
        # la dernière page est affichée
        else:
            if step_num == -1:
                self.labelEndIcon.setPixmap(self.icon_error)
                self.labelEnd1.setText('La déclaration n’a pas été télétransmise.')
                self.labelEnd1.setStyleSheet('color: rgb(226,87,76);')
                self.labelEnd2.setText(step_text)
                self.labelEnd2.setStyleSheet('color: rgb(226,87,76);')
                self.pushButtonNext.setText('Réessayer')
                icon = QtGui.QIcon.fromTheme('edit-redo')

            else:
                self.labelEndIcon.setPixmap(self.icon_checked)
                self.labelEnd1.setText('La déclaration a été télétransmise.')
                self.labelEnd1.setStyleSheet('color: rgb(61, 179, 158);')
                self.labelEnd2.setText(f'Un courriel récapitulatif a été envoyé à {self.cfg["AdresseElectronique"]}.')
                self.labelEnd2.setStyleSheet('color: rgb(61, 179, 158);')
                self.pushButtonNext.setText('Nouvelle déclaration')
                icon = QtGui.QIcon.fromTheme('document-new')

            self.pushButtonNext.setIcon(icon)
            self.go_next()

    def pr_progress(self):
        if self.labelStep.text()[-3:] == '...':
            self.labelStep.setText(self.labelStep.text()[:-3])
        else:
            self.labelStep.setText(self.labelStep.text() + '.')

    @QtCore.pyqtSlot(Declaration, bool)
    def declaration_to_thread(self, declaration, fake_emailing):
        self.declaration_signal.emit(declaration, fake_emailing)
