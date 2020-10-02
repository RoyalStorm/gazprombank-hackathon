from hdbscan import HDBSCAN


def cluster(vertexes, min_cluster_size=150, min_samples=1):
    return HDBSCAN(
        metric='manhattan',
        min_cluster_size=min_cluster_size,
        min_samples=min_samples).fit(vertexes)
