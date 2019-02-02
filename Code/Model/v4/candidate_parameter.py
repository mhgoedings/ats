from base import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    Boolean,
    Numeric,
    DateTime,
)


class CandidateParameter(Base):
    __tablename__ = "candidate_parameters"
    id = Column(Integer, primary_key=True)

    candidate_id = Column(Integer, ForeignKey("candidates.id"))

    name = Column(String(32), nullable=True)
    value = Column(String(255), nullable=True)
    data_type = Column(String(8), nullable=True)
    input_type = Column(String(32), nullable=True)  # = range
