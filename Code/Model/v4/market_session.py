from base import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class MarketSession(Base):
    __tablename__ = "market_sessions"
    id = Column(Integer, primary_key=True)

    session_start = Column(Integer)
    session_end = Column(Integer)

    prototypes = relationship("Prototype", backref="market_session", lazy="dynamic")
    markets = relationship("Market", backref="market_session", lazy="dynamic")
    # strategies = relationship("Strategy", backref='market_session', lazy='dynamic')
