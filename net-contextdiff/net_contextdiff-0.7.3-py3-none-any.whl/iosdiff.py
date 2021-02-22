# iosdiff.py
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Cisco IOS configuration differences module.

This module compares two configurations for Cisco IOS devices and
produces a delta configuration.
"""



# --- imports ---



import re

from .configdiff import ConfigDiff



# --- context parser ---



class CiscoIOSConfigDiff(ConfigDiff):
    """This class is used to compare two IOS configuration files and
    generate a configuration file to transform one into the other.
    """


    # the 'rules' are used to control which parts of the configuration
    # are included into the comparison and which not
    #
    # it is set by the constructor to be a ConfigElementRules object


    def _matchinfo_comment(self, matchinfo):
        """This method adds a Cisco IOS comment (with leading '!') with
        the supplied 'matchinfo' to the output.

        It overrides the abstract method in the parent class, which
        raises a NotImplementedError exception.
        """

        return self._diffs.append("! [ " + matchinfo + " ]")


    def _diff_list(self, from_list, to_list, cmd, subcontext, description=None,
                  item_prefix=None, seq_first=None, seq_step=10,
                  check_area=None, check_id=None):

        """Compares two lists - the from-list and the to-list - and
        adds commands to the supplied configuration object, if it needs
        to be updated to get it into the to-list state (add, delete or
        recreate the list because something has changed in it).

        If the from-list exists and the to-list does not (to-list is
        None), the list is deleted.  If the the to-list does but the
        from-list does not, the list is created.

        If both lists exist, they are compared line by line and, if
        they differ, the old list is removed and the new replacement
        created.  The differences between them are highlighted with
        Cisco IOS comments (leading "!"s).

        If the lists are identical, nothing is added to the
        configuration.

        The lists can be of various types - access-lists, IP prefix-
        lists, etc.: the parameters to the function allow the output to
        be customised to fit the syntax of these different types.

        The comparison is not intelligent in that it doesn't try to
        understand situations where two lists might be identical but
        just differ due to syntactic differences: it just compares the
        literal strings for each item.  To cope with this situation,
        the lists must 'tidied up' or canoncalised by the code which
        parses them.

        Keyword arguments:

        from_list -- the starting list; this is None, if the list does
        not exist

        to_list -- the end state list; this is None, if the list does
        not exist

        cmd -- the command required to configure the list (e.g. "ip
        access-list extended LIST-ACL4")

        subcontext -- this flag is set if the configuration of the
        items in the list is done in a subconfiguration mode: the
        context will be entered with 'cmd' and the items entered one-
        by-one; if not set, each item will be specified with 'cmd'
        prefixed

        description=None -- a description of the list to put in the
        accompanying comments

        item_prefix=None -- if specified, this string is prefixed
        before the sequence number for each item

        seq_first=None -- if specified, this integer gives the sequence
        number for the first item; if not specified, the seq_step value
        is used

        seq_step=10 -- this is the stepping interval for sequence
        numbers of each item

        check_area=None -- the area for the configuration change to
        check against the rules; ignored unless the rules are set

        check_id=None -- the id for the configuration change to check
        against the rules; ignored unless the rules are set
        """


        # if the sequence first number was not specified, we assume
        # it's the same as the stepping interval

        if seq_first == None:
            seq_first = seq_step


        # if both lists do not exist, we don't need to do anything

        if (from_list is None) and (to_list is None):
            return


        # if there was no from-list (but there is a to-list), we just
        # need to create the to-list as a new list

        if from_list is None:
            # if the rules exclude creating this list, just abort

            if not self._include("+", check_area, check_id):
                return


            self._diffs.append("! new list - create "
                               + (description if description else cmd))


            # if the list items are added in a subcontext, we need the
            # starting command to create the new list

            if subcontext:
                self._diffs.append(cmd)


            # work through the items in the to-list, printing each one
            # with the list command (if not in a subcontext) and the
            # sequence item prefix (if specified)

            seq_num = seq_first

            for item in to_list:
                self._diffs.append((" " if subcontext else (cmd + " "))
                                   + ((item_prefix + " ") if item_prefix
                                          else "")
                                   + str(seq_num)
                                   + " "
                                   + item)

                seq_num += seq_step


            # add a blank line and mark this block as changed

            self._diffs.append()
            self._diffs.changed()

            return


        # if there is no to-list (but there is a from-list) we just
        # delete the list

        if to_list is None:
            # if the rules exclude deleting this list, just abort

            if not self._include("-", check_area, check_id):
                return


            self._diffs.append("no %s" % cmd)
            self._diffs.append()

            self._diffs.changed()

            return


        # if we get here, we have a from-list and a to-list and need to
        # work out if anything has changed
        #
        # as far as building up the configuration, we proceed as if
        # something has changed or not and use the block changed
        # features of the BlockedConfigChanges class to discard them,
        # if unused


        # begin the conditional block (this will be discarded, if
        # nothing ends up being changed)

        self._diffs.blockbegin()


        # if the rules exclude changing this list, just abort
        #
        # we have to do this inside the block as the _include() method
        # will add a comment if it would be included (even if nothing
        # changes)

        if not self._include("=", check_area, check_id):
            self._diffs.blockend()
            return


        # for convenience (to avoid repeatedly having to do this), set
        # a variable to use as an indent space, if we're using a
        # subcontext, otherwise an empty string

        indent = " " if subcontext else ""


        # we add a comment indicating things have changed

        self._diffs.append("! changed list - replace "
                               + (description if description else cmd),
                           "no " + cmd)


        # if configuring in a subcontext, include the opening command
        # to enter that context

        if subcontext:
            self._diffs.append(cmd)


        # del_lines and add_lines are used to batch up changes so
        # groups of lines being deleted and added are printed
        # adjacently in the output, rather than line by line - this
        # makes it clearer what has changed

        del_lines = []
        add_lines = []


        # work through the items in the from and to-lists - we do this
        # by counting through the elements (to the maximum of the
        # length of the two lists)

        seq_num = seq_first

        for item_num in range(0, max(len(from_list), len(to_list))):
            # again, for convenience, work out the prefix for any
            # particular line in the list - this will include:
            #
            #   * the leading command (if the list is not configured as
            #     a subconfiguration stanza)
            #
            #   * the supplied prefix for an item, if specified
            #
            #   * the sequence number

            item_seq_prefix = (("" if subcontext else (cmd + " "))
                               + ((item_prefix + " ") if item_prefix
                                      else "")
                               + str(seq_num))


            # if this item number is greater than the length of the to-
            # list, the from-list is longer and we're removing
            # extraneous items

            if item_num >= len(to_list):
                del_lines.append(indent
                                 + ("!- %s %s" % (item_seq_prefix,
                                                  from_list[item_num])))

                self._diffs.changed()


            # if this item number if greater than the length of the
            # from-list, the to-list is longer and we're adding extra
            # items

            elif item_num >= len(from_list):
                # if this is the first extra item, and we've not
                # already started replacing a block of items, mark the
                # additional items with a comment

                if (item_num == len(from_list)) and (not del_lines):
                    add_lines.append(indent + "!+ ...")


                add_lines.append(indent
                                 + ("%s %s" % (item_seq_prefix,
                                               to_list[item_num])))

                self._diffs.changed()


            else:
                # if this item is different, add it to the list of
                # items to delete (which may be empty)
                #
                # we do this to batch the deletions together into a
                # block

                if from_list[item_num] != to_list[item_num]:
                    del_lines.append(indent
                                     + ("!- %s %s" % (item_seq_prefix,
                                                      from_list[item_num])))

                    self._diffs.changed()


                # this item is the same - if we have changes batched
                # up, 'print' and purge those changes

                elif del_lines:
                    self._diffs.extend(del_lines, add_lines)

                    del_lines = []
                    add_lines = []


                    # mark the beginning of the point where the items
                    # in both lists match again

                    self._diffs.append(indent + "!= ...")


                # add this item - if pending changes are being batched
                # up, we add it to the batch; otherwise, we're in a
                # section where the items match and can just 'print' it
                # directly

                line = (indent
                        + ("%s %s" % (item_seq_prefix, to_list[item_num])))

                if del_lines:
                    add_lines.append(line)

                else:
                    self._diffs.append(line)


            seq_num += seq_step


        # add any remaining batched changes to the output

        self._diffs.extend(del_lines, add_lines)


        # add a blank line and end the configuration block - this will
        # discard it, if nothing changed

        self._diffs.append()

        self._diffs.blockend()



    def diff_configs(self, from_cfg, to_cfg):
        """This method compares two configurations (the from_cfg and
        the to_cfg) and stores the commands converting one to the other
        in the object.

        This function can be called multiple times to build up the
        differences in stages, but the comparison will only be between
        the two entire configurations supplied each time.

        Nothing is returned.  The final, aggregate, differences are
        retrieved with the get_diff() method.
        """

        # VLANS


        # this section is commented heavily to explain what is going
        # on: there are other areas of the configuration comparison
        # code which follow much the same pattern and aren't documented
        # for brevity, except where they do something different


        # add or update VLANs - go through the list of VLANs in the 'to
        # configuration'

        for tag in sorted(to_cfg.get("vlans", {})):
            # the 'id' is used for configuration inclusion rules

            vlan_id = "vlan%d" % tag


            # the 'with' construct creates an optional block in the
            # configuration

            with self._diffs.block():
                # does the VLAN exist already?
                #
                # we store this so we can use it later, to ignore rules
                # which might stop adding/updating attributes
                # underneath it, when we're actually creating the whole
                # thing from scratch

                add_vlan = tag not in from_cfg.get("vlans", {})

                if add_vlan:
                    # check the rules include adding new VLANs - if
                    # not, skip this

                    if not self._include("vlan", vlan_id, "+"):
                        continue

                    self._diffs.append("! create new VLAN")
                    self._diffs.changed()


                    # for convenience later, assume an empty 'from
                    # configuration' for this VLAN

                    from_vlan = {}

                else:
                    # it exists - get the configuration for it

                    from_vlan = from_cfg["vlans"][tag]


                self._diffs.append("vlan %d" % tag)

                self._diffs.indentbegin()


                # get the 'to configuration' for this VLAN

                to_vlan = to_cfg["vlans"][tag]


                # get the new name for this VLAN (or None, if it's not
                # defined)

                to_vlan_name = to_vlan.get("name")


                # if we're adding the VLAN, we ignore any more-specific
                # rules which might prevent us from setting the name
                # because, fundamentally, we're permitting adding
                # VLANs, if we've got here
                #
                # otherwise, we check the rules permit the operation to
                # set/unset/change the name

                if (add_vlan or
                    self._compare_include(from_vlan.get("name"), to_vlan_name,
                                          "vlan.name", vlan_id)):

                    # if we get here, we're either adding a new VLAN,
                    # or something has changed (i.e. the 'from
                    # configuration' and 'to configuration' names are
                    # different)

                    if to_vlan_name is not None:
                        # the 'to configuration' name is set, so we're
                        # either setting a name where there wasn't one
                        # before, or we're changing the existing one

                        # TODO - IOS does not allow two VLANs with the
                        # same name, so we should ideally detect this
                        # and rename things in multiple stages, if
                        # that's the case (perhaps by changing names
                        # temporarily to "VLAN<tag>"

                        self._diffs.append("name %s" % to_vlan_name)

                    else:
                        # the 'to configuration' name is empty, so
                        # we're clearing the existing one

                        self._diffs.append("no name")


                    self._diffs.changed()


                self._diffs.indentend()


                # add a blank line at the end of the block

                self._diffs.append()


                # the block ends here, either discarding or storing the
                # changes



        # delete VLANs - go through the list of VLANs in the 'from
        # configuration', looking for ones which are not in the 'to
        # configuration'

        for tag in sorted(from_cfg.get("vlans", {})):
            if tag not in to_cfg.get("vlans", {}):
                # this VLAN needs to be deleted - check the rules
                # include that

                if self._include("vlan", "vlan%d" % tag, "-"):
                    self._diffs.append("no vlan %d" % tag)
                    self._diffs.append()

                    self._diffs.changed()


        # SPANNING TREE


        # no spanning-tree ...

        from_no_stp = set(from_cfg.get("no-stp", []))
        to_no_stp = set(to_cfg.get("no-stp", []))

        with self._diffs.block():
            for tag in sorted(to_no_stp.difference(from_no_stp)):
                if self._include("stp.no", "vlan%d" % tag, "-"):
                    self._diffs.append("no spanning-tree vlan %d" % tag)
                    self._diffs.changed()

            self._diffs.append()


        with self._diffs.block():
            for tag in sorted(from_no_stp.difference(to_no_stp)):
                if self._include("stp.no", "vlan%d" % tag, "+"):
                    self._diffs.append("spanning-tree vlan %d" % tag)
                    self._diffs.changed()

            self._diffs.append()


        # spanning-tree vlan ... priority ...

        from_stp_priority = from_cfg.get("stp-priority", {})
        to_stp_priority = to_cfg.get("stp-priority", {})

        with self._diffs.block():
            for tag in sorted(to_stp_priority):
                if self._compare_include(from_stp_priority.get(tag),
                                         to_stp_priority[tag], "stp.priority",
                                         "vlan%d" % tag):

                    self._diffs.append("spanning-tree vlan %s priority %s"
                                         % (tag, to_stp_priority[tag]))

                    self._diffs.changed()

            self._diffs.append()

        with self._diffs.block():
            for tag in sorted(from_stp_priority):
                if ((tag not in to_stp_priority) and
                    self._include("-", "stp.priority", "vlan%d" % tag)):

                    self._diffs.append(
                        "no spanning-tree vlan %d priority" % tag)

                    self._diffs.changed()

            self._diffs.append()


        # INTERFACES


        # go through all the interfaces before and after

        for interface in sorted(set(from_cfg.get("interfaces", {})).union(
                                    to_cfg.get("interfaces", {}))):

            if interface not in to_cfg.get("interfaces"):
                # skip fixed interfaces

                if re.match("^(Mgmt|Eth|Fa|Gi|Te|Fo)\d", interface):
                    continue

                if not self._include("-", "interface", interface):
                    continue

                self._diffs.append("no interface %s" % interface)
                self._diffs.append()
                self._diffs.changed()

                continue


            add_interface = interface not in from_cfg.get("interfaces")

            if add_interface:
                if not self._include("+", "interface", interface):
                    continue

                self._diffs.append("! create new interface")
                self._diffs.changed()

                from_interface = {}

            else:
                from_interface = from_cfg["interfaces"][interface]


            # start a block (don't use 'with' as this is a big one)

            self._diffs.blockbegin("interface " + interface, " ")


            to_interface = to_cfg["interfaces"][interface]


            # cdp enable

            to_interface_cdp_ena = "cdp-enable" in to_interface.get(
                                                       "options", set())
            from_interface_cdp_ena = "cdp-enable" in from_interface.get(
                                                         "options", set())

            if (add_interface or
                self._compare_include(from_interface_cdp_ena,
                                      to_interface_cdp_ena,
                                      "interface.cdp-enable", interface)):

                if to_interface_cdp_ena:
                    self._diffs.append("cdp enable")
                else:
                    self._diffs.append("no cdp enable")

                self._diffs.changed()


            # description

            from_interface_description = from_interface.get("description")
            to_interface_description = to_interface.get("description")

            if (add_interface or
                self._compare_include(from_interface_description,
                                      to_interface_description,
                                      "interface.description", interface)):

                if to_interface_description is not None:
                    self._diffs.append(
                        "description " + to_interface_description)

                elif from_interface_description is not None:
                    self._diffs.append(" no description")

                self._diffs.changed()


            # encapsulation

            from_interface_encap = from_interface.get("encap")
            to_interface_encap = to_interface.get("encap")

            if (add_interface or
                self._compare_include(from_interface_encap,
                                      to_interface_encap,
                                      "interface.encapsulation",
                                      interface)):

                if to_interface_encap is not None:
                    self._diffs.append(
                        "encapsulation " + to_interface_encap)

                elif from_interface_encap is not None:
                    self._diffs.append(
                        "no encapsulation " + from_interface_encap)

                self._diffs.changed()


            # vrf forwarding
            #
            # This must happen before any commands that refer to IP addresses
            # as changing the VRF of an interface clears all those out.

            from_interface_vrf_fwd = from_interface.get("vrf-forwarding")
            to_interface_vrf_fwd = to_interface.get("vrf-forwarding")

            # set up a flag to record if we change VRF - we will use that to
            # re-apply IP commands, if we do that.
            #
            # TODO: need to handle a VRF change re-applying all IP commands.
            vrf_change = False

            with self._diffs.block():
                 if (add_interface or
                     self._compare_include(from_interface_vrf_fwd,
                                           to_interface_vrf_fwd,
                                           "interface.vrf-fwd",
                                           interface)):

                     if to_interface_vrf_fwd is not None:
                         self._diffs.append(
                             "vrf forwarding " + to_interface_vrf_fwd,
                             " ! TODO: need to reapply IP information")

                     elif from_interface_vrf_fwd is not None:
                         self._diffs.append(
                             "no vrf forwarding",
                             " ! TODO: need to reapply IP information")

                     self._diffs.changed()

                     vrf_change = True


            # ip helper-address
            #
            # addition or deletion of ip helper-addresses is regarded as a
            # change

            self._diffs.blockbegin()

            iphelp_include, iphelp_remove, iphelp_add = (
                self._compare_set_include(
                    from_interface.get("ip-helper-addr"),
                    to_interface.get("ip-helper-addr"),
                    "interface.ip-helper-addr", interface))
 
            if add_interface or iphelp_include:
                for iphelperaddr in iphelp_remove:
                    self._diffs.append(
                        "no ip helper-address %s" % iphelperaddr)

                    self._diffs.changed()

                for iphelperaddr in iphelp_add:
                    self._diffs.append(
                        "ip helper-address %s" % iphelperaddr)

                    self._diffs.changed()

            self._diffs.blockend()


            # ip access-group

            self._diffs.blockbegin()

            for direction in ["in", "out"]:
                from_interface_access_group = from_interface.get(
                    "ip-access-group", {}).get(direction)
                to_interface_access_group = to_interface.get(
                    "ip-access-group", {}).get(direction)

                if (add_interface or
                    self._compare_include(from_interface_access_group,
                                          to_interface_access_group,
                                          "interface.ip-access-group",
                                          interface)):

                    if to_interface_access_group is not None:
                        self._diffs.append(
                            "ip access-group %s %s" %
                                (to_interface_access_group, direction))

                        self._diffs.changed()

                    elif from_interface_access_group is not None:
                        self._diffs.append("no ip access-group " + direction)

                        self._diffs.changed()

            self._diffs.blockend()


            # ip address

            # (primary)

            from_interface_ip_addr = from_interface.get("ip-address")
            to_interface_ip_addr = to_interface.get("ip-address")

            with self._diffs.block():
                if (add_interface or
                    self._compare_include(from_interface_ip_addr,
                                          to_interface_ip_addr,
                                          "interface.ip-addr",
                                          interface)):

                    if to_interface_ip_addr:
                        self._diffs.append(
                            "ip address %s %s" % to_interface_ip_addr)

                    elif from_interface_ip_addr:
                        self._diffs.append("no ip address")

                    self._diffs.changed()


            # (secondary)
            #
            # addition or deletion of secondary ip addresses is regarded as a
            # change

            self._diffs.blockbegin()

            ipaddr_include, ipaddr_remove, ipaddr_add = (
                self._compare_set_include(
                    from_interface.get("ip-address-secondary"),
                    to_interface.get("ip-address-secondary"),
                    "interface.ip-address", interface))

            if add_interface or ipaddr_include:
                for a in ipaddr_remove:
                    self._diffs.append("no ip address %s %s secondary" % a)
                    self._diffs.changed()

                for a in ipaddr_add:
                    self._diffs.append("ip address %s %s secondary" % a)
                    self._diffs.changed()

            self._diffs.blockend()


            # ipv6 address

            self._diffs.blockbegin()

            ipaddr_include, ipaddr_remove, ipaddr_add = (
                self._compare_set_include(
                    from_interface.get("ipv6-address"),
                    to_interface.get("ipv6-address"),
                    "interface.ipv6-address", interface))

            if add_interface or ipaddr_include:
                for a in ipaddr_remove:
                    self._diffs.append("no ipv6 address %s" % a)
                    self._diffs.changed()

                for a in ipaddr_add:
                    self._diffs.append("ipv6 address %s" % a)
                    self._diffs.changed()

            self._diffs.blockend()


            # service-policy

            self._diffs.blockbegin()

            servpol_include, servpol_remove, servpol_add = (
                self._compare_set_include(
                    from_interface.get("service-policy"),
                    to_interface.get("service-policy"),
                    "interface.service-policy", interface))

            if add_interface or servpol_include:
                for servpol in servpol_remove:
                   self._diffs.append("no service-policy %s" % servpol)
                   self._diffs.changed()

                for servpol in servpol_add:
                   self._diffs.append("service-policy %s" % servpol)
                   self._diffs.changed()

            self._diffs.blockend()


            # shutdown

            to_interface_shutdown = "shutdown" in to_interface.get(
                                                      "options", set())
            from_interface_shutdown = "shutdown" in from_interface.get(
                                                        "options", set())

            if (add_interface or
                self._compare_include(from_interface_shutdown,
                                      to_interface_shutdown,
                                      "interface.shutdown", interface)):

                if to_interface_shutdown:
                    self._diffs.append("shutdown")
                else:
                    self._diffs.append("no shutdown")

                self._diffs.changed()


            # skip VLAN changes on this port, if it's part of a port channel

            if "chgrp" not in to_interface:
                # switchport trunk native vlan ...

                from_native = from_interface.get("swport-trk-ntv")
                to_native = to_interface.get("swport-trk-ntv")

                if self._compare_include(
                       from_native, to_native,
                       "interface.switchport.trunk.native", interface):

                    if to_native is not None:
                        self._diffs.append(
                            "switchport trunk native vlan %s" % to_native)

                    else:
                        self._diffs.append("no switchport trunk native vlan")

                    self._diffs.changed()


                # switchport trunk allowed vlan ...

                _, vl_remove, vl_add = (
                    self._compare_set_include(
                        from_interface.get("swport-trk-alw"),
                        to_interface.get("swport-trk-alw"),
                        "interface.switchport.trunk.allow", interface))

                for vl in vl_remove:
                    self._diffs.append(
                        "switchport trunk allowed vlan remove %s" % vl)
                    self._diffs.changed()

                for vl in vl_add:
                    self._diffs.append(
                        "switchport trunk allowed vlan add %s" % vl)
                    self._diffs.changed()


            # xconnect

            from_interface_xconn = from_interface.get("xconnect")
            to_interface_xconn = to_interface.get("xconnect")

            if (add_interface or
                self._compare_include(from_interface_xconn,
                                      to_interface_xconn,
                                      "interface.xconnect",
                                      interface)):

                if to_interface_xconn is not None:
                    self._diffs.append("xconnect " + to_interface_xconn)

                elif from_interface_xconn is not None:
                    self._diffs.append("no xconnect")

                self._diffs.changed()


            # end of interface

            self._diffs.append()

            self._diffs.blockend()


        # STATIC ROUTES


        with self._diffs.block():
            _, rt4_remove, rt4_add = (
                self._compare_set_include(from_cfg.get("route4"),
                                          to_cfg.get("route4"), "ip-route",
                                          None))

            for rt4 in rt4_remove:
                self._diffs.append("no ip route " + rt4)
                self._diffs.changed()

            for rt4 in rt4_add:
                self._diffs.append("ip route " + rt4)
                self._diffs.changed()

            self._diffs.append()


        with self._diffs.block():
            _, rt6_remove, rt6_add = (
                self._compare_set_include(from_cfg.get("route6"),
                                          to_cfg.get("route6"), "ip-route",
                                          None))

            for rt6 in rt6_remove:
                self._diffs.append("no ip route " + rt6)
                self._diffs.changed()

            for rt6 in rt6_add:
                self._diffs.append("ip route " + rt6)
                self._diffs.changed()

            self._diffs.append()


        # ACCESS-LISTS


        # ip access-list standard ...

        from_acl4_std = from_cfg.get("acl4-std", {})
        to_acl4_std = to_cfg.get("acl4-std", {})

        for id in sorted(set(from_acl4_std).union(to_acl4_std)):
            self._diff_list(from_acl4_std.get(id), to_acl4_std.get(id),
                            "ip access-list standard " + id, subcontext=True,
                            description="IPv4 standard access list",
                            check_area="acl4", check_id=id)


        # ip access-list extended ...

        from_acl4_ext = from_cfg.get("acl4-ext", {})
        to_acl4_ext = to_cfg.get("acl4-ext", {})

        for id in [i for i in sorted(set(from_acl4_ext).union(to_acl4_ext))
                       if not i.startswith("acl-copp-")]:

            self._diff_list(from_acl4_ext.get(id), to_acl4_ext.get(id),
                            "ip access-list extended " + id, subcontext=True,
                            description="IPv4 extended access list",
                            check_area="acl4", check_id=id)


        # ipv6 access-list ...

        from_acl6 = from_cfg.get("acl6", {})
        to_acl6 = to_cfg.get("acl6", {})

        for id in [i for i in sorted(set(from_acl6).union(to_acl6))
                       if not i.startswith("acl-copp-")]:

            self._diff_list(from_acl6.get(id), to_acl6.get(id),
                            "ipv6 access-list " + id, subcontext=True,
                            description="IPv6 access list", item_prefix="seq",
                            check_area="acl6", check_id=id)


        # PREFIX-LISTS


        # ip prefix-list ...

        from_pfx4 = from_cfg.get("pfx4", {})
        to_pfx4 = to_cfg.get("pfx4", {})

        for name in sorted(set(from_pfx4).union(to_pfx4)):
            self._diff_list(from_pfx4.get(name), to_pfx4.get(name),
                            "ip prefix-list " + name, subcontext=False,
                            description="IPv4 prefix list", item_prefix="seq",
                            seq_step=5, check_area="pfx4", check_id=name)


        # ipv6 prefix-list ...

        from_pfx6 = from_cfg.get("pfx6", {})
        to_pfx6 = to_cfg.get("pfx6", {})

        for name in sorted(set(from_pfx6).union(to_pfx6)):
            self._diff_list(from_pfx6.get(name), to_pfx6.get(name),
                            "ipv6 prefix-list " + name, subcontext=False,
                            description="IPv6 prefix list", item_prefix="seq",
                            seq_step=5, check_area="pfx6", check_id=name)


        # END


    def get_diffs(self):
        """This method extends the inherited class to add a line with
        'end' onto the end of the the configuration.
        """

        # add the 'end' statement (but this will discarded, if nothing
        # has changed)

        self._diffs.append("end")


        return super().getconfig()
