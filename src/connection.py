from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL_TO_DB = "postgresql://postgres:password@localhost:5432/postgres"

engine = create_engine(URL_TO_DB)
Session = sessionmaker(bind=engine)
session = Session()
