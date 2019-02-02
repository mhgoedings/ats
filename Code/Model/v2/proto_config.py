from sqlalchemy import Column, String, Integer, Date, Boolean, DateTime
from base import Base


class ProtoConfig(Base):
    __tablename__ = 'proto_configs'
    id = Column(Integer, primary_key=True)
    #session_id = Column(Integer, ForeignKey('sessions.id'))
    session_id = Column(Integer)

    #template = Column(String(250), nullable=False)
    data_set = Column(Integer)
    data_block =Column(Integer) 
    cand_prefix = Column(String(32))
    symbol = Column(String(12))
    use_second_data = Column(Boolean)
    timeframe_1 = Column(Integer)
    timeframe_1_unit = Column(String(10))
    timeframe_2 = Column(Integer,nullable=True)
    timeframe_2_unit = Column(String(10),nullable=True)
    fitness_function = Column(String(12))
    max_days_back = Column(Integer)
    #prestart_dt = Column(Date)
    #start_dt = Column(Date)
    #end_dt = Column(Date)
    lsb = Column(String(12),nullable=True)
    trades_per_day = Column(String(12),nullable=True)
    day_swing = Column(String(12),nullable=True)
    poi_switch = Column(String(12),nullable=True)
    poi_n1 = Column(String(12),nullable=True)
    natr = Column(String(12),nullable=True)
    fract = Column(String(12),nullable=True)
    filter_1_switch = Column(String(12),nullable=True)
    filter_1_n1 = Column(String(12),nullable=True)
    filter_1_n2 = Column(String(12),nullable=True)
    filter_2_switch = Column(String(12),nullable=True)
    filter_2_n1 = Column(String(12),nullable=True)
    filter_2_n2 = Column(String(12),nullable=True)
    t_segment = Column(String(12),nullable=True)
    sl_switch = Column(String(12),nullable=True)
    stop_loss = Column(String(12),nullable=True)
    pt_switch = Column(String(12),nullable=True)
    profit_target = Column(String(12),nullable=True)

    bt_start_dt = Column(Date)
    bt_end_dt = Column(Date)

    #in_sample_file = Column(String(128),nullable=True)
    #out_of_sample_file = Column(String(128),nullable=True)

    status = Column(String(12),nullable=True)
    status_state = Column(String(12),nullable=True)

    start_run = Column(DateTime,nullable=True)
    end_run = Column(DateTime,nullable=True)


    def __init__(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe_1 = timeframe

