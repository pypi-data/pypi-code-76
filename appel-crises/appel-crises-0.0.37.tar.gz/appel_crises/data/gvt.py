from typing import List

from appel_crises.mailer import MailingPerson, mailing_person

GVT: List[MailingPerson] = [
    mailing_person("alexis.kohler@elysee.fr", "Présidence de la République"),
    mailing_person(
        "benoit.ribadeau-dumas@pm.gouv.fr", "Gouvernement (Premier Ministre)"
    ),
    mailing_person(
        "emmanuel.moulin@cabinets.finances.gouv.fr",
        "Gouvernement (Ministère de l’Économie et des Finances)",
    ),
    mailing_person(
        "marine.braud@ecologique-solidaire.gouv.fr",
        "Gouvernement (Ministère de la Transition Écologique)",
    ),
]
