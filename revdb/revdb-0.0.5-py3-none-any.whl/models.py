from mjango import models
from revdb import db_settings


class Model(models.Model):
    class Meta:
        settings = db_settings
        collection = None
