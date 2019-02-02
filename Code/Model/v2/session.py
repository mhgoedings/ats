from base import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
 
 
class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    session_start = Column(Integer)
    session_end = Column(Integer)

    prototypes = relationship("Prototype", backref='session', lazy='dynamic')
    strategies = relationship("Strategy", backref='session', lazy='dynamic')

