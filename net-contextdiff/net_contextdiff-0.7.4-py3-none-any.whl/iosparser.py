# iosparser.py
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Cisco IOS configuration parser module.

This module parses Cisco IOS configuration files into a dictionary with
all of the recognised elements stored in it.

It is used to compare two configurations and determine the differences.
"""



# --- imports ---



import re, sys

from netaddr import IPNetwork

from .configparser import IndentedContextualConfigParser



# --- classes ----



# class CiscoIOSConfigParser()
#
# This is the concrete class to parse Cisco IOS configuration files.


class CiscoIOSConfigParser(IndentedContextualConfigParser):
    "This class parses Cisco IOS configuration files."


    def _post_parse_file(self):
        """Extend the inherited method to flush any pending IPv4
        standard ACL rules into the configuration.
        """

        # there isn't anything in the inherited method, by we should
        # call it in case there is in future
        super()._post_parse_file()

        # go through the pending IPv4 standard ACLs and store them
        # (we need to convert this to a list as _acl4_std_store_-
        # pending() will change the dictionary during iteration)
        for id in list(self._config.get("acl4-std-pending", {})):
            self._acl4_std_store_pending(id)


    # this function has a number of locally-defined functions that are the
    # action functions for the various contexts
    #
    # each function is defined and then the command using it added with
    # _add_command() to keep them adjacent and make it easier to see what
    # groups the regular expression is defining


    # VLANS


    _CMD_VLAN_RE = r"vlan (?P<tag>\d+)",

    def _cmd_vlan(self, groups, contextconfig, params):
        tag = int(groups["tag"])

        # create parts of the configuration, if they don't exist
        self._config.setdefault("vlans", {})
        self._config["vlans"].setdefault(tag, {})

        # remember what VLAN we're in the context of
        params["tag"] = tag

        # store a reference to this VLAN's part of the configuration
        params["config"] = self._config["vlans"][tag]


    _CMD_VLAN_NAME_RE = r"name (?P<name>\S+)",

    def _cmd_vlan_name(self, groups, contextconfig, params):
        name = groups["name"]

        # store the name of this VLAN
        contextconfig["name"] = name


    # SPANNING TREE


    _CMD_STP_NO_RE = r"no spanning-tree vlan (?P<tags>[-0-9,]+)"

    def _cmd_stp_no(self, groups, contextconfig, params):
        # create parts of the configuration, if they don't exist
        self._config.setdefault("no-stp", set())

        # the tags are a comma-separated list
        tags = groups["tags"].split(",")

        # the items in the tag list might be ranges, separated by hyphens
        for tag in tags:
            tag_range = tag.split("-")
            if len(tag_range) == 1:
                self._config["no-stp"].add(int(tag))

            else:
                for tag_elem in range(int(tag_range[0]),
                                      int((tag_range[1])) + 1):

                    self._config["no-stp"].add(tag_elem)


    _CMD_STP_PRIORITY_RE = (
        r"spanning-tree vlan (?P<tags>[-0-9,]+) priority (?P<priority>\d+)")

    def _cmd_stp_priority(self, groups, contextconfig, params):
        # create parts of the configuration, if they don't exist
        self._config.setdefault("stp-priority", {})

        # the tags are a comma-separated list
        tags = groups["tags"].split(",")
        priority = groups["priority"]

        # the items in the tag list might be ranges, separated by hyphens
        for tag in tags:
            tag_range = tag.split("-")
            if len(tag_range) == 1:
                self._config["stp-priority"][int(tag)] = priority

            else:
                for tag_elem in range(int(tag_range[0]),
                                      int((tag_range[1])) + 1):

                    self._config["stp-priority"][tag_elem] = priority


    # INTERFACES


    _CMD_INT_RE = r"interface (?P<name>\S+)",

    def _cmd_int(self, groups, contextconfig, params):
        # interface type aliases and their canonical forms

        INTERFACE_CANONICALS = {
          "ethernet": "Eth",
          "fastethernet": "Fa",
          "gigabitethernet": "Gi",
          "tengigabitethernet": "Te",
          "fortygigabitethernet": "Fo",
          "port-channel": "Po",
          "vl": "Vlan"
        }


        # canonicalise the type of an interface as they can be specified in
        # various shorthand forms, and in mixed case
        #
        # the canonical form is '<type><number>'; the type is first character
        # capitalised
        #
        # TODO: handle regexp of interface name

        name = groups["name"]
        match = re.match(r"^(?i)([-a-z]+)([0-9/.]*)$", name.lower())
        if match:
            type, num = match.groups()
            type = INTERFACE_CANONICALS.get(type, type).capitalize()
            name = type + num


        # create parts of the configuration, if they don't exist
        self._config.setdefault("interfaces", {})
        self._config["interfaces"].setdefault(name, {})

        # remember what interface we're in the context of
        params["name"] = name

        # store a reference to this interface's part of the configuration
        params["config"] = self._config["interfaces"][name]


    _CMD_INT_CDP_ENA_RE = r"(?P<no>no )?cdp enable"

    def _cmd_int_cdp_ena(self, groups, contextconfig, params):
        contextconfig.setdefault("options", set())

        # set the 'cdp enable' option, or remove it, if already set and
        # disabled
        if not groups["no"]:
            contextconfig["options"].add("cdp-enable")
        else:
            contextconfig["options"].discard("cdp-enable")


    _CMD_INT_CHGRP_RE = r"channel-group (?P<id>\d+)(?P<mode> .+)?"

    def _cmd_int_chgrp(self, groups, contextconfig, params):
        contextconfig["chgrp"] = (groups["id"], groups["mode"])


    _CMD_INT_DESC_RE = r"description (?P<description>.+)"

    def _cmd_int_desc(self, groups, contextconfig, params):
        contextconfig["description"] = groups["description"]


    _CMD_INT_ENCAP_RE = r"encapsulation (?P<encap>dot1q \d+( native)?)"

    def _cmd_int_encap(self, groups, contextconfig, params):
        # lower case the encapsulation definition as IOS stores 'dot1q'
        # as 'dot1Q'
        contextconfig["encap"] = groups["encap"].lower()


    _CMD_INT_HELPER_ADDR_RE = (
        r"ip helper-address (?P<helper_addr>(global )?\S+)")

    def _cmd_int_ip_helper_addr(self, groups, contextconfig, params):
        # create parts of the configuration, if they don't exist
        contextconfig.setdefault("ip-helper-addr", set())

        contextconfig["ip-helper-addr"].add(groups["helper_addr"])


    _CMD_INT_IP_ACCESS_GROUP_RE = (
        r"ip access-group (?P<access_group>\S+) (?P<direction>in|out)")

    def _cmd_int_ip_access_group(self, groups, contextconfig, params):
        # create parts of the configuration, if they don't exist
        contextconfig.setdefault("ip-access-group", {})

        contextconfig["ip-access-group"][groups["direction"]] = (
           groups["access_group"])


    _CMD_INT_IP_ADDR_RE = (
        r"ip address (?P<addr>\S+) (?P<netmask>\S+)"
        r"(?P<secondary> secondary)?")

    def _cmd_int_ip_addr(self, groups, contextconfig, params):
        if not groups["secondary"]:
            # primary address - record that specially
            contextconfig["ip-address"] = (groups["addr"], groups["netmask"])

        else:
            # secondary address - record it in a list

            # create parts of the configuration, if they don't exist
            contextconfig.setdefault("ip-address-secondary", set())

            contextconfig["ip-address-secondary"].add(
                (groups["addr"], groups["netmask"]))


    _CMD_INT_IPV6_ADDR_RE = r"ipv6 address (?P<addr>\S+)"

    def _cmd_int_ipv6_addr(self, groups, contextconfig, params):
        contextconfig.setdefault("ipv6-address", set())

        contextconfig["ipv6-address"].add(groups["addr"].lower())


    _CMD_INT_VRF_FWD_RE = (r"vrf forwarding (?P<vrf>\S+)")

    def _cmd_int_vrf_fwd(self, groups, contextconfig, params):
        contextconfig["vrf-forwarding"] = groups["vrf"]


    _CMD_INT_SERV_POL_RE = r"service-policy (?P<policy>.+)"

    def _cmd_int_serv_pol(self, groups, contextconfig, params):
        # create parts of the configuration, if they don't exist
        contextconfig.setdefault("service-policy", set())

        contextconfig["service-policy"].add(groups["policy"])


    _CMD_INT_SHUTDOWN_RE = r"(?P<no>no )?shutdown"

    def _cmd_int_shutdown(self, groups, contextconfig, params):
        contextconfig.setdefault("options", set())

        # set the 'shutdown' option, or remove it, if already set and disabled
        if not groups["no"]:
            contextconfig["options"].add("shutdown")
        else:
            contextconfig["options"].discard("shutdown")


    _CMD_INT_SWPORT_TRK_NTV_RE = r"switchport trunk native vlan (?P<vlan>\d+)"

    def _cmd_int_swport_trk_ntv(self, groups, contextconfig, params):
        contextconfig["swport-trk-ntv"] = groups["vlan"]


    _CMD_INT_SWPORT_TRK_ALW_RE = (
        r"switchport trunk allowed vlan (add )?(?P<vlans>[0-9,-]+)")

    def _cmd_int_swport_trk_alw(self, groups, contextconfig, params):
        contextconfig.setdefault("swport-trk-alw", set())

        vlans = groups["vlans"]

        # work through the comma-separated list of VLANs

        for i in vlans.split(","):
            if i.find("-") < 0:
                # there is no hyphen ("-") then this is a simple number, so
                # just add that

                contextconfig["swport-trk-alw"].add(int(i))

            else:
                # there is a hyphen, so it's a range of VLANs, work out all
                # the involved numbers and add those

                low, high = i.split("-")
                for n in range(int(low), int(high) + 1):
                    contextconfig["swport-trk-alw"].add(n)


    _CMD_INT_XCONN_RE = r"xconnect (?P<remote>[0-9.]+ \d+ .+)"

    def _cmd_int_xconn(self, groups, contextconfig, params):
        contextconfig["xconnect"] = groups["remote"]


    # IPV4 AND IPV6 STATIC ROUTES


    _CMD_IP_ROUTE_RE = r"ip route (?P<route>.+)"

    def _cmd_ip_route(self, groups, contextconfig, params):
        # create parts of the configuration, if they don't exist
        self._config.setdefault("route4", set())

        self._config["route4"].add(groups["route"])


    _CMD_IPV6_ROUTE_RE = r"ipv6 route (?P<route>.+)"

    def _cmd_ipv6_route(self, groups, contextconfig, params):
        # create parts of the configuration, if they don't exist
        self._config.setdefault("route6", set())

        self._config["route6"].add(groups["route"].lower())


    # ACCESS LISTS (IPV4 STANDARD)


    # regular expression for matching an IPv4 standard ACL rule, compiled once
    # for efficiency

    _ACL4_STD_RULE_RE = re.compile(
        r"^"
        r"(?P<action>permit|deny)"
        r" +"

        # we match "0.0.0.0 255.255.255.255" as "any" because the
        # netaddr module assumes the mask is a netmask (= /32) rather
        # than a hostmask
        r"((?P<any>any|0\.0\.0\.0 255\.255\.255\.255)|"
            r"(?:host )?(?P<host>[0-9.]+)|"
            r"(?P<net>[0-9.]+) (?P<mask>[0-9.]+))"
        r"$")


    def _acl4_std_rule_parse(self, rule):
        """Parse an IPv4 standard ACL rule, returning a 2-element tuple
        consisting of the 'action' ('permit' or 'deny') and an
        IPNetwork object specifying the address/network to match.
        """


        match = self._ACL4_STD_RULE_RE.match(rule)
        if not match:
            raise ValueError(
                      "failed to parse IPv4 standard ACL rule: '%s'" % rule)


        action = match.group("action")


        # match some special cases and, if not those, match as a
        # network/hostmask

        if match.group("any"):
            ipnet4 = IPNetwork("0.0.0.0/0")

        elif match.group("host"):
            ipnet4 = IPNetwork(match.group("host"))

        else:
            ipnet4 = IPNetwork(match.group("net") + "/" + match.group("mask"))


        return action, ipnet4


    def _ipnet4_to_ios(self, ipnet4):
        """This method converts an IPv4 IPNetwork object into its
        representation in Cisco IOS as a string.

        Conversions include '0.0.0.0/0' to 'any' and single host
        networks (i.e. simple addresses) into a plain address with no
        mask.
        """

        if ipnet4 == IPNetwork("0.0.0.0/0"):
            return "any"

        if ipnet4.prefixlen == 32:
            return str(ipnet4.ip)

        return str(ipnet4.ip) + " " + str(ipnet4.hostmask)


    def _acl4_std_add_rule(self, id, rule):
        """This method adds a rule to an IPv4 standard ACL.  The name
        (or number) of ACL is supplied, along with the rule in string
        form.  The rule will be parsed into the action and address
        portions.

        The process is significantly complicated by IOS's tendency to
        reorganise rules in a standard ACL.  It preserves the semantics
        of the rules (never putting an overlapping 'permit' and 'deny'
        in the wrong order, but can move rules which don't interact
        around.

        The solution adopted here is to build the ACL up in 'blocks'.
        Each block is a set of rules where the address portions don't
        overlap - these are built up and then, finally, sorted into
        numeric address order, before storing.

        When a rule is read which has an address portion that overlaps
        one of the rules in the current ("pending") block so far, the
        existing rules are sorted and stored, then a new block begun
        with the new rule.

        This results in lists which are not necessarily in the same
        order as they were constructed, but two lists should be the
        same.  This allows two lists to be compared with the
        _diff_lists() method.
        """

        action, ipnet4 = self._acl4_std_rule_parse(rule)

        # create parts of the configuration, if they don't exist
        self._config.setdefault("acl4-std-pending", {})
        self._config["acl4-std-pending"].setdefault(id, set())

        # check if there is an overlap with the address part of a rule
        # in the current block
        overlap = [None for _, check_ipnet4
                       in self._config["acl4-std-pending"][id]
                       if ((ipnet4.first <= check_ipnet4.last)
                           and (ipnet4.last >= check_ipnet4.first))]

        # if there was an overlap, store the pending block and create a
        # new, empty one
        if overlap:
            self._acl4_std_store_pending(id)
            self._config["acl4-std-pending"][id] = set()

        # add this rule to the pending block (either the existing one,
        # or a new one)
        self._config["acl4-std-pending"][id].add((action, ipnet4))


    def _acl4_std_store_pending(self, id):
        """This method stores the current ("pending") block in the
        configuration and then deletes it (so if any further rules are
        added, a new "pending" block will need to be created first).

        The rules are first sorted, into address order, then converted
        into IOS textual format.
        """

        # sort the rules in the current block based on the address
        # portion (the second tuple) and then convert them to text form
        rules = [(action + " " + self._ipnet4_to_ios(ipnet4))
                 for action, ipnet4
                 in sorted(self._config["acl4-std-pending"][id],
                           key=(lambda rule: rule[1]))]

        # create parts of the configuration, if they don't exist
        self._config.setdefault("acl4-std", {})
        self._config["acl4-std"].setdefault(id, [])

        self._config["acl4-std"][id].extend(rules)

        # delete the current block (it will need to be recreated with
        # an empty set, if it is required)
        self._config["acl4-std-pending"].pop(id)


    _CMD_ACL_STDNUM_RE = (
        r"access-list (?P<num>\d{1,2}|1[3-9]\d{2}) (?P<rule>.+)")

    def _cmd_acl_stdnum(self, groups, contextconfig, params):
        num = groups["num"]

        self._acl4_std_add_rule(num, groups["rule"])


    _CMD_ACL_STDNAME_RE = r"ip access-list standard (?P<name>.+)"

    def _cmd_acl_stdname(self, groups, contextconfig, params):
        name = groups["name"]

        # create parts of the configuration, if they don't exist
        self._config.setdefault("acl4-std", {})
        self._config["acl4-std"].setdefault(name, [])

        # remember what ACL we're in the context of
        params["name"] = name


    _CMD_ACL_STDNAME_RULE_RE = r"(?P<rule>(permit|deny) +.+)"

    def _cmd_acl_stdname_rule(self, groups, contextconfig, params):
        rule = groups["rule"]

        self._acl4_std_add_rule(params["name"], groups["rule"])


    # ACCESS LISTS (IPV4 EXTENDED + IPV6 COMMON)


    def _service_to_port(self, service):
        """Converts a Cisco service name 'service' (as displayed/usable
        in an access-list rule) into a port number and return it as an
        integer.

        If the service name is not defined, it is assumed to already be
        numeric and is converted to an integer and returned.  If this
        conversion fails, an exception will be raised.
        """


        _service_ports = {
            "bootps": 67,
            "bootpc": 68,
            "discard": 9,
            "domain": 53,
            "ftp-data": 20,
            "ftp": 21,
            "gopher": 70,
            "ident": 113,
            "isakmp": 500,
            "lpd": 515,
            "mail": 25,
            "non500-isakmp": 4500,
            "ntp": 123,
            "smtp": 25,
            "snmp": 161,
            "tftp": 69,
            "www": 80
        }

        return int(_service_ports.get(service, service))


    # ACCESS LISTS (IPV4 EXTENDED)


    # regular expression for matching an IPv4 extended ACL rule, compiled once
    # for efficiency

    _ACL4_EXT_RULE_RE = re.compile(
        r"^"
        r"(?P<action>permit|deny)"
        r" +"
        r"(?P<protocol>ip|icmp|tcp|udp|igmp|pim|gre|esp)"
        r" "
        r"(?P<src_addr>any|host ([0-9.]+)|([0-9.]+) ([0-9.]+))"
        r"( ("
            # 'eq' and 'neq' can support a list of services - we need to match
            # them non-greedy
            r"((?P<src_port_listop>eq|neq) (?P<src_port_list>\S+( \S+)*?))|"

            r"((?P<src_port_1op>lt|gt) (?P<src_port_num>\S+))|"
            r"range (?P<src_port_low>\S+) (?P<src_port_high>\S+)"
        r"))?"
        r" "
        r"(?P<dst_addr>any|host ([0-9.]+)|([0-9.]+) ([0-9.]+))"
        r"( ("
            r"((?P<dst_port_listop>eq|neq) (?P<dst_port_list>\S+( \S+)*?))|"
            r"((?P<dst_port_1op>lt|gt) (?P<dst_port_num>\S+))|"
            r"range (?P<dst_port_low>\S+) (?P<dst_port_high>\S+)|"
            r"(?P<icmp_type>echo(-reply)?)"
        r"))?"
        r"(?P<established> established)?"
        r"(?P<qos> (dscp \S+))?"
        r"(?P<log> (log|log-input))?"
        r"$"
    )


    def _acl4_ext_rule_parse(self, rule):
        """Parse an IPv4 extended ACL rule, returning a 'normalised'
        form of the rule as a string.  The normalised form should allow
        two ACL rules which mean the same thing to be compared using a
        simple string comparison.

        This mainly involves extracting the port numbers and
        [potentially] translating them into port numbers, if they're
        named services (which can be used in rules, plus IOS will
        translate a numbered service to a name, if one matches).

        Note that no attempt is made to check the rule for validity.
        """


        match = self._ACL4_EXT_RULE_RE.match(rule)
        if not match:
            raise ValueError(
                      "failed to parse IPv4 extended ACL rule: '%s'" % rule)

        action, protocol, src_addr, dst_addr = match.group(
            "action", "protocol", "src_addr", "dst_addr")


        # group() will return an error if a named group does not exist in the
        # regexp; on the other hand, groupdict() will return a default value
        # (None, if not specified) for named groups that do not exist
        #
        # as such, we need to check if the retrieved groups are blank or not

        groups = match.groupdict()


        src_port = ""

        if groups["src_port_listop"]:
            # if 'src_port_eq' was found in the regular expression, it will be
            # one or more services, separated by spaces - we need to split the
            # list up and turn each one into a port number, then join the list
            # back together again

            src_port = (
                " %s %s" % (
                    groups["src_port_listop"],
                    " ".join([str(self._service_to_port(s))
                              for s
                              in groups["src_port_list"].split(" ")])))

        elif groups["src_port_1op"]:
            src_port = " %s %d" % (
                          groups["src_port_1op"],
                          self._service_to_port(groups["src_port_num"]))

        elif groups["src_port_low"]:
            src_port = " range %d %d" % (
                           self._service_to_port(groups["src_port_low"]),
                           self._service_to_port(groups["src_port_high"]))


        dst_port = ""

        if groups["dst_port_listop"]:
            dst_port = (
                " %s %s" % (
                    groups["dst_port_listop"],
                    " ".join([str(self._service_to_port(s))
                              for s
                              in groups["dst_port_list"].split(" ")])))

        elif groups["dst_port_1op"]:
            dst_port = " %s %d" % (
                          groups["dst_port_1op"],
                          self._service_to_port(groups["dst_port_num"]))

        elif groups["dst_port_low"]:
            dst_port = " range %d %d" % (
                           self._service_to_port(groups["dst_port_low"]),
                           self._service_to_port(groups["dst_port_high"]))


        elif groups["icmp_type"]:
            dst_port = " %s" % groups["icmp_type"]


        established = groups.get("established", "")

        qos = groups.get("qos", "")

        log = groups.get("log", "")


        return "%s %s %s%s %s%s%s%s" % (
                   action, protocol, src_addr, src_port, dst_addr, dst_port,
                   established, qos)


    _CMD_ACL_EXTNUM_RE = (
        r"access-list (?P<num>1\d{2}|2[0-6]\d{2}) (?P<rule>.+)")

    def _cmd_acl_extnum(self, groups, contextconfig, params):
        name = groups["num"]

        # create parts of the configuration, if they don't exist
        self._config.setdefault("acl4-ext", {})
        self._config["acl4-ext"].setdefault(name, [])

        rule = self._acl4_ext_rule_parse(groups["rule"])
        self._config["acl4-ext"][name].append(rule)


    _CMD_ACL_EXTNAME_RE = r"ip access-list extended (?P<name>.+)"

    def _cmd_acl_extname(self, groups, contextconfig, params):
        name = groups["name"]

        # create parts of the configuration, if they don't exist
        self._config.setdefault("acl4-ext", {})
        self._config["acl4-ext"].setdefault(name, [])

        # remember what ACL we're in the context of
        params["name"] = name


    _CMD_ACL_EXTNAME_RULE_RE = r"(?P<rule>(permit|deny) +.+)"

    def _cmd_acl_extname_rule(self, groups, contextconfig, params):
        rule = groups["rule"]

        self._config["acl4-ext"][params["name"]].append(
            self._acl4_ext_rule_parse(rule))


    # ACCESS-LISTS (IPV6)


    # regular expression for matching an IPv6 access-list rule, compiled once
    # for efficiency
    #
    # TODO: we know this doesn't match some of the more complicated rules (such
    # as the CP policing ones matching ICMPv6 types) but we're excluding those
    # in the output, anyway, so we just ignore them.  As such, we don't match
    # the end of string ('$').

    _ACL6_RULE_RE = re.compile(
        r"^"
        r"(?P<action>permit|deny)"
        r"( "
          r"(?P<protocol>ipv6|icmp|tcp|udp|\d+)"
        r")?"
        r" "
        r"(?P<src_addr>any|host [0-9A-Fa-f:]+|[0-9A-Fa-f:]+/\d+)"
        r"( ("
            r"((?P<src_port_1op>eq|lt|gt|neq) (?P<src_port_num>\S+))|"
            r"range (?P<src_port_low>\S+) (?P<src_port_high>\S+)"
        r"))?"
        r" "
        r"(?P<dst_addr>any|host [0-9A-Fa-f:]+|[0-9A-Fa-f:]+/\d+)"
        r"( ("
            r"((?P<dst_port_1op>eq|lt|gt|neq) (?P<dst_port_num>\S+))|"
            r"range (?P<dst_port_low>\S+) (?P<dst_port_high>\S+)|"
            r"(?P<icmp_type>echo(-reply)?)"
        r"))?"
        r"(?P<established> established)?"
        r"(?P<log> (log|log-input))?"
    )


    def _acl6_rule_parse(self, rule):
        """Parse an IPv6 ACL rule, returning a 'normalised' form of the
        rule as a string.  The normalised form should allow two ACL
        rules which mean the same thing to be compared using a simple
        string comparison.

        This mainly involves extracting the port numbers and
        [potentially] translating them into port numbers, if they're
        named services (which can be used in rules, plus IOS will
        translate a numbered service to a name, if one matches).

        Note that no attempt is made to check the rule for validity.
        """


        match = self._ACL6_RULE_RE.match(rule)
        if not match:
            raise ValueError("failed to parse IPv6 ACL rule: '%s'" % rule)


        action, protocol, src_addr, dst_addr = match.group(
            "action", "protocol", "src_addr", "dst_addr")


        # if the protocol was not specified, we default to 'ipv6'

        if protocol is None:
            protocol = "ipv6"


        # lower case the source and destination addresses since IPv6 addresses
        # can either be in upper or lower case (usually upper, in IOS); we
        # choose lower here, though, to avoid upper casing the keywords 'host'
        # and 'any'

        src_addr = src_addr.lower()
        dst_addr = dst_addr.lower()


        # group() will return an error if a named group does not exist in the
        # regexp; on the other hand, groupdict() will return a default value
        # (None, if not specified) for named groups that do not exist
        #
        # as such, we need to check if the retrieved groups are blank or not

        groups = match.groupdict()


        src_port = ""

        if groups["src_port_num"]:
            src_port = " %s %d" % (
                          groups["src_port_1op"],
                          self._service_to_port(groups["src_port_num"]))

        elif groups["src_port_low"]:
            src_port = " range %d %d" % (
                           self._service_to_port(groups["src_port_low"]),
                           self._service_to_port(groups["src_port_high"]))


        dst_port = ""

        if groups["dst_port_num"]:
            dst_port = " %s %d" % (
                          groups["dst_port_1op"],
                          self._service_to_port(groups["dst_port_num"]))

        elif groups["dst_port_low"]:
            dst_port = " range %d %d" % (
                           self._service_to_port(groups["dst_port_low"]),
                           self._service_to_port(groups["dst_port_high"]))


        elif groups["icmp_type"]:
            dst_port = " %s" % groups["icmp_type"]


        established = groups.get("established", "")

        log = groups.get("log", "")


        return ("{action} {protocol} {src_addr}{src_port} "
                "{dst_addr}{dst_port}{established}").format(
                   action=action, protocol=protocol,
                   src_addr=src_addr, src_port=src_port, dst_addr=dst_addr,
                   dst_port=dst_port, established=established)



    _CMD_ACL6_RE = r"ipv6 access-list (?P<name>.+)"

    def _cmd_acl6(self, groups, contextconfig, params):
        name = groups["name"]

        # create parts of the configuration, if they don't exist
        self._config.setdefault("acl6", {})
        self._config["acl6"].setdefault(name, [])

        # remember what ACL we're in the context of
        params["name"] = name



    _CMD_ACL6_RULE_RE = r"(?P<rule>(permit|deny) +.+)"

    def _cmd_acl6_rule(self, groups, contextconfig, params):
        rule = groups["rule"]

        self._config["acl6"][params["name"]].append(
            self._acl6_rule_parse(rule))


    # IPV4 AND IPV6 PREFIX LISTS


    _CMD_PFX_RE = r"ip prefix-list (?P<list>\S+) (seq \d+ )?(?P<rule>.+)"

    def _cmd_pfx4(self, groups, contextconfig, params):
        list = groups["list"]

        # create parts of the configuration, if they don't exist
        self._config.setdefault("pfx4", {})
        self._config["pfx4"].setdefault(list, [])

        self._config["pfx4"][list].append(groups["rule"].lower())


    _CMD_PFX6_RE = (r"ipv6 prefix-list (?P<list>\S+) (seq \d+ )?"
                    r"(?P<action>\w+ )(?P<pfx>.+?)"
                    r"(?P<comparison>|ge \d+|le \d+)")

    def _cmd_pfx6(self, groups, contextconfig, params):
        list = groups["list"]

        # create parts of the configuration, if they don't exist
        self._config.setdefault("pfx6", {})
        self._config["pfx6"].setdefault(list, [])

        # we parse elements of the rule to get the address portion in upper
        # case (the others we assume are in lower case)
        self._config["pfx6"][list].append(groups["action"] +
                                    groups["pfx"].upper() +
                                    groups["comparison"].lower())


    # ADD COMMANDS


    def _add_commands(self):
        """Add commands for parsing Cisco IOS configuration files.
        """


        # VLANs

        self._add_command(".", self._CMD_VLAN_RE, self._cmd_vlan, "vlan")
        self._add_command("vlan", self._CMD_VLAN_NAME_RE, self._cmd_vlan_name)


        # spanning tree

        self._add_command(".", self._CMD_STP_NO_RE, self._cmd_stp_no)
        self._add_command(".", self._CMD_STP_PRIORITY_RE,
                          self._cmd_stp_priority)


        # interfaces

        self._add_command(".", self._CMD_INT_RE, self._cmd_int, "interface")
        self._add_command("interface", self._CMD_INT_CDP_ENA_RE,
                          self._cmd_int_cdp_ena)
        self._add_command("interface", self._CMD_INT_CHGRP_RE,
                          self._cmd_int_chgrp)
        self._add_command("interface", self._CMD_INT_DESC_RE,
                          self._cmd_int_desc)
        self._add_command("interface", self._CMD_INT_ENCAP_RE,
                          self._cmd_int_encap)
        self._add_command("interface", self._CMD_INT_HELPER_ADDR_RE,
                          self._cmd_int_ip_helper_addr)
        self._add_command("interface", self._CMD_INT_IP_ACCESS_GROUP_RE,
                          self._cmd_int_ip_access_group)
        self._add_command("interface", self._CMD_INT_IP_ADDR_RE,
                          self._cmd_int_ip_addr)
        self._add_command("interface", self._CMD_INT_IPV6_ADDR_RE,
                          self._cmd_int_ipv6_addr)
        self._add_command("interface", self._CMD_INT_VRF_FWD_RE,
                          self._cmd_int_vrf_fwd)
        self._add_command("interface", self._CMD_INT_SERV_POL_RE,
                          self._cmd_int_serv_pol)
        self._add_command("interface", self._CMD_INT_SWPORT_TRK_NTV_RE,
                          self._cmd_int_swport_trk_ntv)
        self._add_command("interface", self._CMD_INT_SWPORT_TRK_ALW_RE,
                          self._cmd_int_swport_trk_alw)
        self._add_command("interface", self._CMD_INT_SHUTDOWN_RE,
                          self._cmd_int_shutdown)
        self._add_command("interface", self._CMD_INT_XCONN_RE,
                          self._cmd_int_xconn)


        # static routes

        self._add_command(".", self._CMD_IP_ROUTE_RE, self._cmd_ip_route)
        self._add_command(".", self._CMD_IPV6_ROUTE_RE, self._cmd_ipv6_route)


        # ipv4 standard access-lists

        self._add_command(".", self._CMD_ACL_STDNUM_RE, self._cmd_acl_stdnum)

        self._add_command(".", self._CMD_ACL_STDNAME_RE,
                          self._cmd_acl_stdname, "acl4-stdname")

        self._add_command("acl4-stdname", self._CMD_ACL_STDNAME_RULE_RE,
                          self._cmd_acl_stdname_rule)


        # ipv4 extended access-lists

        self._add_command(".", self._CMD_ACL_EXTNUM_RE, self._cmd_acl_extnum)

        self._add_command(".", self._CMD_ACL_EXTNAME_RE, self._cmd_acl_extname,
                          "acl4-extname")

        self._add_command("acl4-extname", self._CMD_ACL_EXTNAME_RULE_RE,
                          self._cmd_acl_extname_rule)


        # ipv6 access-lists

        self._add_command(".", self._CMD_ACL6_RE, self._cmd_acl6, "acl6")

        self._add_command("acl6", self._CMD_ACL6_RULE_RE, self._cmd_acl6_rule)


        # prefix-lists

        self._add_command(".", self._CMD_PFX_RE, self._cmd_pfx4)

        self._add_command(".", self._CMD_PFX6_RE, self._cmd_pfx6)
