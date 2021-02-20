"""Script that build and save a database postal code to MP.

Needed data:
    - MP index, with district and department numbers, downloaded from
    https://www.voxpublic.org/spip.php?page=annuaire&cat=deputes&lang=fr
    and saved to deputes.csv

Output:
    - MP data, from , saved as json object into district_to_mp.json

"""
import csv
import json
import logging
from typing import Iterable, Tuple, Dict

CodedDistrict = str
ReducedMP = Tuple[str, str, str, str]  # nom, sexe, nom_circo, email

logger = logging.getLogger(__name__)


def parse_mp_email(emails: str, nom: str):
    """Parse emails and return only the one from Assemblée nationale."""
    if emails.find('|') == -1:
        return emails

    l_emails = list(filter(lambda s: len(s) > 0, emails.split('|')))

    for email in l_emails:
        if email.endswith("@assemblee-nationale.fr"):
            return email

    logger.info("No correct email found for %s, taking the first from %s", nom, emails)

    return l_emails[0]


class MP:
    """Represents a MP."""

    nom: str
    sexe: str
    num_deptmt: int
    nom_circo: str
    num_circo: int
    groupe_sigle: str
    commission_permanente: str
    fonction: str
    sites_web: str
    emails: str
    twitter: str
    autres_mandats: str
    tel: str
    adresse_permanence: str
    cp_permanence: str
    ville_permanence: str

    email: str
    coded_district: CodedDistrict

    def __init__(
        self,
        nom,
        sexe,
        num_deptmt,
        nom_circo,
        num_circo,
        groupe_sigle,
        commission_permanente,
        fonction,
        sites_web,
        emails,
        twitter,
        autres_mandats,
        tel,
        adresse_permanence,
        cp_permanence,
        ville_permanence,
    ):
        """Build a MP from its column in deputes.csv"""
        self.nom = nom
        self.sexe = sexe
        self.num_deptmt = dpt_to_int(num_deptmt)
        self.nom_circo = nom_circo
        self.num_circo = int(num_circo)
        self.groupe_sigle = groupe_sigle
        self.commission_permanente = commission_permanente
        self.fonction = fonction
        self.sites_web = sites_web
        self.emails = emails
        self.twitter = twitter
        self.autres_mandats = autres_mandats
        self.tel = tel
        self.adresse_permanence = adresse_permanence
        self.cp_permanence = cp_permanence
        self.ville_permanence = ville_permanence

        self.email = parse_mp_email(emails, nom)
        self.coded_district = "{}.{}".format(self.num_deptmt, self.num_circo)

    def reduce(self) -> ReducedMP:
        """Return only interesting columns."""
        return (self.nom, self.sexe, self.nom_circo, self.email)

    def __repr__(self):
        return f"{self.nom} ({self.num_deptmt}.{self.num_circo})"


def dpt_to_int(dpt: str) -> int:
    """Convert a dpt to an int"""
    if type(dpt) is int:
        return int(dpt)

    if dpt[0] == 'Z':
        return 0  # Handling has to be done higher

    if dpt[1].upper() == 'A' or dpt[1].upper() == 'B':
        return 20

    else:
        return int(dpt)


def import_mps() -> Iterable[MP]:
    """Import mps from deputes.csv"""
    result = list()
    with open("deputes.csv") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            result.append(MP(*row))

    logger.info("Imported %d mps.", len(result))

    return result


def build_mps(mps: Iterable[MP]) -> Dict[CodedDistrict, ReducedMP]:
    """Build relation between districts numbers and mps"""
    result = dict()
    for mp in mps:
        result[mp.coded_district] = mp.reduce()

    return result


def save(obj: object, filename):
    """Save the object into filename"""
    with open(filename, "w") as f:
        f.write(json.dumps(obj))
        logger.info("Object saved into %s", filename)


def main():
    """Main function."""
    logging.basicConfig(level="DEBUG")

    raw_deputes = import_mps()
    districts_to_mps = build_mps(raw_deputes)

    save(districts_to_mps, "district_to_mp.json")

    print(districts_to_mps["93.1"])


if __name__ == '__main__':
    main()
