"""Summary
"""
import os

from orbis_plugin_scoring_nel_scorer.main import Main


def load_data(file_name):
    local_dir = os.path.abspath("/".join(os.path.realpath(__file__).split("/")[:-1]))
    with open(local_dir + "/data/" + file_name) as open_file:
        content = eval(open_file.read())
    return content


def test_get_scored():
    """Summary
    """
    entity_mappings = load_data("get_scored_entity_mappings")
    gold_0 = load_data("get_scored_gold_0")
    computes_0 = load_data("get_scored_computed_0")
    scorer_conditions = load_data("get_scored_scorer_condition")

    main = Main()
    results = main.get_scored(
        entity_mappings,
        gold_0,
        computes_0,
        scorer_conditions
    )

    assert results[0] is load_data("get_scored_entity_mappings_1")
    assert results[1] is load_data("get_scored_gold_0_1")
    assert results[2] is load_data("get_scored_computed_0_1")


def test_get_unscored():
    """Summary
    """
    entity_mappings = None
    computed_0 = None
    main = Main()
    result = main.get_unscored(entity_mappings, computed_0)
    #assert result is None


def test_confusion_matrix():
    """Summary
    """
    entity_mappings = None
    main = Main()
    result = main.get_confusion_matrix(entity_mappings)
    #assert result is None


def test_run():
    """Summary
    """
    computed = None
    gold = None
    scorer_conditions = None
    main = Main()
    result = main.run(computed, gold, scorer_conditions)
    #assert result is None
