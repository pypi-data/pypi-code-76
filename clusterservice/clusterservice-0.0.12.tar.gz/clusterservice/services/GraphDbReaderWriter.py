'''
Input format and output format:
{
    'question-1': {
        'cluster-head1': {
            'similarity_score': 0.4,
            'element_count': 10,
            'cluster_elements': [
                [element1, chunk1, comment1],
                [element2, chunk2, comment2]
            ]
        }
    }
}
'''
import hashlib
import logging
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def uuid(text):
    return str(hashlib.md5(text.encode()).hexdigest())


class GraphDbReaderWriter:

    def __init__(self, db):
        logger.debug('initialising GraphDbReaderWriter')
        self.db = db

    def save_cluster(self, cluster_dic, forum_id, client_id):
        logger.debug('GraphDbReaderWriter.save_cluster')
        to_delete_ids = set()
        to_keep = {
            'Question': set(),
            'ClusterHead': set(),
            'ClusterElement': set(),
            'Chunk': set(),
            'Comment': set(),
        }
        for q_text in cluster_dic:
            do_delete = False
            if self.db.exists('Question', text=q_text, forum_id=forum_id):
                results = self.db.execute_query("""
                    MATCH (q:Question)
                        -[:ANSWERS]-(h:ClusterHead)
                        -[:DECOMPOSES]-(e:ClusterElement)
                        -[:DERIVES_FROM]-(s:Chunk)
                        -[:DECOMPOSES]-(c:Comment)
                    WHERE q.text=$q_text AND q.forum_id=$forum_id
                    RETURN DISTINCT id(q) AS question_id
                        , id(h) AS cluster_head_id
                        , id(e) AS cluster_element_id
                        , id(s) AS chunk_id
                        , id(c) AS comment_id
                    """, q_text=q_text, forum_id=forum_id)

                node_types = ['question', 'cluster_head', 'cluster_element', 'chunk', 'comment']
                for r in results:
                    for node_type in node_types:
                        to_delete_ids.add(r['{}_id'.format(node_type)])

                do_delete = True

            q_node = self.db.add_node('Question',
                uid=uuid(q_text),
                text=q_text,
                client_id=client_id,
                forum_id=forum_id,
            )

            if do_delete and q_node.id in to_delete_ids:
                to_delete_ids.remove(q_node.id)
                to_keep['Question'].add(q_node.id)

            # each item is in the form: head, similarity, element count, element list
            for h_text in cluster_dic[q_text]:
                h_node = self.db.add_node('ClusterHead',
                    uid=uuid(h_text),
                    text=h_text,
                    similarity_score=cluster_dic[q_text][h_text]['similarity_score'],
                    client_id=client_id,
                    forum_id=forum_id,
                )

                if do_delete and h_node.id in to_delete_ids:
                    to_delete_ids.remove(h_node.id)
                    to_keep['ClusterHead'].add(h_node.id)

                h_node.question.connect(q_node)

                for el in cluster_dic[q_text][h_text]['cluster_elements']:
                    e_node = self.db.add_node('ClusterElement',
                        uid=uuid(el[0]),
                        text=el[0],
                        client_id=client_id,
                        forum_id=forum_id,
                    )

                    if do_delete and e_node.id in to_delete_ids:
                        to_delete_ids.remove(e_node.id)
                        to_keep['ClusterElement'].add(e_node.id)

                    e_node.cluster_head.connect(h_node)

                    s_node = self.db.add_node('Chunk',
                        uid=uuid(el[1]),
                        text=el[1],
                        client_id=client_id,
                        forum_id=forum_id,
                    )

                    if do_delete and s_node.id in to_delete_ids:
                        to_delete_ids.remove(s_node.id)
                        to_keep['Chunk'].add(s_node.id)

                    e_node.chunks.connect(s_node)

                    c_node = self.db.add_node('Comment',
                        uid=uuid(el[2]),
                        text=el[2],
                        client_id=client_id,
                        forum_id=forum_id,
                        #create_datetime=datetime.fromisoformat(el[3]),
                        create_datetime=datetime.strptime(el[3], "%Y-%m-%dT%H:%M:%S.%f"),
                    )

                    if do_delete and c_node.id in to_delete_ids:
                        to_delete_ids.remove(c_node.id)
                        to_keep['Comment'].add(c_node.id)

                    s_node.comment.connect(c_node)

        self.db.delete_nodes(list(to_delete_ids))

    def get_from_db(self, question_texts, forum_id):
        logger.debug('GraphDbReaderWriter.get_from_db')
        cluster_dic = {}
        for q_text in question_texts:
            results = self.db.execute_query("""
                MATCH (q:Question)
                    -[:ANSWERS]-(h:ClusterHead)
                    -[:DECOMPOSES]-(e:ClusterElement)
                    -[:DERIVES_FROM]-(s:Chunk)
                    -[:DECOMPOSES]-(c:Comment)
                WHERE q.text=$q_text AND q.forum_id=$forum_id
                RETURN DISTINCT q.client_id AS client_id
                    , q.forum_id AS forum_id
                    , q.uid as question_uid
                    , h.uid as cluster_head_uid
                    , h.text AS cluster_head_text
                    , h.similarity_score AS cluster_head_similarity_score
                    , h.element_count AS cluster_head_element_count
                    , e.uid as cluster_element_uid
                    , e.text AS cluster_element_text
                    , s.uid AS chunk_uid
                    , s.text AS chunk_text
                    , c.uid AS comment_uid
                    , c.text AS comment_text
                """, q_text=q_text, forum_id=forum_id)

            for r in results:
                client_id = r['client_id']
                forum_id = r['forum_id']
                q_uid = r['question_uid']
                if q_uid not in cluster_dic:
                    cluster_dic[q_uid] = {
                        'uuid': q_uid,
                        'text': q_text,
                        'client_id': client_id,
                        'forum_id': forum_id,
                        'cluster_heads': {},
                    }

                cluster_heads = cluster_dic[q_uid]['cluster_heads']
                h_uid = r['cluster_head_uid']
                if h_uid not in cluster_heads:
                    cluster_heads[h_uid] = {
                        'uuid': h_uid,
                        'text': r['cluster_head_text'],
                        'similarity_score': r['cluster_head_similarity_score'],
                        'element_count': r['cluster_head_element_count'],
                        'client_id': client_id,
                        'forum_id': forum_id,
                        'cluster_elements': {},
                    }

                cluster_elements = cluster_heads[h_uid]['cluster_elements']
                e_uid = r['cluster_element_uid']
                if e_uid not in cluster_elements:
                    cluster_elements[e_uid] = {
                        'uuid': e_uid,
                        'text': r['cluster_element_text'],
                        'client_id': client_id,
                        'forum_id': forum_id,
                        'comments': {},
                    }

                comments = cluster_elements[e_uid]['comments']
                c_uid = r['comment_uid']
                if c_uid not in comments:
                    comments[c_uid] = {
                        'uuid': c_uid,
                        'text': r['comment_text'],
                        'client_id': client_id,
                        'forum_id': forum_id,
                        'chunks': {},
                    }

                chunks = comments[c_uid]['chunks']
                s_uid = r['chunk_uid']
                if s_uid not in chunks:
                    chunks[s_uid] = {
                        'uuid': s_uid,
                        'text': r['chunk_text'],
                        'client_id': client_id,
                        'forum_id': forum_id,
                    }

        nested_props = ['cluster_heads', 'cluster_elements', 'comments', 'chunks']
        nested_props.reverse()
        return convert_nested_dict_to_list(cluster_dic, nested_props)


def _convert_nested_dict_to_list(obj, values):
    if len(values) == 0: return obj
    prop = values.pop()
    obj[prop] = [_convert_nested_dict_to_list(o, values.copy()) for o in obj[prop].values()]
    return obj


def convert_nested_dict_to_list(obj, values):
    return [_convert_nested_dict_to_list(o, values) for o in obj.values()]
