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


class StrategyReoptParameter(Base):
    __tablename__ = "strategy_reopt_parameters"
    id = Column(Integer, primary_key=True)

    strategy_id = Column(Integer, ForeignKey("strategies.id"))

    name = Column(String(32), nullable=True)
    value = Column(String(255), nullable=True)
    data_type = Column(String(8), nullable=True)
    input_type = Column(String(32), nullable=True)  # = range


    def __str__(self):
        return f"""
           id          = {self.id}
           strategy_id = {self.strategy_id}
           name        = {self.name}

           value       = {self.value}
           data_type   = {self.data_type}

           input_type  = {self.input_type}"""

