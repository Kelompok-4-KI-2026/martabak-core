from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    # Phase 2 additions — nullable for backward compat with existing rows
    full_name = Column(String(150), nullable=True)
    outlet_name = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
