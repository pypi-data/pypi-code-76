# configchanges.py
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Configuration changes module.

This module is used to assist in building up a configuration file to
transform one configuration into another.  The configuration is
constructed of 'blocks' which may be discarded, if no difference is
recorded within them.
"""



# --- classes ----



class BlockedConfigChanges:
    """This class is used to build up a configuration file which will
    transform a configuration into a new configuration.

    Lines can be added to the configuration in blocks (which correspond
    to marked ranges, not necessarily indented sections of
    configuration).  A block defaults to 'unchanged' but can be marked
    as 'changed', when a difference is encounted.

    When a block is completed, if it was marked as changed, it will be
    included in the resulting configuration.  If it did not contain any
    changes, it will be discarded.  This allows previous lines (perhaps
    entering subcontext / indented sections) to be built up but thrown
    away, if they weren't needed.

    Blocks can be nested to arbitrary depths.  If a subblock is marked
    as changed, this will propagate to the parent block, including that
    in the output.

    Blocks can be marked in two ways: with surrounding blockbegin() and
    blockend() method calls, or using 'with' construct against the
    block() method (which will automatically call these at the start
    and end of the block.
    """


    def __init__(self):
        # the block stack contains the parent blocks, when nesting is
        # used it starts out empty; blockbegin() and blockend()
        # handle nesting

        self._block_stack = []


        # these contain the stack of indent strings (added to and
        # removed from using identbegin() and indentend()) and the
        # current entire indent string (the elements of the indent
        # stack joined together)
        #
        # the stack starts empty and, by association, the entire indent
        # string is also empty

        self._indent_stack = []
        self._indent = ""


        # the lines in the current block

        self._lines = []


        # the changed flag for the current block

        self._changed = False


    def append(self, *lines):
        """Append one or more lines to the current block.

        Keyword arguments:

        *lines -- one or more lines to add, as a series of arguments;
        if no lines are specified, a single blank line is added
        """

        if lines:
            self.extend(lines)
        else:
            self._lines.append(self._indent)


    def extend(self, *lines_list):
        """Append one or more lists of lines to the current block.

        Keyword arguments:

        *lines_list -- one or more lists of lines to add
        """

        for lines in lines_list:
            self._lines.extend([ self._indent + l for l in lines ])


    def appendtext(self, text):
        """Append a piece of text to the current block.  The text is
        split on newlines and each separate line added.  This is useful
        where a multiline string (using triple-quotes) is more
        convenient to add than separate lines through multiple calls to
        append().

        Leading or trailing newlines will be removed, avoiding the need
        to strip those out, when placing triple quotes on separate
        lines.

        To add multiple lines explicitly, rather than rely on spliting
        a block of text, the append() method is more suitable.

        Keyword arguments:

        multiline -- multiline string to split and add the lines of
        """

        self.extend([ self._indent + l
                          for l in multiline.strip("\n").split("\n") ])


    def changed(self):
        """Set the 'changed' flag of current block, such that the lines
        in it are included in the final output.
        """

        self._changed = True


    def blockbegin(self, header=None, indent=None):
        """Start a new sub-block in the configuration.  This pushes the
        current block onto the stack and resets the lines and changed
        flag to the empty and unset, respectively.

        Use blockend() when the block is completed.

        Alternatively, a block can be begun/ended using a 'with'
        statement and the block() method.  These can be freely mixed
        but not for a particular block.

        Keyword arguments:

        header=None -- if this is specified, the string is added to the
        block, after it has been begun but before the indenting has
        been configured.

        indent=None -- if this is specified, the new block will be
        indented using the supplied string; this will be saved in the
        block stack and the indented block ended, when the block is
        ended
        """


        # push the current block status onto the block stack

        self._block_stack.append((self._lines, self._changed, indent))


        # reset the lines and changed status for the current block

        self._lines = []
        self._changed = False


        # if a leading line of text was specified, add it to the newly
        # begun block

        if header:
            self.append(header)


        # if an indent string was specified, start an indent

        if indent:
            self.indentbegin(indent)


    def blockend(self):
        """This marks a block as completed.  If nothing has changed in
        the current block, it is discarded.  Conversely, if something
        has changed, the lines in it will be added to the parent block
        and the changed flag on the parent block is set.

        The parent block's context will then be restored as the current
        block.

        If the block was indented when begun using blockbegin(), the
        indented will be ended.
        """


        if not self._block_stack:
            raise(IndexError("block stack is empty"))


        # pop the details of the parent block off the block stack

        parent_lines, parent_changed, child_indent = self._block_stack.pop()


        # if this block has changed, add the lines to the parent block
        # and set the changed flag in it

        if self._changed:
            parent_lines.extend(self._lines)
            parent_changed = True


        # restore the parent block's context as the current block

        self._lines = parent_lines
        self._changed = parent_changed


        # end the indented section, if this block was indented when it
        # was begun

        if child_indent:
            self.indentend()


    def indentbegin(self, indent=" "):
        """Begin an indented section of the configuration, indented
        with the supplied string (or a single space, if no string is
        specified).

        This is an alternative to explicitly specifying the indent in
        each append()ed line, but using this feature ensures that all
        lines are appropriately indented.

        The entire indent string is updated accordingly and the string
        used for this level recorded in the indent stack.

        An indented block is ended using indentend().

        An indented section can also be begun using blockbegin() (and
        ended with blockend()) with the appropriate arguments, avoiding
        the need to do this explicitly.
        """

        self._indent_stack.append(indent)

        # recalculate the entire indent string
        self._indent = "".join(self._indent_stack)


    def indentend(self):
        """This method ends an indented block, removing the most recent
        ident string from the indent stack and recalculating the indent
        string.

        blockend() will also end an indented block, if it started with
        the appropriate argument to blockbegin().
        """

        if not self._indent_stack:
            raise(IndexError("indent stack is empty"))

        self._indent_stack.pop()

        # recalculate the entire indent string
        self._indent = "".join(self._indent_stack)


    def block(self, header=None, indent=None):
        """This method returns a _BlockedConfigChangesBlock object,
        which allows a block to be begun and ended using a 'with'
        statement, rather than explicitly, using blockbegin() and
        blockend().
        """

        return _BlockedConfigChangesBlock(self, header, indent)


    def getconfig(self):
        """Return the configuration changes as a single, multiline
        string.  If nothing changed, None is returned.

        This method can only be called at the top level block (i.e.
        when no subblocks have been entered), otherwise an exception
        will be raised.
        """

        if self._block_stack:
            raise(IndexError("block stack is not empty"))

        if not self._changed:
            return None

        return "\n".join(self._lines)



class _BlockedConfigChangesBlock:
    """This class is returned by the BlockedConfigChanges.block()
    method to allow a configuration block to be begun and ended using a
    'with' statement, rather than explicitly, using the blockbegin()
    and blockend() methods.

    The constructor takes two arguments: header and indent - these are
    used when entering the block as the equivalent arguments to
    blockbegin().
    """


    # variable to store the BlockedConfigChanges object in

    cfg = None


    # the constructor simply stores the supplied BlockedConfigChanges
    # object

    def __init__(self, init_cfg, header=None, indent=None):
        self.cfg = init_cfg
        self._header = header
        self._indent = indent


    # begin and end blocks, when the 'with' statement is entered and
    # exited

    def __enter__(self):
        self.cfg.blockbegin(self._header, self._indent)

    def __exit__(self, type, value, tb):
        self.cfg.blockend()
