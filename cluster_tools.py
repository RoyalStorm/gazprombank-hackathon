from hdbscan import HDBSCAN


def cluster(X, y):
    return HDBSCAN(
        min_cluster_size=None,
        min_samples=None).fit_predict()
