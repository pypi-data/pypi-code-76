# encoding: utf-8
"""
TODO: Translation work to do...
TODO: Cleaning and testing work to do...
"""

import os
import re
import time

from behave import given, then, when
from bs4 import BeautifulSoup
from klity.features.steps.steps_utils import get_value
from selenium.webdriver import ActionChains
from slugify import slugify

DEBUG = True


def print_debug(message):
    if DEBUG:
        print(message)


########################################################################################
# Given
########################################################################################
@given(u'I visit "{url}"')
@given(u'que je visite le site "{url}"')
@given(u'que je visite l\'url "{url}"')
def step_impl(context, url):
    url = get_value(context, url)
    context.browser.get(url)


########################################################################################
# When
########################################################################################
@when(u'je clique sur le bouton "{value}"')
@when(u'que je clique sur le bouton "{value}"')
def step_impl(context, value):
    value = get_value(context, value)
    element = find_button(context, value)
    element.click()


@when(u'je sélectionne la valeur "{value}" du champ "{field}"')
@when(u'que je sélectionne la valeur "{value}" du champ "{field}"')
def step_impl(context, value, field):
    value = get_value(context, value)
    field = get_value(context, field)
    # For select tag
    try:
        element = find_option(context, field, value)
    except:
        print_debug("Selet is not working, trying with radio buttons")
        # For radio button
        element = find_radio_button(context, field, value)
    element.click()


@when(u'je clique sur le lien "{value}"')
@when(u'que je clique sur le lien "{value}"')
def step_impl(context, value):
    value = get_value(context, value)
    element = find_link(context, value)
    element.click()


@when(u'je clique sur l\'élément contenant "{value}"')
@when(u'que je clique sur l\'élément contenant "{value}"')
def step_impl(context, value):
    value = get_value(context, value)
    element = find_element(context, value)
    element.click()


@when(u'je vide le champ "{field}"')
@when(u'que je vide le champ "{field}"')
@when(u'je tape "" dans le champ "{field}"')
@when(u'que je tape "" dans le champ "{field}"')
@when(u'je tape "{value}" dans le champ "{field}"')
@when(u'que je tape "{value}" dans le champ "{field}"')
def step_impl(context, field, value=""):
    value = get_value(context, value)
    field = get_value(context, field)
    element = find_input(context, field)
    if element is None:
        assert False, "Elément %s non trouvé" % field
    element.clear()
    if value != "":
        element.send_keys(value)


@when(u'je tape ""')
@when(u'que je tape ""')
@when(u'je tape "{value}"')
@when(u'que je tape "{value}"')
def step_impl(context, value=""):
    value = get_value(context, value)
    if value != "":
        actions = ActionChains(context.browser)
        actions.send_keys(value)
        actions.perform()


@when(u'je clique sur le bouton radio "{value}"')
@when(u'que je clique sur le bouton radio "{value}"')
def step_impl(context, value):
    value = get_value(context, value)
    element = find_radio_button(context, "", value)
    if not element.is_selected():
        element.click()


@when(u'je coche la case à cocher "{value}"')
@when(u'que je coche la case à cocher "{value}"')
def step_impl(context, value):
    value = get_value(context, value)
    element = find_checkbox(context, value)
    if not element.is_selected():
        element.click()


@when(u'je décoche la case à cocher "{value}"')
@when(u'que je décoche la case à cocher "{value}"')
def step_impl(context, value):
    value = get_value(context, value)
    element = find_checkbox(context, value)
    if element.is_selected():
        element.click()


@when(u'je sélectionne le fichier "{filename}" dans le champ "{field}"')
@when(u'que je sélectionne le fichier "{filename}" dans le champ "{field}"')
def select_file(context, filename, field):
    filename = get_value(context, filename)
    field = get_value(context, field)
    filepath = find_file(filename, os.getcwd())
    if os.path.isfile(filepath):
        element = find_input(context, field)
        element.clear()
        element.send_keys(filepath)


@when(u'je sélectionne le fichier "{filename}" dans le champ invisible "{field}"')
@when(u'que je sélectionne le fichier "{filename}" dans le champ invisible "{field}"')
def step_impl(context, filename, field):
    filename = get_value(context, filename)
    field = get_value(context, field)
    filepath = find_file(filename, os.getcwd())
    if os.path.isfile(filepath):
        element = find_input(context, field, False)
        element.clear()
        element.send_keys(filepath)


@when(u'j\'attends un élément contenant "{value}"')
@when(u'que j\'attends un élément contenant "{value}"')
def step_impl(context, value):
    value = get_value(context, value)
    start = time.perf_counter()
    while True:
        if (time.perf_counter() - start) > 10:
            assert False, "Timeout"
        if find_element(context, value) is not None:
            return
        time.sleep(0.1)


########################################################################################
# Then
########################################################################################
@then(u'le titre de la page contient "{text}"')
def step_impl(context, text):
    text = get_value(context, text)
    assert text in context.browser.title


@then(u'le titre de la page est "{text}"')
def step_impl(context, text):
    text = get_value(context, text)
    assert text == context.browser.title


@then(u'page contains "{text1}"')
@then(u'la page contient "{text1}"')
@then(u'la page contient "{text1}" ou "{text2}"')
def step_impl(context, text1, text2=""):
    text1 = get_value(context, text1)
    text2 = get_value(context, text2)
    print(text1)
    try:
        content = re.sub(
            "[ \n\t]+", " ", BeautifulSoup(context.browser.page_source, "lxml").text
        )
        if text2 != "":
            assert (text1 in content) or (text2 in content)
        else:
            assert text1 in content
    except:
        if text2 != "":
            assert False, "Textes non trouvés: %s - %s" % (text1, text2)
        else:
            print(content)
            assert False, "Texte non trouvé: %s" % text1


@then(u'la page ne contient pas "{text1}"')
def step_impl(context, text1):
    text1 = get_value(context, text1)
    try:
        content = re.sub(
            "[ \n\t]+", " ", BeautifulSoup(context.browser.page_source, "lxml").text
        )
        assert text1 not in content
    except:
        print_debug(content)
        assert False, "Texte trouvé: %s" % text1


@then(u'le titre de l\'élément "{element}" est "{text}"')
def step_impl(context, element, text):
    element = get_value(context, element)
    text = get_value(context, text)
    element = find_element(context, element, False)
    if element.get_attribute("title") != text:
        assert False, "Texte %s non trouvé pour l'élément %s (%s)" % (
            text,
            element,
            element.get_attribute("title"),
        )


@then(u'le titre de l\'élément qui contient "{element}" est "{text}"')
def step_impl(context, element, text):
    element = get_value(context, element)
    text = get_value(context, text)
    element = find_element(context, element, False)
    if element.get_attribute("title") != text:
        assert False, "Texte %s non trouvé pour l'élément %s" % (text, element)


@then(u'le titre du champ "{field}" est "{text}"')
def step_impl(context, field, text):
    text = get_value(context, text)
    field = get_value(context, field)
    element = find_input(context, field, False)
    assert element.get_attribute("title") == get_value(context, text)


@then(u'le champ "{field}" est vide')
@then(u'le champ "{field}" contient "{text}"')
def step_impl(context, field, text=""):
    text = get_value(context, text)
    field = get_value(context, field)
    element = find_input(context, field, False)
    print(element.get_attribute("value"))
    assert get_value(context, text) in element.get_attribute("value")


@then(u'le champ "{field}" ne contient pas "{text}"')
def step_impl(context, field, text=""):
    text = get_value(context, text)
    field = get_value(context, field)
    element = find_input(context, field, False)
    assert get_value(context, text) not in element.get_attribute("value")


@then(u'le champ "{field}" n\'est pas vide')
def step_impl(context, field):
    field = get_value(context, field)
    element = find_input(context, field, False)
    assert element.get_attribute("value") != ""


@then(u'le champ "{field}" contient "{nombre}" caractères')
def step_impl(context, field, nombre):
    field = get_value(context, field)
    nombre = get_value(context, nombre)
    element = find_input(context, field, False)
    if element.tag_name == "textarea":
        assert len(element.text) == int(nombre)
    else:
        assert len(element.get_attribute("value")) == int(nombre)


@then(u'le champ "{field}" contient moins de "{nombre}" caractères')
def step_impl(context, field, nombre):
    field = get_value(context, field)
    nombre = get_value(context, nombre)
    element = find_input(context, field, False)
    if element.tag_name == "textarea":
        assert len(element.text) < int(nombre)
    else:
        assert len(element.get_attribute("value")) < int(nombre)


@then(u'le champ "{field}" contient plus de "{nombre}" caractères')
def step_impl(context, field, nombre):
    field = get_value(context, field)
    nombre = get_value(context, nombre)
    element = find_input(context, field, False)
    if element.tag_name == "textarea":
        assert len(element.text) > int(nombre)
    else:
        assert len(element.get_attribute("value")) > int(nombre)


@then(u'le champ "{field}" contient entre "{nombre_min}" et "{nombre_max}" caractères')
def step_impl(context, field, nombre_min, nombre_max):
    field = get_value(context, field)
    nombre_min = get_value(context, nombre_min)
    nombre_max = get_value(context, nombre_max)
    # TODO: This part is to be tested
    if element.tag_name == "textarea":
        assert int(nombre_min) <= len(element.text) <= int(nombre_max)
    else:
        assert int(nombre_min) <= len(element.get_attribute("value")) <= int(nombre_max)


@then(u'le champ "{field}" contient l\'option "{value}"')
@then(u'le champ "{field}" contient l\'option ""')
def step_impl(context, field, value=""):
    field = get_value(context, field)
    value = get_value(context, value)
    element = find_option(context, field, value)
    # print_debug(element)
    assert element is not None


@then(u'le champ "{field}" ne contient pas l\'option "{value}"')
@then(u'le champ "{field}" ne contient pas l\'option ""')
def step_impl(context, field, value=""):
    field = get_value(context, field)
    value = get_value(context, value)
    # For select tag
    try:
        element = find_option(context, field, value)
        if element is not None:
            assert False, 'l\'option "%s" du champ "%s" a été trouvée' % (value, field,)
    except:
        assert True


@then(u'l\'option "{value}" du champ "{field}" est sélectionnée')
@then(u'l\'option "" du champ "{field}" est sélectionnée')
def step_impl(context, field, value=""):
    field = get_value(context, field)
    value = get_value(context, value)
    # For select tag
    try:
        element = find_option(context, field, value)
    except:
        print_debug("On essaye autre chose ?")
        # For radio button
        element = find_radio_button(context, field, value, False)
    assert element.is_selected()


@then(u'la case à cocher "{field}" est cochée')
def step_impl(context, field):
    field = get_value(context, field)
    assert find_checkbox(context, field, False).is_selected()


@then(u'la case à cocher "{field}" n\'est pas cochée')
@then(u'la case à cocher "{field}" est décochée')
def step_impl(context, field):
    field = get_value(context, field)
    element = find_checkbox(context, field, False)
    try:
        assert not element.is_selected()
    except AttributeError:
        # no "is_selected"
        assert True


@then(u'je clique sur le bouton "{value}"')
@then(u'que je clique sur le bouton "{value}"')
def step_impl(context, value):
    value = get_value(context, value)
    element = find_button(context, value, False)
    element.click()


@then(u'je clique sur le lien "{value}"')
@then(u'que je clique sur le lien "{value}"')
def step_impl(context, value):
    value = get_value(context, value)
    find_link(context, value, False).click()


@then(u'le champ "{field}" existe')
def step_impl(context, field):
    field = get_value(context, field)
    try:
        element = find_input(context, field, False)
        assert element is not None
    except:
        assert False, "Champ non trouvé: %s" % field


@then(u'le champ "{field}" n\'existe pas')
def step_impl(context, field):
    field = get_value(context, field)
    element = None
    try:
        element = find_input(context, field, False)
    except:
        pass
    if element is not None:
        assert False, "Champ trouvé: %s" % field


@then(u'le tableau contient "{nombre}" colonnes')
def step_impl(context, nombre):
    tableau = get_table(context)
    if tableau is None:
        assert False, "Tableau non trouvé"

    nombre = get_value(context, nombre)
    if len(tableau["colonnes"]) == int(nombre):
        assert True
    else:
        assert False, "Le tableau contient %d colonnes au lieu de %d" % (
            len(tableau["colonnes"]),
            int(nombre),
        )


@then(u'le tableau contient "{nombre}" lignes')
def step_impl(context, nombre):
    tableau = get_table(context)
    if tableau is None:
        assert False, "Tableau non trouvé"

    nombre = get_value(context, nombre)
    if len(tableau["lignes"]) == int(nombre):
        assert True
    else:
        assert False, "Le tableau contient %d lignes au lieu de %d" % (
            len(tableau["lignes"]),
            int(nombre),
        )


@then(u'le tableau contient moins de "{nombre}" lignes')
def step_impl(context, nombre):
    tableau = get_table(context)
    if tableau is None:
        assert False, "Tableau non trouvé"

    nombre = get_value(context, nombre)
    if len(tableau["lignes"]) <= int(nombre):
        assert True
    else:
        assert False, "Le tableau contient %d lignes au lieu de moins de %d" % (
            len(tableau["lignes"]),
            int(nombre),
        )


@then(u'la ligne "{index}" de la colonne "{colonne}" du tableau contient "{value}"')
@then(u'la ligne "{index}" de la colonne "{colonne}" du tableau contient ""')
@then(u'la ligne "{index}" de la colonne "{colonne}" du tableau est vide')
def step_impl(context, index, colonne, value=""):
    tableau = get_table(context)
    if tableau is None:
        assert False, "Tableau non trouvé"

    index = int(get_value(context, index)) - 1
    colonne = get_value(context, colonne)
    value = get_value(context, value)
    try:
        col_index = tableau["colonnes"].index(colonne)
    except:
        assert False, "La colonne %s n'existe pas dans le tableau" % colonne

    if len(tableau["lignes"]) <= index:
        assert False, (
            "Le numéro de ligne est trop grand pour le tableau. Celui-ci ne contient que %d lignes"
            % len(tableau["lignes"])
        )

    if tableau["lignes"][index][col_index] != value:
        assert False, "La cellule (%d,%d) du tableau contient %s au lieu de %s" % (
            index + 1,
            col_index,
            tableau["lignes"][index][col_index],
            value,
        )


@then(u'la ligne "{index}" de la colonne "{colonne}" du tableau n\'est pas vide')
def step_impl(context, index, colonne):
    tableau = get_table(context)
    if tableau is None:
        assert False, "Tableau non trouvé"

    index = int(get_value(context, index)) - 1
    colonne = get_value(context, colonne)
    try:
        col_index = tableau["colonnes"].index(colonne)
    except:
        assert False, "La colonne %s n'existe pas dans le tableau" % colonne

    if len(tableau["lignes"]) <= index:
        assert False, (
            "Le numéro de ligne est trop grand pour le tableau. Celui-ci ne contient que %d lignes"
            % len(tableau["lignes"])
        )

    if tableau["lignes"][index][col_index] == "":
        assert False, "La cellule (%d,%d) du tableau n'est pas vide et contient %s" % (
            index + 1,
            col_index,
            tableau["lignes"][index][col_index],
        )


@then(u'la colonne "{colonne}" du tableau est triée dans l\'ordre {order}')
def step_impl(context, colonne, order):
    tableau = get_table(context)
    if tableau is None:
        assert False, "Tableau non trouvé"

    colonne = get_value(context, colonne)
    order = get_value(context, order)
    if order not in (
        "croissant",
        "décroissant",
        "decroissant",
        "alphabétique",
        "alphabétique inverse",
        "alphabetique",
        "alphabetique inverse",
    ):
        raise NotImplementedError
    try:
        col_index = tableau["colonnes"].index(colonne)
    except:
        assert False, "La colonne %s n'existe pas dans le tableau" % colonne
    # Getting values of specified column
    ligne = []
    for i in range(len(tableau["lignes"])):
        ligne.append(slugify(tableau["lignes"][i][col_index]).replace("-", ""))
    if order in ("croissant", "alphabétique", "alphabetique"):
        if not all(ligne[i] <= ligne[i + 1] for i in range(len(ligne) - 1)):
            old_item = ligne[0]
            for item in ligne:
                if old_item > item:
                    print("%s > %s" % (old_item, item))
                old_item = item
            assert False, "Le contenu de la colonne %s n'est pas dans l'ordre %s" % (
                colonne,
                order,
            )
    else:
        if not all(ligne[i] >= ligne[i + 1] for i in range(len(ligne) - 1)):
            old_item = ligne[0]
            for item in ligne:
                if old_item < item:
                    print("%s < %s" % (old_item, item))
                old_item = item
            assert False, "Le contenu de la colonne %s n'est pas dans l'ordre %s" % (
                colonne,
                order,
            )


@then(u'le bouton "{value}" existe')
def step_impl(context, value):
    value = get_value(context, value)
    element = find_button(context, value)
    assert element is not None


@then(u'le bouton "{value}" n\'existe pas')
def step_impl(context, value):
    value = get_value(context, value)
    try:
        find_button(context, value)
    except AssertionError:
        assert True


########################################################################################
# Utilities
########################################################################################
def get_element_by_xpath(context, selector):
    return context.browser.find_element_by_xpath(selector)


def get_elements_by_xpath(context, selector):
    return context.browser.find_elements_by_xpath(selector)


def get_element_by_css(context, selector):
    return context.browser.find_element_by_css_selector(selector)


def get_elements_by_css(context, selector):
    return context.browser.find_elements_by_css_selector(selector)


def normalize_for_xpath(value):
    if "'" in value:
        values = value.split("'")
        result = "concat("
        for val in values:
            result += "'%s', " % val
            result += '"\'", '
        new_value = result[:-7] + ")"
    else:
        new_value = "'%s'" % value
    print("Normalization : %s" % new_value)
    return new_value


def normalize_for_css(value):
    if "'" in value:
        return "'%s'" % value.replace("'", "\\'")
    return "'%s'" % value


def get_first_visible_element(elements):
    print_debug(" => %d élements transmis" % len(elements))
    for element in elements:
        print_debug(" ID: %s" % element.get_attribute("id"))
        print_debug(" displayed: %s" % element.is_displayed())
        print_debug(" invisible: %s" % element.get_attribute("class").lower())
        if (
            element.is_displayed()
            and "invisible" not in element.get_attribute("class").lower()
        ):
            print_debug(" élément visible")
            return element


def is_element_exists(context, value):
    try:
        context.browser.find_element_by_id(value)
    except:
        try:
            context.browser.find_element_by_name(value)
        except:
            try:
                get_element_by_xpath(
                    context, "//*[title=%s]" % normalize_for_xpath(value)
                )
            except:
                try:
                    get_element_by_xpath(
                        context,
                        "//*[contains(normalize-space(.),%s)]"
                        % normalize_for_xpath(value),
                    )
                except:
                    return False
    return True


def find_element(context, value, visible=True):
    elements = get_elements_by_xpath(
        context,
        "//*[not(self::p) and not(self::div) and not(self::li) and normalize-space()=%s]"
        % normalize_for_xpath(value),
    )
    if elements == []:
        elements = get_elements_by_css(context, "[id=%s]" % normalize_for_css(value))
        if elements == []:
            elements = get_elements_by_css(
                context, "[name=%s]" % normalize_for_css(value)
            )
            if elements == []:
                elements = get_elements_by_css(
                    context, "[value=%s]" % normalize_for_css(value)
                )
                if elements == []:
                    elements = get_elements_by_xpath(
                        context,
                        "//*[normalize-space()=%s]" % normalize_for_xpath(value),
                    )

    if elements == []:
        return None
    if visible:
        return get_first_visible_element(elements)
    return elements[0]


def find_button(context, value, visible=True):
    elements = context.browser.find_elements_by_id(value)
    if elements == []:
        elements = context.browser.find_elements_by_name(value)
        if elements == []:
            elements = get_elements_by_xpath(
                context,
                "//*[(self::button or self::input or self::img) and normalize-space(.)=%s]"
                % normalize_for_xpath(value),
            )
            print("//*[(self::button or self::input or self::img) and normalize-space(.)=%s]"
                % normalize_for_xpath(value))
            print(elements)
            if elements == []:
                elements = get_elements_by_xpath(
                    context,
                    "//*[(self::button or self::input or self::img) and contains(.,%s)]"
                    % normalize_for_xpath(value),
                )
                print("//*[(self::button or self::input or self::img) and contains(.,%s)]"
                    % normalize_for_xpath(value))
                print(elements)
                if elements == []:
                    elements = get_elements_by_xpath(
                        context,
                        "//*[(self::button or self::input or self::img) and normalize-space(@value)=%s]"
                        % normalize_for_xpath(value),
                    )
                    if elements == []:
                        elements = get_elements_by_xpath(
                            context,
                            "//*[(self::button or self::input or self::img) and normalize-space(@title)=%s]"
                            % normalize_for_xpath(value),
                        )
                        if elements == []:
                            elements = get_elements_by_xpath(
                                context,
                                "//*[(self::button or self::input or self::img) and normalize-space()=%s]"
                                % normalize_for_xpath(value),
                            )
                            if elements == []:
                                elements = get_elements_by_xpath(
                                    context,
                                    "//*[self::a and normalize-space(@value)=%s]"
                                    % normalize_for_xpath(value),
                                )
                                if elements == []:
                                    elements = get_elements_by_xpath(
                                        context,
                                        "//*[self::a and normalize-space(@title)=%s]"
                                        % normalize_for_xpath(value),
                                    )
                                    if elements == []:
                                        elements = get_elements_by_xpath(
                                            context,
                                            "//*[self::a and normalize-space()=%s]"
                                            % normalize_for_xpath(value),
                                        )
                                        if elements == []:
                                            assert False, "Bouton %s non trouvé" % value

    print(elements)

    if visible:
        return get_first_visible_element(elements)
    return elements[0]


def find_option(context, field, value):
    try:
        label_for = find_label(context, field).get_attribute("for")
        if label_for != "":
            element = get_element_by_xpath(
                context,
                "//select[@id=%s]/option[contains(normalize-space(.),%s)]"
                % (normalize_for_xpath(label_for), normalize_for_xpath(value),),
            )
    except:
        try:
            element = get_element_by_xpath(
                context,
                "//select[@id=%s]/option[contains(normalize-space(.),%s)]"
                % (normalize_for_xpath(field), normalize_for_xpath(value),),
            )
        except:
            try:
                element = get_element_by_css(
                    context,
                    "select[id=%s]>option[value=%s]"
                    % (normalize_for_css(field), normalize_for_css(value),),
                )
            except:
                try:
                    element = get_element_by_css(
                        context,
                        "select[id=%s]>option[title=%s]"
                        % (normalize_for_css(field), normalize_for_css(value),),
                    )
                except:
                    try:
                        element = get_element_by_xpath(
                            context,
                            "//select[@name=%s]/option[contains(normalize-space(.),%s)]"
                            % (normalize_for_xpath(field), normalize_for_xpath(value),),
                        )
                    except:
                        try:
                            element = get_element_by_css(
                                context,
                                "select[name=%s]>option[value=%s]"
                                % (normalize_for_css(field), normalize_for_css(value),),
                            )
                        except:
                            try:
                                element = get_element_by_css(
                                    context,
                                    "select[name=%s]>option[title=%s]"
                                    % (
                                        normalize_for_css(field),
                                        normalize_for_css(value),
                                    ),
                                )
                            except:
                                assert False, "Elément %s de la liste %s non trouvé" % (
                                    value,
                                    field,
                                )
    return element


def find_radio_button(context, field, value, visible=True):
    try:
        print_debug(
            "Recherche d'un bouton radio via son label %s (%s)" % (value, visible,)
        )
        label_for = find_label(context, value, visible).get_attribute("for")
        print_debug("  label for : %s" % label_for)
        if label_for != "":
            element = get_element_by_xpath(
                context,
                "//input[@type='radio' and @id=%s]" % normalize_for_xpath(label_for),
            )
        else:
            print_debug("label non trouvé")
    except:
        print_debug("Recherche via l'id")
        elements = get_elements_by_xpath(
            context, "//input[@type='radio' and @id=%s]" % normalize_for_xpath(value)
        )
        if elements == []:
            print_debug("Recherche via le nom du champ et le contenu")
            print_debug("  champ : %s" % normalize_for_xpath(field))
            print_debug("  contenu : %s" % normalize_for_xpath(value))
            elements = get_elements_by_xpath(
                context,
                "//input[@type='radio' and @name=%s and contains(normalize-space(.),%s)]"
                % (normalize_for_xpath(field), normalize_for_xpath(value),),
            )
            if elements == []:
                print_debug("Recherche via le nom du champ et l'id")
                print_debug("  champ : %s" % normalize_for_xpath(field))
                print_debug("  id : %s" % normalize_for_xpath(value))
                elements = get_elements_by_xpath(
                    context,
                    "//input[@type='radio' and @name=%s and @id=%s]"
                    % (normalize_for_xpath(field), normalize_for_xpath(value),),
                )
                if elements == []:
                    print_debug("Recherche via le nom du champ et la value")
                    print_debug("  champ : %s" % normalize_for_xpath(field))
                    print_debug("  value : %s" % normalize_for_xpath(value))
                    elements = get_elements_by_xpath(
                        context,
                        "//input[@type='radio' and @name=%s and @value=%s]"
                        % (normalize_for_xpath(field), normalize_for_xpath(value),),
                    )
                    if elements == []:
                        assert False, (
                            "Option %s de la liste de choix %s non trouvée"
                            % (value, field)
                        )
    if elements == []:
        elements = get_elements_by_xpath(
            context, "//input[@type='radio' and @id=%s]" % normalize_for_xpath(value)
        )
        if elements == []:
            elements = get_elements_by_xpath(
                context,
                "//input[@type='radio' and @name=%s]" % normalize_for_xpath(value),
            )
            if elements == []:
                elements = get_elements_by_xpath(
                    context,
                    "//input[@type='radio' and @value=%s]" % normalize_for_xpath(value),
                )
                if elements == []:
                    elements = get_elements_by_xpath(
                        context,
                        "//input[@type='radio' and @name=%s]"
                        % normalize_for_xpath(value),
                    )
                    if elements == []:
                        if field != "":
                            assert False, (
                                "Option %s de la liste de choix %s non trouvée"
                                % (value, field)
                            )

    if elements == []:
        return None
    if visible:
        return get_first_visible_element(elements)
    return elements[0]


def find_link(context, value, visible=True):
    elements = get_elements_by_css(context, "a[id=%s]" % normalize_for_css(value))
    if elements == []:
        elements = get_elements_by_css(context, "a[name=%s]" % normalize_for_css(value))
        if elements == []:
            elements = get_elements_by_css(
                context, "a[title=%s]" % normalize_for_css(value)
            )
            if elements == []:
                elements = get_elements_by_xpath(
                    context,
                    "//a[contains(normalize-space(.),%s)]" % normalize_for_xpath(value),
                )
                if elements == []:
                    assert False, "Lien %s non trouvé" % value

    if elements == []:
        return None
    if visible:
        return get_first_visible_element(elements)
    return elements[0]


def find_label(context, value, visible=True):
    elements = get_elements_by_xpath(
        context, "//label[contains(normalize-space(.),%s)]" % normalize_for_xpath(value)
    )

    if elements == []:
        return None
    if visible:
        return get_first_visible_element(elements)
    return elements[0]


def find_input(context, value, visible=True):
    elements = []
    print_debug("Recherche du champ %s" % value)
    try:
        print_debug("  Via le label")
        label_for = find_label(context, value, visible).get_attribute("for")
        print_debug("  Label %s trouvé, et lié à %s" % (value, label_for))
        if label_for != "":
            print_debug("    Recherche d'éléments liés")
            elements = get_elements_by_xpath(
                context, "//*[@id=%s]" % normalize_for_xpath(label_for)
            )
            if elements == []:
                print_debug("  Pas de champ correspondant au label %s" % label_for)
                assert False, "Champ %s non trouvé" % value
                return
        else:
            print_debug("  Label non trouvé")
    except:
        print_debug("  Exception lors de la recherche par label")
        pass
    if elements == []:
        print_debug("  Recherche par css via l'id")
        elements = get_elements_by_css(context, "[id=%s]" % normalize_for_css(value))
        # print_debug(elements)
        # print_debug(normalize_for_css(value))
        if elements == []:
            print_debug("  Recherche par css via le name")
            elements = get_elements_by_css(
                context, "[name=%s]" % normalize_for_css(value)
            )
            if elements == []:
                print_debug("  Recherche par css via le title")
                elements = get_elements_by_css(
                    context, "[title=%s]" % normalize_for_css(value)
                )
                if elements == []:
                    print_debug("  Recherche par css via le value")
                    elements = get_elements_by_css(
                        context, "[value=%s]" % normalize_for_css(value)
                    )
                    if elements == []:
                        assert False, "Champ %s non trouvé" % value
    print_debug("  %d Elements trouvés:" % len(elements))
    print_debug(elements)

    if elements == []:
        return None
    if visible:
        return get_first_visible_element(elements)
    return elements[0]


def find_checkbox(context, value, visible=True):
    elements = []
    try:
        label_for = find_label(context, value, visible).get_attribute("for")
        if label_for != "":
            elements = get_elements_by_xpath(
                context,
                "//input[@type='checkbox'][@id=%s]" % normalize_for_xpath(label_for),
            )
            if elements == []:
                assert False, "Case à cocher %s non trouvée" % value
    except:
        pass
    if elements == []:
        elements = get_elements_by_css(
            context, "input[type='checkbox'][value=%s]" % normalize_for_css(value)
        )
        if elements == []:
            elements = get_elements_by_css(
                context, "input[type='checkbox'][id=%s]" % normalize_for_css(value)
            )
            if elements == []:
                elements = get_elements_by_css(
                    context,
                    "input[type='checkbox'][name=%s]" % normalize_for_css(value),
                )
                if elements == []:
                    elements = get_elements_by_css(
                        context,
                        "input[type='checkbox'][title=%s]" % normalize_for_css(value),
                    )
                    if elements == []:
                        assert False, "Case à cocher %s non trouvée" % value

    if elements == []:
        return None
    if visible:
        return get_first_visible_element(elements)
    return elements[0]


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def get_table(context):
    tableau = {
        "colonnes": [],
        "lignes": [],
    }
    soup = BeautifulSoup(context.browser.page_source, "lxml")
    table = soup.find("table")

    ths = table.find("thead").find_all("th")
    if len(ths) == 0:
        ths = table.find("tr").find_all("th")
    if len(ths) == 0:
        ths = table.find("tr").find_all("td")
    for th in ths:
        tableau["colonnes"].append(re.sub("[ \n\t]+", " ", th.text).strip())

    trs = table.find("tbody").find_all("tr")
    if len(trs) == 0:
        trs = table.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        ligne = []
        for td in tds:
            text = re.sub(
                "[ \n\t]+", " ", "".join(["%s" % content for content in td.contents])
            ).strip()
            ligne.append(text)
        tableau["lignes"].append(ligne)

    return tableau
