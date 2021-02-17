# Import python libs
from typing import Any, Dict


async def read(hub) -> Dict[str, Any]:
    """
    Read in the data from an encrypted roster
    """
    if hub.OPT.heist.get("roster_file"):
        return hub.crypto.init.decrypt_file(
            hub.OPT.heist.roster_file, hub.OPT.acct.acct_key, crypto_plugin="fernet"
        )
    return {}
