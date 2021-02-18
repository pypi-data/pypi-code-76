import configparser
from os import replace
import pathlib
import re

from fnmatch import fnmatch
from collections import Mapping


def get_config(config_file):
    config = configparser.ConfigParser()
    config_path = pathlib.Path(config_file).expanduser().resolve()

    if config_path.exists():
        config.read_string(config_path.read_text())
    return config


def get_sections(config_file):
    config = get_config(config_file)
    sections = {}
    for section_name in config.sections():
        if section_name.lower() == 'default':
            continue
        sections[section_name] = config[section_name]
    return sections


def get_cwd_sections(config_file):
    return get_sections(config_file)


def get_naming_rules(config_file="~/.aws/awsprofile"):
    global_sections = get_sections(config_file)
    cwd_sections = get_cwd_sections("./.awsprofile")
    sections = {}

    cwd_naming_opts = sections.get("naming", {})

    if str2bool(cwd_naming_opts.get("inherit_global", "true")):
        sections.update(global_sections)
    sections.update(cwd_sections)

    naming_rules = {}
    for section_name in sections:
        if section_name.startswith('naming '):
            naming_name = section_name.split(' ')[-1]
            naming_rules[naming_name] = sections[section_name]
    
    return naming_rules


def get_aliases(config_file="~/.aws/awsprofile") -> Mapping:
    sections = get_sections(config_file)
    
    results = {}
    for section_name in sections:
        if section_name.startswith('profile '):
            profile_name = section_name.split(' ')[-1]
            section = sections[section_name]
            if 'alias' in section:
                results[section['alias']] = profile_name
    
    return results


def get_naming_rule(profile_name, naming_rules: Mapping):
    for rule_name, rule in naming_rules.items():
        match = rule.get("match", None)
        negate = str2bool(rule.get("negate", "false"))
        if match:
            re_match = re.match(match, profile_name)
            if (re_match is None) == negate:
                return rule
    return None


def save_current_naming(match: str, replace_with: str, config_file="./.awsprofile"):
    config = get_config(config_file)

    section_name = "naming hide-others"
    if section_name not in config:
        config.add_section(section_name)
    
    section = config[section_name]
    section["match"] = match
    section["negate"] = "true"
    section["visible"] = "false"

    section_name = "naming cwd"
    if section_name not in config:
        config.add_section(section_name)
    
    section = config[section_name]
    section["match"] = match
    section["replace"] = replace_with
    
    config_path = pathlib.Path(config_file).expanduser().resolve()
    with config_path.open('w') as fhd:
        config.write(fhd)


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


def get_profiles(config_file="~/.aws/credentials") -> Mapping:
    sections = get_sections(config_file)
    naming_rules = get_naming_rules()
    
    results = {}
    for section_name in sections:
        naming_rule = get_naming_rule(section_name, naming_rules)
        if naming_rule:
            if str2bool(naming_rule.get("visible", "True")):
                match = naming_rule["match"]
                replace_str = naming_rule.get("replace", "")
                profile_alias = re.sub(match, replace_str, section_name)
                results[profile_alias] = section_name
        else:
            results[section_name] = section_name
    
    aliases = get_aliases()
    for alias in aliases:
        results[alias] = aliases[alias]
    
    return results


def get_profile(profile_name: str, config_file="~/.aws/credentials"):
    profiles = get_profiles(config_file=config_file)

    if profile_name in profiles:
        return profiles[profile_name]
    return None


def save_alias(profile_name: str, alias:str, config_file="~/.aws/awsprofile"):
    config = get_config(config_file)

    section_name = f"profile {profile_name}"
    if section_name not in config:
        config.add_section(section_name)
    section = config[section_name]

    section['alias'] = alias
    config_path = pathlib.Path(config_file).expanduser()
    with config_path.open('w') as fhd:
        config.write(fhd)


def get_regions():
    return [
        'us-west-2',
        'us-east-2',
        'us-east-1',
        'us-west-1',
        'af-south-1',
        'ap-east-1',
        'ap-south-1',
        'ap-northeast-3',
        'ap-northeast-2',
        'ap-southeast-1',
        'ap-southeast-2',
        'ap-northeast-1',
        'ca-central-1',
        'cn-north-1',
        'cn-northwest-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
        'eu-south-1',
        'eu-west-3',
        'eu-north-1',
        'me-south-1',
        'sa-east-1',
        'us-gov-east-1',
        'us-gov-west-1'
    ]