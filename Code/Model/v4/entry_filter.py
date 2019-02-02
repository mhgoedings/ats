from sqlalchemy import Column, Integer, String
from base import Base


class EntryFilter(Base):
    __tablename__ = "entry_filters"
    id = Column(Integer, primary_key=True)

    filter_type = Column(String(32), nullable=True)
    long_logic = Column(String(256), nullable=True)
    short_logic = Column(String(256), nullable=True)
    common_logic = Column(String(256), nullable=True)
    long_params = Column(String(32), nullable=True)
    short_params = Column(String(32), nullable=True)
    vars = Column(String(32), nullable=True)
    status = Column(String(12), nullable=True)

    def __repr__(self):
        return f"<EntryFilter({self.id}: {self.filter_type} long={self.long_logic}  short={self.short_logic}>"
