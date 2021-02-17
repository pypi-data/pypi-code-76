from datetime import datetime

from bottle import Bottle, request, response
from sqlalchemy import JSON, Boolean, Column, Enum, MetaData, String, Table, create_engine, insert, select, update
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session, declarative_base

rest_api = Bottle(catchall=False, autojson=True)
engine = create_engine(
    "sqlite://",
    # environ["RDBMS_URI"].replace("postgres", "postgresql+psycopg2", 1)
    echo=True,
    future=True,
)
metadata = MetaData()
Base = declarative_base()
config_tbl = Table(
    "config_tbl",
    metadata,
    Column(
        "dataset_name", String, doc="name of dataset", default="mnist", primary_key=True
    ),
    Column(
        "tfds_dir",
        String,
        doc="directory to look for models in",
        default="~/tensorflow_datasets",
        nullable=False,
    ),
    Column(
        "K",
        Enum("np", "tf", name="K"),
        doc="backend engine, e.g., `np` or `tf`",
        default="np",
        nullable=False,
    ),
    Column("as_numpy", Boolean, doc="Convert to numpy ndarrays", default=None),
    Column(
        "data_loader_kwargs", JSON, doc="pass this as arguments to data_loader function"
    ),
    comment="Acquire from the official tensorflow_datasets model zoo, or the ophthalmology focussed ml-prepare\n\n"
    ":returns: Train and tests dataset splits. Defaults to (np.empty(0), np.empty(0))\n"
    ":rtype: ```Union[Tuple[tf.data.Dataset, tf.data.Dataset], Tuple[np.ndarray, np.ndarray]]```",
)
metadata.create_all(engine)

stmt = insert(config_tbl)
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()


class Config(Base):
    __tablename__ = 'config_tbl'

    dataset_name = Column(
        String, doc="name of dataset", default="mnist", primary_key=True
    )

    tfds_dir = Column(
        String,
        doc="directory to look for models in",
        default="~/tensorflow_datasets",
        nullable=False,
    )

    K = Column(
        Enum("np", "tf", name="K"),
        doc="backend engine, e.g., `np` or `tf`",
        default="np",
        nullable=False,
    )

    as_numpy = Column(Boolean, doc="Convert to numpy ndarrays", default=None)

    data_loader_kwargs = Column(JSON, doc="pass this as arguments to data_loader function")

    def __repr__(self):
        """
        Emit a string representation of the current instance

        :returns: String representation of instance
        :rtype: ```str```
        """
        return "Config(dataset_name={dataset_name!r}, tfds_dir={tfds_dir!r}, " \
               "K={K!r}, as_numpy={as_numpy!r}, data_loader_kwargs={data_loader_kwargs!r})".format(
            dataset_name=self.dataset_name, tfds_dir=self.tfds_dir, K=self.K,
            as_numpy=self.as_numpy, data_loader_kwargs=self.data_loader_kwargs
        )


def orm_to_dict(orm_instance):
    """
    Convert instance of an SQLalchemy declarative base class into a Python dictionary

    :param orm_instance: Instance of an SQLalchemy declarative base class
    :type orm_instance: ```Base```

    :returns: Dict representation of instance
    :rtype: ```Optional[dict]```
    """
    return None if orm_instance is None \
        else {col.name: getattr(orm_instance, col.name) for col in orm_instance.__table__.columns}


# print(config_tbl_str)
# print(ast.dump(ast.parse(config_decl_base_str).body[0], indent=4))


@rest_api.route('/api')
@rest_api.route('/api/status')
def status():
    return {'server_time': datetime.now().strftime("%I:%M%p on %B %d, %Y")}


@rest_api.post('/api/config')
def create0():
    """
    Create `Config`

    ```yml
    requests:
        description: `Config` to add
        content:
          'application/json':
            schema:
              $ref: ```Config```

    responses:
      '201':
        description: A `Config` object.
        content:
          application/json:
            schema:
              $ref: ```Config```
      '400':
        description: A `ServerError` object.
        content:
          application/json:
            schema:
              $ref: ```ServerError```
    ```

    :returns: Created ```Config``` instance (as a dict), or an error
    :rtype: ```dict```
    """
    try:
        config = Config(**request.json)
    except TypeError as e:
        response.status = 400
        return {"error": "ValidationError", "error_description": "\n".join(e.args)}

    try:
        with Session(engine) as session:
            session.add(config)
            session.commit()
            created_config = orm_to_dict(config)
    except DatabaseError as e:
        response.status = 400
        return {"error": e.__class__.__name__, "error_code": e.code, "error_description": str(e.__cause__)}

    return created_config


@rest_api.post('/api/config1')
def create1():
    """
    Create `Config`

    ```yml
    requests:
        description: `Config` to add
        content:
          'application/json':
            schema:
              $ref: ```Config```

    responses:
      '201':
        description: A `Config` object.
        content:
          application/json:
            schema:
              $ref: ```Config```
      '400':
        description: A `ServerError` object.
        content:
          application/json:
            schema:
              $ref: ```ServerError```
    ```

    :returns: Created ```Config``` instance (as a dict), or an error
    :rtype: ```dict```
    """
    return create_helper0(request, response)(Config)


@rest_api.post('/api/config2')
def create2():
    """
    Create `Config`

    ```yml
    requests:
        description: `Config` to add
        content:
          'application/json':
            schema:
              $ref: ```Config```

    responses:
      '201':
        description: A `Config` object.
        content:
          application/json:
            schema:
              $ref: ```Config```
      '400':
        description: A `ServerError` object.
        content:
          application/json:
            schema:
              $ref: ```ServerError```
    ```

    :returns: Created ```Config``` instance (as a dict), or an error
    :rtype: ```dict```
    """
    code, body = create_helper1(Config, request.body)
    response.status = code
    return body


def create_helper0(req, res):
    """
    Create / handle-errors with Bottle and SQLalchemy

    :param req: Bottle request
    :type req: ```bottle.request```

    :param res: Bottle response
    :type res: ```bottle.response```

    :returns: A function which actually does the work
    :rtype: ```Callable[[Base], dict]```
    """
    def _create_helper(orm_class):
        """
        Create / handle-errors with Bottle and SQLalchemy

        :param orm_class: An ORM class inheriting SQLalchemy declarative base class
        :type orm_class: ```Base```

        :returns: Created (as a dict) or error dict
        :rtype: ```dict```
        """
        try:
            orm_instance = orm_class(**req.json)
        except TypeError as e:
            res.status = 400
            return {"error": "ValidationError", "error_description": "\n".join(e.args)}

        try:
            with Session(engine) as session:
                session.add(orm_instance)
                session.commit()
                created = orm_to_dict(orm_instance)
        except DatabaseError as e:
            res.status = 400
            return {"error": e.__class__.__name__, "error_code": e.code, "error_description": str(e.__cause__)}

        return created

    return _create_helper


def create_helper1(orm_class, body):
    """
    Create / handle-errors with Bottle and SQLalchemy

    :param orm_class: An ORM class inheriting SQLalchemy declarative base class
    :type orm_class: ```Base```

    :param body: Body of the instance to create
    :type body: ```dict```

    :returns: Status code, created (as a dict) or error dict
    :rtype: ```Tuple[int, dict]```
    """
    try:
        orm_instance = orm_class(**body)
    except TypeError as e:
        return 400, {"error": "ValidationError", "error_description": "\n".join(e.args)}

    try:
        with Session(engine) as session:
            session.add(orm_instance)
            session.commit()
            created = orm_to_dict(orm_instance)
    except DatabaseError as e:
        return 400, {"error": e.__class__.__name__, "error_code": e.code, "error_description": str(e.__cause__)}

    return 201, created


# paths:
#   /api/config/{dataset_name}:
#     parameters:
#     - name: dataset_name
#       in: path
#       required: true
#       description: The primary key of the `Config` to lookup
#       schema:
#         type: string


@rest_api.get('/api/config/:dataset_name')
def read(dataset_name):
    """
    Find one `Config` or error

    ```yml
    responses:
      '200':
        description: Found `Config` object.
        content:
          application/json:
            schema:
              $ref: ```Config```
      '404':
        description: A `ServerError` object indicating no `Config` was found.
        content:
          application/json:
            schema:
              $ref: ```ServerError```
    ```

    :param dataset_name: The primary key of `Config`
    :type dataset_name: ```str```

    :returns: Found `Config` (as a dict) or error dict
    :rtype: ```dict```
    """
    with Session(engine) as session:
        config = session.execute(select(Config).filter_by(dataset_name=dataset_name)).one_or_none()

    if config is None:
        response.status = 404
        return {"error": "NotFound", "error_description": "Config not found"}

    return orm_to_dict(config[0])


@rest_api.put('/api/config/:dataset_name')
def edit(dataset_name):
    """
    Update one `Config` or error

    ```yml
    responses:
      '200':
        description: Updated `Config` object.
        content:
          application/json:
            schema:
              $ref: ```Config```
      '404':
        description: A `ServerError` object indicating no `Config` was found.
        content:
          application/json:
            schema:
              $ref: ```ServerError```
      '400':
        description: A `ServerError` object.
        content:
          application/json:
            schema:
              $ref: ```ServerError```
    ```

    :param dataset_name: The primary key of `Config`
    :type dataset_name: ```str```

    :returns: Found `Config` (as a dict) or error dict
    :rtype: ```dict```
    """
    #config = Config(dataset_name=dataset_name)

    with Session(engine) as session:
        config = session \
            .execute(select(Config) \
                     .where(Config.dataset_name == dataset_name)) \
            .one_or_none()

        stmt = update(Config) \
            .where(Config.dataset_name == dataset_name) \
            .values(request.json) \
            .execution_options(synchronize_session="fetch")

        row = session \
            .execute(stmt)
        print("row.rowcount:", row.rowcount,
              ";\nconfig:", config, ';')

    #with Session(engine) as session:
    #    res = session.query(Config)
    #                 .filter_by(dataset_name=dataset_name)
    #                 .update(request.json, synchronize_session="fetch")
    #    print("res:", res, ';')

    if config is None:
        response.status = 404
        return {"error": "NotFound", "error_description": "Config not found"}

    return orm_to_dict(config[0])


@rest_api.delete('/api/config/:dataset_name')
def destroy(dataset_name):
    """
    Delete one `Config`

    ```yml
    responses:
      '204':
    ```

    :param dataset_name: The primary key of `Config`
    :type dataset_name: ```str```

    :returns: None. Always. Even if nothing was deleted.
    :rtype: ```dict```
    """
    with Session(engine) as session:
        session \
            .query(Config) \
            .filter(Config.dataset_name == dataset_name) \
            .delete(synchronize_session='evaluate')

    response.status = 204


if __name__ == '__main__':
    rest_api.run(host='0.0.0.0', port=5555, debug=True)
