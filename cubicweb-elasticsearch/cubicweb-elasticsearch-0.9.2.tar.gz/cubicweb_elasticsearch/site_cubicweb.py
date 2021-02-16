options = (
    (
        "elasticsearch-locations",
        {
            "type": "string",
            "default": "",
            "help": "Elastic Search location (eg. 192.168.0.23:9200), "
            "this can be a list of locations (192.168.0.23:9200,192.168.0.24:9200, "
            "you can also include the scheme (eg. http://192.168.0.23:9200) "
            "warning: if this is not defined indexing will be disabled (no localhost default)",
            "group": "elasticsearch",
            "level": 5,
        },
    ),
    (
        "index-name",
        {
            "type": "string",
            "default": "",
            "help": "Elastic Search index name (eg. cubicweb)"
            "warning: if this is not defined indexing will be disabled (no index name default)",
            "group": "elasticsearch",
            "level": 5,
        },
    ),
    (
        "elasticsearch-verify-certs",
        {
            "type": "yn",
            "default": True,
            "help": "Elastic Search connection verify_certs variable"
            "(set to false when using https with unknown or self-signed certificates)",
            "group": "elasticsearch",
            "level": 5,
        },
    ),
    (
        "elasticsearch-ssl-show-warn",
        {
            "type": "yn",
            "default": True,
            "help": "Elastic Search connection ssl-show-warn variable"
            "(set to no if you want to suppress ssl warnings when verify cert is no",
            "group": "elasticsearch",
            "level": 5,
        },
    ),
)
