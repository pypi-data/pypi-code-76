from ehelply_bootstrapper.integrations.integration import Integration
from ehelply_bootstrapper.utils.state import State
from datetime import datetime
from typing import Union
from pydantic import BaseModel
from ehelply_microservice_library.integrations.fact import get_fact_endpoint


class BasicMeta(BaseModel):
    """
    Basic meta
    """
    name: str = None
    slug: str = None


class DetailedMeta(BaseModel):
    """
    Detailed meta based on Notes
    """
    summary_uuid: str = None
    description_uuid: str = None


class DatesMeta(BaseModel):
    """
    Date based meta
    """
    created_at: str = datetime.utcnow().isoformat()
    updated_at: str = datetime.utcnow().isoformat()


class MetaBase(BaseModel):
    """
    Meta
    """
    basic: BasicMeta = BasicMeta()
    detailed: DetailedMeta = DetailedMeta()
    custom: dict = {}
    dates: DatesMeta = DatesMeta()


class MetaDynamo(MetaBase):
    """
    A meta from DynamoDB
    """
    uuid: str


class BasicMetaCreate(BaseModel):
    """
    Basic meta
    """
    name: str = None
    slug: bool = True


class DetailedMetaCreate(BaseModel):
    """
    Detailed meta based on Notes
    """
    summary: str = None
    description: str = None


class DetailedMetaGet(DetailedMetaCreate):
    """
    Detailed meta based on Notes
    """
    summary_history: list = None
    description_history: list = None


class MetaCreate(BaseModel):
    """
    Meta
    """
    basic: BasicMetaCreate = BasicMetaCreate()
    detailed: DetailedMetaCreate = DetailedMetaCreate()
    custom: dict = {}


class MetaGet(BaseModel):
    """
    Meta
    """
    uuid: str
    basic: BasicMeta = BasicMeta()
    detailed: Union[DetailedMetaGet, None] = DetailedMetaGet()
    custom: Union[dict, None] = {}
    dates: Union[DatesMeta, None] = DatesMeta()


class MetaSlugger(BaseModel):
    """
    Meta slugger
    """
    name: str


class Meta(Integration):
    """
    Meta integration is used to talk to the ehelply-meta microservice
    """

    def __init__(self) -> None:
        super().__init__("meta")

        self.m2m = State.integrations.get("m2m")

    def init(self):
        super().init()

    def load(self):
        super().load()

    def get_base_url(self) -> str:
        return get_fact_endpoint('ehelply-meta') + "/meta"

    def create(self, service: str, type_str: str, entity_uuid: str, meta: MetaCreate) -> Union[MetaDynamo, None, bool]:
        """
        Create new meta
        :param service:
        :param type_str:
        :param entity_uuid:
        :param meta:
        :return:
        """
        if type(service) is not str or type(type_str) is not str or type(entity_uuid) is not str:
            State.logger.warning('Invalid payload when trying to create meta.')
            return False

        data: dict = {
            "meta": meta.dict()
        }

        response = self.m2m.requests.post(
            self.get_base_url() + "/service/" + service + "/type/" + type_str + "/entity/" + entity_uuid,
            json=data)

        if response.status_code != 200:
            return None

        return MetaDynamo(**response.json())

    def get(self, service: str, type_str: str, entity_uuid: str, detailed: bool = False, custom: bool = False,
            dates: bool = False) -> Union[None, bool, MetaGet]:
        """
        Get meta
        :param service:
        :param type_str:
        :param entity_uuid:
        :param detailed:
        :param custom:
        :param dates:
        :return:
        """
        if type(service) is not str or type(type_str) is not str or type(entity_uuid) is not str or type(
                detailed) is not bool or type(custom) is not bool or type(dates) is not bool:
            State.logger.warning('Invalid payload when trying to get meta.')
            return False

        response = self.m2m.requests.get(
            self.get_base_url() + "/service/" + service + "/type/" + type_str + "/entity/" + entity_uuid,
            params={"detailed": detailed, "custom": custom, "dates": dates})

        if response.status_code != 200:
            return None

        return MetaGet(**response.json())

    def get_using_uuid(self, meta_uuid: str, detailed: bool = False, custom: bool = False, dates: bool = False) -> \
    Union[None, bool, MetaGet]:
        """
        Get meta
        :param meta_uuid:
        :param detailed:
        :param custom:
        :param dates:
        :return:
        """
        if type(meta_uuid) is not str or type(detailed) is not bool or type(custom) is not bool or type(
                dates) is not bool:
            State.logger.warning('Invalid payload when trying to get meta.')
            return False

        response = self.m2m.requests.get(self.get_base_url() + "/" + meta_uuid,
                                         params={"detailed": detailed, "custom": custom, "dates": dates})

        if response.status_code != 200:
            return None

        return MetaGet(**response.json())

    def update(self, service: str, type_str: str, entity_uuid: str, meta: MetaCreate) -> Union[MetaDynamo, None, bool]:
        """
        Update meta
        :param service:
        :param type_str:
        :param entity_uuid:
        :param meta:
        :return:
        """
        if type(service) is not str or type(type_str) is not str or type(entity_uuid) is not str:
            State.logger.warning('Invalid payload when trying to update meta.')
            return False

        data: dict = {
            "meta": meta.dict()
        }

        response = self.m2m.requests.put(
            self.get_base_url() + "/service/" + service + "/type/" + type_str + "/entity/" + entity_uuid,
            json=data)

        if response.status_code != 200:
            return None

        return MetaDynamo(**response.json())

    def update_using_uuid(self, meta_uuid: str, meta: MetaCreate) -> Union[MetaDynamo, None, bool]:
        """
        Update meta
        :param meta_uuid:
        :param meta:
        :return:
        """
        if type(meta_uuid) is not str:
            State.logger.warning('Invalid payload when trying to update meta.')
            return False

        data: dict = {
            "meta": meta.dict()
        }

        response = self.m2m.requests.put(
            self.get_base_url() + "/" + meta_uuid,
            json=data)

        if response.status_code != 200:
            return None

        return MetaDynamo(**response.json())

    def delete(self, service: str, type_str: str, entity_uuid: str):
        """
        Delete meta
        :param service:
        :param type_str:
        :param entity_uuid:
        :return:
        """
        if type(service) is not str or type(type_str) is not str or type(entity_uuid) is not str:
            State.logger.warning('Invalid payload when trying to delete meta.')
            return False

        response = self.m2m.requests.delete(
            self.get_base_url() + "/service/" + service + "/type/" + type_str + "/entity/" + entity_uuid)

        if response.status_code != 200:
            return None

        return response.json()

    def delete_using_uuid(self, meta_uuid: str):
        """
        Delete meta
        :param meta_uuid:
        :return:
        """
        if type(meta_uuid) is not str:
            State.logger.warning('Invalid payload when trying to delete meta.')
            return False

        response = self.m2m.requests.delete(self.get_base_url() + "/" + meta_uuid)

        if response.status_code != 200:
            return None

        return response.json()

    def touch(self, service: str, type_str: str, entity_uuid: str) -> Union[MetaDynamo, None, bool]:
        """
        Touch meta
        :param service:
        :param type_str:
        :param entity_uuid:
        :return:
        """
        if type(service) is not str or type(type_str) is not str or type(entity_uuid) is not str:
            State.logger.warning('Invalid payload when trying to touch meta.')
            return False

        response = self.m2m.requests.post(
            self.get_base_url() + "/service/" + service + "/type/" + type_str + "/entity/" + entity_uuid + "/touch")

        if response.status_code != 200:
            return None

        return MetaDynamo(**response.json())

    def slug(self, name: str):
        """
        Turn a string into a slug
        :param name:
        :return:
        """
        return self.m2m.requests.post(self.get_base_url() + "/slug", json={"name": name}).json()
