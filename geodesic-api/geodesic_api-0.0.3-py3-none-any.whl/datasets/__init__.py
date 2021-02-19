from geodesic.client import get_client
from geodesic.datasets.dataset import Dataset, DatasetList


def list_datasets(ids=[]):
    client = get_client()

    url = "/entanglement/api/v1/datasets"
    if ids:
        if isinstance(ids, str):
            ids = str.split(",")
        url = url + "?ids=" + ",".join(ids)

    resp = client.get(url)

    ds = [Dataset(**r) for r in resp["datasets"]]
    datasets = DatasetList(ds)
    return datasets
