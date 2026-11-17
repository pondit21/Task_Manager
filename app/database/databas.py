import os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from sqlalchemy import create_engine, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


load_dotenv()
DATABASE_URL =os.getenv("DATABASE_URL")

if not DATABASE_URL:
     raise ValueError("Error:database_url enviroment filter not create")

engine =create_engine(
     DATABASE_URL,
     pool_size=10,
     max_overflow=20,
     pool_pre_ping=True
)
SessionLocal =sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass

# (Task Model)
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

# table create a function
def create_tables():
    Base.metadata.create_all(bind=engine)

# session dependesi (FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



















