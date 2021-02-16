import json

from django.contrib.auth.models import AnonymousUser
from graphene import Schema
from graphql import GraphQLError
from graphene import Mutation
from .models import MutationCommit
import re
import functools


def commit(mutation_name):
    def decorator(func):

        def wrapper(*args, **kwargs):
            result = None
            if isinstance(decorator.data.user, AnonymousUser):
                user = None
            else:
                user = decorator.data.user
            try:
                result = func(*args, **kwargs)
                MutationCommit.objects.create(user=user,
                                              arguments=decorator.data.query_args,
                                              mutation_name=mutation_name)
            except Exception as err:

                MutationCommit.objects.create(user=user,
                                              arguments=decorator.data.query_args,
                                              mutation_name=mutation_name, error=str(err))
                raise GraphQLError(str(err))
            return result

        return wrapper

    return decorator


def login_required(func):
    def wrapper(*args, **kwargs):
        if login_required.data.user.is_authenticated:
            result = func(*args, **kwargs)
        else:
            raise GraphQLError("you are not authorized")
        return result

    return wrapper


class Register(object):

    def __init__(self, *decorators):
        self.decorators = decorators

    def __call__(self, func):
        for deco in self.decorators[::-1]:
            func = deco(func)
        func.data = {}
        func.decorators = self.decorators
        return func


def register(*decorators):
    def register_wrapper(func):
        for deco in decorators[::-1]:
            func = deco(func)
        func.data = {}
        func.decorators = decorators
        return func

    return register_wrapper


class DataSchema:

    def __init__(self):
        pass

    def add_data(self, data):
        self.__dict__.update(data)


class InterLayer:

    def __init__(self, schema: Schema):
        self.schema = schema
        self.query_resolvers_and_functions = {}
        self.get_mutations_attributes()

    def get_mutations_attributes(self):
        queries = {key: value for key, value in self.schema._query.__dict__.items() if key.startswith('resolve_')}
        mutations = {key: value.__dict__['resolver'] for key, value in self.schema._mutation.__dict__.items() if
                     not key.startswith("_")}
        self.query_resolvers_and_functions = dict(
            zip(self.convert_queries_names(list(queries.keys()) + list(mutations.keys())),
                list(queries.values()) + list(mutations.values())))

    def execute(self, query: str, variables: dict, data: dict):
        # deletes all \n \t \s from query string
        one_line_query = re.sub("\s+", '', query)

        # find all queries names from query string
        try:
            query_names = re.findall("\{([a-zA-Z]+)\(", one_line_query)
        except IndexError:
            raise Exception('you have not provided correct graphql query')
        query = query.replace('()', '')
        # create data "container" for pushing his into decorators
        data_schema = DataSchema()
        data_schema.add_data({"query_args": json.dumps(variables)})
        data_schema.add_data(data)

        # pushing data schemas into decorators
        for query_name in query_names:
            self.add_data_schema_to_decorators(data_schema, query_name)

        # quering decorated schema
        result = self.schema.execute(query, variables=variables)
        return result

    def add_data_schema_to_decorators(self, data_schema: DataSchema, query_name):
        try:
            for func in self.query_resolvers_and_functions[query_name].decorators:
                func.data = data_schema
        except KeyError:
            raise Exception('you provided query or mutation name that not exists. Name %s' % query_name)

    @classmethod
    def convert_queries_names(self, queries_names: list):
        result = []
        for query_name in queries_names:
            query_name = query_name.replace('resolve_', '', 1)
            letters_after_ = re.findall("_([a-zA-Z])", query_name)
            for letter in letters_after_:
                query_name = query_name.replace("_" + letter, letter.upper())
            result.append(query_name)
        return result
