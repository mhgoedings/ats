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
    Text,
)
from sqlalchemy.orm import relationship


class Strategy(Base):
    __tablename__ = "strategies"
    id = Column(Integer, primary_key=True)

    cand_id = Column(Integer, ForeignKey("candidates.id"))
    market_id = Column(Integer, ForeignKey("markets.id"))
    market_session_id = Column(Integer, ForeignKey("market_sessions.id"))

    # descriptive
    strat_type = Column(String(12))
    lsb = Column(Integer)
    trades_per_day = Column(Integer)
    day_swing = Column(Integer)

    # chart setup
    symbol = Column(String(12))
    chart_series = Column(String(255))  # "1:@RTY.D:120:m,2:@RTY.D:1440:m"
    max_days_back = Column(Integer)
    fitness_function = Column(String(12))
    oos_start_dt = Column(Date)
    oos_end_dt = Column(Date)

    robust_level = Column(Integer, default=10)

    strategy_template_v  = Column(String(32), nullable=True)
    oos_curve_template_v = Column(String(32), nullable=True)
    jcl_version          = Column(String(32), nullable=True)

    strategy_name = Column(String(250), nullable=True)
    strategy_file = Column(String(250), nullable=True)

    # out-of-sample curve
    oos_param_history = Column(Text,nullable=True)
    strategy_oos_file = Column(String(250),nullable=True)
    ## xact costs
    comm_entry_dol = Column(Numeric(8,4),nullable=True)
    comm_exit_dol = Column(Numeric(8,4),nullable=True)
    slippage_entry_dol = Column(Numeric(8,4),nullable=True)
    slippage_exit_dol = Column(Numeric(8,4),nullable=True)


    reopt_iterations   = Column(Integer, nullable=True)
    reopt_days       = Column(Integer, nullable=True)
    reopt_bars       = Column(Integer, nullable=True)
    reopt_param_names= Column(String(250), nullable=True)
    reopt_string     = Column(String(250), nullable=True)

    status = Column(String(12), nullable=True)
    status_state = Column(String(12), nullable=True)

    start_run = Column(DateTime, nullable=True)
    end_run = Column(DateTime, nullable=True)


    def __str__(self):
        return f"""
           id               = {self.id}
           cand_id          = {self.cand_id}
           robust_level     = {self.robust_level}

           status           = {self.status}
           status_state     = {self.status_state}

           start_run        = {self.start_run}
           end_run          = {self.end_run}"""

settings = relationship("StrategySetting", backref="strategy", lazy="dynamic")
oos_tests = relationship("OosTest", backref='strategy', lazy='dynamic')

