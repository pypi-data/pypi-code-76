from elasticsearch import Elasticsearch
from pandagg.discovery import discover
url = 'http://lb-elasticsearch7.ovh-roubaix.preproduction.internal.alkemics.com:9200/'
client = Elasticsearch(hosts=[url])
# indices = discover(client, 'busin*')
# bu = indices.business_unit_01

from pandagg.search import Search

s = Search(using=client, index='busin*', nested_autocorrect=True, repr_auto_execute=True).update_from_dict({
    "query": {
        "match": {
            "organization_id": 6193
        }
    },
    "_source": {
        "includes": [
            "id"
        ]
    },
    "from": 0,
    "aggs": {
        "suppliers": {
            "nested": {
                "path": "suppliers"
            },
            "aggs": {
                "suppliers.id": {
                    "terms": {
                        "field": "suppliers.id",
                        "size": 100000
                    },
                    "aggs": {
                        "suppliers.name": {
                            "terms": {
                                "field": "suppliers.name",
                                "size": 1
                            }
                        }
                    }
                }
            }
        }
        ,
        "event.id": {
            "terms": {
                "field": "event.id",
                "size": 100000
            },
            "aggs": {
                "event.name": {
                    "terms": {
                        "field": "event.name",
                        "size": 1
                    }
                }
            }
        }
    },
    "size": 20
})

r = s.execute()

r.aggregations.to_dataframe(grouped_by='suppliers.name')
