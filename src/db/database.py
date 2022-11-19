import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# DB 관련 secrets 값 불러오기
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("PASSWORD")
db_host = os.environ.get("HOST")
db_port = os.environ.get("PORT")
db_database = os.environ.get("DATABASE")


DB_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}?charset=utf8"

engine = create_engine(DB_URL, encoding="utf-8", echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
