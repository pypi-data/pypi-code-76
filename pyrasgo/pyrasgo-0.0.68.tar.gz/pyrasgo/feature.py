from typing import List
from collections import Sequence

from pyrasgo.connection import Connection
from pyrasgo.enums import Granularity
from pyrasgo.monitoring import track_usage
from pyrasgo.namespace import Namespace
from pyrasgo.schemas import feature as api


class FeatureList(Sequence):
    """
        Convenience class to enable simpler console presentation,
        iteration and searching through lists of Features objects
    """

    def __init__(self, api_object):
        # TODO: Would this be more useful as a set not a sequence?
        self.data = sorted([Feature(api_object=entry) for entry in api_object], key=lambda x: x.id)

    def __getitem__(self, i: int):
        return self.data[i]

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self):
        ids = [str(feature.id) for feature in self]
        return (f"Features({len(self.data)} total, "
                f"ids: [{','.join(ids if len(self) < 7 else ids[0:3] + ['...'] + ids[-3:])}])")

    def __add__(self, other):
        # TODO: Should this be a set operations??
        if isinstance(other, Feature):
            return type(self)([feature.dict() for feature in self.data + [other]])
        if isinstance(other, type(self)):
            return type(self)([feature.dict() for feature in self.data + other.data])
        if isinstance(other, list) and all(
                [isinstance(entry, Namespace) or isinstance(entry, Feature) for entry in other]):
            return type(self)([feature.dict() for feature in self.data + other])
        raise TypeError(f"unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'")

    def __repr__(self):
        return str(self)

    def filter(self, **kwargs):
        return [feature for feature in self.data
                if [feature.__getattr__(key) for key in kwargs.keys()] == list(kwargs.values())]


class Feature(Connection):
    """
    Stores the properties for a feature
    """

    def __init__(self, api_object, **kwargs):
        # TODO: Determine pathway to create feature via command line? Do we want to allow this?
        super().__init__(**kwargs)
        self._feature = api.Feature(**api_object)

    def __getattr__(self, item):
        try:
            return self._feature.__getattribute__(item)
        except KeyError:
            raise AttributeError(f"No attribute named {item}")

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Feature(id={self.id}, name={self.name}, description={self.description}, orchestrationStatus={self.orchestrationStatus}, organizationId={self.organizationId})"

    @track_usage
    def get(self):
        """
        Updates the Feature object's attributes from the API
        """
        self._feature = api.Feature(**self._get(f"/features/{self.id}", api_version=1).json())

    @track_usage
    def add_tag(self, tag: str):
        if tag in self._feature.tags:
            return
        self._feature = api.Feature(**self._put(f"/features/{self.id}/tags",
                                                api_version=1, _json={"tags": [tag, *self._feature.tags]}).json())

    @track_usage
    def add_tags(self, tags: List[str]):
        if all(tag in self._feature.tags for tag in tags):
            return
        self._feature = api.Feature(**self._put(f"/features/{self.id}/tags",
                                                api_version=1, _json={"tags": [*tags, *self._feature.tags]}).json())

    @track_usage
    def delete_tag(self, tag: str):
        if tag not in self._feature.tags:
            return
        self._feature = api.Feature(**self._delete(f"/features/{self.id}/tags",
                                                   api_version=1, _json={"tags": [tag]}).json())

    @track_usage
    def delete_tags(self, tags: List[str]):
        if all(tag not in self._feature.tags for tag in tags):
            return
        self._feature = api.Feature(**self._delete(f"/features/{self.id}/tags",
                                                   api_version=1, _json={"tags": [*tags]}).json())

    @track_usage
    def get_stats(self):
        try:
            stats_json = self._get(f"/features/{self.id}/stats", api_version=1).json()
        except:
            return 'Cannot find stats for this feature'
        stats_obj = api.FeatureStats(**stats_json['featureStats']) or None
        return stats_obj

    @track_usage
    def build_stats(self):
        return self._post(f"/features/{self.id}/stats", api_version=1).json()

    @property
    @track_usage
    def datasource(self):
        """
        Retrieves datasource name for the feature
        """
        # TODO: This is tightly coupled to the API's response object
        data_source = self._feature.dataSource
        if data_source:
            return data_source.name
        return None

    @property
    @track_usage
    def granularities(self):
        """
        Retrieves granularities for the feature
        """
        # TODO: This is tightly coupled to the API's response object
        granularities = self._feature.granularities
        if granularities:
            return [Granularity(granularity.name) for granularity in granularities]
        return []

    @property
    @track_usage
    def featureSet(self):
        """
        Retrieves the feature set for the feature
        """
        # TODO: This is tightly coupled to the API's response object
        feature_set = self._feature.featureSet
        if feature_set:
            return feature_set.name
        return None

    @property
    @track_usage
    def tags(self) -> List[str]:
        return self._feature.tags
