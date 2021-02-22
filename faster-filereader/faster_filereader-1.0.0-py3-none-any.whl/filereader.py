#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Jul 24 10:08:25 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: file_reader.py -*-
# -*- purpose: -*-

'''
Faster File reader

The FileReader object can be used as an iterator (i.e. using `for event in FileReader`). It also supports `with` context manager.
'''

import struct
from io import BytesIO

# faster modules
import faster.event
import faster.const


_the_header_unpacker = struct.Struct(faster.const.header_fmt)


class FileReader:
    """Stream FASTER events from file"""
    def __init__(self,
                 fasterfile="",
                 maxnevents=faster.const.max_number_of_events_in_file,
                 readoninit=False):
        """Creator

        Keyword arguments:
        evtfile -- path to file to stream - if absent, or incorrect, you'll get an error.
        maxnevents -- number of events to read at most (default = faster.const.max_number_of_events_in_file)
        readoninit -- Experimental feature that reads the whole file into memory first. Basic tests show no evidence that it is speeding up the processing of a file...
        """
        self.fpath = fasterfile
        self.maxnevents = maxnevents
        self.nevents = 0
        if not readoninit:
            self.infile = open(self.fpath, 'rb')
        else:
            print("# Reading all file on init")
            self.infile = BytesIO(open(self.fpath, 'rb').read())

    def __enter__(self):
        '''Enters the context manager'''
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''Exiting the context manager, file is closed! no more reading after this.'''
        self.infile.close()

    def __del__(self):
        '''Destructor'''
        del self.fpath
        del self.infile
        del self.maxnevents
        del self.nevents

    def __repr__(self) -> str:
        'String representation of the file reader'
        return f"<FasterFileReader '{self.fpath}'>"

    def __iter__(self):
        '''With this method, the object can be iterated over'''
        return self

    @staticmethod
    def read_header(data) -> dict:
        '''
        Unpacks a header from data

        Static method, so that it can be used for unpacking grouped events
        '''
        type_alias, _, *clock, label, load_size = _the_header_unpacker.unpack(data)
        return {
            'type_alias': type_alias,
            'clock': clock,
            'label': label,
            'load_size': load_size,
            }

    @staticmethod
    def read_data(src, head):
        ''' Reads head[load_size] from the source

        Static method, so that it can be used for unpacking grouped events'''
        return src.read(head['load_size'])

    def __next__(self):
        """
        Iteration method: returns the next event in the file.

        Raise StopIteration if at the end of the file, or maxnevents is reached.
        """
        if self.nevents >= self.maxnevents:
            raise StopIteration
        head_data = self.infile.read(faster.const.header_size)
        if not head_data:
            raise StopIteration
        self.nevents += 1
        header = self.read_header(head_data)
        evt_data = self.read_data(self.infile, header)
        return faster.event.Event(header, data=evt_data)
