from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from base import Base
 
 
class Playlist(Base):
    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True)
    list_type    = Column(String(32),nullable=True)
    name         = Column(String(50),nullable=True)

    def __repr__(self):
        return f'<Playlist({self.id}: {self.list_type} name={self.name}>'
