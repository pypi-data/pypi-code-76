from hemlock import Embedded, Page, Label, Select, Debug as D, Validate as V
from sqlalchemy_mutable import partial

import os
from random import choice, shuffle

try:
    from yaml import load, CLoader as Loader
except:
    from yaml import load, Loader

dir_path = os.path.dirname(os.path.realpath(__file__))
versions = {
    'IPIP-50': load(
        open(os.path.join(dir_path, 'ipip50.yaml')), Loader=Loader
    ),
    'TIPI': load(
        open(os.path.join(dir_path, 'tipi.yaml')), Loader=Loader
    ),
    'BFI-10': load(
        open(os.path.join(dir_path, 'bfi10.yaml')), Loader=Loader
    )
}

instructions_label = 'How accurately do the following statements describe you?'

trait_abbreviations = {
    'E': 'Extraversion',
    'A': 'Agreeableness',
    'C': 'Conscientiousness',
    'N': 'Neuroticism',
    'O': 'Openness'
}

choice_labels_5 = [
    '1. Very inaccurate',
    '2. Moderately inaccurate',
    '3. Neither accurate nor inaccurate',
    '4. Moderately accurate',
    '5. Very accurate'
]

choice_labels_7 = [
    '1. Very inaccurate',
    '2. Moderately inaccurate',
    '3. Slightly inaccurate',
    '4. Neither accurate nor inaccurate',
    '5. Slightly accurate',
    '6. Moderately accurate',
    '7. Very accurate'
]

def big5(
        *items, version='IPIP-50', page=False, require=False, 
        choice_labels=5, include_instructions=True, shuffle_items=False, 
        record_index=False
    ):
    """
    Create a big 5 personality questionnaire.

    Parameters
    ----------
    \*items :
        Names of big 5 items to include. If no items are specified, this 
        function returns all big 5 items in the given version.

    version : str, default='IPIP-50'
        Version of the big 5 questionnaire. Currently supported are 
        `'IPIP-50'` (50-item version from the Interntaional Personality Item 
        Pool), `'TIPI'` (Ten-Item Personality Inventory), and `'BFI-10'` 
        (10-item Big 5 Inventory).

    page : bool, default=False
        Indicates that this function should return a page with the big 5 
        items. Otherwise, return a list of questions.

    require : bool, default=False
        Indicates that responses are required (for all items).

    choice_labels : int or list, default=5
        List of strings for the choice labels participants can select. May 
        also be `5` or `7` for 5 or 7 default labels.

    include_instructions : bool, default=True
        Indicates that an instructions label should be included before the 
        items.

    shuffle_items : bool, default=False
        Indicates that items should be shuffled.

    record_index : bool, default=False
        Indicates to record the index of the big 5 items as they appear on the 
        page. Only applies of `page` is `True`.

    Returns
    -------
    big5_questionnaire : hemlock.Page or list of hemlock.Question
        If `page` is `True`, this function returns a page containing the 
        requested big 5 items. Otherise, it returns a list of questions.
    """
    def get_choice_labels(choice_labels):
        # generate a list of choice labels
        assert isinstance(choice_labels, (int, list)), 'choice_labels must be int (5 or 7) or list of strings'
        if choice_labels == 5:
            return choice_labels_5
        if choice_labels == 7:
            return choice_labels_7
        return choice_labels

    def gen_question(item):
        # generates a question for a given big 5 item
        _, label, ascending = item_bank[item]
        values = list(range(1, len(choice_labels)+1))
        if not ascending:
            values.sort(reverse=True)
        random_choice = choice(values) if require else choice(values+[''])
        choices = [''] + list(zip(choice_labels, values))
        return Select(
            label,
            choices,
            var='Big5'+item, data_rows=-1, record_index=record_index,
            validate=V.require() if require else None,
            debug=D.click_choices(random_choice)
        )

    item_bank = _get_item_bank(version)
    if not items:
        items = item_bank.keys()
    choice_labels = get_choice_labels(choice_labels)
    questions = [gen_question(item) for item in items]
    if shuffle_items:
        shuffle(questions)
    if include_instructions:
        questions.insert(0, Label(instructions_label))
    if page:
        return Page(
            *questions,
            name='Big5',
            timer=('Big5Time', -1),
            submit=partial(_record_score, item_bank)
        )
    return questions

def _record_score(page, item_bank):
    # records the aggregate score for each personality trait
    scores = {}
    questions = [q for q in page.questions if q.var and (q.data != '')]
    for q in questions:
        trait = item_bank[q.var[len('Big5'):]][0]
        if trait not in scores:
            scores[trait] = []
        scores[trait].append(q.data)
    page.embedded = [
        Embedded(
            trait_abbreviations[trait], 
            sum(score)/float(len(score)), 
            data_rows=-1
        ) 
        for trait, score in scores.items()
    ]

def big5_traits(*traits, version='IPIP-50', **kwargs):
    """
    Create a big 5 personality questionnaire for specified personality traits.

    Parameters
    ----------
    \*traits : 
        Strings of requested traits, `'E'` for extraversion, `'A'` for 
        agreeableness, `'C'` for conscientiousness, `'N'` for neuroticism, 
        `'O'` for openness.

    version : str, default='IPIP-50'
        Version of the big 5 questionnaire.

    \*\*kwargs :
        Keyword arguments are passed to `big5`.

    Returns
    -------
    big5_questionnaire : hemlock.Page or list of hemlock.Question
        If `page` is `True`, this function returns a page containing the 
        requested big 5 items. Otherise, it returns a list of questions.
    """
    assert all([trait in 'EACNO' for trait in traits]), 'Traits must be one of "E", "A", "C", "N", "O"'
    item_bank = _get_item_bank(version)
    item_bank = {
        key: val for key, val in item_bank.items() if val[0] in traits
    }
    obj = big5(version=item_bank, **kwargs)
    if isinstance(obj, Page):
        obj.name = 'Big5 '+' '.join(traits)
        obj.timer.var = 'Big5'+''.join(traits)+'Timer'
    return obj

def _get_item_bank(version):
    """
    Get big 5 items.

    Returns a dict mapping variable names to a (trait, label, ascending) 
    tuple. Trait is one of 'E', 'A', 'C', 'N', 'O'. Label is the question 
    label. Ascending indicates that score is ascending in choices (i.e., 
    opposite of reverse coding).
    """
    assert isinstance(version, (str, dict)), 'version must by str or dict'
    if isinstance(version, str):
        assert version in versions.keys(), "When passing version as str, must be one of "+str(versions.keys())
        return versions[version]
    return version