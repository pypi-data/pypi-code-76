from .base_model import *


class OmsKlReasonType(BaseModel):
    """
    Классификатор причин обращения в поликлинику
    """
    id = models.AutoField(db_column='kl_ReasonTypeID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=50)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255)  # Field name made lowercase.
    date_b = models.DateTimeField(db_column='Date_B')  # Field name made lowercase.
    date_e = models.DateTimeField(db_column='Date_E')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'oms_kl_ReasonType'
