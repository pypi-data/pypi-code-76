import re
import typing as t


def replacer(text: str, replacements: t.Dict[str, str], reverse=False) -> str:
    """ given replacements dict(k, v), replace all k with v in text and return."""
    if len(replacements) == 0:
        return text
    if reverse:
        replacements = {v: k for k, v in replacements.items()}
    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    sorted_replacement_keys = sorted(replacements.keys(), key=len, reverse=True)
    # Create a big OR regex that matches any of the substrings to replace
    pattern = re.compile("|".join([re.escape(key) for key in sorted_replacement_keys]))
    # For each match, look up the new string in the replacements via the old string
    return pattern.sub(lambda match: replacements[match.group(0)], text)
