#!/usr/bin/env python

from PyPDF2.pdf import PdfFileReader

from pathlib import Path, PurePath
from zipfile import ZipFile, BadZipfile
from xml.etree import ElementTree

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate

import re
import smtplib
import socket
import logging

from declatravaux.configuration import Configuration


class TransmissionProcess:
    """
    Processus de transmission de la déclaration
    """

    XML_VERSION = "3.1"
    NAMESPACE_TELESERVICE = f"http://www.reseaux-et-canalisations.gouv.fr/schema-teleservice/{XML_VERSION}"
    NAMESPACE_INSEE = "http://xml.insee.fr/schema"

    def __init__(self, declaration, fake_emailing=False):
        self.cfg = Configuration()
        self.declaration = declaration
        self.declarationPath = Path(self.cfg['RepertoireDeclarations'], PurePath(self.declaration.fileName).stem)
        self.archiveDest = PurePath(
            self.cfg['RepertoireDeclarations'],
            'Archives',
            f'{PurePath(self.declaration.fileName).stem}-d{PurePath(self.declaration.fileName).suffix}',
        )
        self.fake_emailing = fake_emailing

        self.sent_emails = list()
        self.no_pdf = list()
        self.no_demat = list()

    def __iter__(self):

        try:
            yield 0, 'Extraction de l’archive', None
            self.extract_archive()

            yield 1, 'Identification des destinataires', None
            self.operators = self.get_operators()

            # Le troisième item renvoie le nombre de courriels à envoyer
            yield 2, 'Connexion au serveur SMTP', len([x for x
                                                       in self.operators
                                                       if x['demat_management']
                                                       and x['pdf_file']])
            self.connexion = self.get_connexion()

            i = 1
            for operator in self.operators:
                yield 3, 'Envoi des courriels', i
                if self.send_email(operator):
                    i = i + 1

            yield 4, 'Envoi du courriel récapitulatif', None
            self.send_recap_email()

            yield 5, 'Terminé', None

        except BadZipfile:
            self.undo_process()
            yield -1, 'L’archive ne contient pas les données attendues ou est corrompue.', None

        except XmlVersionError as error_msg:
            self.undo_process()
            logging.error(error_msg)
            yield -1, "Le schéma XML du fichier traité n’est pas celui attendu.\n" \
                      "Une mise à jour de DéclaTravaux est nécessaire.", None

        except socket.gaierror:
            self.undo_process()
            yield -1, 'Veuillez vérifier votre connexion Internet.', None

        except smtplib.SMTPAuthenticationError:
            self.undo_process()
            yield -1, 'Veuillez vérifier votre adresse électronique et votre mot de passe.', None

    def extract_archive(self):
        """
        Extrait l'archive obtenue après l'utilisation du téléservice dans le répertoire indiqué en paramètre.
        Retourne le chemin vers le dossier où l'archive a été extraite.
        """

        # Création d'un répertoire qui contiendra le contenu extrait de l'archive ;
        # ce répertoire a pour nom le numéro de la déclaration.
        destination = PurePath(self.cfg['RepertoireDeclarations'], PurePath(self.declaration.fileName).stem)

        # Si le répertoire existe déjà, on supprime son contenu préalablement
        try:
            Path(destination).mkdir(parents=True)

        except FileExistsError:
            for f in Path(destination).iterdir():
                f.unlink()
            Path(destination).mkdir(parents=True, exist_ok=True)

        # On extrait l'ensemble du contenu de l'archive
        # dans le répertoire venant d'être créé.
        archive = ZipFile(self.declaration.filePath)
        archive.extractall(destination)
        archive.close()

        # L'archive principale contient elle-même une archive
        # On extrait donc cette sous-archive et on supprime le fichier .zip correspondant

        sub_archive_path = PurePath(destination, PurePath(self.declaration.fileName).stem + '_description.zip')

        sub_archive = ZipFile(sub_archive_path)
        sub_archive.extractall(destination)
        sub_archive.close()
        Path(sub_archive_path).unlink()

        # L'archive est déplacée dans le dossier « Archives » du répertoire des déclarations
        if not Path(self.cfg['RepertoireDeclarations'], 'Archives').exists():
            Path(self.cfg['RepertoireDeclarations'], 'Archives').mkdir()

        Path(self.declaration.filePath).rename(self.archiveDest)

        return True

    def get_operators(self):
        """
        Retourne la liste des destinataires définis dans le fichier ***_description.xml,
        dont le chemin est indiqué en paramètre
        """

        # On récupère le dictionnaire associant le nom de l'exploitant et son fichier PDF
        pdf_list = self.associate_pdf()

        # On reconstitue le chemin du fichier « *_description.xml »
        xml_file_path = Path(self.declarationPath, PurePath(self.declaration.fileName).stem + '_description.xml')

        # On parse le fichier XML et on se place à la racine
        xml_file = ElementTree.parse(xml_file_path)
        root = xml_file.getroot()

        # Vérification de la version du schéma XML
        # Si la version du fichier ne correspond pas à la version attendue, une exception est levée
        scheme_version = root.tag.split('}')[0].split('/')[-1]
        if scheme_version != self.XML_VERSION:
            raise XmlVersionError(f"La version du schéma XML de la déclaration en cours de "
                                  f"traitement est {scheme_version}, alors que la version "
                                  f"attendue est {self.XML_VERSION}")

        # On indique le namespace utilisé dans le fichier XML
        ns = {'t': self.NAMESPACE_TELESERVICE,
              'ie': self.NAMESPACE_INSEE}

        # On crée la liste des destinataires, qui contient l'ensemble des destinataires
        # indiqués dans le fichier XML sous la forme de dictionnaires,
        # qui contiennent un certain nombre d'informations.
        operators = list()

        # On alimente la liste des destinataires.
        for tag in root.findall('t:listeDesOuvrages/t:ouvrage', ns):

            ouvrage = tag.findtext('t:classeOuvrage', '', ns).replace('_', ' ')

            last_name = tag.findtext('t:listeDesZones/t:zone/t:contact/t:nom/ie:NomFamille', '', ns)
            first_name = tag.findtext('t:listeDesZones/t:zone/t:contact/t:prenom/ie:Prenom', '', ns)
            company = tag.findtext('t:listeDesZones/t:zone/t:contact/t:societe', '', ns)
            agency = tag.findtext('t:listeDesZones/t:zone/t:contact/t:agence', '', ns)
            complement = tag.findtext('t:listeDesZones/t:zone/t:contact/t:complement', '', ns)
            numero = tag.findtext('t:listeDesZones/t:zone/t:contact/t:numero', '', ns)
            street = tag.findtext('t:listeDesZones/t:zone/t:contact/t:voie', '', ns)
            postbox = tag.findtext('t:listeDesZones/t:zone/t:contact/t:lieuDitBP', '', ns)
            postcode = tag.findtext('t:listeDesZones/t:zone/t:contact/t:codePostal', '', ns)
            locality = tag.findtext('t:listeDesZones/t:zone/t:contact/t:commune', '', ns)
            country_code = tag.findtext('t:listeDesZones/t:zone/t:contact/t:codePays', '', ns)

            # L'adresse email peut se trouver sous mailObligatoire ou faxObligatoire
            email = tag.findtext('t:listeDesZones/t:zone/t:contact/t:courriel', '', ns)
            phone_number = tag.findtext('t:listeDesZones/t:zone/t:contact/t:telephone', '', ns)
            fax_number = tag.findtext('t:listeDesZones/t:zone/t:contact/t:fax', '', ns)
            emergency_email = tag.findtext('t:listeDesZones/t:zone/t:contact/t:mailUrgence', '', ns)
            emergency_phone_number = tag.findtext('t:listeDesZones/t:zone/t:contact/t:telephoneUrgence', '', ns)
            emergency_fax_number = tag.findtext('t:listeDesZones/t:zone/t:contact/t:faxUrgence', '', ns)
            dommage_phone_number = tag.findtext('t:listeDesZones/t:zone/t:contact/t:telEndommagement', '', ns)
            demat_management = tag.findtext(
                't:listeDesZones/t:zone/t:contact/t:gestionDesFichiersDematerialises/t:gereLesFichiersDematerialises',
                '', ns)
            demat_management = True if demat_management == 'true' else False
            demat_file_format = tag.findtext(
                't:listeDesZones/t:zone/t:contact/t:gestionDesFichiersDematerialises/t:formatDesFichiersDematerialises',
                '', ns)

            # On associe le destinataire au fichier PDF qui lui correspond.
            pdf_file = [f for f, oDict in pdf_list.items() if oDict['Name'] == company and (
                    oDict['Destinator'] == company or
                    oDict['Destinator'] == ' '.join((agency, last_name)).strip()
            )]

            # pdf_file reprend le nom du pdf associé
            # ou se voit affecté de la valeur « False » si aucun PDF n'est trouvé
            if pdf_file:
                pdf_file = pdf_file[0]
            else:
                pdf_file = False

            # On ajoute un dictionnaire à la liste avec l'ensemble des informations récupérées.
            operators.append({'ouvrage': ouvrage, 'company': company, 'agency': agency,
                              'numero': numero, 'street': street, 'postcode': postcode,
                              'locality': locality, 'country_code': country_code,
                              'email': email, 'phone_number': phone_number, 'faxNumber': fax_number,
                              'emergency_email': emergency_email,
                              'emergency_phone_number': emergency_phone_number,
                              'emergency_fax_number': emergency_fax_number,
                              'dommage_phone_number': dommage_phone_number,
                              'demat_management': demat_management,
                              'demat_file_format': demat_file_format,
                              'pdf_file': pdf_file
                              })

        return operators

    def associate_pdf(self):
        """
        Retourne un dictionnaire associant le nom des fichiers PDF
        au nom des exploitants concernés.

        La fonction est relativement lourde dès lors qu'elle s'appuie sur la bibliothèque PyPDF2.
        """

        pdf_file_regex = re.compile(r'[0-9]{13}[A-Z]([0-9][0-9])?_(.)*_[0-9]{1,2}.pdf')
        # La liste est filtrée pour ne conserver que les formulaires PDF
        files_list = [str(f.resolve()) for f in self.declarationPath.iterdir() if pdf_file_regex.match(f.name)]
        # La liste est triée par ordre croissant
        files_list.sort()

        # Un dictionnaire est créé sous la avec la structure suivante :
        # - clé = nom du fichier PDF ;
        # - valeur = nom de l'exploitant.

        pdf_dict = dict()

        for f in files_list:
            field = PdfFileReader(f).getFields()
            pdf_dict[f] = dict()
            pdf_dict[f]['Name'] = field['Exploitant']['/V'].strip()
            pdf_dict[f]['Destinator'] = field['Destinataire']['/V'].strip()

        return pdf_dict

    def get_connexion(self):
        """
        Renvoie une connexion au serveur SMTP
        """
        connexion = smtplib.SMTP_SSL(self.cfg['ServeurSMTP'], self.cfg['PortServeurSMTP'])
        connexion.login(self.cfg['AdresseElectronique'], self.cfg.password)

        return connexion

    def send_email(self, operator):
        """
        Envoi par courriel des fichiers nécessaires aux différents destinataires identifiés.

        Les fichiers envoyés par courriel dépendent du niveau de dématérialisation du destinataire :
        - pas de dématérialisation : aucun courriel n'est envoyé ;
        - dématérialisation XML et PDF : envoi des fichiers « *_description.xml »,
          « *_emprise.pdf » et « *_ZZZZ_*.pdf » ;
        - dématérialisation XML : envoi du fichier « *_description.xml ».
        """

        sent = False

        # Un courriel n'est envoyé que si le destinataire gère les fichiers dématérialisés
        # et si un fichier PDF a bien été identifié
        if not operator['pdf_file']:

            self.no_pdf.append({'ouvrage': operator['ouvrage'],
                                'company': operator['company'],
                                'demat_management': operator['demat_management'],
                                'demat_file_format': operator['demat_file_format'],
                                'email': operator['email'],
                                'files': [],
                                })

        elif not operator['demat_management']:

            self.no_demat.append({'ouvrage': operator['ouvrage'],
                                  'company': operator['company'],
                                  'demat_management': operator['demat_management'],
                                  'demat_file_format': operator['demat_file_format'],
                                  'email': operator['email'],
                                  'files': [operator['pdf_file'],
                                            self.cfg['RepertoireDeclarations'] + '/' + PurePath(
                                                self.declaration.fileName).stem + '/'
                                            + PurePath(self.declaration.fileName).stem + '_emprise.pdf', ],
                                  })

        elif operator['demat_management']:

            # Le courriel envoyé contient un message, à la fois en version HTML et version texte, ainsi que des
            # pièces jointes.
            #
            # Un tel courriel doit avoir la structure suivante :
            #   - Courriel (multipart/mixed)
            #       - Message (multipart/alternative)
            #           - Version texte du message (text/plain)
            #           - Version HTML du message (text/html)
            #       - Pièce jointe n° 1 (application/***)
            #       - ...
            #       - Pièce jointe n° n (application/***)

            # CRÉATION DE L'EN-TÊTE DU COURRIEL

            email = MIMEMultipart('mixed')

            email['From'] = self.cfg['AdresseElectronique']
            email['To'] = operator['email']
            email['Subject'] = 'Notification d’une déclaration de travaux'
            email['Date'] = formatdate(localtime=True)
            email['Charset'] = 'UTF-8'

            # CRÉATION DU MESSAGE (VERSION TEXTE ET VERSION HTML)

            message_part = MIMEMultipart('alternative')

            text_subpart = """
                           Madame, Monsieur,\n
                           Veuillez trouver ci-joint les éléments
                           relatifs à une déclaration de travaux.\n
                           Meilleures salutations,\n
                           """ + self.cfg['NomExpediteur']

            html_subpart = """
                           <html>
                               <head></head>
                               <body>
                                   <p>Madame, Monsieur,</p>
                                   <p>
                                       Veuillez trouver ci-joint les éléments
                                       relatifs à une déclaration de travaux.
                                   </p>
                                   <p>Meilleures salutations,</p>
                                   <p>""" + self.cfg['NomExpediteur'] + """</p>
                               </body>
                           </html>
                           """

            # Attribution du type MIME correspondant à chaque version
            text_subpart = MIMEText(text_subpart, 'plain')
            html_subpart = MIMEText(html_subpart, 'html')

            # Leux deux versions sont intégrées au conteneur « message_part »
            message_part.attach(text_subpart)
            message_part.attach(html_subpart)

            # Le conteneur « message_part » est lui-même intégré au conteneur principal « email »
            email.attach(message_part)

            # AJOUT DES PIÈCES JOINTES

            # Les pièces jointes sont listées dans la variable « attachments »

            # Quelque soit le niveau de dématérialisation, le fichier *_description.xml est envoyé
            attachments = [self.cfg['RepertoireDeclarations'] + '/' + PurePath(self.declaration.fileName).stem + '/'
                           + PurePath(self.declaration.fileName).stem + '_description.xml', ]

            # Si la dématérialisation est de type XML / PDF,
            # il faut ajouter les fichiers *_emprise.pdf et *_ZZZZ_*.pdf
            if operator['demat_file_format'] == 'XML_PDF':
                # Fichier *_emprise.pdf
                attachments.append(
                    self.cfg['RepertoireDeclarations'] + '/' + PurePath(self.declaration.fileName).stem + '/'
                    + PurePath(self.declaration.fileName).stem + '_emprise.pdf')
                # Fichier *_ZZZZ_*.pdf
                attachments.append(operator['pdf_file'])

            # Chaque fichier contenu dans la variable « attachments »
            # est intégré au conteneur principal « mail » en tant que pièce jointe.
            for f in attachments:
                attachment = open(f, 'rb')

                attachment_part = MIMEBase('application', 'octet-stream')
                attachment_part.set_payload(attachment.read())
                encoders.encode_base64(attachment_part)
                attachment_part.add_header('Content-Disposition', f'attachment; filename="{Path(f).name}"')

                email.attach(attachment_part)

            # Envoi du courriel
            email = email.as_string()
            if not self.fake_emailing:
                self.connexion.sendmail(self.cfg['AdresseElectronique'], operator['email'], email)

            # Liste récapitulative des courriels envoyés
            self.sent_emails.append({'ouvrage': operator['ouvrage'],
                                     'company': operator['company'],
                                     'demat_management': operator['demat_management'],
                                     'demat_file_format': operator['demat_file_format'],
                                     'email': operator['email'],
                                     'files': attachments
                                     })
            sent = True

        return sent

    def send_recap_email(self):
        """
        Envoie un courriel récapitulatif à l'adresse électronique de l'expéditeur.
        """

        # Le courriel envoyé contient un message, à la fois en version HTML et version texte.
        # Il n'y a pas de pièce jointe.
        #
        # Un tel courriel doit avoir la structure suivante :
        #   - Courriel (multipart/alternative)
        #       - Version texte du message (text/plain)
        #       - Version HTML du message (text/html)

        # CRÉATION DE L'EN-TÊTE DU COURRIEL

        email = MIMEMultipart('alternative')

        email['From'] = self.cfg['AdresseElectronique']
        email['To'] = self.cfg['AdresseElectronique']
        email['Subject'] = 'Récapitulatif de la transmission électronique de la déclaration de travaux'
        email['Date'] = formatdate(localtime=True)
        email['Charset'] = 'UTF-8'

        # CRÉATION DU MESSAGE (VERSION TEXTE ET VERSION HTML)

        # Tableau des fichiers envoyés
        text_table_sent = ''
        html_table_sent = ''
        html_table_sent += '<table style="border-collapse: separate; border-spacing: 0px 5px; margin: auto; ' \
                           'font-size: small;"> '
        html_table_sent += '<tr><th>Destinataire</th><th>Courriel</th><th>Fichiers envoyés</th></tr>'

        for entry in self.sent_emails:
            text_table_sent += f'| {entry["company"]} | {entry["email"]} | '
            html_table_sent += f'<tr><td style="border-top: 1px solid black; border-bottom: 1px solid black; ' \
                               f'padding: 4px 8px;">'
            html_table_sent += f'<class style="font-weight: bold">{entry["company"]}</class><br />'
            html_table_sent += f'{entry["ouvrage"]}</td>'
            html_table_sent += f'<td style="border-top: 1px solid black; border-bottom: 1px solid black; ' \
                               f'padding: 4px 8px;"> '
            html_table_sent += f'{entry["email"]}</td>'
            html_table_sent += f'<td style="border-top: 1px solid black; border-bottom: 1px solid black; ' \
                               f'padding: 4px 8px;"> '

            for f in entry['files']:
                text_table_sent += f'{Path(f).name} '
                html_table_sent += f'{Path(f).name}<br />'

            text_table_sent += ' |\n'
            html_table_sent += '</td></tr>'

        html_table_sent += '</table>'

        # Tableau des fichiers non envoyés
        text_table_unsent = ''
        html_table_unsent = ''
        html_table_unsent += '<table style="border-collapse: separate; border-spacing: 0px 5px; margin: auto; ' \
                             f'font-size: small;">'
        html_table_unsent += '<tr><th>Destinataire</th><th>Motif</th><th>Courriel</th><th>Fichiers à envoyer</th></tr>'

        unsent_emails = self.no_demat + self.no_pdf

        for entry in unsent_emails:
            text_table_unsent += f'| {entry["company"]} | {entry["email"]} | '
            html_table_unsent += f'<tr><td style="border-top: 1px solid black; border-bottom: 1px solid black; ' \
                                 f'padding: 4px 8px;">'
            html_table_unsent += f'<class style="font-weight: bold">{entry["company"]}</class><br />'
            html_table_unsent += f'{entry["ouvrage"]}</td>'
            html_table_unsent += f'<td style="border-top: 1px solid black; border-bottom: 1px solid black; ' \
                                 f'padding: 4px 8px;">'

            if not entry['files']:
                html_table_unsent += 'Aucun fichier PDF trouvé</td>'
            elif not entry['demat_management']:
                html_table_unsent += 'À envoyer au format papier</td>'

            html_table_unsent += f'<td style="border-top: 1px solid black; border-bottom: 1px solid black; ' \
                                 f'padding: 4px 8px;">'
            html_table_unsent += f'{entry["email"]}</td>'
            html_table_unsent += f'<td style="border-top: 1px solid black; border-bottom: 1px solid black; ' \
                                 f'padding: 4px 8px;">'

            for f in entry['files']:
                text_table_unsent += f'{Path(f).name} '
                html_table_unsent += f'{Path(f).name}<br />'

            text_table_unsent += ' |\n'
            html_table_unsent += '</td></tr>'

        html_table_unsent += '</table>'

        # Assemblage des tableaux
        text_part = ''
        text_part += 'Voici le récapitulatif de transmission de la déclaration :\n\n'
        text_part += self.declaration.name + '\n\n'
        text_part += text_table_unsent

        html_part = f'''
                    <html>
                        <head></head>
                        <body>
                            <p>Voici le récapitulatif de transmission de la déclaration :</p>
                            <p style="text-align: center; font-weight: bold;">
                                {self.declaration.name}
                            </p>
                            {html_table_sent}
                            '''

        if unsent_emails:
            html_part += f'<p style="text-align: center;">Attention : ' \
                         f'les fichiers suivants n\'ont pas pu être transmis :</p>' \
                         f'{html_table_unsent}'

        html_part += f'</body></html>'

        # Attribution du type MIME correspondant à chaque version
        text_part = MIMEText(text_part, 'plain')
        html_part = MIMEText(html_part, 'html')

        # Leux deux versions sont intégrées au courriel
        email.attach(text_part)
        email.attach(html_part)

        # Envoi du courriel
        email = email.as_string()
        if not self.fake_emailing:
            self.connexion.sendmail(self.cfg['AdresseElectronique'], self.cfg['AdresseElectronique'], email)

    def undo_process(self):
        """
        Annule les déplacements de fichiers réalisés
        """

        # Le cas échéant, l'archive est rétablie dans son dossier initial
        if Path(self.archiveDest).exists():
            Path(self.archiveDest).rename(self.declaration.filePath)

        # Le cas échéant, le dossier de travail correspondant à la déclaration en cours est vidé puis supprimé
        if Path(self.declarationPath).exists():
            for f in Path(self.declarationPath).iterdir():
                Path(f).unlink()

            Path(self.declarationPath).rmdir()


class XmlVersionError(Exception):
    """Lancée lorsque la version du schéma XML ne correspond pas à la version attendue"""
