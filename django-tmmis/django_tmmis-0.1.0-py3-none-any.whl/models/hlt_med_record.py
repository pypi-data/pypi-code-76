from .base_model import *


class HltMedRecord(BaseModel):
    id = models.AutoField(db_column='MedRecordID', primary_key=True)
    uuid = models.CharField(db_column='Guid', max_length=36, unique=True, default=uuid.uuid4)
    confidentiality_code = models.CharField(db_column='ConfidentialityCode', max_length=50)
    crc = models.TextField(db_column='CRC')
    data = models.TextField(db_column='Data')
    date = models.DateTimeField(db_column='Date')
    blank_template = models.IntegerField(db_column='rf_BlankTemplateID')
    lpu_doctor = models.ForeignKey('HltLpuDoctor', models.DO_NOTHING, db_column='rf_LPUDoctorID', related_name='+')
    visit_history = models.ForeignKey('HltVisitHistory', models.DO_NOTHING,
                                      db_column='rf_VisitHistoryID', related_name='med_records')
    sign = models.TextField(db_column='Sign')
    event_data_time = models.DateTimeField(db_column='EventDataTime')
    person = models.ForeignKey('HltMkab', models.DO_NOTHING, db_column='PersonGUID',
                               to_field='uuid', related_name='med_records')
    doc = models.CharField(db_column='rf_DOCGUID', max_length=36)
    doc_type_def = models.CharField(db_column='rf_DocTypeDefGUID', max_length=36)
    view_data = models.TextField(db_column='ViewData')
    create_username = models.CharField(db_column='CreateUserName', max_length=255)
    edit_username = models.CharField(db_column='EditUserName', max_length=255)
    create_user = models.ForeignKey('XUser', models.DO_NOTHING, related_name='+', db_column='rf_CreateUserID')
    edit_user = models.ForeignKey('XUser', models.DO_NOTHING, related_name='+', db_column='rf_EditUserID')
    desc = models.CharField(db_column='DescGuid', max_length=36)
    create_date = models.DateTimeField(db_column='CreateDate')
    description = models.TextField(db_column='Description')
    doc_prvd = models.CharField(db_column='rf_DocPrvdGuid', max_length=36)
    mkab = models.ForeignKey('HltMkab', models.DO_NOTHING, db_column='rf_MKABGuid',
                             to_field='uuid', related_name='+')
    is_upload = models.BooleanField(db_column='isUpload')
    is_del = models.BooleanField(db_column='IsDel')

    flags = models.IntegerField(db_column='Flags')

    class Meta:
        managed = False
        db_table = 'hlt_MedRecord'
