from base import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, Numeric, DateTime
from sqlalchemy.orm import relationship

class CandidateTmp(Base):
    __tablename__ = 'candidate_tmps'
    id = Column(Integer, primary_key=True)
    test_id = Column(Integer)
    proto_id = Column(Integer)
    sec_id = Column(Integer)

    symbol = Column(String(12))

    template_file = Column(String(250),nullable=False)
    strategy_name = Column(String(250),nullable=False)
    session_id = Column(Integer)
    timeframe_1 = Column(Integer)
    timeframe_1_unit = Column(String(10))
    timeframe_2 = Column(Integer,nullable=True)
    timeframe_2_unit = Column(String(10),nullable=True)
    fitness_function = Column(String(12))
    max_days_back = Column(Integer)
    start_dt = Column(Date)
    end_dt = Column(Date)
    use_second_data = Column(Boolean)

    lsb = Column(Integer)
    trades_per_day = Column(Integer)
    day_swing = Column(Integer)
    poi_switch = Column(Integer)
    poi_n1 = Column(Integer)
    natr = Column(Integer)
    fract = Column(Numeric(5,2))
    t_segment = Column(Integer)

    filter_1_switch = Column(Integer,nullable=True)
    filter_1_n1 = Column(Integer,nullable=True)
    filter_1_n2 = Column(Integer,nullable=True)
    filter_2_switch = Column(Integer,nullable=True)
    filter_2_n1 = Column(Integer,nullable=True)
    filter_2_n2 = Column(Integer,nullable=True)

    sl_switch = Column(Integer)
    stop_loss = Column(Numeric(12,5))
    pt_switch = Column(Integer)
    profit_target = Column(Numeric(12,5))

    bt_start_dt = Column(Date)
    bt_end_dt = Column(Date)
 
    input_vars = Column(String(256),nullable=True)
    optimization_string = Column(String(120),nullable=True)

    status = Column(String(12),nullable=True)
    status_state = Column(String(12),nullable=True)

    start_run = Column(DateTime,nullable=True)
    end_run = Column(DateTime,nullable=True)

