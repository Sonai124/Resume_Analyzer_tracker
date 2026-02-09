from sqlalchemy import Column, Integer, Float, Text
from app.core.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer)
    application_id = Column(Integer)
    match_score = Column(Float)
    missing_keywords = Column(Text)
