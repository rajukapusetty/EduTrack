from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

# SQLite database URL
DATABASE_URL = "sqlite:///./microlearning.db"

# Create database engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create session factory (using SQLModel's Session class)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

# Create all tables
def init_db():
    SQLModel.metadata.create_all(engine)

# Dependency function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
