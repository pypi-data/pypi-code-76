from datetime import datetime
from typing import Dict, Iterator, List, Optional, Tuple, Union
from dataclasses import dataclass
import strawberry
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.schema import Table

from ..app import db


@dataclass(init=False)
class CreateUpdateFields:
    # Keep track when records are created and updated.
    created_at: Optional[datetime] = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    updated_at: Optional[datetime] = db.Column(db.DateTime(), index=True, default=datetime.utcnow,
                                               onupdate=datetime.utcnow)
    created_by: Optional[int] = db.Column(db.Integer, default=1)
    updated_by: Optional[int] = db.Column(db.Integer)


class ResourceMixin(CreateUpdateFields):
    __table__: Table
    query: BaseQuery

    @classmethod
    def get_by_id(cls, id: Union[int, str, List[str]]):
        try:
            return cls.query.get(id)
        except ValueError:
            return None

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        """
        Save a model instance.

        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self

    def update(self, update_obj):
        """
        Update a model instance.

        :param update_obj: Model object containing updates
        :return: Model instance
        """
        updates = dict(x for x in update_obj.__dict__.items() if x[0] != '_sa_instance_state')
        for key, value in updates.items():
            setattr(self, key, value)
        self.save()

        return self

    def delete(self) -> None:
        """
        Delete a model instance.

        :return: db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()

    @classmethod
    def _bulk_insert(cls, data, label: str, dtype: str = '') -> None:
        """
        Bulk insert data to the model and log it. This is much more efficient than adding 1 row at a time in a loop.

        :param data: Data to be saved
        :type data: list
        :param dtype: Data type
        :type dtype: str
        :param label: Label for the output
        :type label: str
        :return: None
        """
        db.engine.execute(cls.__table__.insert(), data)
        print(f'Finished inserting {len(data):,} {(dtype + " ") if dtype else ""}{label}.')

        return None


class ResourceMixinWithVersion(ResourceMixin):
    version: Optional[int] = db.Column(db.Integer, nullable=False)
    __mapper_args__ = {'version_id_col': version}


@dataclass(init=False)
class RefSeqFields:
    id: strawberry.ID = db.Column(db.String(24), primary_key=True)  # RefSeq acc version, e.g. NM_003331.5 / NP_003322.3
    acc: str = db.Column(db.String(16), unique=True, index=True, nullable=False)


class RefseqMixin(RefSeqFields):
    query: BaseQuery

    @classmethod
    def find_by_refseq_id(cls, refseq_id: str):
        """Find a model by its RefSeq accession ID."""
        return cls.query.filter((cls.id == refseq_id) | (cls.acc == refseq_id)).first()


class ExternalResourceMixin:
    __table__: Table
    query: BaseQuery

    # Keep track when records are created and updated.
    created_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, default=1)
    updated_by = db.Column(db.Integer)

    @classmethod
    def get_by_id(cls, id: Union[int, str, List[str]]):
        try:
            return cls.query.get(id)
        except ValueError:
            return None


def sort_query(model: db.Model, query: BaseQuery, sort_keys: Dict[str, InstrumentedAttribute],
               order_by: Iterator[str]) -> BaseQuery:
    """Sort list with order_by fields, append id_ASC/id_DESC if not present."""
    sort_list = [order.split('_') for order in order_by]
    query = query.order_by(*[sort_keys[sort_key].desc() if sort_order == 'DESC' else sort_keys[sort_key]
                             for (sort_key, sort_order) in sort_list if sort_key in sort_keys])
    if not ('id_ASC' in order_by or 'id_DESC' in order_by):
        query = query.order_by(model.id.desc() if sort_list[0][1] == 'DESC' else model.id)

    return query


def generate_update_obj(model: db.Model, input, updated_by: strawberry.ID) -> Tuple[Optional[db.Model], str]:
    error = ''
    update_obj: Optional[db.Model] = None

    updated_fields = [field for field in dir(input)
                      if not field.startswith('_') and (input.__dict__.get(field) is not None)]

    if updated_fields:
        update_obj = model()
        for f in updated_fields:
            if f in ('symbol', 'name', 'mass', 'molecular_weight', 'formula_weight') and not input.__dict__.get(f):
                error = f'{f.capitalize()} field cannot be empty'
            else:
                update_obj.__setattr__(f, input.__dict__.get(f))
        if not error:
            update_obj.updated_at = datetime.utcnow()
            update_obj.updated_by = updated_by

    return update_obj, error
