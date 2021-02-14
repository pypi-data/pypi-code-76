
"""
This module provides helpers to build the tree
"""
import logging

from collections import defaultdict

logger = logging.getLogger(__name__)


def build_tree(dfs, keys):
    tree = defaultdict(dict)
    elt0_name = "%s_dict" % keys[0]
    tree[elt0_name]

    l0 = dfs[0].groupby('id')
    for k0, v0 in l0:
        records = v0.to_dict('records')
        tree[elt0_name][k0] = records[0]
        elt1_name = "%s_dict" % keys[1]
        tree[elt0_name][k0][elt1_name] = {}

        df1 = dfs[1]
        l1 = df1[df1['id_parent'] == k0].groupby('id')
        for k1, v1 in l1:
            records = v1.to_dict('records')
            tree[elt0_name][k0][elt1_name][k1] = records[0]
            elt2_name = "%s_dict" % keys[2]
            tree[elt0_name][k0][elt1_name][k1][elt2_name] = {}

            df2 = dfs[2]
            l2 = df2[df2['id_parent'] == k1].groupby('id')
            for k2, v2 in l2:
                records = v2.to_dict('records')
                tree[elt0_name][k0][elt1_name][k1][elt2_name][k2] = records[0]

    return tree


def pretty_print_tree(tree):
    l0 = tree['process_dict']
    print(f"there are {len(l0)} process")
    print(f" {', '.join([str(p) for p in [*l0]])}")

    for k0, v0 in l0.items():
        print(f"  process {k0}:")
        l1 = v0['step_dict']
        print(f"    has {len(l1)} step(s)")
        print(f"     {', '.join([str(i) for i in [*l1]])}")

        for k1, v1 in l1.items():
            print(f"    step {k1}:")
            l2 = v1['task_dict']
            print(f"      has {len(l2)} task(s)")
            print(f"       {', '.join([str(i) for i in [*l2]])}")
            for k2, v2 in l2.items():
                print(f"        task {k2}:")
