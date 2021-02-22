import hashlib
# import logging
import traceback

import nmslib
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from datetime import datetime

# logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
#                     datefmt='%m/%d/%Y %H:%M:%S',
#                     level=logging.DEBUG)
# logger = logging.getLogger(__name__)


class ClusterBuilder:

    def __init__(self, albert, embedder, batch_size, all_comments, all_data, all_chunks, users):
        self.albert = albert
        self.embedder = embedder
        self.batch_size = batch_size
        self.all_comments = all_comments
        self.all_data = all_data
        self.all_chunks = all_chunks
        self.users = users

    def _get_best_head_avg_count(self, cluster_items):
        # logger.debug('_get_best_head_avg_count called')
        n = len(cluster_items)
        # logger.debug('len(cluster_items): {}, len(cluster_items[0]): {}'.format(len(cluster_items),len(cluster_items[0])))
        embeddings = [cluster_items[i][2] for i in range(n)]
        # logger.debug('len(embeddings): {}, firstval:{}'.format(len(embeddings),embeddings[0]))
        # create indexes
        index = nmslib.init(method='hnsw', space='cosinesimil')
        index.addDataPointBatch(embeddings)
        index.createIndex(print_progress=True)

        max_avg_similarity = 0
        max_avg_similarity_i = 0

        #identify cluster centroid
        neighbours = index.knnQueryBatch(embeddings, k=n)#, num_threads=os.cpu_count)
        i = 0
        for _, distances in neighbours:
            avg_similarity = (n - sum(distances)) / n
            if avg_similarity > max_avg_similarity:
                max_avg_similarity = avg_similarity
                max_avg_similarity_i = i
            i += 1
        
        # Added embedding as tuple in head to avoid having to regenerate it in `create_clusters_from_queries`
        return cluster_items[max_avg_similarity_i][0], max_avg_similarity, n, embeddings[max_avg_similarity_i]

    def _is_duplicate_cluster(self, cluster, chunk):
        # logger.debug('_is_duplicate_cluster called')
        for item in cluster:
            if item == chunk:
                return True

            for chunk in cluster[item]:
                if chunk == chunk_id[0]:
                    return True

        return False

    def _get_answers_from_queries(self, query_list):
        # logger.debug('_get_answers_from_queries called')
        query_dic = {}
        for query in query_list:
            query_dic[query] = []
        
        reverse_chunk_dic = {}  # index: chunk-id
        all_chunk_list = []
        i = 0
        for item in self.all_chunks:
            reverse_chunk_dic[i] = item
            all_chunk_list.append(self.all_chunks[item][0])
            i += 1

        i = 0
        offset = 0
        while i < len(all_chunk_list):
            chunks = all_chunk_list[i:min(i + self.batch_size, len(all_chunk_list))]
            try:
                predictions = self.albert.predict(query_list, chunks)
                for pred in list(predictions):
                    if predictions[pred] != '':
                        # the id of the prediction is of the form 'chunkid-qid'
                        id_split = pred.split('-')
                        chunk_i, q_i = int(id_split[0]), int(id_split[1])
                        query_dic[query_list[q_i]].append(
                            (
                                predictions[pred],
                                self.embedder.get_embeddings([predictions[pred]]),
                                reverse_chunk_dic[offset + chunk_i]
                            )
                        )

                offset += self.batch_size
                i = min(i + self.batch_size, len(all_chunk_list))

            except Exception as e:
                # logger.error(str(e))
                traceback.print_exc()

        # { question: [(answer, embedding, chunk-id)] }
        return query_dic

    def _get_mini_clusters(self, embeddings, chunks, orig_ids, min_similarity):
        """
        Parameters:
            embeddings: list of embeddings for answer
            chunks: list of answers for the current question
            orig_ids: list of the chunk ids for each answer
            min_similarity: 
            
        Returns:
            good_clusters: { head_answer_chunk: [(answer, chunk_id, embedding)] }
        """
        # logger.debug('_get_mini_clusters called')
        # TODO format of all items passed
        index = nmslib.init(method='hnsw', space='cosinesimil')
        index.addDataPointBatch(embeddings)
        index.createIndex(print_progress=True)
        n = len(embeddings)
        good_clusters = {}
        orig_ids_str = ''.join([str(x) for x in orig_ids])
        hash_object = hashlib.md5(orig_ids_str.encode())
        orig_ids_str = str(hash_object.hexdigest())

        neighbours = index.knnQueryBatch(embeddings, k=n)#, num_threads=os.cpu_count)
        #i = 0
        processed_ids = set()
        for ids, distances in neighbours:
            # TODO BIG ASSUMPTION to verify... first id is the item itself
            if ids[0] in processed_ids:
                continue

            count = 0
            mini_cluster_ids = []

            for _id, dist in zip(ids, distances):
                # TODO check for optimisation
                if (1 - dist) >= min_similarity:
                    count += 1
                    mini_cluster_ids.append([chunks[_id], orig_ids[_id], embeddings[_id]])
                    # TODO remove the ones already in a cluster
                    processed_ids.add(_id)
            
            # TODO QUETION Why if a chunk have no similarity with any other why just ignore it? Isn't it better be put on separate cluster that not showing it??
            if count >= 2:
                # TODO if removed then no need to check if it exists
                #if not self._is_duplicate_cluster(good_clusters, chunks[i]):
                head, avg, count, head_embedding = self._get_best_head_avg_count(mini_cluster_ids)
                good_clusters[head] = (mini_cluster_ids, head_embedding)
            
            #i += 1

        return good_clusters

    def _get_best_clusters(self, labels, embeddings, answers, ids, min_similarity_start):
        """
        Parameters:
            labels: labels for each answer
            embeddings: list of embeddings for answer
            answers: list of answers for the current question
            ids: list of chunk ids for each answer

        Returns:
            all_mini_clusters: { head_answer_chunk: [(answer, chunk_id, embedding)] }   
        
        clusters format:

            {
                0 : [ids],
                1 : [ids],
                .
                .
                n : [ids],
            }
        """
        # logger.debug('_get_best_clusters called... POSSIBLE ISSUE SOURCE')
        i = 0
        clusters = {}
        for item in labels:
            if item not in clusters:
                clusters[item] = []

            clusters[item].append(i)
            i += 1

        all_mini_clusters = {}
        for item in clusters:
            cluster_embeddings = [embeddings[it] for it in clusters[item]]
            cluster_chunks = [answers[it] for it in clusters[item]]
            cluster_ids = [ids[it] for it in clusters[item]]
            # logger.debug('cluster_embeddings: {} cluster_chunks: {} cluster_ids: {}'.format(len(cluster_embeddings), len(cluster_chunks), len(cluster_ids)))

            if len(cluster_embeddings) > 1:
                mini_clusters = self._get_mini_clusters(
                    cluster_embeddings,
                    cluster_chunks,
                    cluster_ids,
                    min_similarity_start
                )

                all_mini_clusters.update(mini_clusters)

        return all_mini_clusters

    def _merge_clusters(self, full_cluster, max_clusters):
        """Making a cluster of the keys to limit number of clusters."""
        # logger.debug('_merge_clusters called')
        keys = list(full_cluster.keys())
        embeddings = self.embedder.get_embeddings(keys)
        X = np.array(embeddings)
        clustering = AgglomerativeClustering(n_clusters=max_clusters).fit(X)
        labels = clustering.labels_
        clusters = {}
        i = 0
        for item in labels:
            if item not in clusters:
                clusters[item] = []

            clusters[item].extend(full_cluster[keys[i]])
            i += 1

        return clusters

    def _get_formatted_cluster(self, full_cluster):
        # logger.debug('_get_formatted_cluster called')
        formatted_cluster = {}

        for question in full_cluster:
            cluster_head_dic = {}
            for cluster_head in full_cluster[question]:
                head, avg, _, _ = self._get_best_head_avg_count(full_cluster[question][cluster_head])
                # logger.debug('head: {} avg: {} count: {}'.format(head, avg, count))
                cluster_elements = []
                for item in full_cluster[question][cluster_head]:
                    try:
                        chunk_cid = self.all_chunks[item[1]]
                        chunk = chunk_cid[0]
                        comment = self.all_comments[chunk_cid[1]][0]  # comment text
                        comment_date = self.all_comments[chunk_cid[1]][2] \
                                       if len(self.all_comments[chunk_cid[1]]) >= 3 \
                                       else datetime.now().isoformat() # comment created date
                        cluster_elements.append([item[0], chunk, comment, comment_date])
                    except Exception as e: 
                        # logger.error(str(e))
                        continue

                cluster_head_dic[head] = {'cluster_elements': cluster_elements, 'similarity_score': avg}

            formatted_cluster[question] = cluster_head_dic

        return formatted_cluster

    def create_clusters_from_queries(self, query_list, min_clusters, max_clusters, min_similarity_start):
        # logger.debug('create_clusters_from_queries called')
        full_cluster_all = {}
        query_dic = self._get_answers_from_queries(query_list)

        for q in query_dic:
            answer_count = len(query_dic[q])
            if answer_count > 0:
                answers = [item[0] for item in query_dic[q]]
                embeddings = [item[1][0] for item in query_dic[q]]
                ids = [item[2] for item in query_dic[q]]
                # logger.debug('answers: {} embeddings: {} ids: {}'.format(len(answers), len(embeddings), len(ids)))

                if answer_count > 20:
                    X = np.array(embeddings)
                    clustering = AgglomerativeClustering(n_clusters=max_clusters).fit(X)
                    labels = clustering.labels_
                else:
                    labels = [0 for i in range(answer_count)]

                while True:
                    all_mini_clusters = self._get_best_clusters(
                        labels,
                        embeddings,
                        answers,
                        ids,
                        min_similarity_start
                    )
                    full_cluster_all[q] = {}

                    # logger.debug('len(all_mini_clusters):'+ str(len(all_mini_clusters)))
                    if len(all_mini_clusters) > 0:
                        # clustering the keys of all mini clusters
                        all_mini_clusters_keys = list(all_mini_clusters.keys())
                        all_mini_cluster_embeddings = [all_mini_clusters[item][1] for item in all_mini_clusters]
                        all_mini_clusters_ids = [all_mini_clusters[item][0][0][1] for item in all_mini_clusters]
                        clusters_from_keys = self._get_mini_clusters(
                            all_mini_cluster_embeddings,
                            all_mini_clusters_keys,
                            all_mini_clusters_ids,
                            min_similarity_start
                        )
                        full_cluster = {}
                        for item in clusters_from_keys:
                            full_cluster[item] = []
                            for item2 in clusters_from_keys[item][0]:
                                full_cluster[item].extend(all_mini_clusters[item2[0]][0])

                        full_cluster_all[q] = full_cluster

                    if len(full_cluster_all[q]) > min_clusters or min_similarity_start <= 0.3:
                        break
                    else:
                        min_similarity_start -= 0.1
                
                if len(full_cluster_all[q]) > max_clusters:
                    full_cluster_all[q] = self._merge_clusters(full_cluster_all[q], max_clusters)
        # logger.debug('returning from create_clusters_from_queries')
        return self._get_formatted_cluster(full_cluster_all)
