from utils_ak.time import cast_str
from datetime import datetime

from mongoengine import *
from utils_ak.mongoengine import cast_model, cast_dict


class UsersQuerySet(QuerySet):
    def last(self):
        return self.order_by('-id').first()

# todo: add branching


class BaseFeatureSet(Document):
    meta = {'abstract': True, 'queryset_class': UsersQuerySet}

    AUTO_FIELDS = ['created', 'version', '_id']
    name = StringField(default=lambda: cast_str(datetime.utcnow(), '%Y%m%d%H%M%S'))
    account = StringField(required=True)
    metadata = DictField()
    created = DateTimeField(default=datetime.utcnow)
    version = StringField(default=lambda: str(datetime.utcnow()))

    def clone(self):
        fs = cast_dict(self, self.__class__)
        for key in self.AUTO_FIELDS:
            fs.pop(key, None)
        return cast_model(fs, self.__class__)


class FeatureSet(BaseFeatureSet):
    engine = StringField(required=True)
    config = DictField()
    inputs = DictField()


class DatasetSchema(BaseFeatureSet):
    featureset = ReferenceField(FeatureSet, reverse_delete_rule=NULLIFY)
    params = DictField()


class DataSet(BaseFeatureSet):
    scope = DictField()
    dataset_schema = ReferenceField(DatasetSchema, reverse_delete_rule=NULLIFY)
    materialization = DictField()
    contents = DictField()
    state = DictField()


MODELS = {'FeatureSet': FeatureSet, 'featureset': FeatureSet,
          'DatasetSchema': DatasetSchema, 'dataset_schema': DatasetSchema,
          'DataSet': DataSet, 'dataset': DataSet}


def cast_model_class(model_class_name):
    return MODELS[model_class_name]

