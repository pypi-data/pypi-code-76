#!/usr/bin/env python3

"""
|===============================|
| Recence toutes les exceptions |
| propres a raisin.             |
|===============================|

Les exceptions suivent l'arbre suivant:

RaisinError
    DecryptError        : Erreur dans le dechiffrage des donnes.
        PswError            : Mauvais mot de passe.
        AuthenticityError   : Donnees non authentiques
    NotCompliantError   : Conformitee non respectee.
        HeaderError         : Entete incorrecte.
    SuicidalError       : Quand un thread se sucide.
    ThreatenError       : Quand une menace se fait sentir.
    AmbiguousError      : Quand il n'y a pas sufisement d'informations pour pouvoir choisir.
"""

class RaisinError(Exception):
    """
    Classe generale regroupant toutes
    les erreurs liees a raisin.
    """
    pass

class DecryptError(RaisinError):
    """
    Erreur leve l'orsqu'un mot de passe ou une clef n'est pas correcte.
    Ou lorsque l'authenticite n'est pas verifiee.
    """
    pass

class PswError(DecryptError):
    """
    Reflete un mot de passe incorecte.
    """
    pass

class AuthenticityError(DecryptError):
    """
    Exception levee quand les donnees ne sont pas authentiques.
    """
    pass

class NotCompliantError(RaisinError):
    """
    Exception levee lorsque les donnes ne sont pas conformes.
    """
    pass

class HeaderError(NotCompliantError):
    """
    Designe les mauvaises entetes.
    """
    pass

class SucidalError(RaisinError):
    """
    Quand un thread trop depressif passe decide de metre fin a ces jours.
    """
    pass

class ThreatenError(RaisinError):
    """
    Classe de base pour les erreurs levee quand une menace
    se fait sentir
    """
    pass

class AmbiguousError(RaisinError):
    """
    C'est quand il n'y a pas suffisement d'information
    pour pouvoir trancher sans ambiguite.
    """
    pass
