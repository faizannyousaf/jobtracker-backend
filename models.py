from sqlalchemy import Column, Integer, String
from database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)  # Firebase UID
    company = Column(String)
    role = Column(String)
    date_applied = Column(String)
    status = Column(String)