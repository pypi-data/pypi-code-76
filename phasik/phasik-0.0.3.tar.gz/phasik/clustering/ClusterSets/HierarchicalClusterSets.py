from phasik.clustering.ClusterSet.HierarchicalClusterSet import HierarchicalClusterSet
from phasik.clustering.ClusterSets.ClusterSets import ClusterSets


class HierarchicalClusterSets(ClusterSets):
    """Subclass of ClusterSets, to be used for any range of clusters created by a hierarchical method"""

    def __init__(self, snapshots, cluster_limit_type, cluster_limits):
        """
        Parameters
        ----------
        snapshots : Snapshots
        cluster_limit_type : str
            Method that was used to determine when to stop clustering when creating this cluster
            set. e.g. A cluster set can be created by clustering until a particular number of clusters has been
            reached ('maxclust'), or until every cluster is at least a certain distance away from each other
            ('distance').
        cluster_limits : int 
            Values corresponding to the cluster_limit_type described above; a cluster set will be
            created for every value in this iterable object.
        """

        cluster_sets = [HierarchicalClusterSet(snapshots, cluster_limit_type, limit) for limit in cluster_limits]
        super().__init__(cluster_sets, snapshots, cluster_limit_type)
