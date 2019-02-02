from sqlalchemy import Column, Integer, String, Numeric
from base import Base


class Poi(Base):
    __tablename__ = "pois"
    id = Column(Integer, primary_key=True)

    poi_type = Column(String(12), nullable=True)
    long_logic = Column(String(50), nullable=True)
    short_logic = Column(String(50), nullable=True)
    common_logic = Column(String(255), nullable=True)
    long_params = Column(String(32), nullable=True)
    short_params = Column(String(32), nullable=True)
    vars = Column(String(32), nullable=True)
    status = Column(String(12), nullable=True)

    def __repr__(self):
        return f"<POI({self.id}: long={self.long_logic}  short={self.short_logic}>"
