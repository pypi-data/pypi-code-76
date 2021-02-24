from typing import List, Optional, Tuple


def get_meta_value(
    category: str, meta: List[object]
) -> Tuple[bool, Optional[int], List]:
    """
    The business logic is:
        * read it from chain.meta
            * it is Optionaal[JsValue]
            * enabled will never be 0, per Muayad, so enabled is always True,
              we should deprecate it
    More on enabled: if we get a message, the service is enabled,
    hence the first return value is now always True
    """
    enabled, value, sub_groups = True, None, []
    if not meta:
        pass
        print("Empty meta field. Attempting to process anyway; expect errors")
    else:
        if len(meta):
            try:
                value = int(meta["value"])
            except (KeyError, ValueError):
                # apparently for on/off services, this is
                # now the service name
                value = None

            try:
                sub_groups = meta["subGroup"]
            except KeyError:
                sub_groups = []

    return True, value, sub_groups
