from typing import List

from reusingintent.inference_core.algorithms.dbscan import computeDBScan
from reusingintent.inference_core.algorithms.kmeans import computeKMeansClusters
from reusingintent.inference_core.algorithms.linear_regression import computeLR
from reusingintent.inference_core.algorithms.range import range_intent
from reusingintent.inference_core.algorithms.skyline_algorithm import computeSkyline
from reusingintent.inference_core.filter import process_predictions
from reusingintent.inference_core.prediction import Prediction
from reusingintent.server.database.get_predictions import get_predictions


def process_regular(record_id, dataset, selections, dimensions, session):
    selections = [1 if i in selections else 0 for i in dataset["id"].values.tolist()]
    predictions: List[Prediction] = get_predictions(
        record_id, dataset, selections, dimensions, session
    )

    predictions.extend(range_intent(dataset, dimensions, selections))

    predictions = process_predictions(predictions)

    return predictions


def process_filtered(dataset, selections, dimensions, filtered_indices):
    subset = dataset[~dataset.id.isin(filtered_indices)].reset_index(drop=True)
    subset_dims = subset[dimensions]
    selections = [1 if i in selections else 0 for i in subset["id"].values.tolist()]

    dims = ",".join(dimensions)
    kmeansCluster = computeKMeansClusters(subset_dims, dims, -1)
    dbscanCluster = computeDBScan(subset_dims, dims, -1, False)
    dbscanOutlier = computeDBScan(subset_dims, dims, -1, True)
    linearReg = computeLR(subset_dims, dims, -1)
    skyline = computeSkyline(subset_dims, dims, -1)

    algs = []
    algs.extend(kmeansCluster)
    algs.extend(dbscanCluster)
    algs.extend(dbscanOutlier)
    algs.extend(linearReg)
    algs.extend(skyline)

    predictions = []
    for a in algs:
        predictions.extend(a.predict(selections, subset))

    predictions.extend(range_intent(subset, dimensions, selections))

    predictions = process_predictions(predictions)

    return predictions
