# encoding: utf-8
"""
TODO: Translation work to do...
"""

import re
import time
from datetime import datetime, timedelta

from behave import step, then, when

########################################################################################
# Given
########################################################################################


########################################################################################
# When
########################################################################################
@step(u'j\'exécute la requête "{request}"')
@step(u'que j\'exécute la requête "{request}"')
@step(u'j\'exécute la requête "{request}" avec le paramètre "{parameters}"')
@step(u'que j\'exécute la requête "{request}" avec le paramètre "{parameters}"')
@step(u'j\'exécute la requête "{request}" avec les paramètres "{parameters}"')
@step(u'que j\'exécute la requête "{request}" avec les paramètres "{parameters}"')
def step_impl(context, request, parameters=None):
    if request not in context.klity.requests:
        assert False, "Requête %s non trouvée" % request
    if parameters:
        # parameters are separated by comma
        print(request, parameters)
        parameters = re.split(r"(?<!\\),", parameters)
        print(request, parameters)
    try:
        result = context.klity.execute(request, parameters)
        print(result)
    except IndexError:
        assert False, "Nombre de paramètres incorrect; %d paramètres fournis" % len(
            parameters
        )


@step(u'j\'assigne la valeur "{value}" à la variable "{variable}"')
@step(u'que j\'assigne la valeur "{value}" à la variable "{variable}"')
def step_impl(context, value, variable):
    print("CONTEXT: ", context.klity.variables)
    context.klity.variables[variable] = get_value(context, value)
    print("CONTEXT: ", context.klity.variables)


@step(u'j\'assigne le résultat de la requête "{request}" à la variable "{variable}"')
@step(
    u'que j\'assigne le résultat de la requête "{request}" à la variable "{variable}"'
)
@step(
    u'j\'assigne le résultat de la requête "{request}" avec le paramètre "{parameters}" à la variable "{variable}"'
)
@step(
    u'que j\'assigne le résultat de la requête "{request}" avec le paramètre "{parameters}" à la variable "{variable}"'
)
@step(
    u'j\'assigne le résultat de la requête "{request}" avec les paramètres "{parameters}" à la variable "{variable}"'
)
@step(
    u'que j\'assigne le résultat de la requête "{request}" avec les paramètres "{parameters}" à la variable "{variable}"'
)
def step_impl(context, request, variable, parameters=None):
    if request not in context.klity.requests:
        assert False, "Requête %s non trouvée" % request
    print(request)
    if parameters:
        # parameters are separated by comma
        print(request, parameters)
        parameters = re.split(r"(?<!\\),", parameters)
        print(request, parameters)
    try:
        result = context.klity.execute(request, parameters)
        print(result)
    except IndexError:
        assert False, "Nombre de paramètres incorrect; %d paramètres fournis" % len(
            parameters
        )
    print("CONTEXT: ", context.klity.variables)
    context.klity.variables[variable] = result["results"][0][0]
    print("CONTEXT: ", context.klity.variables)


########################################################################################
# Then
########################################################################################
@then(u'le résultat de la requête "{request}" est vide')
@then(u'le résultat de la requête "{request}" contient "{text}"')
def step_impl(context, request, text=""):
    if request not in context.klity.requests:
        assert False, "Requête %s non trouvée" % request
    result = context.klity.execute(request)
    print(request)
    print(result)
    # TODO : Should be able to manage multiple columns
    if text == "":
        try:
            assert result["results"][0][0] is None
        except:
            assert result["results"][0][0] == ""
    else:
        assert text in str(result["results"][0][0]), "Texte %s non trouvé dans %s" % (
            text,
            str(result["results"][0][0]),
        )


@then(u'le résultat de la requête "{request}" n\'est pas vide')
def step_impl(context, request):
    if request not in context.klity.requests:
        assert False, "Requête %s non trouvée" % request
    result = context.klity.execute(request)
    print(request)
    print(result)
    try:
        assert result["results"][0][0] is not None
    except:
        assert result["results"][0][0] != ""


########################################################################################
# STEP
########################################################################################
@step(u"j'attends {second} secondes")
@step(u"j'attends {second} seconde")
@step(u"que j'attends {second} secondes")
@step(u"que j'attends {second} seconde")
def step_impl(context, second):
    time.sleep(float(second))


@step(u"je fais un screenshot")
@step(u'je fais un screenshot sous le nom "{name}"')
@step(u"je fais une capture d'écran")
@step(u'je fais une capture d\'écran sous le nom "{name}"')
@step(u"que je fais un screenshot")
@step(u'que je fais un screenshot sous le nom "{name}"')
@step(u"que je fais une capture d'écran")
@step(u'que je fais une capture d\'écran sous le nom "{name}"')
def step_impl(context, name=None):
    if name is None:
        name = "%s" % datetime.utcnow().strftime("%Y%m%d_%H%M%S%f")
    context.browser.save_screenshot("screenshots/%s.png" % name)


########################################################################################
# Utilities
########################################################################################
def get_value(context, value):
    # Replacing variables
    variables = list(set(re.findall(r"((?<!\\)\$[^$]+\$)", value)))
    print("variables:", variables)
    print(context.klity.variables)
    for variable in variables:
        value = value.replace(variable, context.klity.variables[variable[1:-1]])
    print("value:", value)

    # Replacing constants
    constants = list(set(re.findall(r"((?<!\\)#[^#]+#)", value)))
    print("constantes:", constants)
    for constant in constants:
        new_value = ""
        what = constant[1:-1].split("_")[0]
        how = ""
        if "_" in constant:
            how = "_".join(constant[1:-1].split("_")[1:])
        if what[:4] == "DATE":
            date = datetime.today()
            if len(what) > 4 and what[4] in ("-", "+"):
                date += timedelta(days=int(what[4:]))
            if len(how) > 0:
                new_value = how
                # Replacing year
                for data in ("YEAR", "ANNEE"):
                    new_value = new_value.replace(data, date.strftime("%Y"))
                # Replacing month
                for data in ("MONTH", "MOIS"):
                    new_value = new_value.replace(data, date.strftime("%m"))
                # Replacing day
                for data in ("DAY", "JOUR"):
                    new_value = new_value.replace(data, date.strftime("%d"))
                # Replacing hour
                for data in ("HOUR", "HEURE"):
                    new_value = new_value.replace(data, date.strftime("%H"))
                # Replacing minute
                for data in ("MINUTE",):
                    new_value = new_value.replace(data, date.strftime("%M"))
                # Replacing second
                for data in ("SECOND", "SECONDE"):
                    new_value = new_value.replace(data, date.strftime("%S"))
            else:
                new_value = str(date)
        value = value.replace(constant, str(new_value))
    print("value", value)

    # Replacing escaped characters
    value = value.replace("\$", "$")
    value = value.replace("\#", "#")
    return value
