import os
from base64 import b64decode
from pathlib import Path
from typing import Dict, List, Optional

from certdumper import types
from certdumper.util import clog
from certdumper.conf import config


CertMap = Dict[str, types.AcmeCert]


def dump_changed_certs(acme_path: Path):
    """ Dump certificates affected by the file modification.

    We need to determine which certs have been changes and re-export them
    to disk.
    """
    acme = types.AcmeJson.from_file(acme_path)

    # Load previous ACME config (won't exist on first run).
    prev_acme = None
    if (prev_acme_path := config.rel_path(config.prev_acme_path)).exists():
        prev_acme = types.AcmeJson.from_file(prev_acme_path)

    # Store current ACME config as prev
    with open(prev_acme_path, 'w') as fp:
        fp.write(acme.json(by_alias=True, indent=2))

    # Export all the changed certificates to files in {out_dir}
    if to_export := get_changed_certs(acme, prev_acme):
        out_dir = config.rel_path(config.out_dir)
        for cert in to_export:
            clog(f"-- <32>Change detected, "
                 f"dumping <95>{cert.domain.main} <32>certs to <94>{out_dir}")
            dump_cert(out_dir, cert)
    else:
        clog("-- <32>No certificate changes detected.")


def get_changed_certs(
    next_acme: types.AcmeJson,
    prev_acme: Optional[types.AcmeJson]
) -> List[types.AcmeCert]:
    """ Returns a list of certs changed between 2 acme configurations. """
    cert_map_prev: CertMap = {}
    cert_map_next= {
        cert.domain.main: cert
        for cert in (next_acme.letsencrypt.certs or [])
    }

    if prev_acme:
        cert_map_prev = {
            cert.domain.main: cert
            for cert in (prev_acme.letsencrypt.certs or [])
        }

    certs_changed = []
    for domain, next_cert in cert_map_next.items():
        if prev_cert := cert_map_prev.get(domain):
            if prev_cert != next_cert:
                certs_changed.append(next_cert)
        else:
            certs_changed.append(next_cert)

    return certs_changed


def dump_cert(out_dir: Path, cert: types.AcmeCert):
    base_path = config.out_path.format(domain=cert.domain.main)
    cert_file =  out_dir / f"{base_path}{config.cert_ext}"
    key_file = out_dir / f"{base_path}{config.key_ext}"

    if not cert_file.parent.exists():
        os.makedirs(cert_file.parent)

    elif not cert_file.parent.is_dir():
        raise Exception(f"{out_dir} is not a directory")

    # Write .cert
    with open(cert_file, 'wb') as fp:
        fp.write(b64decode(cert.certificate))

    os.chmod(cert_file, 0o640)
    os.chown(cert_file, uid=0, gid=999)

    # Write .key
    with open(key_file, 'wb') as fp:
        fp.write(b64decode(cert.key))

    os.chmod(key_file, 0o640)
    os.chown(key_file, uid=0, gid=999)
