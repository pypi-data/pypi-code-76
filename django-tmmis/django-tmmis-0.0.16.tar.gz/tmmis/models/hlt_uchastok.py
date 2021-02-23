from .base_model import *


class HltUchastok(BaseModel):
    id = models.AutoField(db_column='UchastokID', primary_key=True)
    uuid = models.CharField(db_column='UGUID', max_length=36, unique=True)

    caption = models.CharField(db_column='UchastoCaption', max_length=500)
    code = models.CharField(db_column='CODE', max_length=6)
    doctor = models.ForeignKey('HltLpuDoctor', models.DO_NOTHING, related_name='+', db_column='rf_LPUDoctorID')
    doc_prvd = models.ForeignKey('HltDocPrvd', models.DO_NOTHING, '+', db_column='rf_DocPRVDID')
    type_uid = models.IntegerField(db_column='rf_kl_TypeUID')
    lpu = models.ForeignKey('OmsLpu', models.DO_NOTHING, related_name='+', db_column='rf_LPUID')
    is_closed = models.IntegerField(db_column='isClosed')
    code_smo = models.CharField(db_column='CodeSMO', max_length=6)
    date_begin = models.DateTimeField(db_column='DateBegin')
    date_end = models.DateTimeField(db_column='DateEnd')
    flags = models.IntegerField(db_column='Flags')

    class Meta:
        managed = False
        db_table = 'hlt_Uchastok'
