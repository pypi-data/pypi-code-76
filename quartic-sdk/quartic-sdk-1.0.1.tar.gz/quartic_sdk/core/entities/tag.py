
"""
The given file contains the class to refer to the tag entity
"""
from quartic_sdk.core.entities.base import Base
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.core.iterators.tag_data_iterator import TagDataIterator


class Tag(Base):
    """
    The given class refers to the tag entity which is created based upon the
    tag object returned from the API
    """

    def __repr__(self):
        """
        Override the method to return the tag name with id
        """
        return f"<{Constants.TAG_ENTITY}: {self.name}_{self.id}>"

    def data(
            self,
            start_time,
            stop_time,
            granularity=0,
            return_type=Constants.RETURN_PANDAS,
            transformations=[]):
        """
        Get the data for the given tag between the start_time and the stop_time
        for the given granularity
        :param start_time: (epoch) Start_time for getting data
        :param stop_time: (epoch) Stop_time for getting data
        :param granularity: Granularity of the data
        :param return_type: The param decides whether the data after querying will be
            json(when value is "json") or pandas dataframe(when value is "pd"). By default,
            it takes the value as "json"
        :param transformations: Refers to the list of transformations. It supports either
            interpolation or aggregation, depending upon which, we pass the value of this
            dictionary. An example value here is:
            [{
                "transformation_type": "interpolation",
                "column": "3",
                "method": "linear"
            }, {
                "transformation_type": "aggregation",
                "aggregation_column": "4",
                "aggregation_dict": {"3": "max"}
            }]
        :return: (DataIterator) DataIterator object which can be iterated to get the data
            between the given duration
        """
        from quartic_sdk.core.entity_helpers.entity_list import EntityList
        return TagDataIterator.create_tag_data_iterator(
            EntityList(
                Constants.TAG_ENTITY,
                [self]),
            start_time,
            stop_time,
            self.api_helper,
            granularity,
            return_type,
            transformations)
