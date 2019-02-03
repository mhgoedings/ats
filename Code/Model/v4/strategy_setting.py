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


class StrategySetting(Base):
    __tablename__ = "strategy_settings"
    id = Column(Integer, primary_key=True)

    strategy_id = Column(Integer, ForeignKey("strategies.id"))

    name      = Column(String(32), nullable=True)
    value     = Column(String(255), nullable=True)
    data_type = Column(String(8), nullable=True)

    #start_dt  = Column(Date)
    #end_dt    = Column(Date)

    #status    = Column(String(12), nullable=True)


##     status            
##     ------------      
##     backtest          
##     current           
##     current           
##     pending           
