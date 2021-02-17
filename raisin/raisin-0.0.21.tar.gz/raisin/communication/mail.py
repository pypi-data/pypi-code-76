#!/usr/bin/env python3

import email.mime.base
import email.mime.multipart
import email.mime.text
import imaplib
import itertools
import os
import re
import smtplib
import socket
import time

import raisin
from ..tools import Printer


class Mail:
    """
    permet de gerer des envois et des reception de couriel
    """
    def __init__(self, address, psw):
        self.address = address  # c'est l'address couriel en question
        self.psw = psw          # c'est le mot de passe qui permet de se connecter a la boite mail
        self.name = "mailbox '%s'" % self.address
        assert re.fullmatch(r"[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]{2,}\.[a-z]{2,4}", self.address), "L'address '%s' n'est pas une address valide." % self.address

    def get_free_space(self, signature=None):
        """
        recupere l'espace disponible en octet
        """
        with Printer("Get free space of '%s'..." % self.name, signature=signature) as p:# on annonce que l'on va faire une operation risque
            ingoing_serv = self.get_ingoing_server(self.address)
            port = 993
            p.show("Connection a '%s' sur le port %d..." % (ingoing_serv, port))
            with imaplib.IMAP4_SSL(host=ingoing_serv, port=port) as imapserver:
                p.show("Autentification a '%s' avec le mdp: '%s'..." % (self.address, self.psw))
                imapserver.login(user=self.address, password=self.psw)
                with Printer("Finding main directory..."):
                    verification, dossiers = imapserver.list()
                    if verification != "OK":
                        raise imaplib.IMAP4.error("Impossible de recuperer le nom des dossiers dans %s." % self.name)
                    dossier = raisin.re.fullmatch(r"\(.*\)\s+\".*\"\s+(?P<dossier>.*)", dossiers[0].decode()).group("dossier")
                    p.show("It is '%s'." % dossier)
                with Printer("Getting quota..."):
                    quota = imapserver.getquotaroot(dossier)
                    p.show(str(quota))
                raise NotImplementedError

    def get_ingoing_server(self, addr, signature=None):
        """
        retourne le nom du serveur imap entran
        liee a l'address mail 'addr'
        """
        domain = addr.split("@")[1].lower()
        dico = {}
        return dico.get(domain, "imap.%s" % domain)

    def get_outgoing_server(self, addr, signature=None):
        """
        retourne le nom du serveur smtp sortant
        liee a l'address mail 'addr'
        """
        domain = addr.split("@")[1].lower()
        dico = {"att.net": "outbound.att.net",
                "bluewin.ch": "smtpauths.bluewin.ch",
                "club-internet.fr": "mail.club-internet.fr",
                "hotmail.com": "smtp.live.com",
                "outlook.com": "smtp.live.com",
                "sympatico.ca": "smtphm.sympatico.ca",
                "verizon.net": "outgoing.verizon.net",
                "yahoo.com": "mail.yahoo.com",
                "mailo.com": "mail.mailo.com"}
        return dico.get(domain, "smtp.%s" % domain)

    def send(self, address, subject, message, attachment=None, signature=None):
        """
        envoi un mail a l'address 'address'
        ce couriel a pour sujet 'subject', pour contenu 'message'
        et possiblement pour piece jointe 'attachment'
        """
        def generator_attachment(attachment):
            """
            cede au fur a meusure le binaire de chaque piece jointe
            lier a son nom
            """
            if attachment:
                if type(attachment) is bytes:
                    yield "attachement", attachment
                elif type(attachment) is str:
                    if os.path.isfile(attachment):
                        with open(attachment, "rb") as f:
                            yield os.path.basename(attachment), f.read()
                elif type(attachment) in (tuple, list, set):
                    for att in set(attachment):
                        for name, data in generator_attachment(att):
                            yield name, data
                else:
                    raise TypeError("la piece jointe n'est pas prise en charge")

        assert raisin.re.fullmatch(r"[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]{2,}\.[a-z]{2,4}", address), "l'address %s n'est pas une address valide" % address
        
        outgoing_serv = self.get_outgoing_server(self.address)                  # address du serveur sortant
        
        with Printer("sending a mail to '%s' from '%s'..." % (address, self.address), signature=signature) as p:
            
            # mise en forme du message
            msg = email.mime.multipart.MIMEMultipart()
            msg["From"] = self.address
            msg["To"] = address
            msg["Subject"] = subject
            msg.attach(email.mime.text.MIMEText(message.encode("utf-8"), "plain", "utf-8"))
            for name, data in generator_attachment(attachment):
                part = email.mime.base.MIMEBase("application", "octet-stream")
                part.set_payload(data)
                email.encoders.encode_base64(part)
                part.add_header("Content-Disposition", "piece; filename= %s" % name)
                msg.attach(part)

            # envoi du message
            for i, (port, SmtplibClass) in enumerate(zip((587, 465), (smtplib.SMTP, smtplib.SMTP_SSL))):
                p.show("connection a '%s' sur le port %d..." % (outgoing_serv, port))
                try:
                    with SmtplibClass(host=outgoing_serv, port=port, timeout=10) as smtpserver:# connexion au serveur sortant (en precisant son nom et son port)
                        # smtpserver.set_debuglevel(True)                       # permet d'afficher tout ce qui se passe en arriere plan
                        smtpserver.ehlo()                                       # on s'assure que la connection soit faite
                        if smtpserver.has_extn("STARTTLS"):                     # si on peu encripter la session
                            p.show("encriptage de la session via STARTTLS...")  # alors on le fait
                            smtpserver.starttls()                               # connection TLS
                            smtpserver.ehlo()                                   # on se reidentifi avec la connection cryptee
                        p.show("autentification a '%s' avec le mdp: '%s'..." % (self.address, self.psw))
                        smtpserver.login(self.address, self.psw)                # autentification
                        p.show("envoi du message...")
                        smtpserver.sendmail(self.address, address, msg.as_string().encode("utf-8"))
                        return None
                except smtplib.SMTPException as e:
                    if i == 0:
                        p.show("echec! deuxieme tentative:")
                    else:
                        raise e from e

    def __repr__(self):
        return self.name


def send(address, subject, message, attachment=None, signature=None):
    """
    tente par tout les moyen d'envoyer ce mail
    ne retourne rien tant que le mail n'est pas envoye
    """
    for server in itertools.cycle(raisin.communication.mail.servers):
        try:
            server.send(address, subject, message, attachment, signature)
            break
        except (smtplib.SMTPResponseException, smtplib.SMTPServerDisconnected, socket.timeout):
            continue
        except socket.gaierror:                                 # si il n'y a pas internet
            time.sleep(30)                                      # on fait une pause en attendant qu'il revienne


servers = [ Mail("raisin@ecomail.fr", "raisin"),
            Mail("raisin@mailo.com", "5uRYSIE670dZ"),           # vrai mot de passe: "raisin"
            Mail("raisin.raisin@aol.com", "rjqqktugnledijkv"),  # vrai mot de passe: "grapegrape"
            Mail("serveurpython.oz@gmail.com", "raisinraisin")]

