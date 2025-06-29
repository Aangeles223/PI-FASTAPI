from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configura tus datos reales
USER = "root"
PASSWORD = "Master12$"
HOST = "localhost"
PORT = "3306"
DB_NAME = "devplay"

DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
