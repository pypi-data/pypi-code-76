CHARLIST = [
    "varchar",
    "text",
]

INTLIST = [
    "int",
]

TYPEUSEDLONG = [
    "varchar",
]

TYPEUNUSEDLONG = [
    "int",
    "text",
]

typeTo = {
    int: "INT",
    str: "VARCHAR",
    list: "VARCHAR",
    tuple: "VARCHAR",
    dict: "VARCHAR",
    bool: "VARCHAR",
    float: "DOUBLE",
}
