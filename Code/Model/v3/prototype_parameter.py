from base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, Numeric, DateTime
from sqlalchemy.orm import relationship

class PrototypeParameter(Base):
    __tablename__ = 'prototype_parameters'
    id = Column(Integer, primary_key=True)
    proto_id = Column(Integer, ForeignKey('prototype_configs.id'))

    name = Column(String(32), nullable=False)
    input_type = Column(String(32), nullable=False)
    value = Column(String(255), nullable=False)
    data_type = Column(String(8), nullable=True)
    re_optimize = Column(String(255), nullable=True) # No | <num_steps>;<step_size>:<min_val>;<max_val>
