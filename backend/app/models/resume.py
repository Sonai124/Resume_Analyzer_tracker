from sqlalchemy import Column, Integer, Text, DateTime
from app.core.database import Base
from datetime import datetime


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
