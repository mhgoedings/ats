from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

engine = create_engine(os.environ['DB_HEROKU'])


Session = sessionmaker(bind=engine)

Base = declarative_base()
Base.metadata.bind = engine
