from base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class ParameterPreset(Base):
    __tablename__ = "parameter_presets"
    id = Column(Integer, primary_key=True)

    name       = Column(String(32), nullable=True)
    param      = Column(String(32), nullable=True)
    input_type = Column(String(32), nullable=True)
    value      = Column(String(32), nullable=True)
