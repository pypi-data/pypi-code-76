#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# Harpia REST API Interface
#--------------------------------------------------------------------------
# Copyright (c) 2018 Light Conversion (UAB MGF "Šviesos konversija")
# All rights reserved.
# www.lightcon.com
#==========================================================================

import time
from ..common.http_methods import HTTP_methods
    

# =============================================================================
# DEBUG
# =============================================================================
#import json
#import urllib
#import urllib.error
#import urllib.request
#import urllib.parse
#import time
#
#class HTTP_methods:    
#    def _get (self, command):
#        time_init = time.perf_counter()
#        try:
#            data = json.loads(urllib.request.urlopen(self.url+command).read().decode('utf-8'))
#        except urllib.error.HTTPError as e:
#            error_string = e.read().decode('utf-8', 'ignore')
#            print (error_string)
#            return error_string
#        
#        if not self.silent:
#            print (command + " : {:.3f} ms".format((time.perf_counter()-time_init)*1000))
#        return data
#        
#    def _put (self, command, data):
#        time_init = time.perf_counter()
#        try:
#            post_url = urllib.request.Request(url=self.url+command, data=data.encode('utf-8'), method='PUT')
#    
#            post_url.add_header('Content-Type', 'application/json')
#            
#            with urllib.request.urlopen(post_url) as f:
#                pass
#            if not self.silent:
#                print (command + " : {:.3f} ms".format((time.perf_counter()-time_init)*1000))
#            return f.status            
#        except urllib.error.HTTPError as e:
#            error_string = e.read().decode('utf-8', 'ignore')
#            print (error_string)
#            return error_string
#        
#        if not self.silent:
#            print (command + " : {:.3f} ms".format((time.perf_counter()-time_init)*1000))
#        return 200
#    
#        
#    def _post (self, command, details={}):
#        time_init = time.perf_counter()
#        try:
#            post_details = urllib.parse.urlencode(details).encode('UTF-8')
#            
#            post_url = urllib.request.Request(self.url+command, post_details)
#            
#            res = urllib.request.urlopen(post_url).read().decode('utf-8', 'ignore')
#        except urllib.error.HTTPError as e:
#            error_string = e.read().decode('utf-8', 'ignore')
#            print (error_string)
#            return error_string
#        
#        if not self.silent:
#            print (command + " : {:.3f} ms".format((time.perf_counter()-time_init)*1000))
#        return res
# =============================================================================
#     
# =============================================================================
class LaserClient (HTTP_methods):
    """REST API interaction logic with PHAROS or CARBIDE laser"""
    
    silent = True
    connected = False
    
    def get_status(self):
        """Get laser status JSON."""
        endpoint_name = 'get_status'
        if (endpoint_name in self.endpoints):
            return self._get(self.endpoints[endpoint_name])
        else:
            return "Function not supported"
        
    def get_frequency(self):
        """Get output frequency (divided by PP) in kilohertz."""
        endpoint_name = 'get_frequency'
        if (endpoint_name in self.endpoints):
            return self._get(self.endpoints[endpoint_name])
        else:
            return "Function not supported"
    
    def get_pp(self):
        """Get PP divider."""
        endpoint_name = 'get_pp'
        if (endpoint_name in self.endpoints):
            return self._get(self.endpoints[endpoint_name])
        else:
            return "Function not supported"
        
    def set_pp(self, value, blocking=False):
        """Set PP divider."""
        endpoint_name = 'set_pp'
        if (endpoint_name in self.endpoints):
            self._put(self.endpoints[endpoint_name], str(value))
        else:
            return "Function not supported"

        if blocking:
            while self.get_pp() != value:
                time.sleep(0.2)
                
    def enable_output(self):
        """Enable laser output."""
        endpoint_name = 'enable_output'
        if (endpoint_name in self.endpoints):
            self._post(self.endpoints[endpoint_name])
        else:
            return "Function not supported"

    def close_output(self):
        """Disable laser output."""
        endpoint_name = 'close_output'
        if (endpoint_name in self.endpoints):
            self._post(self.endpoints[endpoint_name])
        else:
            return "Function not supported"
    
class Pharos (LaserClient):        
    endpoints = {'get_status':      '/Basic',
                 'get_frequency':   '/Basic/ActualOutputFrequency',
                 'get_pp':          '/Basic/ActualPpDivider',
                 'set_pp':          '/Basic/TargetPpDivider',
                 'enable_output':   '/Basic/EnableOutput',
                 'close_output':    '/Basic/CloseOutput'}
    
    def __init__ (self, ip_address, port=20020, version='v1'):
        self.url = 'http://{}:{}/{}/'.format(ip_address, port, version)        
        self.connected = self._get('Basic') != {}
        if self.connected:
            print ('Pharos initialized at', self.url)
            
class Carbide (LaserClient):
    endpoints = {'get_status':      '/Basic',
                 'get_frequency':   '/Basic/ActualOutputFrequency',
                 'get_pp':          '/Basic/ActualPpDivider',
                 'set_pp':          '/Basic/TargetPpDivider',
                 'enable_output':   '/Basic/EnableOutput',
                 'close_output':    '/Basic/CloseOutput'}
    
    def __init__ (self, ip_address, port=20010, version='v1'):
        self.url = 'http://{}:{}/{}/'.format(ip_address, port, version)        
        self.connected = self._get('Basic') != {}
        if self.connected:
            print ('Carbide initialized at', self.url)