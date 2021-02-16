import glob

from pathlib import Path
from subprocess import check_output
from functools import partial

PW_STORE_PATH = str(Path.home() / ".password-store")


def get_gpg_id(rel_p, mapped_gpg_ids):
    # print(f'looking for gpg-id in {rel_p}')
    if rel_p not in mapped_gpg_ids:
        if len(rel_p) > 2:
            return get_gpg_id(str(Path(rel_p).parent), mapped_gpg_ids)
        else:
            print(f'Could not find gpg-id for {rel_p}')
    else:
        return mapped_gpg_ids[rel_p]


def map_gpg_id():
    mapped_gpg_ids = {}
    for f in glob.glob(f'{PW_STORE_PATH}/**/.gpg-id', recursive=True):
        p = Path(f)
        with open(f, 'r', encoding='UTF-8') as id_file:
            mapped_gpg_ids.update({str(Path(get_rel_p(f)).parent): id_file.read().strip()})

    return mapped_gpg_ids


def get_rel_p(p):
    return str(p).replace(PW_STORE_PATH + '/', '')


CACHED_IDS = map_gpg_id()


def test_keymapping():
    mapped_gpg_ids = map_gpg_id()

    for f in glob.glob(f'{PW_STORE_PATH}/**/*.gpg', recursive=True):
        rp = get_rel_p(f)
        print(f'{rp} id -> {get_gpg_id(rp, mapped_gpg_ids)}')


def decrypt_file_with_id(gpg_file, gpg_id) -> str:
    cmd = ['gpg', '--quiet', '--recipient', gpg_id, '--decrypt', gpg_file]
    result = ''
    try:
        result = check_output(cmd, universal_newlines=True)
    except:
        pass

    return result.strip()


def decrypt(keyname):
    result = ''
    for f in glob.glob(f'{PW_STORE_PATH}/**/*.gpg', recursive=True):
        this_name = Path(f).stem
        if this_name == keyname:
            rp = get_rel_p(f)
            gpg_id = get_gpg_id(rp, CACHED_IDS)
            result = decrypt_file_with_id(f, gpg_id)
            break

    return result


def get_secrets(configuration_tuple):
    params = [t for t in configuration_tuple._asdict()]
    secrets = {}
    try:
        for p in params:
            secret = decrypt(p)
            if len(secret) > 0:
                secrets.update({p: secret})
    except:
        # TODO: Wanted to keep this lean, as one might not have gpg installed and what not..
        # Need to provide for example a configuration key 'use gpg' that the user can use to
        # enable this feature. This way it won't get in the way of other use cases.
        pass

    return secrets


def test_decrypt():
    keyname = 'pace_eden_lookup_signid'
    print(decrypt(keyname))

# test_keymapping()
# test_decrypt()
