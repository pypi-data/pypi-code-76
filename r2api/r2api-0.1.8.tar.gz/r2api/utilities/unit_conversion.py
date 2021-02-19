import copy
import re


def convert_units_ing(quantity, unit):
    """
    Pass in a number and a quantity in metric units
    Returns a number and quantity in (American) imperial units
    """
    try:
        quantity = str(quantity)
    except:
        raise TypeError(f"quantity {quantity} cannot be cast as a string")
    try:
        float(quantity)
    except:
        if '/' in quantity:
            try:
                # This quantity doesn't matter
                # but if the '/' can be replaced easily
                # that's all we care about
                float(quantity.replace('/', '.'))
            except:
                return (quantity, unit)
    try:
        unit = str(unit)
    except:
        return (quantity, unit)

    # Dict is in the format:
    # key : (ratio, translated_key)
    # Unlike below, constants are not needed
    # because temperatures are not passed in
    unit_conversion = {
        'g': (0.00220462, 'lb'),
        'gr': (0.00220462, 'lb'),
        'grammi': (0.00220462, 'lb'),
        'kg': (2.205, 'lb'),
        'l': (33.8140227, 'fl oz'),
        'litri': (33.8140227, 'fl oz'),
        'ml': (33.8140227 / 1000, 'fl oz'),
        'millilitri': (33.8140227 / 1000, 'fl oz')
    }

    unit_lower = unit.lower()

    if unit_lower in unit_conversion:
        # The quantity can sometimes contain , instead of .
        # because decimals are written with a comma
        quantity = quantity.replace(',', '.')
        # There is no need for a try/except block because
        # it will be of the proper format if it has gotten this far
        con_q = (round(unit_conversion[unit_lower][0] * float(quantity), 2))
        con_u = unit_conversion[unit_lower][1]
        # Sometimes units will be something like .14 lb
        # So they will be converted to oz if they are small enough
        # Or fl oz to cups/quarts if they're large enough
        con_q, con_u = simplify_units(con_q, con_u)
        return con_q, con_u
    else:
        try:
            quantity = round(float(quantity), 2)
        finally:
            return (quantity, unit)


def convert_units_name(name):
    if not isinstance(name, str):
        raise TypeError("name of ingredient must be a string")

    # If a unit gets put into the name, this method seeks to find it
    # The regex is pretty simple
    regex = r'(\d+)\s?(\w+)'
    for match in re.findall(regex, name):
        # This is later used to match the replaced/replacing text strings
        convertable_quantity, convertable_unit = match[0], match[1]
        converted_quantity, converted_unit = convert_units_ing(
            match[0], match[1])

        # If there hasn't been any conversion, there is no need to proceed
        # This is here to double check that we're not needlessly converting units
        if convertable_quantity != converted_quantity and convertable_unit != converted_unit:
            # The replace method requires two strings, however the converted_quantity
            # Has been cast to float for other purposes
            name = name.replace(convertable_quantity, str(converted_quantity))
            name = name.replace(convertable_unit, converted_unit)
    return name


def convert_units_prep(prep):
    """
    Takes a string, parses it for metric units and converts both them and the quantities into imperial units and quantities
    """
    # We'll make a copy so we don't have any side effects
    # Because we'll be doing some replacing if we have a hit
    return_string = copy.deepcopy(prep)

    # this dictionary is of the format:
    # key: (scalar, constant, unit)
    # N.B. Both temperatures and lengths are here
    unit_conversions = {
        'g': (0.00220462, 0, 'lb'),
        'gr': (0.00220462, 0, 'lb'),
        'grammi': (0.00220462, 0, 'lb'),
        'kg': (2.205, 0, 'lb'),
        'l': (33.814, 0, 'fl oz'),
        'litri': (33.814, 0, 'fl oz'),
        'ml': (33.814 / 1000, 0, 'fl oz'),
        'millilitri': (33.814 / 1000, 0, 'fl oz'),
        '°': (1.8, 32, '°'),
        'gradi': (1.8, 32, 'gradi'),
        'c': (1.8, 32, 'F'),
        'cm': (0.3937, 0, 'inches'),
        'mm': (0.03937, 0, 'inches'),
        'm': (39.37, 0, 'inches')
    }
    # When there is a unit, it comes in one of two formats:
    # 1. quantityunit - i.e. 300g
    # 2. quantity(any of , . / - x)fraction(space)unit - i.e. 1,5 l
    # Regex 3 is so the expression correctly classifies something
    # as the former and the latter as the latter
    # i.e. 1,5l isn't treated as 1, as not a unit and 5l
    # group(1) will always be the quantity, group(2) always the unit
    regex = '(\d+[,\.\/]?\d*[a-zA-Z°]*[\/\-x]?\d*[,\.\/]?\d*)(\s?)([a-zA-Z°]+)'

    match = re.findall(regex, return_string)
    # it's possible that there are multiple unit conversions in one line
    # i.e. 'mettere 1,5 l di crema con 300g di pollo'
    if len(match) > 0:
        # looping through every match
        for group in match:
            # we will get lots of false positives
            # they'll get ignored if they're not
            # of the appropriate form
            if group[2].lower() in unit_conversions:
                unit_lower = group[2].lower()
                # The unit is just the converted unit name and the simplest to replace
                conv_unit = unit_conversions[unit_lower][2]
                # We are doing the same replacement that we did above
                # replacing , with . so it can be converted to a float
                amount_punctuation_replaced = group[0].replace(',', '.')
                extra_units = re.search('[a-zA-Z°+]', group[0])

                # On the rare occasion we get a monstrosity of redundancy such as:
                # '190°-200° C ', we identify the three groups as:
                # 1. '190°-200'
                # 2. ''
                # 3. '°'
                # See the problem? It's the ° in group 1. We need to get rid of it
                if extra_units:
                    amount_punctuation_replaced = amount_punctuation_replaced.replace(extra_units.group(), '')

                try:
                    # This is the simplest case: that it's something like 1,5 (now 1.5)
                    # So we can just make it into a float
                    amount = float(amount_punctuation_replaced)
                    # The converted quantity is equal to the float times the scalar plus the constant
                    conv_amount = round(
                        (amount * unit_conversions[unit_lower][0]) + unit_conversions[unit_lower][1], 2)
                    # We are passing it to the same function to simplify it so we don't have 0.14 lb
                    # Unfortunately we have to repeat it once for every different situation
                    conv_amount, conv_unit = simplify_units(
                        conv_amount, conv_unit)
                # Except occurs if it's not a , but something else
                # such as - as in 2-3
                except:
                    # Therefore we are preserving the two digits as separate entities
                    # But otherwise doing the same action
                    # This regex should capture both 1-2 and 1.2-5.2
                    digits = re.findall(
                        '(\d+[,\.\/]?\d*)(\D)(\d+[,\.\/]?\d*)', amount_punctuation_replaced)[0]
                    # So we split them up into two digits
                    first_digit = round((float(
                        digits[0]) * unit_conversions[unit_lower][0]) + unit_conversions[unit_lower][1], 2)
                    second_digit = round((float(
                        digits[2]) * unit_conversions[unit_lower][0]) + unit_conversions[unit_lower][1], 2)
                    _first_digit, first_conv_unit = simplify_units(
                        first_digit, conv_unit)
                    _second_digit, second_conv_unit = simplify_units(
                        second_digit, conv_unit)
                    # In the rare circumstance that simplify_units will give different units
                    # for a range, we ignore the converison but must dot zero it manually
                    # because simplify_units does it usually
                    if first_conv_unit == second_conv_unit:
                        first_digit = _first_digit
                        second_digit = _second_digit
                        conv_unit = first_conv_unit  # Whichever of the two
                    else:
                        if float_dot_zero(first_digit):
                            first_digit = int(first_digit)
                        if float_dot_zero(second_digit):
                            second_digit = int(second_digit)
                    conv_amount = f"{first_digit}{digits[1]}{second_digit}"
                    # In this case, we are giving the
                    # average of the numbers; this could be improved

                # Now that we've done the conversions, we need to replace the original text
                # with the converted, so we're making a string to find the original and do this

                # Forming the string:
                # N.B. Sometimes we need to replace 1,5 l and sometimes 1,5l
                # group[1] will always be either a space or not - for what we need
                replaced_seq = f"{group[0]}{group[1]}{group[2]}"
                replacing_seq = f"{conv_amount}{group[1]}{conv_unit}"
                return_string = return_string.replace(
                    replaced_seq, replacing_seq)

                # It seems to be only with temperature, but sometimes we get both degrees and
                # a unit marking. Hence the need for this line
                if return_string.find("° C "):
                    return_string = return_string.replace("° C ", "° F ")
            else:
                # There is ONE circumstance where the regex makes an error
                # If there is something like "180° per", where 180° gets caught up
                # as group[0], where an easier solution is to recurse and see if
                # the recursion produced a different route
                # I would be more cautious about this except this method isn't too costly
                _prep = convert_units_prep(group[0])
                # This line is somewhat superfluous -- any change will trigger it, even if it
                # isn't correct -- but I think it elucidates the logic
                if prep != prep.replace(group[0], _prep):
                    return_string = return_string.replace(group[0], _prep)
    return return_string


def simplify_units(quantity, unit, change_unit=True):
    """
    Takes a quantity and unit in imperial units and if it is within certain tolerances, changes it to a more convenient quantity
    """
    return_quantity = quantity
    return_unit = unit

    # A large area for improvement is to do rounding based off of the units
    # For example: 1.07lb should really be 1 or 1.2 cups should really be 1
    if unit == 'inches' and quantity >= 12:
        # Convert any quantity over 12 inches to feet and inches
        feet = quantity // 12
        inches = quantity % 12
        return_quantity = f"{feet}'"
        return_unit = 'feet'
        if inches > 0:
            return_quantity += f"{inches}''"
            return_unit += ' and inches'
    elif unit == 'fl oz' and quantity >= 8:
        # Confort to quart/cup if the quantity is > 32 or > 8
        if quantity >= 32:
            return_quantity = round(quantity/32, 2)
            return_unit = 'quart'
        else:
            return_quantity = round(quantity/8, 2)
            return_unit = 'cup'
    elif unit == 'lb' and quantity < 1:
        # Convert to oz if quantity is less than a pound
        return_quantity = 16 * quantity
        return_unit = 'oz'
    if float_dot_zero(return_quantity):
        return_quantity = int(return_quantity)
    return return_quantity, return_unit


def float_dot_zero(qt):
    """Returns true if a float ends in .0. All other situations return false"""
    if isinstance(qt, float):
        return str(qt).endswith('.0')
    else:
        return False
