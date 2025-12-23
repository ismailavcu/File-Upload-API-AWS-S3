from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime
from sqlalchemy.sql import func

from app.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    s3_key = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    #created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
