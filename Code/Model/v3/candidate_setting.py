from base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, Numeric, DateTime
from sqlalchemy.orm import relationship

class CandidateSetting(Base):
    __tablename__ = 'candidate_settings'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidate_configs.id'))

    name = Column(String(32), nullable=False)
    value = Column(String(255), nullable=False)
    data_type = Column(String(8), nullable=True)
