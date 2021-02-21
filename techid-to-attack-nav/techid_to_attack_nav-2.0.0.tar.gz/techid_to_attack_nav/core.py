"""Main module."""
import json
import re
import base64
from techid_to_attack_nav.template import TEMPLATE_B64

def extract_techniques(input_file):
    input_file = open(input_file)
    p = re.compile("T\d\d\d\d")
    matches = p.findall(input_file.read())
    return matches


def get_template(filename):
    if filename == "default":
        template_dict = json.loads(
            base64.b64decode(TEMPLATE_B64).decode('ascii'))
    else:
        template = open(filename)
        template_dict = json.load(template)
    return template_dict


def write_template(template_dict, filename=""):
    outfile = open(filename, "a")
    outfile.write(json.dumps(template_dict))
    outfile.close()


def align_ttps(template_dict, techniques, score=5):
    for techniques in techniques:
        for item in template_dict['techniques']:
            if techniques == item['techniqueID']:
                item.update({"score": score})


def set_actor(actor_name, template):
    template.update({"name": actor_name + " TTPs"})
