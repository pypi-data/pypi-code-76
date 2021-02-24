# configdiff.py
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from .configchanges import BlockedConfigChanges
from .configrules import ConfigElementRules



# --- context parser ---



class ConfigDiff:
    """This abstract class is used to compare two configuration files
    and generate a configuration file to transform one into the other.
    """


    def __init__(self, init_rules=ConfigElementRules(),
                 init_explain_includes=False):

        """The constructor initialises some instance variables and
        stores the supplied arguments in the instance.

        The method takes two arguments: the first is an object of class
        ConfigElementRules, specifying what elements to include or not;
        the second is a boolean, indicating whether comments should be
        added to explain matches against these rules which include
        elements.

        Note that the 'init_explain_includes' option requires the
        _matchinfo_comment() method to be imeplemented in the concrete
        child class.
        """


        # initialise the configuration changes to empty

        self._diffs = BlockedConfigChanges()


        self._rules = init_rules
        self._explain_includes = init_explain_includes


    def getconfig(self):
        """This method returns the configuration changes (calculated
        through one or more calls to diffconfigs()) as a single,
        multiline string.
        """

        # return the configuration in text form; if it is empty, None
        # will be returned

        return self._diffs.getconfig()


    def _matchinfo_comment(self, matchinfo):
        """This abstract method should be overridden by child classes
        to add a comment containing the string argument 'matchinfo' to
        the generated configuration.  The format of the comment should
        be appropriate for the platform being implemented.  The
        'matchinfo' string explains the details (from the point of view
        of a rule) of the change being made.

        This method is only used if the _explain_includes flag is set.

        The implementation in this class raises a NotImplementedError,
        if it is called.
        """

        raise NotImplementedError("_matchinfo_comment() not implemented")


    def _include(self, check_areastr, check_id, check_op):
        """This method is a wrapper around the include() method of the
        ConfigElementRules class, returning the first element (a
        boolean, indicating whether the configuration element should be
        included or not - same as the check() method of the same
        class).

        However, if it is to be included, it will add a comment,
        showing the rule which matched, along with the element's check
        parameters.
        """

        # do the check and retrieve the match information

        include, matchinfo = self._rules.include(
                                 check_areastr, check_id, check_op)


        # if we are including this element and explaining is enabled,
        # add a comment showing the matching rule information

        if include and self._explain_includes:
            self._matchinfo_comment(matchinfo)


        return include


    def _compare_include(self, from_value, to_value, check_areastr, check_id):
        """This method compares the 'from value' and the 'to value' to
        determine the type of operation being performed (new, delete or
        update) and then uses the _include() method to check if the
        change should be included or not.

        If _explain_includes is set, a comment will be added to the
        differences.

        If the two values are the same, False is returned as,
        regardless of the rules, no update needs to be included.
        """


        # compare the two values to get the operation to go from the
        # "from value" to the "to value"

        compare_op = self._rules.compare_op(from_value, to_value)


        # if the values are the same, nothing needs to be included,
        # regardless of the rules

        if compare_op is None:
            return False


        # check if this should be included or not, based on the rules
        # and the operation determined above

        return self._include(compare_op, check_areastr, check_id)


    def _compare_set_include(
        self, from_set, to_set, check_areastr, check_id):
        """This method is similar to _compare_include() except that it
        compares sets.

        The method behaves slightly differently, depending on whether
        check_id is None or not:

        * if check_id is None, the ID used in the check will be the
          str() the operation will be either add ('+') or remove ('-')
          for each item

        * if check_id is not None, the ID used will be the supplied
          parameter and all changes will be classed as updates ('=')

        If either of the from or to sets are None, an empty set is
        assumed.

        As _include() is used as the underlying test, if
        _explain_includes is set, a comment will be added to the
        differences.

        The return value is a 3-tuple of the _include() flag (if the
        change should be included in the differences) and two lists:
        the first is the items to be added (i.e. items in the 'to set'
        that are not in the 'from set') and the second is the items to
        be removed (i.e. items in the 'from set' not in the 'to set').
        They are returned as lists to match the order of any comments
        inserted by the _include() method, if matching individual
        values.
        """

        # if either the from to to sets are None, assume an empty set

        from_set_set = from_set or set()
        to_set_set = to_set or set()


        # when comparing sets, we also use the "=" (update) operator,
        # regardless of whether items are added or removed

        if check_id:
            include = self._include("=", check_areastr, check_id)

            remove_items = (
                from_set_set.difference(to_set_set) if include else set())

            add_items = (
                to_set_set.difference(from_set_set) if include else set())

        else:
            include = True

            remove_items = [ i for i in from_set_set.difference(to_set_set)
                                if self._include("-", check_areastr, i) ]

            add_items = [ i for i in to_set_set.difference(from_set_set)
                              if self._include("+", check_areastr, i) ]

        return include, remove_items, add_items
