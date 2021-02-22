# -*- coding: utf-8 -*-
# eopayment - online payment library
# Copyright (C) 2011-2020 Entr'ouvert
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''Responses codes emitted by EMV Card or 'Carte Bleu' in France'''

from . import PAID, CANCELLED, ERROR, DENIED


CB_RESPONSE_CODES = {
    '00': {'message': 'Transaction approuvée ou traitée avec succès', 'result': PAID},
    '02': {'message': 'Contacter l\'émetteur de carte'},
    '03': {'message': 'Accepteur invalide'},
    '04': {'message': 'Conserver la carte'},
    '05': {'message': 'Ne pas honorer', 'result': DENIED},
    '07': {'message': 'Conserver la carte, conditions spéciales'},
    '08': {'message': 'Approuver après identification'},
    '12': {'message': 'Transaction invalide'},
    '13': {'message': 'Montant invalide'},
    '14': {'message': 'Numéro de porteur invalide'},
    '15': {'message': 'Emetteur de carte inconnu'},
    '17': {'message': 'Annulation par l\'acheteur', 'result': CANCELLED},
    '30': {'message': 'Erreur de format'},
    '31': {'message': 'Identifiant de l\'organisme acquéreur inconnu'},
    '33': {'message': 'Date de validité de la carte dépassée'},
    '34': {'message': 'Suspicion de fraude'},
    '41': {'message': 'Carte perdue'},
    '43': {'message': 'Carte volée'},
    '51': {'message': 'Provision insuffisante ou crédit dépassé'},
    '54': {'message': 'Date de validité de la carte dépassée'},
    '56': {'message': 'Carte absente du fichier'},
    '57': {'message': 'Transaction non permise à ce porteur'},
    '58': {'message': 'Transaction interdite au terminal'},
    '59': {'message': 'Suspicion de fraude'},
    '60': {'message': 'L\'accepteur de carte doit contacter l\'acquéreur'},
    '61': {'message': 'Dépasse la limite du montant de retrait'},
    '63': {'message': 'Règles de sécurité non respectées'},
    '68': {'message': 'Réponse non parvenue ou reçue trop tard'},
    '90': {'message': 'Arrêt momentané du système'},
    '91': {'message': 'Emetteur de cartes inaccessible'},
    '96': {'message': 'Mauvais fonctionnement du système'},
    '97': {'message': 'Échéance de la temporisation de surveillance globale'},
    '98': {'message': 'Serveur indisponible routage réseau demandé à nouveau'},
    '99': {'message': 'Incident domaine initiateur'},
}


def translate_cb_error_code(error_code):
    'Returns message, eopayment_error_code'

    if error_code in CB_RESPONSE_CODES:
        return CB_RESPONSE_CODES[error_code]['message'], CB_RESPONSE_CODES[error_code].get('result', ERROR)
    return None, None
