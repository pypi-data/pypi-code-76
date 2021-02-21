"""
BOMIST Utilities (bomist.com)
"""

import json
import shutil
import tarfile
import re
from glob import glob
from os import path, getcwd, listdir, makedirs

from .crypto import decode
from .v2 import (create_doc, create_tree_node, create_tree,
                 create_safe_id, generate_random_id, safe_id_str)


def dump1(wspath, outpath=None):
    print(f"Dumping {wspath}")
    if not _check_if_ws_exits(wspath):
        print("ERROR", f"workspace not found at {wspath}",)
        return

    outpath = outpath or getcwd()
    tmp_dir = path.join(outpath, ".tmp")
    shutil.rmtree(tmp_dir, ignore_errors=True)

    datapath = path.join(wspath, "data")

    all_docs = []

    storage_mapper = {}
    labels_mapper = {}
    category_mapper = {}
    docs_mapper = {}  # ref -> id
    files_mapper = {}  # file_main -> id

    parts_cnt = 0
    docs_cnt = 0
    storage_cnt = 0
    labels_cnt = 0
    categories_cnt = 0

    with open(path.join(datapath, ".labels"), "rb") as f:
        d = json.loads(decode(f.read()))
        plabels = d.get("labels", [])
        nodes = []
        for plabel in plabels:
            pname = plabel.get("name")
            pnode = create_tree_node("label", pname)
            labels_cnt += 1
            k = pname
            labels_mapper[k] = pnode['id']
            child_nodes = []
            for slabel in plabel.get("sub", []):
                sname = slabel.get('name')
                snode = create_tree_node(
                    "label", sname, pnode['id'])
                labels_cnt += 1
                child_nodes.append(snode)
                k = "\t".join([pname, sname])
                labels_mapper[k] = snode['id']
            pnode['childNodes'] = child_nodes
            nodes.append(pnode)

        labels_tree_doc = create_doc("tree", create_tree("labels", nodes))
        all_docs += [labels_tree_doc]

    with open(path.join(datapath, ".storage"), "rb") as f:
        d = json.loads(decode(f.read()))
        [tree_doc, storage_docs, mapper] = _create_storage(d)
        storage_mapper = mapper
        all_docs += [tree_doc] + storage_docs
        storage_cnt = len(storage_docs)

    with open(path.join(datapath, ".categories"), "rb") as f:
        category_docs = []
        d = json.loads(decode(f.read()))
        categories = d["categories"]
        for c in categories:
            doc = create_doc("category", {
                'name': c
            })
            category_mapper[c] = doc['_id']
            category_docs.append(doc)
        categories_cnt += len(category_docs)
        all_docs += category_docs

    docpaths = listdir(path.join(datapath, "files"))
    for docpath in docpaths:
        doc_docs = []
        with open(path.join(datapath, "files", docpath, ".doc"), "rb") as f:
            d = json.loads(decode(f.read()))
            doc = create_doc("document", {})
            ext = path.splitext(d['file_main'])[1]
            fpath = f"{safe_id_str(doc['_id'])}{ext}"
            doc.update({
                'document': {
                    'name': d['title'],
                    'notes': d['notes'],
                    'category': category_mapper.get(d['category'], "") if d['category'] else "",
                    'path': {
                        'local': fpath
                    }
                }
            })
            k = d['ref']
            docs_mapper[k] = doc['_id']
            k = path.join(datapath, "files", docpath, d['file_main'])
            if path.exists(k):
                pass
            else: 
                filepaths = listdir(path.join(datapath, "files", docpath))
                if ".doc" in filepaths: filepaths.remove(".doc")
                if len(filepaths) > 0:
                    k = path.join(datapath, "files", docpath, filepaths[0])
                else:
                    k = None
            if k:
                files_mapper[k] = fpath
                doc_docs.append(doc)
        docs_cnt += len(doc_docs)
        all_docs += doc_docs

    partpaths = listdir(path.join(datapath, "parts"))
    for partpath in partpaths:
        part_docs = []
        with open(path.join(datapath, "parts", partpath, ".part"), "rb") as f:
            d = json.loads(decode(f.read()))

            label_k = "\t".join([d['plabel'], d['slabel']])
            label = labels_mapper.get(label_k.strip(), "") if label_k else ""

            storage_k = d['storage']
            storage = storage_mapper.get(storage_k) if storage_k else ""

            re_tolerance = re.compile(
                "([0-9.,]+)\s*(?=%|ppm)").findall(d['value'] or "")
            tolerance = float(re_tolerance[0].replace(",",".")) if len(re_tolerance) > 0 else None

            manufacturer = d['brand'] or "n/a"

            part = {
                'id': create_safe_id("part", f"{d['mpn']}_{manufacturer}"),
                'type': "outsourced",
                'mpn': d['mpn'],
                'ipn': d['ipn'],
                'manufacturer': manufacturer,
                'description': d['desc'],
                'value': d['value'],
                'package': d['package'],
                'tolerance': tolerance,
                'label': label,
                'stock': int(d['stock']),
                'stockInHouse': int(d['stock']),
                'lowStock': int(d['stock_low']),
                'notes': d['notes'],
                'nonStocking': False,
                'hidden': bool(d.get('obsolete', False) or d['stock_ignore']),
                'attrition': {
                    'percent': 0,
                    'value': 0
                },
                'storage': [],
                'alternates': [],
                'prefSupplier': d['seller']
            }
            # print(part['mpn'], "-->", label_k, part['label'])
            doc = create_doc("part", part)

            inventory_doc = create_doc("inventory", {
                'id': f"r/{part['id']}:{generate_random_id('inventory')}",
                'status': 'in_house',
                'storage': storage,
                'qty': int(d['stock'])
            })

            if d['docs']:
                for ref in d['docs']:
                    doc_id = docs_mapper.get(ref)
                    ref_doc = create_doc("ref", {
                        'id': f"r/{part['id']}:{doc_id}",
                        'refId': doc_id
                    })
                    part_docs += [ref_doc]

            parts_cnt += 1
            part_docs += [doc, inventory_doc]

    
        all_docs += part_docs

    # projectpaths = listdir(path.join(datapath, "projects"))
    # for projectpath in projectpaths:
    #     project_data = {}
    #     projectpath = path.join(datapath, "projects", projectpath)
    #     with open(path.join(projectpath, ".project"), "rb") as f:
    #         d = json.loads(decode(f.read()))
    #         project_data = d
    #     print("--- project", project_data)

    #     revpaths = glob(path.join(projectpath, "rev_*"))
    #     # print("revs", revpaths)
    #     for revpath in revpaths:
    #         rev_data = {}
    #         with open(path.join(revpath, ".rev"), "rb") as f:
    #             d = json.loads(decode(f.read()))
    #             rev_data = d
    #         print("rev", rev_data)
    #         varpaths = glob(path.join(projectpath, revpath, "var_*"))
    #         print("varpaths", varpaths)
    #         for varpath in varpaths:
    #             var_data = {}
    #             with open(path.join(varpath, ".var"), "rb") as f:
    #                 d = json.loads(decode(f.read()))
    #                 var_data = d
    #             print("var", json.dumps(var_data, indent=2))
                


    dump_dir = path.join(tmp_dir, "dump-data")
    files_dir = path.join(dump_dir, "files")

    makedirs(files_dir, exist_ok=True)
    makedirs(outpath, exist_ok=True)

    with open(path.join(dump_dir, "allDocs.json"), "w") as f:
        rows = list(map(lambda d: dict({
            'doc': d
        }), all_docs))
        all_docs = {
            'total_rows': len(all_docs),
            'rows': rows
        }
        f.write(json.dumps(all_docs, indent=2))

   
    orig_filepaths = files_mapper.keys()
    for orig_filepath in orig_filepaths:
        fsrc = orig_filepath
        fdst = path.join(files_dir, files_mapper.get(orig_filepath))
        if path.exists(fsrc):
            shutil.copy2(fsrc, fdst)
    
    tarfilename = "legacy.bomist_dump"
    tarpath = path.join(outpath, tarfilename)
    with tarfile.open(tarpath, "w:gz") as tar:
        tar.add(dump_dir, arcname="dump-data")

    shutil.rmtree(tmp_dir)

    print("Parts", parts_cnt)
    print("Documents", docs_cnt)
    print("Categories", categories_cnt)
    print("Storage", storage_cnt)
    print("Labels", labels_cnt)

    print(f"{tarfilename} created")


def _create_storage(storage):
    mapper = {}
    storage_docs = []

    def _for_each_storage(storage, parent=None, parent_path=None):
        nodes = []
        for s in storage:
            values = s.get('data', [])
            name = values[0]
            spath = (parent_path or []) + [name]
            node = create_tree_node("storage", name, parent)
            k = "\t".join(spath)
            mapper[k] = node['id']
            sdoc = create_doc("storage", {'name': name, 'id': node['id']})
            storage_docs.append(sdoc)
            node['childNodes'] = _for_each_storage(
                s.get('children', []), node['id'], spath)
            nodes.append(node)
        return nodes

    tree_nodes = _for_each_storage(storage, None)
    storage_tree_doc = create_doc("tree", create_tree("storage", tree_nodes))
    return [storage_tree_doc, storage_docs, mapper]


def _check_if_ws_exits(wspath):
    wsfile = ".ws"
    wspath = path.join(wspath, wsfile)
    return path.isfile(wspath)
