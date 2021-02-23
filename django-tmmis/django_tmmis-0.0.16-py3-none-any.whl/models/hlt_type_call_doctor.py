from .base_model import *


class HltTypeCallDoctor(BaseModel):
    id = models.AutoField(db_column='TypeCallDoctorID', primary_key=True)
    code = models.CharField(db_column='CODE', max_length=1)
    name = models.CharField(db_column='NAME', max_length=20)
    datebegin = models.DateTimeField(db_column='DateBegin')
    dateend = models.DateTimeField(db_column='DateEnd')
    enumname = models.CharField(db_column='EnumName', max_length=50)
    flags = models.IntegerField(db_column='Flags')

    class Meta:
        managed = False
        db_table = 'hlt_TypeCallDoctor'
