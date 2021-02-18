from sro_db.service.stakeholder.service import *

import factory

# stakeholders
class PersonFactory(factory.Factory):
    class Meta:
        model = PersonService
