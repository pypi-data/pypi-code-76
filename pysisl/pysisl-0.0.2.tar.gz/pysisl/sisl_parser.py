# Copyright PA Knowledge Ltd 2021

from .parser_error import ParserError


def p_sisl_object(p):
    """sisl_object : BEGIN_OBJECT sisl_triplets END_OBJECT """
    p[0] = p[2]


def p_sisl_triplets(p):
    """sisl_triplets : empty_triplet
                     | sisl_triplet
                     | sisl_triplet_list """
    p[0] = p[1]


def p_empty_triplet(p):
    """ empty_triplet : """
    p[0] = {}


def p_sisl_triplet(p):
    """ sisl_triplet : NAME type_and_value """
    p[0] = {p[1]: p[2]}


def p_type_and_value(p):
    """ type_and_value : type value """
    p[0] = dict(p[1], **p[2])


def p_type(p):
    """ type : TYPE """
    p[0] = {"type": p[1]}


def p_value(p):
    """ value : VALUE
              | sisl_object """
    p[0] = {"value": p[1]}


def p_sisl_triplet_list(p):
    """ sisl_triplet_list : sisl_triplet LIST_SEPARATOR sisl_triplets """
    p[0] = {**p[1], **p[3]}


def p_error(p):
    raise ParserError(p)
