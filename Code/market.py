from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from base import Base
 
 
class Market(Base):
    __tablename__ = 'markets'
    id = Column(Integer, primary_key=True)
    symbol = Column(String(12),nullable=True)
    ts_symbol = Column(String(12),nullable=True)
    name = Column(String(32),nullable=True)
    group_1 = Column(String(32),nullable=True)
    value_1_tick = Column(Numeric(10,4))
    ticks_per_point = Column(Numeric(8,3))
    margin_init = Column(Numeric(8,2))
    margin_maint = Column(Numeric(8,2))
    margin_day = Column(Numeric(8,2))
    default_session = Column(Integer)

    #prototypes = relationship("Prototype", backref='mkt_future', lazy='dynamic')
    #candidates = relationship("Candidate", backref='mkt_future', lazy='dynamic')
    #strategies = relationship("Strategy", backref='mkt_future', lazy='dynamic')
