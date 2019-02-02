from base import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
 
 
class TradeSession(Base):
    __tablename__ = 'trade_sessions'
    id = Column(Integer, primary_key=True)
    session_start = Column(Integer)
    session_end = Column(Integer)

    #prototypes = relationship("Prototype", backref='trade_session', lazy='dynamic')
    #strategies = relationship("Strategy", backref='trade_session', lazy='dynamic')

