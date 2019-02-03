from base import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Date,
)


class StrategyOosPeriod(Base):
    __tablename__ = "strategy_oos_periods"
    id = Column(Integer, primary_key=True)

    strategy_id = Column(Integer, ForeignKey("strategies.id"))

    start_dt  = Column(Date)
    end_dt    = Column(Date)


