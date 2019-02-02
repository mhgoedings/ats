from base import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    Boolean,
    Numeric,
    DateTime,
)
from sqlalchemy.orm import relationship


class Prototype(Base):
    __tablename__ = "prototypes"
    id = Column(Integer, primary_key=True)

    market_id = Column(Integer, ForeignKey("markets.id"))
    market_session_id = Column(Integer, ForeignKey("market_sessions.id"))

    template_version = Column(String(32), nullable=True)
    jcl_version = Column(String(32), nullable=True)

    data_set = Column(Integer)
    data_block = Column(Integer)

    symbol = Column(String(12))
    chart_series = Column(String(255))  # "1:@RTY.D:120:m,2:@RTY.D:1440:m"
    fitness_function = Column(String(12))
    max_days_back = Column(Integer)
    trades_per_day = Column(String(12), nullable=True)
    day_swing = Column(String(12), nullable=True)

    prestart_dt = Column(Date)
    start_dt = Column(Date)
    end_dt = Column(Date)
    bt_start_dt = Column(Date)
    bt_end_dt = Column(Date)

    in_sample_file = Column(String(128), nullable=True)
    out_of_sample_file = Column(String(128), nullable=True)

    status = Column(String(12), nullable=True)
    status_state = Column(String(12), nullable=True)

    start_run = Column(DateTime, nullable=True)
    end_run = Column(DateTime, nullable=True)

    run_rank = Column(Integer, default=10)

    # def area(self):
    # return self.rectangle_storage.width * self.rectangle_storage.height

    candidates = relationship("Candidate", backref="prototype", lazy="dynamic")
    parameters = relationship("PrototypeParameter", backref="prototype", lazy="dynamic")
