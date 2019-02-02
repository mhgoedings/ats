from base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, Numeric, DateTime
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import relationship

class OosTrade(Base):
    __tablename__ = 'oos_trades'
    id = Column(Integer, primary_key=True)
    oos_id = Column(Integer, ForeignKey('oos_reports.id'))

    #trades
    dt = Column(Date)

    run_ts = Column(DateTime,nullable=True)

