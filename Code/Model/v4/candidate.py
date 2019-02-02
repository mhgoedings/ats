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


class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True)

    proto_id = Column(Integer, ForeignKey("prototypes.id"))

    test_id = Column(Integer)
    template_version = Column(String(32), nullable=True)
    jcl_version = Column(String(32), nullable=True)

    strategy_file = Column(String(250), nullable=True)
    strategy_name = Column(String(250), nullable=True)

    wfa_file = Column(String(250), nullable=True)

    number_of_trades = Column(Integer, nullable=True)
    opt_iterations   = Column(Integer, nullable=True)
    reopt_days       = Column(Integer, nullable=True)
    reopt_bars       = Column(Integer, nullable=True)
    reopt_param_names= Column(String(250), nullable=True)
    reopt_string     = Column(String(250), nullable=True)

    bt_start_dt = Column(Date)
    bt_end_dt = Column(Date)

    robust_level = Column(Integer, default=10)

    status = Column(String(12), nullable=True)
    status_state = Column(String(12), nullable=True)

    start_run = Column(DateTime, nullable=True)
    end_run = Column(DateTime, nullable=True)

    run_rank = Column(Integer, default=10)

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

    settings = relationship("CandidateSetting", backref="candidate", lazy="dynamic")
    parameters = relationship("CandidateParameter", backref="candidate", lazy="dynamic")
