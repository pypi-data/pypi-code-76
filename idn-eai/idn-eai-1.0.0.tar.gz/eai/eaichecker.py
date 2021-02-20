#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author : Arpit Gupta
Created Date : 27-April-2020
This script is written to find out whether domain's Mail Server has SMTPUTF8 support or not
"""

import smtplib
import dns.resolver


def smtputf8_check(domain):
    """
        :param domain: name of the valid domain
        :return: whether domain mail server has UTF-8 support or not
    """

    return_values = ["TRUE", "FALSE", "EXCEPTION"]

    try:

        mx_list = []

        # check whether domain contains utf-8 string
        '''
        if not re.search("^[a-zA-Z0-9.-]+$", domain):
            domain = domain.decode("utf-8")
        '''

        # domain = argparser.ArgumentParser(description='Parse Domain')
        # domain.add_argument()
        for x in dns.resolver.resolve(domain, 'MX'):
            #  print(x.to_text())
            mx_list.append(x.to_text().split()[1])

        mx_list.sort()

        # print(mxList[0])
        smtpobject = smtplib.SMTP(mx_list[0], 25)
        # print(smtpObj.ehlo()[1])
        # print(type(smtpObj.ehlo()))
        # strObj = ''.join(smtpObj.ehlo())
        bytes_string_object = smtpobject.ehlo()[1]
        # print(strObj)
        '''
        In Python 3, strings are Unicode, but when transmitting on the network, 
        the data needs to be bytes string instead 
        '''
        if b'SMTPUTF8' in bytes_string_object:
            # log_exception("Domain "+domain+" does have SMTPUTF8 in ehlo response\n")
            print(f"Domain {domain} does have SMTPUTF8 in ehlo response")
            return return_values[0]
        else:
            # log_exception("Domain "+domain+" does not have SMTPUTF8 in ehlo response\n")
            print(f"Domain {domain} does not have SMTPUTF8 in ehlo response")
            return return_values[1]

    except dns.resolver.NXDOMAIN:
        # log_exception("Domain "+domain+" not found\n")
        print(f"Domain {domain} not found")
        return return_values[2]
    except Exception as ex:
        # log_exception("Some Exception occured")
        print(f"Some Exception occured for {domain} : {ex}")
        return return_values[2]
