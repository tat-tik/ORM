import sqlalchemy
from sqlalchemy.orm import sessionmaker
from modelsorm import create_tables

DSN = "postgresql://postgres:postgres@localhost:5432/orm"

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


session.close