from .base_model import *


class OmsDepartment(BaseModel):
    id = models.AutoField(db_column='DepartmentID', primary_key=True)
    uuid = models.CharField(db_column='GUIDDepartment', max_length=36, unique=True)

    code = models.CharField(db_column='DepartmentCODE', max_length=50)
    name = models.CharField(db_column='DepartmentNAME', max_length=255)
    type = models.ForeignKey(
        'OmsKlDepartmentType',
        models.DO_NOTHING,
        related_name='+',
        db_column='rf_kl_DepartmentTypeID'
    )
    lpu = models.ForeignKey('OmsLpu', models.DO_NOTHING, db_column='rf_LPUID')
    zav_pcod = models.CharField(db_column='ZAVPCOD', max_length=10)
    zav_fio = models.CharField(db_column='ZAVFIO', max_length=70)
    profile = models.ForeignKey(
        'OmsKlDepartmentProfile',
        models.DO_NOTHING,
        related_name='+',
        db_column='rf_kl_DepartmentProfileID'
    )
    code_department = models.IntegerField(db_column='Code_Department')
    n_otd = models.CharField(db_column='N_OTD', max_length=5)
    rem = models.CharField(db_column='Rem', max_length=255)
    age_group = models.ForeignKey(
        'OmsKlAgeGroup',
        models.DO_NOTHING,
        related_name='+',
        db_column='rf_kl_AgeGroupID'
    )
    date_b = models.DateTimeField(db_column='Date_B')
    date_e = models.DateTimeField(db_column='Date_E')
    code_kladr = models.CharField(db_column='CodeKLADR', max_length=10)
    fax = models.CharField(db_column='FAX', max_length=50)
    address = models.ForeignKey('KlaAddress', models.DO_NOTHING, related_name='+', db_column='rf_AddressID')
    tel = models.CharField(db_column='Tel', max_length=50)
    med_care_type = models.ForeignKey(
        'OmsKlMedCareType',
        models.DO_NOTHING,
        related_name='+',
        db_column='rf_kl_MedCareTypeID'
    )

    class Meta:
        managed = False
        db_table = 'oms_Department'
