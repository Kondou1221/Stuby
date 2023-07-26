from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker, declarative_base

Mysql_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/STUBY?charset=utf8"

engine = create_engine(Mysql_DATABASE_URL, echo=True)
sessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=Session
)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
