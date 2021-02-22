# configrules.py
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Configuration rules module.

This module is used to handle a hierarchical list of rules which
specify whether sections or individual elements of a configuration file
should be included or not, similar to an access control list.

Rules match on the position in the hiearchy of configuration (e.g.
"interface.description"), ID (e.g. "Vlan810") and/or the type of
operation being performed on them (being set/created, unset/deleted
or changed).
"""



# --- imports ---



import re



# --- classes ----



class ConfigElementRules:
    """This class keeps a list of rules used to include or exclude
    sections of a configuration.  They are used when generating a file
    of configuration changes to avoid overwriting parts which may be
    controlled elsewhere.

    An 'element' is a part of the configuration consisting of the
    following properties:

      * the 'operation' is the type of adjustment being performed;
        usually this is one of 'new' (creating a new VLAN, interface,
        etc.), 'update' (adjusting an existing setting), or 'delete'
        (removing something no longer needed)

      * the 'area' is a path to the part of the configuration being
        adjusted - they are parsed and stored as a list of items in
        the path but often represented as a string, with the items
        separated by periods ('.'), for convenience to the user; the
        path allows an area to be matched with the required level of
        granularity when matching it - for example, the Spanning Tree
        priority may be represented by 'stp.priority', allowing it to
        be matched in a rule with 'stp.priority' (to specifically
        identify a priority new/update/delete) or 'stp' to match any
        Spanning Tree differences

      * the 'id' identifies the thing being operated upon - e.g.
        'Vlan100'

    A list of rules is assembled using add_rule() or add_rules(), with
    each rule specified in string form '[!][{+-=}][<area>][:<id>]'.

      * a leading '!' (or not) specifies whether elements matching the
        rule should be included or not: a '!' indicates the rule should
        exclude matching elements; if the character is omitted, they
        should be included

      * the next (or first, if '!' isn't used) character indicates the
        'operation': a '+' means create/set operations, '-' means
        delete/unset operations and '=' update operations (changing an
        already-set value for another)

    The list of rules starts empty, with the default case being to
    include the element.

    When the configuration changes are generated, each element can be
    matched using the check() method, which will return True (include
    this element) or False (exclude it).
    """


    def __init__(self):
        # initialise the list of element rules to the empty list; the
        # default case (if nothing matches) is to include everything
        #
        # the list consists of a number of 4-tuples for each rule, with
        # the tuples giving the 'include/exclude' action, 'operation'
        # (add/remove/update), 'area' (of configuration) and 'id' (name
        # of area - such as VLAN name, port/interface number, etc.)

        self._rules = []


    def _areastr_to_list(self, areastr):
        """Parse the area string (with the area levels separated by
        periods), as used in elements, into its various levels and
        return the levels as a list.

        Alternatively, if the supplied area string is None (or empty),
        None is returned (which means 'match any', in a rule).
        """

        return areastr.split(".") if areastr else None


    def _parse_rule(self, rule):
        """Parse a rule (in the form of a string in the syntax
        described in the class documentation.

        The return value is a 4-value tuple in the form (include, op,
        area, id), with missing items returned as None.  'include' is
        True for include or False for exclude.
        """


        # use a regular expression to parse a rule

        match = re.match(
                    r"^"
                    r"(?P<include>[!])?"
                    r"(?P<op>[-+=])?"
                    r"(?P<area>[A-Za-z0-9][-.A-Za-z0-9]+)?"
                    r"(:(?P<id>[A-Za-z0-9][-_.A-Za-z0-9]+))?"
                    r"$",

                    rule)

        if not match:
            raise ValueError("error parsing rule '%s'" % rule)


        # get the parts of the rule and return them

        groups = match.groupdict()

        include = groups["include"] != "!"
        op = groups["op"]
        area = self._areastr_to_list(groups["area"])
        id = groups["id"]

        return include, op, area, id


    def add_rule(self, rule):
        """Add a single rule to the list.  The rule is supplied as a
        string, parsed and appended.

        The rule is lower-cased before adding to canoncalise it and
        avoid case comparisons when matching (matched elements are
        lower-cased before check()ing).
        """

        self._rules.append(self._parse_rule(rule.lower()))


    def add_rules(self, rules):
        "Add a list of element rules to the list."

        for rule in rules:
            self.add_rule(rule)


    def read_rules(self, filename):
        """Read a list of rules from filename and add them to the list
        using add_rule().

        A hash ('#') and anything following it is stripped out as a
        comment.  Trailing whitespace is also removed.  Blank lines
        (including those created by the above actions) are skipped.
        """

        # add the rules in the file specified
        for rule in open(filename):
            # strip out anything following a '#' (indicating comment) and
            # any trailing whitespace
            rule = re.sub("#.*", "", rule)
            rule = rule.rstrip()

            # skip blank lines (or lines with only comments/whitespace)
            if rule == "":
                continue

            self.add_rule(rule)


    # MATCHING


    def _area_match(self, match_area, check_area):
        """This function is used to check if the supplied 'match area'
        is the same, or contains the supplied 'check area'.  It is used
        to check if hierarchies of areas should be included or not.

        The return value is an integer: 0 if they don't match, or
        the match area doesn't not contain the check area; 1 if they
        match exactly; or -1 if the match area contains the check area
        (i.e. is a perfect sub-area, not exactly matching).

        Both areas are supplied as lists of area levels.
        """


        # we use these in several places, so just calculate them once

        match_area_len = len(match_area)
        check_area_len = len(check_area)


        # if the length of the match area is longer than the check
        # area, there's no way we can have a match

        if match_area_len > check_area_len:
            return 0


        # go through the levels in the match area to check each one
        # against the check area

        for level in range(0, match_area_len):
            # if the names of the areas at this level are different,
            # there is no match

            if match_area[level] != check_area[level]:
                return 0


        # if we got to the end of the match area and there are more
        # levels in the check area, the check area is a perfect sub-
        # area of the match area

        if level < (check_area_len - 1):
            return -1


        # if we get here, the areas paths are the same length, so must
        # be exactly equal

        return 1


    def _match(self, check_op, check_areastr, check_id):
        """This private method is used to check in the rules to see if
        a particular element should be included in the output
        configuration or not, it will also return the rule which
        matched the check conditions.

        The public method that uses this is include().

        The arguments are operation ("-", "+" or "="), area (in
        period-separated string form) and id.

        The returned value is a 4-element tuple consisting of:

          * a boolean indicating if the element should be included
            (True) or excluded (False)

          * the operation character ("+", "-" or "=") of the matching
            rule (or None, if wildcarded)

          * the area (in period-separated string format) of the
            matching rule (or None, if that was wildcarded)

          * the ID of the matching rule (or None, if wildcarded)

        If only the include/exclude action is required, just the first
        element can be extracted with "[0]".
        """


        # convert the check area into a list of areas, after lower-
        # casing it, to canonicalise the case

        check_area = self._areastr_to_list(check_areastr.lower())


        # lower case the id field to canoncalise the case

        check_id_lower = check_id.lower()


        # go through the list of rules and, once we have a match,
        # return the include/exclude action specified by that rule

        for match_include, match_op, match_area, match_id in self._rules:

            # compare the match and check areas: 0 = no match; 1 =
            # exact match; -1 = check area is sub-area of match area
            #
            # if the area part is None, it's a wildcard, so assume an
            # exact match

            area_match = (
                self._area_match(match_area, check_area) if match_area
                    else 1)


            # if the match and check areas are the same, the operation
            # must match; if check area is a sub-area of the match
            # area, the operation is a considered an update ("=") on
            # that area of the configuration, regardless of whether it
            # is a new, delete or update operation at the individual
            # command level

            if (((match_id is None) or (match_id == check_id_lower)) and

                (((area_match == 1) and
                  ((match_op is None) or (match_op == check_op))) or

                 ((area_match == -1) and
                  ((match_op is None) or (match_op == "="))))):

                return (match_include, matcp_op,
                        ".".join(match_area) if match_area else None,
                        match_id)


        # if we get to the end of the list without a match, we default
        # to including it; the 'None's for the match information
        # indicate the default rule

        return True, None, None, None


    def _rule_to_str(self, op, areastr, id):
        """This function converts a rule, specified by the three
        arguments: area (in period-separated string form), id and
        operation (any of which can be None, if wildcarded) into a
        string.  The string will be in the same format as parsing
        ("[!][<area>][:<id>]{+-=}").
        """

        return (op or "") + (areastr or "") + ((":" + id) if id else "")


    def include(self, check_op, check_areastr, check_id):
        """This method is a wrapper around _match() which will turn the
        information about the matching rule into a printable string, as
        well as the information about the element being checked.

        The return value with be a 2-element tuple with a boolean: the
        first indicates whether the check element should be included
        or not, the second is a string describing the match and check
        information (in the form "<match-rule> matches <check-rule>").
        """

        match_include, match_op, match_areastr, match_id = (
            self._match(check_op, check_areastr, check_id))

        match_str = self._rule_to_str(match_op, match_areastr, match_id)
        check_str = self._rule_to_str(check_op, check_areastr, check_id)

        return (match_include,
                ("%s matches %s" % (check_str, match_str or "<default>")))


    def compare_op(self, from_value, to_value):
        """This method compares the 'from value' and the 'to value' to
        determine the type of operation being performed (new, delete or
        update) and then returns a single character string, with the
        same value as those used in rules ("-" = delete, "+" = new, "="
        = update).

        However, if both values are the same, None is returned,
        indication no change is required.
        """


        # if the values are the same, nothing's being changed, so
        # nothing needs to be included

        if from_value == to_value:
            return None


        # the values are different, so check if we're setting, unset-
        # ting or updating the value to determine the operation

        if from_value is None:
            return "+"

        elif to_value is None:
            return "-"

        return "="
