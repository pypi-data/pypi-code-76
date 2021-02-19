"""Summary
"""
from operator import itemgetter
import os
import re
import hashlib
from inscriptis import get_text

from .templates.js_arrow_key_navigation import js_arrow_key_navigation as js_arrow_key_navigation_template
from .templates.css_bootstrap import css_bootstrap as css_bootstrap_template
from .templates.js_bootstrap import js_bootstrap as js_bootstrap_template
from .templates.css_html import css_html as css_html_template
from .templates.js_navigation import js_navigation as js_navigation_template

from .templates.html_body import html_body as html_body_template
from .templates.navigation import navigation as navigation_template
from .templates.orbis_header import orbis_header as orbis_header_template
from .templates.item_header import item_header as item_header_template
from .templates.gold_corpus import gold_corpus as gold_corpus_template
from .templates.gold_entities import gold_entities as gold_entities_template
from .templates.predicted_corpus import predicted_corpus as predicted_corpus_template
from .templates.predicted_entities import predicted_entities as predicted_entities_template

from .templates.css_text_container import css_text_container as css_text_container_template
from .templates.css_color import css_color as css_color_template
from .templates.js_color import js_color as js_color_template
from .templates.js_popper import js_popper as js_popper_template

from .templates.js_dropdown import js_dropdown as js_dropdown_template
from .templates.css_dropdown import css_dropdown as css_dropdown_template


def get_hashid(url):
    hashid = f"i{int(hashlib.md5(url.encode('utf-8')).hexdigest(), 16)}"
    return hashid


def _add_annotation_colors(strings, hash_id, entry, annotations_colors):
    if "annotations" in entry:
        for annotation in entry["annotations"]:
            color = annotations_colors[annotation["type"]][annotation["entity"]]
            strings.add(f'.{annotation["type"]}#{hash_id} {{color: black; background-color: {color}}}')


def get_color_css(sf_colors, type_colors, annotations_colors, item, rucksack):
    strings = set()

    for entry in item['gold']:
        id_ = "{},{}".format(entry['start'], entry['end'])
        hash = get_hashid(id_)
        color = sf_colors[entry['key']]
        strings.add(f'.entities#{hash} {{color: black; background-color: {color}}}')
        _add_annotation_colors(strings, hash, entry, annotations_colors)

    if 'computed' in item and item['computed']:
        for entry in item['computed']:
            id_ = "{},{}".format(entry['document_start'], entry['document_end'])
            hash = get_hashid(id_)
            color = sf_colors[entry['key']]
            strings.add(f'.entities#{hash} {{color: black; background-color: {color}}}')
            _add_annotation_colors(strings, hash, entry, annotations_colors)

    for entry in item['gold']:
        id_ = "{},{}".format(entry['start'], entry['end'])
        hash = get_hashid(id_)
        color = type_colors[entry['entity_type']]
        strings.add(f'.types#{hash} {{color: black; background-color: {color}}}')

    if 'computed' in item and item['computed']:
        for entry in item['computed']:
            id_ = "{},{}".format(entry['document_start'], entry['document_end'])
            hash = get_hashid(id_)
            color = type_colors[entry['entity_type']]
            strings.add(f'.types#{hash} {{color: black; background-color: {color}}}')

    found = []
    classification_colors = {
        "TP": "#00FF00",
        "FP": "#FF00FF",
        "FN": "#FF0000"
    }
    if 'computed' in item and item['computed']:
        for computed_entry in item['computed']:

            computed_entry_id = "{},{}".format(computed_entry['document_start'], computed_entry['document_end'])

            fp_ids = rucksack.resultview(item['index'], specific="binary_classification")['confusion_matrix']['fp_ids']
            tp_ids = rucksack.resultview(item['index'], specific="binary_classification")['confusion_matrix']['tp_ids']
            fn_ids = rucksack.resultview(item['index'], specific="binary_classification")['confusion_matrix']['fn_ids']

            if computed_entry_id in fp_ids:
                classification = "FP"
            elif computed_entry_id in tp_ids:
                classification = "TP"
            elif computed_entry_id in fn_ids:
                classification = "FN"
            else:
                print(f"{computed_entry_id} not in fp: {fp_ids} tp: {tp_ids} fn: {fn_ids}")
                continue

            computed_hash = get_hashid(computed_entry_id)
            color = classification_colors[classification]
            strings.add(f'.results#{computed_hash} {{color: black; background-color: {color}}}')

            for gold_entry in item['gold']:
                gold_entry_id = "{},{}".format(gold_entry['start'], gold_entry['end'])

                if gold_entry_id == computed_entry_id:
                    gold_hash = get_hashid(gold_entry_id)
                    color = classification_colors[classification]
                    strings.add(f'.results#{gold_hash} {{color: black; background-color: {color}}}')
                    found.append(gold_entry_id)
                    continue

    for gold_entry in item["gold"]:
        gold_entry_id = "{},{}".format(gold_entry['start'], gold_entry['end'])
        gold_hash = get_hashid(gold_entry_id)
        if gold_entry_id not in found:
            color = "#808000"
            strings.add(f'.results#{gold_hash} {{color: black; background-color: {color}}}')

    colors = "\n".join(list(strings))
    return colors


def get_type_coloring():
    return ""


def get_score_coloring():
    return ""


def get_gold_entities(rucksack, item, gold_html, entity_types=False):
    """Summary

    Args:
        rucksack (TYPE): Description
        item (TYPE): Description
        gold_html (TYPE): Description
        entity_types (bool, optional): Description

    Returns:
        TYPE: gold_entities, gold_html
    """

    gold_entities = []

    if not item['gold'] or len(item['gold']) <= 0:
        return gold_entities, gold_html

    last_start = int(len(item['corpus']))
    last_end = int(len(item['corpus']))

    for entity in sorted(item['gold'], key=itemgetter("end"), reverse=True):
        entity_id = "{},{}".format(entity['start'], entity['end'])

        if entity_types and len(entity_types) > 0 and entity['entity_type'] not in entity_types:
            continue

        hashid = f'{get_hashid(entity_id)}'
        start_tag = f'<abbr title="{entity["key"]}" class="color entities" id="{hashid}">'
        end_tag = '</abbr>'

        entity_start = False
        if entity['start'] and int(entity['start']) <= int(last_start):
            if int(entity['start']) < int(last_end):
                entity_start = int(entity['start'])

        entity_end = False
        if entity['end'] and int(entity['end']) < int(last_end):
            if int(entity['end']) < int(last_start):
                entity_end = int(entity['end'])

        if isinstance(entity_start, int) and entity_end:
            gold_html = gold_html[:int(entity['end'])] + end_tag + gold_html[int(entity['end']):]
            gold_html = gold_html[:int(entity['start'])] + start_tag + gold_html[int(entity['start']):]
        else:
            if len(entity['key']) > 0:
                overlap_warning = '<abbr title="{}" class="color entities" id="{}"><b>&#x22C2;</b></abbr>'.format(
                    entity['key'],
                    hashid
                )
                gold_html = gold_html[:int(last_start)] + overlap_warning + gold_html[int(last_start):]

        last_start = entity_start or last_start
        last_end = entity_end or last_end

        gold_entities.append({
            "surfaceForm": entity['surfaceForm'],
            "key": entity['key'],
            "start": entity['start'],
            "end": entity['end'],
            "entity_type": entity['entity_type'],
            "hashid": hashid
        })

    return gold_entities, gold_html


def get_state_tag(is_fp, is_fn, is_tp):
    state_tag = ""
    if is_fp:
        state_tag = "FP"
    elif is_fn:
        state_tag = "FN"
    elif is_tp:
        state_tag = "TP"
    return state_tag


def get_predicted_entities(config, rucksack, item, predicted_html):
    """Summary

    Args:
        config (TYPE): Description
        rucksack (TYPE): Description
        item (TYPE): Description
        predicted_html (TYPE): Description

    Returns:
        TYPE: predicted_entities, predicted_html
    """
    predicted_entities = []

    if len(item['computed']) <= 0:
        return predicted_entities, predicted_html

    last_start = len(item['corpus'])
    last_end = len(item['corpus'])

    # logger.error(f"84: {item['computed']}")
    for e_idx, entity in enumerate(sorted(item['computed'], key=itemgetter("document_end"), reverse=True)):
        entity_types = config['scoring'].get('entities', [])

        if entity['entity_type'] not in entity_types and len(entity_types) > 0:
            continue

        is_fp = False
        entity_id = "{},{}".format(entity['document_start'], entity['document_end'])
        is_fp = True if entity_id in \
                        rucksack.resultview(item['index'], specific="binary_classification")['confusion_matrix'][
                            'fp_ids'] else False
        is_tp = True if entity_id in \
                        rucksack.resultview(item['index'], specific="binary_classification")['confusion_matrix'][
                            'tp_ids'] else False
        is_fn = True if entity_id in \
                        rucksack.resultview(item['index'], specific="binary_classification")['confusion_matrix'][
                            'fn_ids'] else False

        state_tag = get_state_tag(is_fp, is_fn, is_tp)
        hashid = get_hashid(entity_id)
        # print(hashid)

        if is_fp:
            start_tag = '<s><abbr title="{} ({})" class="color entities" id="{}">'.format(entity['key'], state_tag,
                                                                                          hashid)
            end_tag = '</abbr></s>'
        else:
            start_tag = '<abbr title="{} ({})" class="color entities" id="{}">'.format(entity['key'], state_tag, hashid)
            end_tag = '</abbr>'

        # print(start_tag)
        entity_start = False
        if int(entity['document_start']) <= int(last_start):
            if int(entity['document_start']) < int(last_end):
                entity_start = int(entity['document_start'])

        entity_end = False
        if int(entity['document_end']) < int(last_end):
            if int(entity['document_end']) < int(last_start):
                entity_end = int(entity['document_end'])

        if isinstance(entity_start, int) and entity_end:
            predicted_html = predicted_html[:int(entity['document_end'])] + end_tag + predicted_html[
                                                                                      int(entity['document_end']):]
            predicted_html = predicted_html[:int(entity['document_start'])] + start_tag + predicted_html[int(
                entity['document_start']):]
        else:
            if len(entity['key']) > 0:
                if is_fp:
                    overlap_warning = '<s><b><abbr title="{} ({})" class="color entities" id="{}">&#x22C2;</abbr></b></s>'.format(
                        entity['key'], state_tag, hashid)
                else:
                    overlap_warning = '<b><abbr title="{} ({})" class="color entities" id="{}">&#x22C2;</abbr></b>'.format(
                        entity['key'], state_tag, hashid)
                predicted_html = predicted_html[:int(last_start)] + overlap_warning + predicted_html[int(last_start):]

        last_start = entity_start or last_start
        last_end = entity_end or last_end

        predicted_entities.append({
            "surfaceForm": entity['surfaceForm'],
            "key": entity['key'],
            "start": entity['document_start'],
            "end": entity['document_end'],
            "entity_type": entity['entity_type'],
            "hashid": hashid,
            "state_tag": state_tag
        })

    return predicted_entities, predicted_html


def get_top_header(config, rucksack):
    """Summary

    Args:
        config (TYPE): Description
        rucksack (TYPE): Description

    Returns:
        TYPE: Description
    """
    if config['aggregation']['service']['name'] and config['evaluation']['name'] and config['scoring']['name']:
        top_header_0 = {
            "aggregator_name": config['aggregation']['service']['name'],
            "aggregator_profile": config['aggregation']['service'].get("profile", "None"),
            "aggregator_limit": config['aggregation']['service'].get("limit", "None"),
            "aggregator_location": config['aggregation']['service']['location']
        }

        top_header_1 = {
            "aggregator_data_set": config['aggregation']['input']['data_set']['name'],
            "evaluator_name": config['evaluation']['name'],
            "scorer_name": config['scoring']['name'],
            "entities": ", ".join([e for e in rucksack.result_summary(specific='binary_classification')['entities']])
        }

        top_header_2 = {
            "has_score": rucksack.result_summary(specific='binary_classification')['has_score'],
            "no_score": rucksack.result_summary(specific='binary_classification')['no_score'],
            "empty_responses": rucksack.result_summary(specific='binary_classification')['empty_responses']
        }

        micro_precision = f"{rucksack.result_summary(specific='binary_classification')['micro']['precision']:.3f}"
        macro_precision = f"{rucksack.result_summary(specific='binary_classification')['macro']['precision']:.3f}"
        micro_macro_precision = "(" + "/".join([str(micro_precision), str(macro_precision)]) + ")"
        micro_recall = f"{rucksack.result_summary(specific='binary_classification')['micro']['recall']:.3f}"
        macro_recall = f"{rucksack.result_summary(specific='binary_classification')['macro']['recall']:.3f}"
        micro_macro_recall = "(" + "/".join([str(micro_recall), str(macro_recall)]) + ")"
        micro_f1_score = f"{rucksack.result_summary(specific='binary_classification')['micro']['f1_score']:.3f}"
        macro_f1_score = f"{rucksack.result_summary(specific='binary_classification')['macro']['f1_score']:.3f}"
        micro_macro_f1_score = "(" + "/".join([str(micro_f1_score), str(macro_f1_score)]) + ")"

        top_header_3 = {
            "precision": micro_macro_precision,
            "recall": micro_macro_recall,
            "f1_score": micro_macro_f1_score,
        }
    else:
        top_header_0 = {
            "aggregator_name": None,
            "aggregator_profile": None,
            "aggregator_limit": None,
            "aggregator_location": None
        }

        top_header_1 = {
            "aggregator_data_set": None,
            "evaluator_name": None,
            "scorer_name": None,
            "entities": None
        }

        top_header_2 = {
            "has_score": None,
            "no_score": None,
            "empty_responses": None
        }
        top_header_3 = {
            "precision": None,
            "recall": None,
            "f1_score": None
        }

    header_html_0 = """
    <b>Aggregator Name:</b>\t{aggregator_name}</br>
    <b>Aggregator Profile:</b>\t{aggregator_profile}</br>
    <b>Aggregator Limit:</b>\t{aggregator_limit}</br>
    <b>Aggregator Service:</b>\t{aggregator_name}</br>
    """.format(**top_header_0)

    header_html_1 = """
    <b>Aggregator Dataset:</b>\t{aggregator_data_set}</br>
    <b>Evaluator Name:</b>\t{evaluator_name}</br>
    <b>Scorer Name:</b>\t{scorer_name}</br>
    <b>Entities:</b>\t{entities}</br>
    """.format(**top_header_1)

    header_html_2 = """
    <b>Some Score:</b>\t{has_score}</br>
    <b>No Score:</b>\t{no_score}</br>
    <b>Empty Responses:</b>\t{empty_responses}</br>
    """.format(**top_header_2)

    header_html_3 = """
    <b>Precision (micro/macro):</b>\t{precision}</br>
    <b>Recall (micro/macro):</b>\t{recall}</br>
    <b>F1 Score (micro/macro):</b>\t{f1_score}</br>
    """.format(**top_header_3)

    return header_html_0, header_html_1, header_html_2, header_html_3


def get_item_header(config, rucksack, key):
    """Summary

    Args:
        rucksack (TYPE): Description
        key (TYPE): Description

    Returns:
        TYPE: Description
    """
    if config['aggregation']['service']['name'] and config['evaluation']['name'] and config['scoring']['name']:
        item_header_0 = {
            "precision": rucksack.resultview(key, specific='binary_classification')['precision'],
            "recall": rucksack.resultview(key, specific='binary_classification')['recall'],
            "f1_score": rucksack.resultview(key, specific='binary_classification')['f1_score']
        }

        item_header_1 = {
            "tp": sum(rucksack.resultview(key, specific='binary_classification')['confusion_matrix']['tp']),
            "fp": sum(rucksack.resultview(key, specific='binary_classification')['confusion_matrix']['fp']),
            "fn": sum(rucksack.resultview(key, specific='binary_classification')['confusion_matrix']['fn'])
        }
    else:
        item_header_0 = {"precision": 0, "recall": 0, "f1_score": 0}
        item_header_1 = {"tp": None, "fp": None, "fn": None}

    header_html_0 = """
    <b>Precision:</b>\t{precision:.3f}</br>
    <b>Recall:</b>\t{recall:.3f}</br>
    <b>F1 Score:</b>\t{f1_score:.3f}</br>
    """.format(**item_header_0)

    header_html_1 = """
    <b>True Positives:</b>\t{tp}</br>
    <b>False Positives:</b>\t{fp}</br>
    <b>False Negatives:</b>\t{fn}</br>
    """.format(**item_header_1)
    return header_html_0, header_html_1


def get_gold_html(config, rucksack, item):
    """Summary

    Args:
        rucksack (TYPE): Description
        item (TYPE): Description

    Returns:
        TYPE: Description
    """
    gold_html = item['corpus']
    if config['aggregation']['service']['name'] and config['evaluation']['name'] and config['scoring']['name']:
        entity_types = rucksack.result_summary(specific='binary_classification')['entities']
    else:
        entity_types = False
    gold_entities, gold_html = get_gold_entities(rucksack, item, gold_html, entity_types)
    gold_entities_html = ""

    for entity in list(reversed(gold_entities)):
        gold_entities_html += '<p><span class="color entities" id="{hashid}"><b>{surfaceForm}</b></span> (<a href="{key}">{key}</a>): {start} - {end}: {entity_type}</p>'.format(
            **entity)

    return gold_html, gold_entities_html


def get_predicted_html(config, rucksack, item):
    """Summary

    Args:
        config (TYPE): Description
        rucksack (TYPE): Description
        item (TYPE): Description

    Returns:
        TYPE: Description
    """

    predicted_html = item['corpus']
    # logger.error(f"250: {item['computed']}")
    predicted_entities, predicted_html = get_predicted_entities(config, rucksack, item, predicted_html)
    predicted_entities_html = ""

    for entity in list(reversed(predicted_entities)):
        if entity["state_tag"] == "FP":
            predicted_entities_html += '<p><span class="color entities" id="{hashid}"><s><b>{surfaceForm}</b></s></span> (<a href="{key}">{key}</a>): {start} - {end}: {entity_type} ({state_tag})</p>'.format(
                **entity)
        else:
            predicted_entities_html += '<p><span class="color entities" id="{hashid}"><b>{surfaceForm}</b></span> (<a href="{key}">{key}</a>): {start} - {end}: {entity_type} ({state_tag})</p>'.format(
                **entity)

    return predicted_html, predicted_entities_html


def get_next_button(key):
    """Summary

    Args:
        key (TYPE): Description

    Returns:
        TYPE: Description
    """

    html = """<p><a id="next_page_link" class="btn btn-secondary" href="{url}" role="button" style="float: right;">Next Item &raquo;</a></p>"""
    url = os.path.join(str(key) + ".html")

    if key:
        next_button = html.format(url=url)
    else:
        next_button = ""

    return next_button


def get_previous_button(key):
    """Summary

    Args:
        key (TYPE): Description

    Returns:
        TYPE: Description
    """

    html = """<p><a id="previous_page_link" class="btn btn-secondary" href="{url}" role="button">&laquo; Previous Item</a></p>"""
    url = os.path.join(str(key) + ".html")

    if key:
        previous_button = html.format(url=url)
    else:
        previous_button = ""

    return previous_button


def get_js_annotation_code(annotations_colors):
    remove_classes = []
    click = []
    for annotations_color in annotations_colors:
        remove_active = f"$('#{annotations_color.lower()}_button').removeClass('active');\n"
        remove_annotation_class = f"$('.color').removeClass('{annotations_color}');\n"
        remove_classes.append(remove_active + remove_annotation_class)
        button_action = f'document.getElementById("{annotations_color.lower()}_button").onclick = function() {{ \n' \
                        f'removeClasses();\n $(\'.color\').addClass(\'{annotations_color}\') \n' \
                        f'$(\'#{annotations_color.lower()}_button\').addClass(\'active\')}} '
        click.append(button_action)

    return ' '.join(remove_classes), ' '.join(click)


def get_display_buttons(annotations_colors):
    display_button = []
    for annotations_color in annotations_colors:
        display_button.append(f'<button id="{annotations_color.lower()}_button" class="btn btn-secondary" '
                              f'type="button">{annotations_color}</button>')
    return " ".join(display_button)


def _prettify_with_inscriptis(html, text):
    inscriptis_text = get_text(html)
    text_split = text.split()
    new_text = []
    whitespace = re.split('([^\s]+)', inscriptis_text)
    index_of_whitespace = 0
    abbr_sequence = False
    exact_match = True
    for element in text_split:
        new_text.append(element)
        if not abbr_sequence and '<abbr' in element:
            abbr_sequence = True
            new_text.append(" ")
        elif abbr_sequence and '>' in element:
            exact_match = False
            abbr_sequence = False
        if not abbr_sequence:
            for x in range(index_of_whitespace, index_of_whitespace + 20):
                if (len(whitespace) > x + 1) and ((whitespace[x] == element and exact_match) or
                                              (whitespace[x] in element and not exact_match)):
                    new_text.append(whitespace[x + 1])
                    index_of_whitespace = x
                    break
        else:
            new_text.append(" ")
        if '</abbr>' in element:
            new_text.append(" ")
            exact_match = True
            abbr_sequence = False
    return "".join(new_text)


def build_blocks(config, rucksack, item, next_item, previous_item, sf_colors, type_colors, annotations_colors):
    """Summary

    Args:
        config (TYPE): Description
        rucksack (TYPE): Description
        item (TYPE): Description
        next_item (TYPE): Description
        previous_item (TYPE): Description
        sf_colors (TYPE): Description
        type_colors (TYPE): Description
        annotations_colors (TYPE): Description

    Returns:
        TYPE: Description
    """

    key = item['index']

    orbis_column_0, orbis_column_1, orbis_column_2, orbis_column_3 = get_top_header(config, rucksack)
    orbis_header = orbis_header_template.format(
        orbis_column_0=orbis_column_0,
        orbis_column_1=orbis_column_1,
        orbis_column_2=orbis_column_2,
        orbis_column_3=orbis_column_3
    )

    item_column_0, item_column_1 = get_item_header(config, rucksack, key)
    display_buttons = get_display_buttons(annotations_colors)
    item_header = item_header_template.format(
        item_number=key,
        display_buttons=display_buttons,
        item_column_0=item_column_0,
        item_column_1=item_column_1
    )

    gold_html, gold_entities_html = get_gold_html(config, rucksack, item)
    if "corpus_modified" in item and item["corpus_modified"]:
        gold_html = _prettify_with_inscriptis(item["corpus_modified"], gold_html)

    gold_corpus = gold_corpus_template.format(gold_html=gold_html)
    gold_entities = gold_entities_template.format(gold_entities_html=gold_entities_html)

    if config['aggregation']['service']['name']:
        predicted_html, predicted_entities_html = get_predicted_html(config, rucksack, item)

        if "corpus_modified" in item and item["corpus_modified"]:
            predicted_html = _prettify_with_inscriptis(item["corpus_modified"], predicted_html)

        predicted_corpus = predicted_corpus_template.format(predicted_html=predicted_html)
        predicted_entities = predicted_entities_template.format(predicted_entities_html=predicted_entities_html)
    else:
        predicted_corpus = ""
        predicted_entities = ""

    previous_button = get_previous_button(previous_item)
    next_button = get_next_button(next_item)
    navigation = navigation_template.format(prev=previous_button, next=next_button)

    color_css = css_color_template.format(get_color_css(sf_colors, type_colors, annotations_colors, item, rucksack))

    js_color = js_color_template.format(*get_js_annotation_code(annotations_colors))

    html_item_dict = {
        'orbis_header': orbis_header,
        'item_header': item_header,
        'gold_corpus': gold_corpus,
        'gold_entities': gold_entities,
        'predicted_corpus': predicted_corpus,
        'predicted_entities': predicted_entities,
        'navigation': navigation,
        'js_arrow_key_navigation': js_arrow_key_navigation_template,
        'css_bootstrap': css_bootstrap_template,
        'js_bootstrap': js_bootstrap_template,
        'css_html': css_html_template,
        'js_navigation': js_navigation_template,
        'css_text_container': css_text_container_template,
        'css_color': color_css,
        'js_color': js_color,
        'js_popper': js_popper_template,
        'js_dropdown': js_dropdown_template,
        'css_dropdown': css_dropdown_template
    }

    return html_item_dict


def build_page(html_item_dict):
    """Summary

    Args:
        html_item_dict (TYPE): Description

    Returns:
        TYPE: Description
    """
    html = html_body_template.format(**html_item_dict)
    return html


def build(config, rucksack, item, next_item, previous_item, sf_colors, type_colors, annotations_colors):
    """Summary

    Args:
        config (TYPE): Description
        rucksack (TYPE): Description
        item (TYPE): Description
        next_item (TYPE): Description
        previous_item (TYPE): Description
        sf_colors (TYPE): Description
        type_colors (TYPE): Description
        annotations_colors (TYPE): Description

    Returns:
        TYPE: Description
    """
    html_blocks = build_blocks(config, rucksack, item, next_item, previous_item, sf_colors, type_colors,
                               annotations_colors)
    html = build_page(html_blocks)
    return html, html_blocks
