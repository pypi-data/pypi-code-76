import json
import os
from enum import Enum
from io import BytesIO

import pandas as pd
import pandavro

from maquette_lib.__client import Client
from maquette_lib.__user_config import EnvironmentConfiguration

config = EnvironmentConfiguration()
client = Client.from_config(config)


class ERetentionUnit(str, Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    YEARS = "years"


class EAccessType(str, Enum):
    DIRECT = "direct"
    CASHED = "cashed"


class EDataAssetType(str, Enum):
    DATASET = "dataset"
    COLLECTION = "collection"
    SOURCE = "source"


class EAuthorizationType(str, Enum):
    USER = "user"
    ROLE = "role"
    WILDCARD = "*"


class EProjectPrivilege(str, Enum):
    MEMBER = "member"
    PRODUCER = "producer"
    CONSUMER = "consumer"
    ADMIN = "admin"


class EDatasetPrivilege(str, Enum):
    PRODUCER = "producer"
    CONSUMER = "consumer"
    ADMIN = "admin"


class EDataClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class EDataVisibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class EPersonalInformation(str, Enum):
    NONE = "none"
    PERSONAL_INFORMATION = "pi"
    SENSITIVE_PERSONAL_INFORMATION = "spi"


# TODO Doku (of course)

class DataAsset:
    """
    Base class for all Data Assets
    """
    project: str = None
    project_name: str = None
    #TODO: IMPORTANT - project id needs to be either initialized here, read from the ENV variable, config file or not in the header!!!
    data_asset_name: str = None
    header = None

    def __init__(self, data_asset_name: str, title: str = None, summary: str = "Lorem Impsum",
                 visibility: str = EDataVisibility.PUBLIC,
                 classification: str = EDataClassification.PUBLIC,
                 personal_information: str = EPersonalInformation.NONE,
                 project_name: str = None, project_id: str = None, data_asset_type: EDataAssetType = None):

        self.data_asset_name = data_asset_name
        if title:
            self.title = title
        else:
            self.title = data_asset_name

        self.summary = summary
        self.visibility = visibility
        self.classification = classification
        self.personal_information = personal_information
        self.project_name = project_name
        if project_id:
            self.project = project_id
            self.header = {'x-project': self.project}
        else:
            if config.get_project():
                self.project = config.get_project()
                self.header = {'x-project': self.project}
        self.data_asset_type = data_asset_type

    def create(self):
        """
        BASE FUNCTION FOR INHERITANCE: Creates the Data Asset via API in the Maquette Hub
        Returns: the instantiated Data Asset

        """
        client.command(cmd='{}s create'.format(self.data_asset_type),
                       args={'name': self.data_asset_name, 'title': self.title, 'summary': self.summary,
                             'visibility': self.visibility, 'classification': self.classification,
                             'personalInformation': self.personal_information},
                       headers=self.header)
        return self

    def update(self, to_update: str):
        """
        BASE FUNCTION FOR INHERITANCE: Updates the Data Asset with the "top_update" name, with the calling object's arguments
        Args:
            to_update: the name of the Data Asset to update

        Returns: the updated Data Asset

        """
        client.command(cmd='{}s update'.format(self.data_asset_type),
                       args={self.data_asset_type: to_update, 'name': self.data_asset_name, 'title': self.title,
                             'summary': self.summary,
                             'visibility': self.visibility, 'classification': self.classification,
                             'personalInformation': self.personal_information},
                       headers=self.header)
        return self

    def remove(self):
        """
        Removes the Data Asset from the Maquette Hub
        """
        client.command(cmd='{}s remove'.format(self.data_asset_type),
                       args={'{}'.format(self.data_asset_type): self.data_asset_name},
                       headers=self.header)

    def delete(self):
        """
        Removes the Data Asset from the Maquette Hub
        """
        self.remove()


class Collection(DataAsset):
    """
    A Data Collection contains binary objects like files and images in a directory based structure
    """
    def __init__(self, data_asset_name: str, title: str = None, summary: str = "Lorem Impsum",
                 visibility: str = EDataVisibility.PUBLIC,
                 classification: str = EDataClassification.PUBLIC,
                 personal_information: str = EPersonalInformation.NONE,
                 project_name: str = None, project_id: str = None):
        super().__init__(data_asset_name, title, summary, visibility, classification, personal_information,
                         project_name, project_id,
                         EDataAssetType.COLLECTION)

    def put(self, data, short_description: str = None)-> 'Collection':
        """
        Send single files to a collection. ZIP File upload is not intended from the Python SDK
        Args:
            data: the actual data as binary object
            short_description: optinal string to describe the object, if not provided an automatic commit message will
                                be created

        Returns: the version identification as string

        """
        if short_description is None:
            short_description = os.path.basename(data.name) + " uploaded to collection " + self.data_asset_name

        if self.header:
            headers = {'Accept': 'application/octet-stream', **self.header}
        else:
            headers = {'Accept': 'application/octet-stream'}

        resp = client.post('data/collections/' + self.data_asset_name, files={
            'file': (os.path.basename(data.name), data, 'avro/binary', {'Content-Type': 'avro/binary'})
        }, headers=headers, json={
            'name': os.path.basename(data.name),
            'message': short_description})
        return self

    def get(self, filename, tag: str = None):
        """
        Function to download binary Data from a collection

        Args:
            filename: path to the binary object in the Collection
            tag: optional version tag, if not provided, the latest version will be downloaded

        Returns: the binary object

        """
        if tag:
            resp = client.get('data/collections/' + self.data_asset_name + '/tags/' + tag + '/' + filename, headers=self.header)
        else:
            resp = client.get('data/collections/' + self.data_asset_name + '/latest/' + filename, headers=self.header)
        return BytesIO(resp.content)

    def tag(self, tag: str, short_description: str = None):
        client.command(cmd='collections tag',
                       args={'collection': self.data_asset_name,
                             'tag': tag,
                             'message': short_description},
                       headers=self.header)
        return self


class Source(DataAsset):
    """
    A Data Asset for accessing structural Database sources
    """
    def __init__(self, data_asset_name: str, title: str = None, summary: str = "Lorem Impsum",
                 visibility: str = EDataVisibility.PUBLIC,
                 classification: str = EDataClassification.PUBLIC,
                 personal_information: str = EPersonalInformation.NONE, access_type: EAccessType = EAccessType.DIRECT,
                 db_properties: dict = None, project_name: str = None, project_id: str = None):
        self.access_type = access_type
        self.db_properties = db_properties
        super().__init__(data_asset_name, title, summary, visibility, classification, personal_information,
                         project_name, project_id,
                         EDataAssetType.SOURCE)

    def create(self):
        """
        Create the Data Source via API on the Maquette Hub. Properties for the Database to access have to be provieded
        Returns: the initiated Data Source object

        """
        client.command(cmd='sources create'.format(self.data_asset_type),
                       args={'name': self.data_asset_name, 'title': self.title, 'summary': self.summary,
                             'visibility': self.visibility, 'classification': self.classification,
                             'personalInformation': self.personal_information, 'properties': self.db_properties,
                             'accessType': self.access_type},
                       headers=self.header)
        return self

    def update(self, to_update: str):
        """

        Args:
            to_update:

        Returns:

        """
        client.command(cmd='sources update',
                       args={'source': to_update, 'name': self.data_asset_name, 'title': self.title,
                             'summary': self.summary,
                             'visibility': self.visibility, 'classification': self.classification,
                             'accessType': self.access_type, 'properties': self.db_properties,
                             'personalInformation': self.personal_information},
                       headers=self.header)
        return self

    #TODO: def update_db...
    # for convenience

    def get(self) -> pd.DataFrame:
        """

        Returns:

        """
        resp = client.get('data/sources/' + self.data_asset_name)
        return pandavro.from_avro(BytesIO(resp.content))


class Dataset(DataAsset):
    """

    """
    version: str = None

    def __init__(self, data_asset_name: str, title: str = None, summary: str = "Lorem Impsum",
                 visibility: str = EDataVisibility.PUBLIC,
                 classification: str = EDataClassification.PUBLIC,
                 personal_information: str = EPersonalInformation.NONE,
                 project_name: str = None, project_id: str = None, version: str = None):
        if version:
            self.version = version
        super().__init__(data_asset_name, title, summary, visibility, classification, personal_information,
                         project_name, project_id,
                         EDataAssetType.DATASET)

    def put(self, data: pd.DataFrame, short_description: str) -> 'Dataset':
        """

        Args:
            data:
            short_description:

        Returns:

        """
        ds = self.data_asset_name

        file: BytesIO = BytesIO()
        pandavro.to_avro(file, data)
        file.seek(0)

        if self.header:
            headers = {'Accept': 'application/csv', **self.header}
        else:
            headers = {'Accept': 'application/csv'}

        resp = client.post('data/datasets/' + ds, files={
            'file': (short_description, file, 'avro/binary', {'Content-Type': 'avro/binary'})
        }, headers=headers, json={
            'message': short_description})

        self.version = json.loads(resp.content)["version"]
        return self

    def get(self, version: str = None) -> pd.DataFrame:
        """

        Args:
            version:

        Returns:

        """
        ds = self.data_asset_name
        if version:
            resp = client.get('data/datasets/' + ds + '/' + version, headers=self.header)
        else:
            resp = client.get('data/datasets/' + ds, headers=self.header)
        return pandavro.from_avro(BytesIO(resp.content))


class Stream(DataAsset):
    """

    """
    def __init__(self, data_asset_name: str, title: str = None, summary: str = "Lorem Impsum",
                 visibility: str = EDataVisibility.PUBLIC,
                 classification: str = EDataClassification.PUBLIC,
                 personal_information: str = EPersonalInformation.NONE,
                 schema: dict = None,
                 retention: dict = None,
                 project_name: str = None,
                 project_id: str = None):
        self.schema = schema
        if retention:
            self.retention = retention
        else:
            self.retention = {"unit": ERetentionUnit.HOURS, "retention": 6}
        super().__init__(data_asset_name, title, summary, visibility, classification, personal_information,
                         project_name, project_id,
                         EDataAssetType.DATASET)

    def update(self, to_update: str):
        """

        Args:
            to_update:

        Returns:

        """
        client.command(cmd='sources update'.format(self.data_asset_type),
                       args={self.data_asset_type: to_update, 'name': self.data_asset_name, 'title': self.title,
                             'summary': self.summary,
                             'visibility': self.visibility, 'classification': self.classification,
                             'schema': self.schema, 'retention': self.retention,
                             'personalInformation': self.personal_information},
                       headers=self.header)
        return self

    def get(self) -> dict:
        """

        Returns:

        """
        resp = client.get('data/streams/' + self.data_asset_name, headers=self.header)
        return json.loads(resp.content)


class Project:
    """

    """
    name: str = None
    title: str = None
    summary: str = None
    id: str = None

    __header = None

    def __init__(self, name: str = None, title: str = None, summary: str = None, id: str = None):
        self.name = name
        self.summary = summary
        if title:
            self.title = title
        else:
            self.title = name
        if id:
            self.id = id
            self.__header = {'x-project': self.id}
        else:
            if config.get_project():
                self.id = config.get_project()
                self.__header = {'x-project': self.id}

    def create(self) -> 'Project':
        """

        Returns:

        """
        client.command(cmd='projects create',
                       args={'title': self.title, 'name': self.name, 'summary': self.summary})
        return self

    def activate(self) -> 'Project':
        """
        Activates the current project in getting the project id, and setting it to the configuration
        Environment variable needs to be set separately
        :return:
        """
        if self.__header:
            headers = {'Content-Type': 'application/json', **self.__header}
        else:
            headers = {'Content-Type': 'application/json'}
        status, resp = client.command(cmd='projects get',
                              args={'name': self.name},
                              headers=headers)
        data = resp["data"]
        self.__init__(name=data["name"], title=data["title"], summary=data["summary"], id=data["id"])

        return self

    def update(self, to_update: str):
        """

        Args:
            to_update:

        Returns:

        """
        client.command(cmd='projects update', args={'project': to_update, 'title': self.title, 'name': self.name,
                                                    'summary': self.summary})
        return self

    def remove(self):
        """

        Returns:

        """
        resp = client.command(cmd='projects remove',
                              args={'name': self.name})

    def delete(self):
        """

        Returns:

        """
        self.remove()

    def datasets(self, to_csv=False):
        """

        Args:
            to_csv:

        Returns:

        """
        if to_csv:
            resp = client.command(cmd='datasets list', headers={'Accept': 'application/csv',
                                                                'x-project': self.name})
        else:
            resp = client.command(cmd='datasets list',
                                  headers={'x-project': self.name})
        return resp[1]

    def dataset(self, dataset_name: str = None, dataset_title: str = None, summary: str = None,
                visibility: str = None, classification: str = None, personal_information: str = None) -> Dataset:
        """

        Args:
            dataset_name:
            dataset_title:
            summary:
            visibility:
            classification:
            personal_information:

        Returns:

        """
        args = [arg for arg in
                [dataset_name, dataset_title, summary, visibility, classification, personal_information] if
                arg]
        return Dataset(project_name=self.name, *args)

    def source (self, source_name: str = None, source_title: str = None, summary: str = None, visibility: str = None, classification: str = None, personal_information:str = None,
                access_type: str = None, db_properties = None) -> 'Source':
        args = [arg for arg in
                [source_name, source_title, summary, visibility, classification, personal_information, access_type] if arg]
        return Source(project_name=self.name, db_properties=db_properties, *args)


    def collection(self, collection_name: str = None, collection_title: str = None, summary: str = None,
                   visibility: str = None, classification: str = None, personal_information: str = None) -> Collection:
        """

        Args:
            collection_name:
            collection_title:
            summary:
            visibility:
            classification:
            personal_information:

        Returns:

        """
        args = [arg for arg in
                [collection_name, collection_title, summary, visibility, classification, personal_information] if
                arg]
        return Collection(project_name=self.name, *args, )


#TODO: Read project_id via config!
def project(name: str, title: str = None, summary: str = None) -> Project:
    """
    A project factory.

    Args:
        name (str) :
        title (str) : Defaults to None
        summary (str) : Defaults to None


    (Generated by docly)
    """
    return Project(name=name, title=title, summary=summary)


def dataset(dataset_name: str = None, dataset_title: str = None, summary: str = None,
            visibility: str = None, classification: str = None, personal_information: str = None) -> Dataset:
    """

    Args:
        dataset_name:
        dataset_title:
        summary:
        visibility:
        classification:
        personal_information:

    Returns:

    """
    args = [arg for arg in
            [dataset_title, summary, visibility, classification, personal_information] if
            arg]
    return Dataset(data_asset_name=dataset_name, project_name=os.environ.get('MQ_PROJECT_NAME', 'Project_42'), *args)


def collection(collection_name: str = None, collection_title: str = None, summary: str = None,
               visibility: str = None, classification: str = None, personal_information: str = None) -> Collection:
    """

    Args:
        collection_name:
        collection_title:
        summary:
        visibility:
        classification:
        personal_information:

    Returns:

    """
    args = [arg for arg in
            [collection_title, summary, visibility, classification, personal_information] if
            arg]
    return Collection(data_asset_name=collection_name, project_name=os.environ.get('MQ_PROJECT_NAME', 'Project_42'),
                      *args)


def source(source_name: str = None, source_title: str = None, summary: str = None,
           visibility: str = None, classification: str = None, personal_information: str = None,
           access_type: str = None, db_properties: dict = None) -> Source:
    """
    Construct a Source object.

    Args:
        source_name (str) : Defaults to None
        source_title (str) : Defaults to None
        summary (str) : Defaults to None
        visibility (str) : Defaults to None
        classification (str) : Defaults to None
        personal_information (str) : Defaults to None
        access_type (str) : Defaults to None
        db_properties (dict) : Defaults to None


    (Generated by docly)
    """
    args = [arg for arg in
            [source_title, summary, visibility, classification, personal_information, access_type, db_properties] if
            arg]
    return Source(data_asset_name=source_name, project_name=os.environ.get('MQ_PROJECT_NAME', 'Project_42'), *args)


def stream(stream_name: str = None, stream_title: str = None, summary: str = None,
           visibility: str = None, classification: str = None, personal_information: str = None, retention: dict = None,
           schema: dict = None) -> Stream:
    """
    Create a Stream object.

    Args:
        stream_name (str) : Defaults to None
        stream_title (str) : Defaults to None
        summary (str) : Defaults to None
        visibility (str) : Defaults to None
        classification (str) : Defaults to None
        personal_information (str) : Defaults to None
        retention (dict) : Defaults to None
        schema (dict) : Defaults to None


    (Generated by docly)
    """
    args = [arg for arg in
            [stream_title, summary, visibility, classification, personal_information, retention, schema] if
            arg]
    return Stream(data_asset_name=stream_name, project_name=os.environ.get('MQ_PROJECT_NAME', 'Project_42'), *args)


# TODO list functions for collections, streams and sources


def datasets(to_csv=False):
    """

    Args:
        to_csv:

    Returns:

    """
    if to_csv:
        resp = client.command(cmd='datasets list', headers={'Accept': 'application/csv',
                                                            'x-project': os.environ.get('MQ_PROJECT_NAME',
                                                                                        'Project_42')})
    else:
        resp = client.command(cmd='datasets list',
                              headers={'x-project': os.environ.get('MQ_PROJECT_NAME', 'Project_42')})
    return resp[1]


def projects(to_csv=False):
    """
    List projects

    Args:
        to_csv : Defaults to False


    (Generated by docly)
    """
    if to_csv:
        resp = client.command(cmd='projects list', headers={'Accept': 'application/csv'})
    else:
        resp = client.command(cmd='projects list')
    return resp[1]
