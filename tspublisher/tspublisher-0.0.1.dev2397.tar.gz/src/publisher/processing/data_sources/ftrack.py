import ftrack_api
from ftrack_api.exception import NoResultFoundError


def _get_ftrack_session():
    try:
        # Initially try creating session using environment variables
        session = ftrack_api.Session()
    except TypeError:
        # Fallback to details stored in ftrack secrets file
        from ftrackSecrets import API_KEY, API_USER
        session = ftrack_api.Session(server_url="https://touch-surgery.ftrackapp.com", api_key=API_KEY,
                                     api_user=API_USER)
    return session


def get_procedure_details(procedure_code):

    session = _get_ftrack_session()

    try:
        procedure = session.query("Project where name is '{}'".format(procedure_code)).one()
    except NoResultFoundError:
        procedure = session.query("Procedure where name is '{}'".format(procedure_code)).one()

    custom_attributes = procedure['custom_attributes']
    specialties = custom_attributes['speciality'] if custom_attributes.get('speciality') else []
    channel = custom_attributes['institution'][0] if custom_attributes.get('institution') else ''
    if isinstance(procedure, session.types['Procedure']):
        procedure_name = procedure['description']
        vbs = "VBS" in procedure['name']
    else:
        procedure_name = procedure['custom_attributes'].get('procedure_name')
        sim_type = custom_attributes['sim_type'][0] if custom_attributes.get('sim_type') else ''
        vbs = sim_type == 'vbs'

    return procedure_name, specialties, channel, vbs


def get_procedure_phase_list(procedure_code):

    session = _get_ftrack_session()

    def _phase_detail(phase):

        return {
            "phase_code": phase['name'],
            "phase_name": phase['description'],
            "procedure_code": procedure_code,
            "order": phase['custom_attributes']['module_order']
        }

    phases = session.query("select name, description, custom_attributes from Module where status.name is_not 'omit' "
                           "and project.name is '{}'".format(procedure_code)).all()
    if not phases:
        phases = session.query("select name, description, custom_attributes from Moduleold where status.name is_not "
                               "'omit' and ancestors any (name is '{}')".format(procedure_code)).all()

    phase_list = [_phase_detail(phase) for phase in phases]
    return sorted(phase_list, key=lambda p: (p["order"], p["phase_code"]))


def get_phase_data(phase_code):

    session = _get_ftrack_session()

    try:
        phase = session.query("select name, description, custom_attributes, project.name from Module where name is "
                              "'{}'".format(phase_code)).one()
    except NoResultFoundError:
        phase = session.query("select name, description, custom_attributes, ancestors.name from Moduleold where name is"
                              " '{}'".format(phase_code)).one()

    if isinstance(phase, session.types['Moduleold']):
        for ancestor in phase['ancestors']:
            if isinstance(ancestor, session.types['Procedure']):
                procedure_code = ancestor['name']
                break
    else:
        procedure_code = phase['project']['name']

    return {
            "phase_code": phase['name'],
            "phase_name": phase['description'],
            "procedure_code": procedure_code,
            "order": phase['custom_attributes']['module_order']
        }
