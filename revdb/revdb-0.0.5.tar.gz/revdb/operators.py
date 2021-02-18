class Compiler:
    def __init__(self, db, query, method):
        self.db = db
        self.query = query
        self.method = method

    def compile(self, query=None):
        if not query:
            query = self.query
        if isinstance(query, AND):
            return self.db.compile_and(query, self)
        if isinstance(query, OR):
            return self.db.compile_or(query, self)
        if isinstance(query, EMPTY):
            return self.db.compile_empty(query, self)

    def execute(self, **kwargs):
        expressions = self.compile()
        return getattr(self.db, self.method)(expressions, **kwargs)


class BaseOperator:
    selector = None

    def __init__(self, *args, **kwargs):
        self.sub_queries = args
        self.kwargs = kwargs

        if not all([isinstance(query, BaseOperator) for query in self.sub_queries]):
            raise TypeError('args should be instanceof BaseOperator')

    def get_compiler(self, db, method):
        return Compiler(db, self, method)


class EMPTY(BaseOperator):
    def __init__(self, *args, **kwargs):
        pass


class Logical(BaseOperator):
    pass


class AND(Logical):
    pass


class OR(Logical):
    pass


class NOR(Logical):
    pass


class NOT(BaseOperator):
    pass
