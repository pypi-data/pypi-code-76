from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from pprint import pprint


try:
    SQLALCHEMY_DATABASE_URI = f"postgres://{os.environ['USERDB']}:{os.environ['PASSWORDDB']}@{os.environ['HOST']}/{os.environ['DBNAME']}"
    # SQLALCHEMY_DATABASE_URI = f"postgres://{os.environ['USERDB']}:{os.environ['PASSWORDDB']}@{os.environ['HOST']}/sro_ontology"
    # SQLALCHEMY_DATABASE_URI = "postgres://postgres:1234@localhost/sro_ontology"
except Exception as e:
    print(e)
    print("Favor configurar as variáveis de ambiente: [USERDB, PASSWORDDB, HOST, DBNAME]")
    exit(1)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine)
session = session()
Base = declarative_base()

class Config():

    def create_database(self):
        Base.metadata.create_all(engine)

