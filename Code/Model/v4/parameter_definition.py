from base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship


class ParameterDefinition(Base):
    __tablename__ = "parameter_definitions"
    id = Column(Integer, primary_key=True)

    name = Column(String(32), nullable=True)
    min_value = Column(Numeric(12, 4))
    max_value = Column(Numeric(12, 4))
    step_size = Column(Numeric(12, 4))
    data_type = Column(String(32), nullable=True)
    num_steps = Column(Integer)
    re_opt    = Column(String(1), nullable=True)
