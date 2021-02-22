import logging

from neo4j import GraphDatabase
from neomodel import config, db

from clusterservice.models.BaseGraphDatabase import BaseGraphDatabase
from clusterservice.models.neo4j_node_classes import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

NODE_TYPES = [
    'Question',
    'ClusterHead',
    'ClusterElement',
    'Chunk',
    'Comment',
    'Sentiment',
    'Emoji',
]


class Neo4jDatabase(BaseGraphDatabase):

    def __init__(self, host, username, password):
        logger.debug('initialising Neo4jDatabase')
        config.DATABASE_URL = 'bolt://{}:{}@{}:7687'.format(username, password, host)
        config.ENCRYPTED_CONNECTION = False
        self.node_classes = {item: db._NODE_CLASS_REGISTRY[frozenset({item})]
                             for item in NODE_TYPES}
        db_url = 'neo4j://{}:7687'.format(host)
        self.driver = GraphDatabase.driver(db_url, auth=(username, password))

    def exists(self, node_type, **kwargs):
        logger.debug('Neo4jDatabase.exists')
        q = 'MATCH (n:{}) WHERE '
        q += ' AND '.join(['n.{key} = ${key}'.format(key=key) for key in kwargs.keys()])
        q += ' RETURN COUNT(n) > 0 AS exists'
        return db.cypher_query(q.format(node_type), kwargs)[0][0][0]

    def _execute_query(self, tx, query, **kwargs):
        logger.debug('Neo4jDatabase._execute_query')
        result = tx.run(query, **kwargs)
        return list(result)

    def execute_query(self, query, **kwargs):
        logger.debug('Neo4jDatabase.execute_query')
        with self.driver.session() as sess:
            results = sess.read_transaction(
                self._execute_query,
                query,
                **kwargs,
            )

        return results

    def find_node(self, node_type, **kwargs):
        logger.debug('Neo4jDatabase.find_node')
        return self.node_classes[node_type].nodes.first_or_none(**kwargs)

    def add_node(self, node_type, **kwargs):
        logger.debug('Neo4jDatabase.add_node')
        return self.node_classes[node_type].get_or_create(kwargs)[0]

    def create_or_update_node(self, node_type, **kwargs):
        logger.debug('Neo4jDatabase.update_node')
        return self.node_classes[node_type].create_or_update(kwargs)[0]

    def delete_nodes(self, id_list):
        logger.debug('Neo4jDatabase.delete_nodes')
        q = 'MATCH (n) WHERE id(n) IN $id_list DETACH DELETE n'
        with self.driver.session() as sess:
            results = sess.write_transaction(
                self._execute_query,
                q,
                id_list=id_list,
            )

        return results

    def delete_all_nodes(self):
        logger.debug('Neo4jDatabase.delete_all_nodes')
        q = 'MATCH (n) DETACH DELETE n'
        with self.driver.session() as sess:
            results = sess.write_transaction(
                self._execute_query,
                q,
            )

        return results
