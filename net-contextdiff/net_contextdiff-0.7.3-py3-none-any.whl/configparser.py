# configparser.py
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Contextual configuration parser module.

This module contains a class to parse configuration files that use
indented blocks to indicate the context of commands.
"""



# --- imports ---



import re



# --- classes ----



class IndentedContextualConfigParser:
    """The abstract base class for the indent-based contextual parser.
    Child classes (e.g. one to parse Cisco IOS configuration files)
    inherit from this to handle specific types.
    """


    def __init__(self):
        """Initialise the object by calling _add_commands() to add the
        commands for this configuration platform.

        Child classes would typically override that method to add the
        specific commands for that file type.
        """


        # _config = {}
        #
        # This dictionary holds the parsed configuration.  The parse_-
        # file() method adds things to this, as they're parsed.

        self._config = {}


        # _commands = {}
        #
        # Command parsing is handled through a dictionary indexed by
        # the name of the current context (contexts are begun and end
        # with the levels of indent).  Each item in this dictionary is
        # a list of dictionaries: one item in the list for each command
        # matched in this context, containing the following mandatory
        # keys:
        #
        #   * command -- a string giving an uncompiled regular
        #     expression for a command, to match against lines in this
        #     context; if this matches, the command is considered
        #     "found" and no further commands are checked for, so it
        #     must be adequately specified to not match the wrong
        #     command; an implicit '^' and '$' surround the expression
        #     and leading whitespace is also removed
        #
        #   * re -- the compiled regular expression, constructed from
        #     re.compile() of the textual command 'command'; the add_-
        #     command() method automatically sets this
        #
        # There are also two optional keys:
        #
        #   * action -- this is a function to be called when the line
        #     matches this command; three parameters will be supplied (below)
        #
        #   * new_context -- if the command matches, the current
        #     context will be changed to this to parse commands in
        #     child contexts; commands with no child contexts can just
        #     omit this
        #
        # The action function takes three arguments
        #
        #   * match -- a dictionary (obtained with re.match.groupdict()) for
        #     the groups matched in the regular expression 're'
        #
        #   * contextconfig -- a reference to part of the configuration
        #     dictionary appropriate to the context the command is in
        #     (a structure under self._config) to make it easy to modify that
        #     portion of the configuration; this typically set to the same as
        #     params["config"], if it exists, or None, if not, defined by the
        #     command which caused the context to be entered
        #
        #   * params -- a dictionary of the parameters applying to the
        #     current context: action functions from parent contexts
        #     can modify this to record information parsed from their
        #     command lines - e.g. the "vlan ..." command can record
        #     the tag number in their params dictionary which is then
        #     passed to any action functions in the child contexts;
        #     they are, thus, cumulative
        #
        # the command dictionary is initialised with a single context
        # of "." (the toplevel context) containing no commands

        self._commands = {
            ".": []
        }


        # add the commands for this parser

        self._add_commands()


    def _add_commands(self):
        """Add the commands for this configuration platform.  Child
        classes would override this method to add the commands for
        the platform they are handling.

        This abstract class has no commands so does nothing.
        """

        pass


    def _add_command(self, context, command, action=None, new_context=None):
        """Append a command to list for the specified context.  If the
        context does not exist, it is created.

        Keyword arguments:

        context -- the name of the context in which to add the command;
        this is "." for the top level context

        command -- text (uncompiled) regular expression for the command; note
        that, once a command matches, parser assumes that it has been found and
        does not consider any further commands, so the regular expression must
        be suitably specific not to match other commands

        action=None -- function to call in the event the command is matched

        new_context=None -- new [sub]context to switch to, in the event the
        command is matched; if None, the subcontext is effectively unprocessed
        (no commands will be matched inside it)
        """


        # if the context doesn't exist yet, create it with an empty list of
        # commands

        self._commands.setdefault(context, [])


        # build a dictionary for the new command, only adding the items where
        # they have been specified

        command_dict = {
            "text": command,
            "re": re.compile("^%s$" % command, re.IGNORECASE)
        }

        if action:
            command_dict["action"] = action

        if new_context:
            command_dict["new_context"] = new_context


        # add the command to the list of commands in this context

        self._commands[context].append(command_dict)



    def parse_file(self, filename, debug=False):
        """Parse a file and return the configuration as a dictionary.

        Keyword arguments:

        filename -- name of the file to read and parse into a
        dictionary of the configuration
        """


        # open the specified file for reading

        file = open(filename, "r")


        # the context stack stores the list of contexts in effect at the
        # current line being processed

        context_stack = []


        # go through the file, reading the lines one by one

        for line in file:
            # skip blank lines (or lines consisting solely of spaces)

            if line.lstrip(" ") == "\n":
                continue


            if debug:
                print(line, file=sys.stderr)


            # calculate the number of leading spaces for this line; this is
            # used to work out if we've changed context

            line_indent = len(line) - len(line.lstrip(" "))


            # if we're in a context (not at the top level), check how this line
            # compares to that context (and its parents)

            if context_stack:
                # get the indent of the current (topmost) context

                context_indent = context_stack[-1]["indent"]


                if line_indent == context_indent:
                    # this line is indented the same as the previous one, so
                    # we're in the same context as it (that of the parent
                    # context)
                    #
                    # as such, we need to replace the current context (which
                    # was that moved into by the previous command, in case it
                    # had a subcontext) - remove the top one from the stack
                    # (we'll add this new context later)

                    context_stack.pop()

                elif line_indent > context_indent:
                    # this line is indented more than the previous one, so
                    # we're moving into a subcontext - we don't do anything
                    # here (we'll just add the new context later)

                    pass

                elif line_indent < context_indent:
                    # this line is indented less than the previous one so we've
                    # moved up at least one context - keep popping contexts
                    # from the stack until we find a matching indent level

                    while (context_stack and
                           (context_stack[-1]["indent"] >= line_indent)):

                        context_stack.pop()


            # get the name of the current context, or "." if we're at the top
            # level (no indent)
            #
            # if the current context has no name, we default to None

            context_name = (
                "." if not context_stack
                    else context_stack[-1]["name"]
                             if context_stack and ("name" in context_stack[-1])
                             else None)


            # get the parameters for the current context and [shallow] copy
            # them, so we can add additional parameters, if required
            #
            # if we're at the top level default to the empty dictionary

            context_params = (
                context_stack[-1]["params"].copy()
                    if context_stack and ("params" in context_stack[-1])
                    else {})


            # start building a dictionary for the new context

            new_context = { "indent": line_indent }


            # strip leading spaces from the line

            line_strip = line.lstrip(" ")


            # go through the commands in this context, seeing if the line
            # matches one of them
            #
            # note that we only switch to a context if there are commands
            # registered in it, so we don't need to check for that here; only
            # that the context is not None

            if debug:
                print("--- context '%s'" % context_name)

            if context_name:
                for command in self._commands[context_name]:
                    if debug:
                            print("--- matches? '%s'" % command["text"],
                                  file=sys.stderr)

                    match = re.match(command["re"], line_strip)

                    if match:
                        if debug:
                            print("--- match", file=sys.stderr)


                        # if this command specifies an action function is to
                        # be called, do that

                        if "action" in command:
                            if debug:
                                print("--- calling action function",
                                      file=sys.stderr)

                            command["action"](
                                match.groupdict(),
                                context_params.get("config", None),
                                context_params)


                        # if this command specifies a new [sub] context is to
                        # entered, change to that

                        if "new_context" in command:
                            if command["new_context"] in self._commands:
                                if debug:
                                    print("--- new context '%s'" %
                                              command["new_context"],

                                          file=sys.stderr)

                                new_context["name"] = command["new_context"]

                            else:
                                if debug:
                                    print("--- new context '%s' unknown - "
                                          "ignoring" % command["new_context"],

                                          file=sys.stderr)


                        # take the parameters which may have been modified by
                        # the action function and store them in the new context

                        new_context["params"] = context_params


                        # since we've found a matching command, don't bother
                        # looking for any more

                        break


                # store the new context on the stack

                context_stack.append(new_context)


        file.close()


        # perform any post-parsing processing

        self._post_parse_file()


    def _post_parse_file(self):
        """This method is called after parsing a file into the
        configuration dictionary with parse_file().  In this abstract
        class, it does nothing, but can be overridden in child classes
        to perform any necessary processing.
        """

        pass


    def get_config(self):
        "Return the parsed configuration."

        return self._config
