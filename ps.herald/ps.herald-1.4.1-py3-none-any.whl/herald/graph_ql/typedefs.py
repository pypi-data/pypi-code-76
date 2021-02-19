import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from ps.herald.model import Log, HeartBeat


class GLog(SQLAlchemyObjectType):
    class Meta:
        model = Log


class GLogFields:
    id = graphene.Int()
    created = graphene.String()
    threadname = graphene.String()
    api_version = graphene.String()
    package_version = graphene.String()
    name = graphene.String()
    relativecreated = graphene.String()
    process = graphene.String()
    args = graphene.String()
    module = graphene.String()
    funcname = graphene.String()
    levelno = graphene.String()
    processname = graphene.String()
    thread = graphene.String()
    msecs = graphene.String()
    message = graphene.String()
    exc_text = graphene.String()
    exc_info = graphene.String()
    stack_info = graphene.String()
    pathname = graphene.String()
    filename = graphene.String()
    asctime = graphene.String()
    levelname = graphene.String()
    lineno = graphene.String()
    # These are "extra fields" not in the standard python logging
    produkt_id = graphene.String()
    system_id = graphene.String()
    sub_system_id = graphene.String()
    sub_sub_system_id = graphene.String()
    user_spec_1 = graphene.String()
    user_spec_2 = graphene.String()
    summary = graphene.String()

class AddGLogFields(graphene.InputObjectType, GLogFields):
      pass


class GHeartBeat(SQLAlchemyObjectType):
    class Meta:
        model = HeartBeat


class GHearBeatFields:
    id = graphene.Int()
    newest_hearbeat = graphene.String()
    system_id = graphene.String()
