import ast

from cdd.tests.mocks.sqlalchemy import config_decl_base_str

r = '''
def create_helper(req, res):
    """
    Create / handle-errors with Bottle and SQLalchemy

    :param req: Bottle request
    :type req: ```bottle.request```

    :param res: Bottle response
    :type res: ```bottle.response```

    :returns: A function which actuall does the work
    :rtype: ```Callable[[Base], dict]```
    """
    def _create_helper(orm_class):
        """
        Create / handle-errors with Bottle and SQLalchemy

        :param orm_class: An ORM class inheriting SQLalchemy declarative base class
        :type orm_class: ```Base```

        :returns: Created (as a dict) or error dict
        :rtype: ```dict```
        """
        try:
            orm_instance = orm_class(**req.json)
        except TypeError as e:
            res.status = 400
            return {"error": "ValidationError", "error_description": "\\n".join(e.args)}

        try:
            with Session(engine) as session:
                session.add(orm_instance)
                session.commit()
                created = orm_to_dict(orm_instance)
        except DatabaseError as e:
            res.status = 400
            return {"error": e.__class__.__name__, "error_code": e.code, "error_description": str(e.__cause__)}

        return created

    return _create_helper
'''

print(ast.dump(ast.parse(r).body[0], indent=4))

print(config_decl_base_str)
