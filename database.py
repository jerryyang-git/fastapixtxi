from sqlalchemy import create_engine, QueuePool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "mysql://root:yang71613@localhost/fastapi"

# Sqllite 需要 `connect_args={"check_same_thread": False}`
# Mysql 需要 `poolclass=QueuePool`
engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=QueuePool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
