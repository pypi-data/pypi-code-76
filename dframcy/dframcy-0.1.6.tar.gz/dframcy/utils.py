from wasabi import Printer

messenger = Printer()


def get_default_columns():
    """
    Default columns for dataframe
    :return: list of default attributes
    """
    return ["id", "text", "start", "end", "pos_", "tag_", "dep_", "head", "ent_type_"]


def get_spacy_token_class_config():
    """
    Configuration of spacy's Token class attribute
    :return: config dictionary of attributes/properties
    """
    token_config = {
        "PROPERTIES": [
            "lefts",
            "rights",
            "n_lefts",
            "subtree",
            "children",
            "n_rights",
            "ancestors",
            "conjuncts",
            "has_vector",
            "is_sent_start",
        ],
        "ATTRIBUTES": [
            "text",
            "head",
            "pos_",
            "tag_",
            "dep_",
            "orth_",
            "norm_",
            "lang_",
            "lemma_",
            "lower_",
            "shape_",
            "is_oov",
            "ent_id_",
            "prefix_",
            "suffix_",
            "is_stop",
            "ent_iob_",
            "is_alpha",
            "is_ascii",
            "is_digit",
            "is_lower",
            "is_upper",
            "is_title",
            "is_punct",
            "is_space",
            "is_quote",
            "like_url",
            "like_num",
            "left_edge",
            "ent_type_",
            "right_edge",
            "ent_kb_id_",
            "is_bracket",
            "like_email",
            "is_currency",
            "is_left_punct",
            "is_right_punct",
        ],
        "ADDITIONAL_ATTRIBUTES": ["id", "start", "end"],
        "INT_FORMAT_ATTRIBUTES": [
            "pos",
            "tag",
            "dep",
            "orth",
            "norm",
            "lang",
            "lower",
            "shape",
            "ent_id",
            "prefix",
            "suffix",
            "ent_iob",
            "ent_type",
        ],
    }

    return token_config


def check_columns_consistency(columns):
    """
    Checks consistency of column names passed by users
    with spacy's Token class.
    :param columns: list of column names
    :return: list of consistent column names
    """
    spacy_token_config = get_spacy_token_class_config()
    consistent_column_names = []
    for column_name in columns:
        if column_name in spacy_token_config["PROPERTIES"]:
            consistent_column_names.append((column_name, "property"))
        elif column_name in spacy_token_config["ATTRIBUTES"]:
            consistent_column_names.append((column_name, "attribute"))
        elif column_name in spacy_token_config["ADDITIONAL_ATTRIBUTES"]:
            consistent_column_names.append((column_name, "additional_attribute"))
        elif column_name in spacy_token_config["INT_FORMAT_ATTRIBUTES"]:
            consistent_column_names.append((column_name, "int_format_attribute"))
        else:
            messenger.warn(
                "Column name '{}' not consistent with spacy's Token class".format(
                    column_name
                )
            )

    return consistent_column_names
