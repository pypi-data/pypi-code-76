import graphene
from ps.herald.graph_ql.query import Query
from ps.herald.graph_ql.mutation import Mutation
from ps.herald.graph_ql.typedefs import GLog, GHeartBeat
from ps.herald.database import get_session


schema = graphene.Schema(
    query=Query, mutation=Mutation, types=[GLog, GHeartBeat]
)
#schema.execute(context_value={'session': get_session()})
