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


class CandidateConfig(Base):
    __tablename__ = "candidate_configs"
    id = Column(Integer, primary_key=True)
    test_id = Column(Integer)
    proto_id = Column(Integer, ForeignKey("proto_configs.id"))
    # sec_id = Column(Integer, ForeignKey('markets.id'))
    # session_id = Column(Integer,ForeignKey('sessions.id'))

    template_version = Column(String(12), nullable=True)
    jcl_version = Column(String(12), nullable=True)

    # symbol = Column(String(12))
    # chart_series = Column(String(255))     # "1:@RTY.D:120:m,2:@RTY.D:1440:m"
    # fitness_function = Column(String(12))
    # max_bars_back = Column(Integer)
    # trades_per_day = Column(Integer)
    # day_swing = Column(Integer)

    # start_dt = Column(Date)
    # end_dt = Column(Date)
    # bt_start_dt = Column(Date)
    # bt_end_dt = Column(Date)

    strategy_file = Column(String(250), nullable=True)
    strategy_name = Column(String(250), nullable=True)

    status = Column(String(12), nullable=True)
    status_state = Column(String(12), nullable=True)

    start_run = Column(DateTime, nullable=True)
    end_run = Column(DateTime, nullable=True)

    def __str__(self):
        return f"""
           id               = {self.id}
           test_id          = {self.test_id}
           proto_id         = {self.proto_id}
           strategy_file    = {self.strategy_file}
           strategy_name    = {self.strategy_name}
           status           = {self.status}
           status_state     = {self.status_state}
           start_run        = {self.start_run}
           end_run          = {self.end_run}"""
        # sec_id           = {self.sec_id}
        # session_id       = {self.session_id}
        # template_version = {self.template_version}
        # symbol           = {self.symbol}
        # chart_series     = {self.chart_series}

    candidate_settings = relationship(
        "CandidateSetting", backref="candidate_config", lazy="dynamic"
    )
    candidate_parameters = relationship(
        "CandidateParameter", backref="candidate_config", lazy="dynamic"
    )
