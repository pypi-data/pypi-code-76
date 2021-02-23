from .base_model import *


class HltDocPrvd(BaseModel):
    id = models.AutoField(db_column='DocPRVDID', primary_key=True)  
    lpu_doctor = models.ForeignKey('HltLpuDoctor', models.DO_NOTHING, '+', db_column='rf_LPUDoctorID')
    d_prik = models.DateTimeField(db_column='D_PRIK')  
    s_st = models.DecimalField(db_column='S_ST', max_digits=5, decimal_places=3)  
    d_end = models.DateTimeField(db_column='D_END')  
    prvs = models.ForeignKey('OmsPrvs', models.DO_NOTHING, '+', db_column='rf_PRVSID')
    healing_room_id = models.IntegerField(db_column='rf_HealingRoomID')
    kat_id = models.IntegerField(db_column='rf_KV_KATID')
    department = models.ForeignKey('OmsDepartment', models.DO_NOTHING, '+', db_column='rf_DepartmentID')
    main_work_place = models.BooleanField(db_column='MainWorkPlace')
    guid = models.CharField(db_column='GUID', max_length=36)  
    in_time = models.IntegerField(db_column='InTime')
    prvd = models.ForeignKey('OmsPrvd', models.DO_NOTHING, '+', db_column='rf_PRVDID')
    name = models.CharField(db_column='Name', max_length=100)  
    rf_equipment_id = models.IntegerField(db_column='rf_EquipmentID')
    rf_resourcetype_id = models.IntegerField(db_column='rf_ResourceTypeID')
    shown_in_schedule = models.BooleanField(db_column='ShownInSchedule')
    er_id = models.CharField(db_column='ERID', max_length=8000)
    er_name = models.CharField(db_column='ERName', max_length=8000)
    nom_service_code = models.CharField(db_column='NomServiceCode', max_length=50)
    is_special = models.BooleanField(db_column='isSpecial')
    department_type_id = models.IntegerField(db_column='rf_kl_DepartmentTypeID')
    is_dismissal = models.BooleanField(db_column='isDismissal')
    interval = models.IntegerField(db_column='Interval')  
    is_use_interval = models.BooleanField(db_column='isUseInterval')
    pcod = models.CharField(db_column='PCOD', max_length=20)  
    is_conclusion = models.BooleanField(db_column='isConclusion')
    assignment_doctor_id = models.IntegerField(db_column='rf_AssignmentDoctorID')

    class Meta:
        managed = False
        db_table = 'hlt_DocPRVD'
