from typing import List
from sklearn import cluster, metrics
from .query_cluster import EvaluationScore, QueryClusterModel, EstimatorElem
from .query_cluster import Sentence2Vector, QueryClusterCoach


class QueryClusterCoachKMeans(QueryClusterCoach):
    def __init__(self, sent2vec: Sentence2Vector, model: QueryClusterModel, model_file: str = "",
                 max_exp_count: int = 8):
        """ query cluster """
        super().__init__(sent2vec, model, model_file, max_exp_count)

    def create_estimators(self, max_exp_count: int = 8):
        """
        创建多实验的聚类算子
        :param max_exp_count:
        :return:
        """
        self.estimators = {
            i: EstimatorElem(estimator=cluster.KMeans(n_clusters=i + 2), class_num=i + 2) for i in range(max_exp_count)
        }

    def search_best_model(self, scores: List[EvaluationScore]):
        """
        选择最优模型
        :return:
        """
        best_value = -10000
        best_score = EvaluationScore()
        for score in scores:
            if score.silhouette > best_value:
                best_score = score.copy()
                best_value = score.silhouette

        self.model.set_model_score(best_score.copy())

    def evaluate_cluster(self, matrix, estimator_elem: EstimatorElem):
        """
        根据当前的estimator计算评估值
        :param matrix:
        :param estimator_elem:
        :return:
        """
        return EvaluationScore(
            class_num=estimator_elem.class_num,
            labels=estimator_elem.estimator.labels_,
            sse=estimator_elem.estimator.inertia_,
            silhouette=metrics.silhouette_score(
                X=matrix, labels=estimator_elem.estimator.labels_
            ),
            calinski_harabasz=metrics.calinski_harabasz_score(
                X=matrix, labels=estimator_elem.estimator.labels_
            )
        )


def main():
    with open("queries", "r") as fp:
        queries = [line.strip("\r\n") for line in fp.readlines()]

    QueryClusterCoachKMeans(
        sent2vec=Sentence2Vector(),
        model=QueryClusterModel(),
        model_file="", max_exp_count=8
    ).train(queries=queries, saved_model="kmeans_best_model.pkl")


if __name__ == '__main__':
    main()
