# -*- coding: utf-8 -*-
"""Summary

Attributes:
    logger (TYPE): Description
"""

from operator import itemgetter

from .conditions import conditions

from orbis_eval.core.base import PluginBaseClass

import logging
logger = logging.getLogger(__name__)


class Main(PluginBaseClass):

    """Summary
    """

    def __init__(self):
        """Summary
        """
        super(Main, self).__init__()

    def run(self, computed, gold, scorer_condition):
        """Summary

        Args:
            computed (TYPE): Description
            gold (TYPE): Description
            scorer_condition (TYPE): Description

        Returns:
            TYPE: Description
        """

        gold_0 = gold.copy()
        computed_0 = computed.copy()
        entity_mappings = []

        self.catch_data(gold_0, "run", "gold_0", __file__)
        self.catch_data(computed_0, "run", "computed_0", __file__)

        entity_mappings, gold_0, computed_0 = self.get_scored(entity_mappings, gold_0, computed_0, scorer_condition)
        self.catch_data(entity_mappings, "run", "entity_mappings", __file__)
        self.catch_data(gold_0, "run", "gold_0_1", __file__)
        self.catch_data(computed_0, "run", "computed_0_1", __file__)

        entity_mappings, computed_0 = self.get_unscored(entity_mappings, computed_0)
        self.catch_data(entity_mappings, "run", "entity_mappings_1", __file__)
        self.catch_data(computed_0, "run", "computed_0_2", __file__)

        confusion_matrix = self.get_confusion_matrix(entity_mappings)
        self.catch_data(confusion_matrix, "run", "confusion_matrix", __file__)

        return confusion_matrix

    def get_scored(self, entity_mappings, gold_0, computed_0, scorer_condition):
        """Summary

        Args:
            entity_mappings (TYPE): Description
            gold_0 (TYPE): Description
            computed_0 (TYPE): Description
            scorer_condition (TYPE): Description

        Returns:
            TYPE: Description
        """

        self.catch_data(entity_mappings, "get_scored", "entity_mappings", __file__)
        self.catch_data(gold_0, "get_scored", "gold_0", __file__)
        self.catch_data(computed_0, "get_scored", "computed_0", __file__)
        self.catch_data(scorer_condition, "get_scored", "scorer_condition", __file__)

        for gold_entry in sorted(gold_0, key=itemgetter("start")):
            gold_start = int(gold_entry["start"])
            gold_end = int(gold_entry["end"])
            gold_id = "{},{}".format(gold_start, gold_end)
            gold_url = gold_entry["key"].strip()
            gold_type = gold_entry["entity_type"].strip()
            gold_surface_form = gold_entry["surfaceForm"].strip()
            entity_mapping = [gold_id, False, 0, "fn"]

            for comp_entry in sorted(computed_0, key=itemgetter("document_start")):
                comp_start = int(comp_entry["document_start"])
                comp_end = int(comp_entry["document_end"])
                comp_url = comp_entry["key"].strip()
                comp_type = comp_entry["entity_type"].strip()
                comp_surface_form = comp_entry["surfaceForm"].strip()

                states = {
                    "same_url": gold_url == comp_url,
                    "same_type": gold_type == comp_type,
                    "same_surfaceForm": gold_surface_form == comp_surface_form,
                    "overlap": gold_end >= comp_start and gold_start <= comp_end,
                    "same_start": gold_start == comp_start,
                    "same_end": gold_end == comp_end
                }

                # multiline_logging(app, states)
                if all([states[condition] for condition in conditions[scorer_condition]]):
                    comp_id = f"{comp_start},{comp_end}"
                    entity_mapping[1] = comp_id
                    entity_mapping[2] += 1
                    entity_mapping[3] = states
                    gold_0.remove(gold_entry)
                    computed_0.remove(comp_entry)
                    break
                    """
                elif any([states[condition] for condition in conditions[scorer_condition]]):
                    score = self.calc_score(states)
                    comp_id = f"{comp_start},{comp_end}"
                    entity_mapping[1] = comp_id
                    entity_mapping[2] += score
                    entity_mapping[3] = states
                    gold_0.remove(gold_entry)
                    computed_0.remove(comp_entry)
                    break
                    """
                else:
                    continue

            entity_mappings.append(entity_mapping)

        self.catch_data(entity_mappings, "get_scored", "entity_mappings_1", __file__)
        self.catch_data(gold_0, "get_scored", "gold_0_1", __file__)
        self.catch_data(computed_0, "get_scored", "computed_0_1", __file__)

        return entity_mappings, gold_0, computed_0

    def calc_score(self, states):
        """
        noting yet...
        """
        right, wrong = 0, 0

        for k, v in states.items():
            if v:
                right += 1
            else:
                wrong += 1

        return 0

    def get_unscored(self, entity_mappings, computed_0):
        """Summary

        Args:
            entity_mappings (TYPE): Description
            computed_0 (TYPE): Description

        Returns:
            TYPE: Description
        """
        self.catch_data(entity_mappings, "get_unscored", "entity_mappings", __file__)
        self.catch_data(computed_0, "get_unscored", "computed_0", __file__)

        for comp_entry in sorted(computed_0, key=itemgetter("document_start")):

            comp_start = int(comp_entry["document_start"])
            comp_end = int(comp_entry["document_end"])
            comp_id = f"{comp_start},{comp_end}"
            entity_mapping = [False, comp_id, 0, "fp"]
            entity_mappings.append(entity_mapping)

        self.catch_data(entity_mappings, "get_unscored", "entity_mappings_1", __file__)
        self.catch_data(computed_0, "get_unscored", "computed_0_1", __file__)

        return entity_mappings, computed_0

    def get_confusion_matrix(self, entity_mappings):
        """Summary

        Args:
            entity_mappings (TYPE): Description

        Returns:
            TYPE: Description

        Raises:
            RuntimeError: Description
        """

        self.catch_data(entity_mappings, "get_confusion_matrix", "entity_mappings", __file__)

        confusion_matrix = {
            "tp": [],
            "fp": [],
            "fn": [],
            "tp_ids": [],
            "fp_ids": [],
            "fn_ids": [],
            "states": []
        }

        for gold, comp, num, state in entity_mappings:

            confusion_matrix["states"].append(state)

            if gold and comp:
                # logger.debug("TP: Gold: {}; Comp: {}; ({})".format(gold, comp, num))
                confusion_matrix["tp"].append(1)
                confusion_matrix["fp"].append(0)
                confusion_matrix["fn"].append(0)
                confusion_matrix["tp_ids"].append(comp)

            elif comp and not gold:
                # logger.debug("FP: Gold: {}; Comp: {}; ({})".format(gold, comp, num))
                confusion_matrix["tp"].append(0)
                confusion_matrix["fp"].append(1)
                confusion_matrix["fn"].append(0)
                confusion_matrix["fp_ids"].append(comp)

            elif gold and not comp:
                # logger.debug("FN: Gold: {}; Comp: {}; ({})".format(gold, comp, num))
                confusion_matrix["tp"].append(0)
                confusion_matrix["fp"].append(0)
                confusion_matrix["fn"].append(1)
                confusion_matrix["fn_ids"].append(gold)

            elif not gold and not comp:
                raise RuntimeError

            else:
                # print("Error")
                pass

        confusion_matrix["tp_sum"] = sum(confusion_matrix["tp"])
        confusion_matrix["fp_sum"] = sum(confusion_matrix["fp"])
        confusion_matrix["fn_sum"] = sum(confusion_matrix["fn"])

        self.catch_data(confusion_matrix, "get_confusion_matrix", "confusion_matrix", __file__)
        return confusion_matrix
