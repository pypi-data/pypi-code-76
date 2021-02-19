import graphene
from ps.herald.model import Log, HeartBeat
from ps.herald.graph_ql.typedefs import GLog, GHeartBeat
from ps.herald.database import get_session
from ps.basic import Config

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))
    goodbye = graphene.String()
    get_logs = graphene.List(GLog,search=graphene.String(),
                                  first=graphene.Int(),
                                  skip=graphene.Int(),)
    get_by_system_id = graphene.List(GLog, system_id=graphene.String())
    get_search_options = graphene.String()

    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'

    @staticmethod
    def resolve_get_logs(parent, info,search=None, first=None, skip=None, **args):
          Config.logger.info("resolve_get_logs entered")

          if search:
               qs = GLog.get_query(info).filter(Log.message.contains(search)).all()
               Config.logger.info(f"resolve_get_logs search entered{search}")
          else:
               qs = GLog.get_query(info).all()

          if skip:
            qs = qs[skip:]

          if first:
            qs = qs[:first] 
          return qs

    @staticmethod
    def resolve_get_by_system_id(parent, info, **args):
          system_id = args.get("system_id")
          system_id_query  = GLog.get_query(info)
          Config.logger.info(f" resolve_get_by_system_id with system_id {system_id}")
          return     system_id_query.filter(Log.system_id.contains(system_id)).all()

    @staticmethod
    def resolve_get_search_options(parent, info, **args):
          Config.logger.info("get_search_options entered")
          session = get_session()
          pids = session.query(Log.produkt_id).distinct().all() + ["not_selected"]
          sids = session.query(Log.system_id).distinct().all() + ["not_selected"]
          sub_sids = session.query(Log.sub_system_id).distinct().all() + ["not_selected"]   
          sub_sub_sids = session.query(Log.sub_sub_system_id).distinct().all() + ["not_selected"]   
          u1s = session.query(Log.user_spec_1).distinct().all() + ["not_selected"]
          u2s = session.query(Log.user_spec_2).distinct().all() + ["not_selected"]

          return {"produkt_ids":pids,
                  "system_ids":sids,
                  "sub_system_ids":sub_sids,
                  "sub_sub_system_ids":sub_sub_sids, 
                  "user_spec_1s":u1s,
                  "user_spec_2s":u2s
                  }

