from .msg import Msg
from .protobuf import nonbibrecord_pb2

class NonBibRecord(Msg):

    def __init__(self, *args, **kwargs):
        instance = nonbibrecord_pb2.NonBibRecord()
        data_links_rows = kwargs.pop('data_links_rows', None)  # remove for special handling
        super(NonBibRecord, self).__init__(instance, args, kwargs)
        if data_links_rows:
            # populate rows from database field
            for current in data_links_rows:
                row = instance.data_links_rows.add()
                row.link_type = current['link_type']
                row.link_sub_type = current['link_sub_type']
                row.item_count = current['item_count']
                row.url.extend(current['url'])
                row.title.extend(current['title'])
                

class NonBibRecordList(Msg):

    def __init__(self, *args, **kwargs):
        super(NonBibRecordList, self).__init__(nonbibrecord_pb2.NonBibRecordList(), args, kwargs)


class DataLinksRecord(Msg):

    def __init__(self, *args, **kwargs):
        instance = nonbibrecord_pb2.DataLinksRecord()
        data_links_rows = kwargs.pop('data_links_rows', None)  # remove for special handling
        super(DataLinksRecord, self).__init__(instance, args, kwargs)
        if data_links_rows:
            # populate rows from database field
            for current in data_links_rows:
                row = instance.data_links_rows.add()
                row.link_type = current['link_type']
                row.link_sub_type = current['link_sub_type']
                row.item_count = current['item_count']
                row.url.extend(current['url'])
                row.title.extend(current['title'])


class DataLinksRecordList(Msg):
    def __init__(self, *args, **kwargs):
        super(DataLinksRecordList, self).__init__(nonbibrecord_pb2.DataLinksRecordList(), args, kwargs)
