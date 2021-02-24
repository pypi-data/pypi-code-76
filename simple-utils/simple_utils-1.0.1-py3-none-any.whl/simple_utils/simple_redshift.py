class Column():
    def __init__(self, name, column_type, attr="", comment=""):
        self.name = name
        self.column_type = column_type
        self.attr = attr
        self.comment = comment


def df_type_to_redshift_type(df, columns):
    wdf = df.copy()
    case_insensitive_check = lambda x, word: word.lower() in [s.lower() for s in x]
    for column in columns:
        if case_insensitive_check(["BIGINT", "INT", "SMALLINT"], column.column_type):
            wdf[column.name] = wdf[column.name].astype(int)
        elif case_insensitive_check(["FLOAT"], column.column_type):
            wdf[column.name] = wdf[column.name].astype(float)
        elif column.column_type.upper().startswith("VARCHAR"):
            wdf[column.name] = wdf[column.name].astype(str)
        elif case_insensitive_check(["BOOLEAN"], column.column_type):
            wdf[column.name] = wdf[column.name].astype(bool)            
        elif column.column_type in ["DATE", "TIMESTAMP"]:
            pass
        else:
            raise ValueError(f"Unknown type {column.column_type}")

    return wdf
