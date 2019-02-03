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


class StrategyOosSetting(Base):
    __tablename__ = "strategy_oos_settings"
    id = Column(Integer, primary_key=True)

    strategy_id = Column(Integer, ForeignKey("strategies.id"))
    period_id   = Column(Integer, ForeignKey("strategy_oos_periods.id"))

    name      = Column(String(32), nullable=True)
    value     = Column(String(255), nullable=True)
    data_type = Column(String(8), nullable=True)

