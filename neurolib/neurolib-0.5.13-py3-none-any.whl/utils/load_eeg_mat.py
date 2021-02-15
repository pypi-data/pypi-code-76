"""These loader classes are adapted from https://github.com/pupuis/sleepy
"""

from scipy.io import loadmat, savemat
import numpy as np


class Dataset:
    def load(path):
        """Static API-method that returns a raw data object for a given path.
        Must be implemented by direct subclasses.

        :param path: An absolute path to a file whose contents should be loaded
        as a raw data object.

        :returns: Raw data object representing the dataset.
        """

        pass

    def __init__(self, raw=None, path=""):
        """Abstract Dataset class, serving as an interface for all implementations.
        """

        self.raw = raw

        self.path = path

        self.samplingRate = 500

        self.changesMade = False

        self.dataSources = {}

    @property
    def filename(self):
        return self.path.split("/")[-1]

    @property
    def epochs(self):
        return self._epochs

    @epochs.setter
    def epochs(self, epochs):
        self._epochs = epochs

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def labels(self):
        try:
            return self._labels
        except AttributeError:

            self._labels = np.array([])

            return self._labels

    @labels.setter
    def labels(self, labels):
        self._labels = labels

    @property
    def userLabels(self):

        try:
            return self._userLabels
        except AttributeError:
            return []

    @userLabels.setter
    def userLabels(self, userLabels):
        self._userLabels = userLabels

    @property
    def filteredData(self):
        """By default, if no filteredData is set, the filteredData is simply
        equal the unfiltered data, i.e. self.data.
        """

        try:

            return self._filteredData
        except AttributeError:

            self.filteredData = self.data.copy()

            return self._filteredData

    @filteredData.setter
    def filteredData(self, filteredData):
        self._filteredData = filteredData

    @property
    def tags(self):
        """If tags are not set by the caller, then the tags are set to 0 using
        the labels array.
        """

        tags = self._tags if hasattr(self, "_tags") else None

        self._tags = self.constructTags(tags)

        return self._tags

    def constructTags(self, tags):
        """Constructs the tags array given the old (and potentially None-type) array of
        tags. Can be used by an inheriting class to ensure that the tags are constructed
        correctly.

        :param tags: A candidate array of new tags.

        :returns: A valid array of tags
        """

        if tags is not None:

            if not self.__tagsShapeObsolete(tags):

                return tags

        numberOfChannels = len(self.labels)

        tags = [np.zeros(len(self.labels[channel])) for channel in range(numberOfChannels)]

        return np.array(tags)

    @tags.setter
    def tags(self, tags):
        self._tags = tags

    @property
    def checkpoint(self):
        return self._checkpoint

    @checkpoint.setter
    def checkpoint(self, checkpoint):
        self._checkpoint = checkpoint

    def save(self):
        """Call to the dataset to save its contents on disk.
        """
        pass

    def setChangesMadeFrom(self, result):
        """Sets changesMade to true if the result array is equal to the labels
        in the dataset.
        """

        try:
            labels = self.dataSet.labels
        except AttributeError:
            return True

        self.changesMade = not np.array_equal(result, labels)

    def forEachChannel(self, labels, converter):
        """Supplies a converter function for each pair of channel and label that
        is stored in this dataset. The converter function is supplied with the
        following arguments:

        * Label
        * Data source containing the data of the epoch that contains the label

        The goal of this method is to abstract extracting the necessary data
        from the dataset to create a new event. The converter function can
        create an event based on this input and return it.

        :param labels: A np.array (channel * labelsPerEpoch) containing the labels.

        :param converter: A function that respects the said format.

        :returns: A list of lists of the return values of each converter function
        call.
        """

        numberOfChannels = labels.shape[0]

        return [self.__forEachLabel(labels, channel, converter) for channel in range(numberOfChannels)]

    def getDataSource(self, channel, label):
        """Returns a data source for a given channel and a given label.
        Extracts the first element from the label. The goal is to create one
        data source for each epoch such that events in the same epoch can share
        the data source (and data must not be copied that often). This instance
        buffers the data sources it has already created. If the epoch to which
        the given label belongs did not occur already, a new data source is
        allocated.

        :param channel: The index of the channel for which the data source shall
        be retrieved.

        :param label: The label containing a point or an interval in samples
        indicating where the event occurs.

        :returns: An instance of :class:`sleepy.gui.tagging.model.datasource.DataSource`
        containing the epoch data of the label.
        """

        if isinstance(label, np.ndarray):
            label = label[0]

        epochIndex = self.__findIndexInInterval(label)

        dataSource = self.__getBufferedDataSource(epochIndex, channel)

        dataSource.addLabel(label)

        return dataSource

    def __forEachLabel(self, labels, channel, converter):
        """Supplies a set of parameters to a converter and returns
        the result to the caller. Parameters a numpy array type of a label
        """

        numberOfLabels = labels[channel].shape[0]

        def getObject(labelIndex):

            label = np.array([labels[channel][labelIndex]]).ravel()

            dataSource = self.getDataSource(channel, label)

            # tag = self.tags[channel][labelIndex]

            return converter(label, dataSource)

        return [getObject(idx) for idx in range(numberOfLabels)]

    def __findIndexInInterval(self, point):
        """Finds the epoch interval by index to which a given point belongs.
        """

        startPoints = self.epochs[:, 0]
        endPoints = self.epochs[:, 1]

        startIndices = np.where(startPoints <= point)

        endIndices = np.where(endPoints >= point)

        intersection = np.intersect1d(startIndices, endIndices)

        # We assume the intervals to be non-overlapping and thus
        # it can only be one index match in both queries
        return intersection[0]

    def __getBufferedDataSource(self, epochIndex, channel):
        """Checks the buffer if the data source for the epoch specified by
        epochIndex and channel. If the data source does not exist, creates
        a new data source for this epoch. Returns the data source in both cases.
        """

        self.__ensureChannelInDataSources(channel)

        if not epochIndex in self.dataSources[channel]:

            self.__allocateDataSource(epochIndex, channel)

        return self.dataSources[channel][epochIndex]

    def __allocateDataSource(self, epochIndex, channel):
        """Creates a new data source for an epoch specified by epochIndex and
        channel.
        """

        epochInterval = self.epochs[epochIndex]

        epochData = self.__getEpochData(epochIndex, channel)

        self.dataSources[channel][epochIndex] = DataSource(*epochData, epochInterval, self.samplingRate)

    def __getEpochData(self, epochIndex, channel):
        """Retrieves the raw and the filtered data of the epoch, specified by
        epochIndex and channel, from the dataset.
        """

        epoch = self.data[epochIndex][channel]

        epochFiltered = self.filteredData[epochIndex][channel]

        return epoch, epochFiltered

    def __ensureChannelInDataSources(self, channel):
        """Ensures that the buffer contains an entry for a given channel.
        """

        if not channel in self.dataSources:

            self.dataSources[channel] = {}

    def __tagsShapeObsolete(self, tags):
        """Compares the first two dimension of the shape of the tags with the
        shape of the labels. This has to be done for each dimension as the number of
        labels is unlikely equal in every channel. Thus, the second dimension is
        hidden. Returns true if the tags' shape is obsolete.
        """

        if len(tags) == len(self.labels):

            if Dataset.__collectShape(tags) == Dataset.__collectShape(self.labels):

                return False

        return True

    def __collectShape(array):
        """Collects the inner length of all the entries of a given array.
        """

        return [len(entry) for entry in array]


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


class MatDataset(Dataset):
    """Implements the :class:`Dataset` interface of getters and setters. The
    sleepy-properties make use of a decorator that prepares the sleepy structure
    in mat-file before calling the getter or setter.
    This class is inherited by the publicly visible :class:`MultiChannelMatDataset`,
    which implements the logic behind the dataset. This class merely provides
    the bridge between the file-format and a convenient numpy format.
    """

    def importData(filename, structName="data"):

        """Load Matlab file with EEG data and save all fields in a Python dictionary"""

        try:

            fullDictData = loadmat(filename)

            keys = fullDictData[structName][0, 0].dtype.descr

            vals = fullDictData[structName][0, 0]

        except:
            raise

        dictData = {}

        for i in range(len(keys)):

            key = keys[i][0]

            dictData[key] = np.squeeze(vals[key])  # Converts Matlab arrays into Python numpy arrays

        return dictData

    def load(path):

        raw = MatDataset.importData(path)

        raw.pop("cfg", None)

        return raw

    @property
    def samplingRate(self):
        return self.raw["fsample"]

    @samplingRate.setter
    def samplingRate(self, value):
        self.raw["fsample"] = value

    @property
    def epochs(self):
        return self.raw["sampleinfo"].copy()  # [0][0][6].copy()

    @property
    def data(self):
        return self.raw["trial"].copy()  # [0][0][1][0].copy()

    @property
    def labels(self):

        if "sleepy-labels" not in self.raw:

            self.raw["sleepy-labels"] = np.array([])

        labels = self.raw["sleepy-labels"].copy()

        self.convertToPy(labels)

        return labels

    @labels.setter
    def labels(self, labels):
        """Sets labels as a numpy array to the sleepy addition and derives the
        tags from the new labels too.
        """

        self.setChangesMadeFrom(labels)

        self.raw["sleepy-labels"] = np.asarray(labels).copy()

    @property
    def tags(self):
        """Constructs the tags using the parent method constructTags. This method
        guarantees that the tags have a valid form. Converts the result into a
        more pythonic form and returns the result.

        :returns: A np.array with a valid shape, representing the tags of this
        dataset.
        """

        tags = self.convertToPy(self.raw["sleepy-tags"]) if "sleepy-tags" in self.raw else None

        self.raw["sleepy-tags"] = self.constructTags(tags)

        tags = self.raw["sleepy-tags"].copy()

        self.convertToPy(tags)

        return tags

    @tags.setter
    def tags(self, tags):
        self.raw["sleepy-tags"] = tags.copy()

    @property
    def filteredData(self):
        """Copies the content from the dataset's data if no filtered data is
        available.
        """

        if "sleepy-filteredData" not in self.raw:

            self.raw["sleepy-filteredData"] = self.data.copy()

        return self.raw["sleepy-filteredData"]

    @filteredData.setter
    def filteredData(self, filteredData):

        if filteredData is not None:
            if not np.array_equal(filteredData, self.filteredData):

                self.changesMade = True

        self.raw["sleepy-filteredData"] = filteredData

    @property
    def userLabels(self):

        if "sleepy-userLabels" not in self.raw:

            self.raw["sleepy-userLabels"] = np.array([])

        return self.raw["sleepy-userLabels"].copy()

    @userLabels.setter
    def userLabels(self, userLabels):

        if not np.array_equal(userLabels, self.userLabels):

            self.changesMade = True

        self.raw["sleepy-userLabels"] = userLabels.copy()

    @property
    def checkpoint(self):

        try:

            return tuple(self.raw["sleepy-metadata-checkpoint"].tolist())
        except KeyError:
            pass

    @checkpoint.setter
    def checkpoint(self, checkpoint):

        self.raw["sleepy-metadata-checkpoint"] = np.array(list(checkpoint))

    def removeCheckpoint(self):

        # Removes the metadata if it exists in the dictionary
        self.raw.pop("sleepy-metadata-checkpoint", None)

    def convertToPy(self, array):
        """Convert the given array into pythonic format.

        :param array: Input array to convert.

        :returns: The converted array for chaining.
        """

        for index in range(len(array)):

            array[index] = array[index].squeeze() if array[index].shape != (1,) else array[index]

        return array

    def save(self, path, navigators):
        """Collects potentially changed data from a list of navigators and
        stores the data in the raw structure. Then, saves the raw data in the
        .mat file.
        """

        self.userLabels = np.array([navigator.getLabelPartition()[1] for navigator in navigators])

        self.tags = np.array([navigator.getComputedEventTags() for navigator in navigators])

        self.saveToDisk(path)

    def saveToDisk(self, path):
        """I/O method writing the contents of this dataset to the disk. Override
        this in a test environment to avoid I/O.

        :param path: Location of the saved file.
        """

        savemat(path, {"data": self.raw})
