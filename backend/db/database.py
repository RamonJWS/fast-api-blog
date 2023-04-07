from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import SQLALCHEMY_DATABASE_DIR

engine = create_engine(
    SQLALCHEMY_DATABASE_DIR, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# used to create db models.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
