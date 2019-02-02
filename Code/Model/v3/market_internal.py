from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from base import Base
 
 
class MarketInternal(Base):
    __tablename__ = 'market_internals'
    id = Column(Integer, primary_key=True)
    name = Column(String(32),nullable=True)
    src = Column(String(),nullable=True)

    ## data
    data_1_symbol    = Column(String(12),nullable=True)
    data_1_timeframe = Column(Integer,nullable=True)
    data_1_session   = Column(Integer,nullable=True)
    data_1_zone      = Column(String(12),nullable=True)

    data_2_symbol    = Column(String(12),nullable=True)
    data_2_timeframe = Column(Integer,nullable=True)
    data_2_session   = Column(Integer,nullable=True)
    data_2_zone      = Column(String(12),nullable=True)

    data_3_symbol    = Column(String(12),nullable=True)
    data_3_timeframe = Column(Integer,nullable=True)
    data_3_session   = Column(Integer,nullable=True)
    data_3_zone      = Column(String(12),nullable=True)

    data_4_symbol    = Column(String(12),nullable=True)
    data_4_timeframe = Column(Integer,nullable=True)
    data_4_session   = Column(Integer,nullable=True)
    data_4_zone      = Column(String(12),nullable=True)

    data_5_symbol    = Column(String(12),nullable=True)
    data_5_timeframe = Column(Integer,nullable=True)
    data_5_session   = Column(Integer,nullable=True)
    data_5_zone      = Column(String(12),nullable=True)

    data_6_symbol    = Column(String(12),nullable=True)
    data_6_timeframe = Column(Integer,nullable=True)
    data_6_session   = Column(Integer,nullable=True)
    data_6_zone      = Column(String(12),nullable=True)

    data_7_symbol    = Column(String(12),nullable=True)
    data_7_timeframe = Column(Integer,nullable=True)
    data_7_session   = Column(Integer,nullable=True)
    data_7_zone      = Column(String(12),nullable=True)

    def __repr__(self):
        return f'{self.id}. {self.name}'
        #return "(name='%s', symbol='%s', group='%s')>" % (self.name, self.ts_symbol, self.group_1)
