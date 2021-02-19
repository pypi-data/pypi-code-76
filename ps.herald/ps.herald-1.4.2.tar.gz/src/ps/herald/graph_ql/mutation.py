import graphene
from ps.herald.database import get_session
from ps.herald.model import Log 
from ps.herald.graph_ql.typedefs import GLog , AddGLogFields

class AddLog(graphene.Mutation):
    log = graphene.Field(lambda: GLog)

    class Arguments:
        input = AddGLogFields(required=True)

    @staticmethod
    def mutate(self, info, input):
        session = get_session()
        log = Log(**input)
        session.add(log)
        session.commit()
        return AddLog(log=log )



class Mutation(graphene.ObjectType):
    addLog= AddLog.Field()
