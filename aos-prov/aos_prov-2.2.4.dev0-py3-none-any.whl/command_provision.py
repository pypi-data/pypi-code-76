#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

from aos_prov.communication.cloud.cloud_api import CloudAPI
from aos_prov.communication.unit.unit_communacation import UnitCommunication
from aos_prov.communication.utils.config import Config
from aos_prov.communication.utils.user_credentials import UserCredentials
from colorama import Fore, Style


def run_provision(unit_address: str, user_credentials: UserCredentials, register_port):
    cloud_api = CloudAPI(user_credentials, register_port)
    cloud_api.check_cloud_access()

    config = Config()
    uc = UnitCommunication(unit_address)

    config.system_id, model_name = uc.get_system_info()
    config.set_model(model_name)
    cloud_api.check_unit_is_not_provisioned(config.system_id)

    config.supported_cert_types = uc.get_cert_types()

    for cert_type in config.supported_cert_types:
        uc.clear(cert_type)

    for cert_type in config.supported_cert_types:
        config.unit_certificates.append(uc.create_keys(cert_type, ''))

    for cert_type in config.supported_cert_types:
        uc.set_cert_owner(cert_type, '')

    register_payload = {
        'hardware_id': config.system_id,
        'system_uid':  config.system_id,
        'board_model_name': config.model_name,
        'board_model_version': config.model_version,
        'provisioning_software': "aos-provisioning:{version}".format(version=3.1),
        'additional_csrs': []
    }

    for c in config.unit_certificates:
        if c.cert_type == 'online':
            register_payload['online_public_csr'] = c.csr
        elif c.cert_type == 'offline':
            register_payload['offline_public_csr'] = c.csr
        else:
            register_payload['additional_csrs'].append({'cert_type': c.cert_type, 'csr': c.csr})

    response = cloud_api.register_device(register_payload)

    additional_certs = response.get('additional_certs', [])
    for c in config.unit_certificates:
        if c.cert_type == 'online':
            c.certificate = response.get('online_certificate')
        elif c.cert_type == 'offline':
            c.certificate = response.get('offline_certificate')
        else:
            for ac in additional_certs:
                if ac['cert_type'] == c.cert_type:
                    c.certificate = ac['cert']
                    break

    for c in config.unit_certificates:
        uc.apply_certificate(c)

    claims = response.get('claim')
    if claims:
        uc.set_users([claims])

    uc.finish_provisioning()

    print(f'{Fore.GREEN}Finished successful{Style.RESET_ALL}')
