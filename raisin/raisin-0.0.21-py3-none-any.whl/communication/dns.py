#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Associ un "nom de dommaine" raisin, a
un vrai nom de dommaine ou a une ip et un port.
"""
import ipaddress
import os
import socket

from ..tools import Printer

def get(rais_domain, signature):
    """
    Si le nom de domain est un nom de domaine recence par raisin.
    Les informations permettant de se connecter a ce serveur sont retourne.
    Sinon retourne None.
    L'objet retourne ressemble a ca:
        {
        "ipv4_wan": "37.45.168.54",
        "ipv4_lan": "192.168.1.24",
        "ipv6": "2a01:cb15:829b:c600:4ca7:56b3:fd1e:1719",
        "dns_ipv4": "machin_chose.ddns.net",
        "dns_ipv6": None,
        "port": 16395,
        "port_forwarding": None,
        "last_check": 1602927982.9591131,
        }
    """
    assert type(rais_domain) is str, "Le nom de domaine doit etre une chaine de caractere. Pas %s." % type(rais_domain)
    with raisin.Printer("Recherche du domain %s..." % rais_domain, signature=signature) as p:
        filename = os.path.join(os.path.expanduser("~"), "dns.py")
        if not os.path.exists(filename): # si le fichier n'existe pas
            p.show("File not found.")
            return None
        with open(filename, "r", encoding="utf-8") as f:
            dico = eval(f.read()) # c'est vraiment moche cette ligne niveau complexite!
        if rais_domain not in dico:
            p.show("Domain not present in the database.")
            return None
        infos = dico[rais_domain]
        p.show("Trouve: %s" % repr(infos))
        return infos

def is_ipv4(addr):
    """
    |===========================|
    | Verification format ipv4. |
    |===========================|

    entree
    ------
    :param addr: Adresse dont ou shouaite avoir des informations.
    :type addr: str

    sortie
    ------
    :return: Retourne True si il s'agit d'une adresse ipv4. False sinon.
    :rtype: boolean
    """
    assert isinstance(addr, str), \
        ("Pour ce test, l'ip doit etre une chaine "
        "de caractere, pas %s." % type(addr).__name__)
    try:
        ipaddress.IPv4Address(addr)
        return True
    except ipaddress.AddressValueError:
        return False

def is_ipv6(addr):
    """
    |===========================|
    | Verification format ipv6. |
    |===========================|

    entree
    ------
    :param addr: Adresse dont ou shouaite avoir des informations.
    :type addr: str

    sortie
    ------
    :return: Retourne True si il s'agit d'une adresse ipv6. False sinon.
    :rtype: boolean
    """
    assert isinstance(addr, str), \
        ("Pour ce test, l'ip doit etre une chaine "
        "de caractere, pas %s." % type(addr).__name__)
    try:
        ipaddress.IPv6Address(addr)
        return True
    except ipaddress.AddressValueError:
        return False

def is_domain(domain):
    """
    |==========================================|
    | S'assure que le format peut correspondre |
    | a celui d'un nom de domaine.             |
    |==========================================|

    entree
    ------
    :param domain: Chaine dont ou shouaite savoir
        si elle corespond a un nom de domaine.
    :type domain: str

    sortie
    ------
    :return: L'ip du dommaine si il s'agit d'un nom de domaine
        associe a une adresse ip. Une chaine vide sinon.
    :rtype: str
    """
    assert isinstance(domain, str), \
        ("Le nom de dommaine doit etre une chaine "
        "de caractere, pas un %s." % type(domain).__name__)
   
    import re
    if not re.fullmatch(r"(?!\-)(?:[a-zA-Z\d\-]{0,62}[a-zA-Z\d]\.){1,126}(?!\d+)[a-zA-Z\d]{1,63}", domain):
        return ""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return ""
