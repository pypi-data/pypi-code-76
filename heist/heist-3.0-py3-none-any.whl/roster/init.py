from typing import Any, Dict


async def read(hub, roster: str = None) -> Dict[str, Any]:
    """
    Given the rosters to read in, the tgt and the tgt_type
    """
    ret = {}

    # If a specific roster plugin wasn't specified then determine the best roster plugin automatically
    if roster is None:
        roster_file = hub.OPT.heist.get("roster_file")
        if roster_file:
            if roster_file.endswith(".fernet"):
                roster = "fernet"
            else:
                roster = "flat"
        else:
            roster = "scan"
        hub.log.info(f"Picking default roster: {roster}")

    ready = await hub.roster[roster].read()

    if not ready:
        raise ValueError(f"The roster {roster} did not return data when rendered")

    if not isinstance(ready, dict):
        raise ValueError(f"The roster {roster} is not formatted correctly")

    for id_, condition in ready.items():
        if not isinstance(condition, dict):
            raise ValueError(f"The roster {roster} is not formatted correctly.")
        ret[condition.get("id", id_)] = condition
        if "id" not in condition:
            condition["id"] = id_

        ret[condition["id"]] = condition

    return ret
