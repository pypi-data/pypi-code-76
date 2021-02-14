"""
This module provides helpers to store the model
"""
import logging


class ModelPrettyPrinter:
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self, tree_model, schema):
        self.tree_model = tree_model
        self.schema = schema

    @classmethod
    def pretty_print(self):
        tree = self.tree_model.tree
        keys = self.schema.levels_keys()
        resources_keys = self.schema.resources_keys()

        lines = []
        elt0_name = "%s_dict" % keys[0]
        l0 = tree[elt0_name]
        lines.append(f"there are {len(l0)} {keys[0]}(s)")
        lines.append(f"  {', '.join([str(p) for p in [*l0]])}")

        for k0, v0 in l0.items():
            lines.append(f"  {keys[0]} {k0}: {v0[keys[0]]}")
            elt1_name = "%s_dict" % keys[1]
            l1 = v0[elt1_name]
            lines.append(f"    has {len(l1)} {keys[1]}(s)")
            lines.append(f"      {', '.join([str(i) for i in [*l1]])}")

            for k1, v1 in l1.items():
                lines.append(f"      {keys[1]} {k1}: {v1[keys[1]]}")
                elt2_name = "%s_dict" % keys[2]
                l2 = v1[elt2_name]
                lines.append(f"        has {len(l2)} {keys[2]}(s)")
                lines.append(f"          {', '.join([str(i) for i in [*l2]])}")
                for k2, v2 in l2.items():
                    lines.append(f"          {keys[2]} {k2}: {v2[keys[2]]}")

                    for name in resources_keys:
                        eltr_name = "%s_dict" % name
                        lr = v2[eltr_name]
                        lines.append(f"            has {len(lr)} {name}(s)")
                        if len(lr) > 0:
                            lines.append(f"               {', '.join([str(i) for i in [*lr]])}")
                            for kr, vr in lr.items():
                                lines.append(f"                 {name} {kr}: {vr[name]}")

        return lines
