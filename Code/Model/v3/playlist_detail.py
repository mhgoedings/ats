from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from base import Base
 
 
class PlaylistDetail(Base):
    __tablename__ = 'playlist_details'
    id      = Column(Integer, primary_key=True)
    list_id = Column(Integer,nullable=False)
    item_id = Column(Integer,nullable=False)

