from datetime import datetime
import random
import re


def _generate_slug(length=14):
    letters = "2346789abcdefghijkmnpqrtwxyz"
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def safe_id_str(s):
    s = s.lower()
    return re.sub(r'[^a-z0-9_]', "_", s)


def create_safe_id(docType, uid=None):
    return f"{docType}:{safe_id_str(uid)}" if uid else generate_random_id(docType)


def generate_random_id(docType):
    return f"{docType}:{int(datetime.utcnow().timestamp())}_{_generate_slug()}"


def create_doc(docType, data):
    return {
        '_id': data.get("id", generate_random_id(docType)),
        'type': docType,
        'created_at': datetime.now().astimezone().replace(microsecond=0).isoformat(),
        "schema": "0",
        docType: data
    }


def create_tree(name, nodes, nodeDocType=""):
    return {
        'id': f"tree:{name}",
        'nodes': nodes,
        'nodeDocType': nodeDocType
    }


def create_tree_node(docType, label, parent=None, child_nodes=[]):
    return {
        'id': generate_random_id(docType),
        'label': label,
        'parentId': parent,
        'childNodes': child_nodes
    }
