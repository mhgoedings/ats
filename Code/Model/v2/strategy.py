from base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, Numeric, DateTime, Text
#from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import relationship

class Strategy(Base):
    __tablename__ = 'strategies'
    id = Column(Integer, primary_key=True)
    proto_id = Column(Integer, ForeignKey('prototypes.id'))
    cand_id = Column(Integer, ForeignKey('candidates.id'))
    sec_id = Column(Integer, ForeignKey('markets.id'))

    symbol = Column(String(12))

    robust_level = Column(Integer,nullable=True)

    strategy_file = Column(String(250),nullable=False)
    strategy_oos_file = Column(String(250),nullable=False)

    #chart setup
    session_id = Column(Integer,ForeignKey('sessions.id'))
    timeframe_1 = Column(Integer)
    timeframe_1_unit = Column(String(10))
    timeframe_2 = Column(Integer,nullable=True)
    timeframe_2_unit = Column(String(10),nullable=True)
    max_days_back = Column(Integer)
    oos_start_dt = Column(Date)
    oos_end_dt = Column(Date)
    use_second_data = Column(Boolean)

    #strategy 
    lsb = Column(Integer)
    trades_per_day = Column(Integer)
    day_swing = Column(Integer)
    poi_switch = Column(Integer)
    poi_n1 = Column(Integer)
    natr = Column(Integer)
    fract = Column(Numeric(5,2))
    filter_1_switch = Column(Integer,nullable=True)
    filter_1_n1 = Column(Integer,nullable=True)
    filter_1_n2 = Column(Integer,nullable=True)
    filter_2_switch = Column(Integer,nullable=True)
    filter_2_n1 = Column(Integer,nullable=True)
    filter_2_n2 = Column(Integer,nullable=True)
    t_segment = Column(Integer)

    ## exits
    sl_switch = Column(Integer)
    stop_loss = Column(Numeric(12,5))
    pt_switch = Column(Integer)
    profit_target = Column(Numeric(12,5))

    #optimization
    fitness_function = Column(String(12))
    input_vars = Column(String(120),nullable=True)
    reopt_period_days = Column(Integer,nullable=True)
    next_reopt_dt = Column(Date,nullable=True)
    next_reopt_start_dt = Column(Date,nullable=True)
    next_reopt_end_dt = Column(Date,nullable=True)
    oos_param_history = Column(Text,nullable=True)

    ## market internals
    mi_id = Column(Integer, ForeignKey('market_internals.id'))
    mi_n1 = Column(Integer, nullable=True)
    mi_n2 = Column(Integer, nullable=True)

    ## xact costs
    comm_entry_dol = Column(Numeric(8,4),nullable=True)
    comm_exit_dol = Column(Numeric(8,4),nullable=True)
    slippage_entry_dol = Column(Numeric(8,4),nullable=True)
    slippage_exit_dol = Column(Numeric(8,4),nullable=True)

    status = Column(String(12),nullable=True)
    status_state = Column(String(12),nullable=True)

    start_run = Column(DateTime,nullable=True)
    end_run = Column(DateTime,nullable=True)

    oos_tests = relationship("OosTest", backref='strategy', lazy='dynamic')
