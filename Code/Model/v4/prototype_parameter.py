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


class PrototypeParameter(Base):
    __tablename__ = "prototype_parameters"
    id = Column(Integer, primary_key=True)

    proto_id = Column(Integer, ForeignKey("prototypes.id"))

    name = Column(String(32), nullable=True)
    input_type = Column(String(32), nullable=True)
    value = Column(String(255), nullable=True)
    data_type = Column(String(8), nullable=True)
    re_optimize = Column(String(255), nullable=True)


# re_optimize:
# No | <num_steps>;<step_size>:<min_val>;<max_val>
