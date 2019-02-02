from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date, DateTime
from sqlalchemy.orm import relationship
from base import Base
 
 
class OosTest(Base):
    __tablename__ = 'oos_tests'
    id = Column(Integer, primary_key=True)
    strat_id = Column(Integer, ForeignKey('strategies.id'))
    sec_id = Column(Integer, ForeignKey('markets.id'))
    symbol = Column(String(12),nullable=True)
    test_type  = Column(String(12),nullable=True)

    oos_file = Column(String(250),nullable=True)
    oos_start_dt = Column(Date,nullable=True)
    oos_end_dt = Column(Date,nullable=True)
    
    ## exits
    stop_loss = Column(Numeric(8,2),nullable=True)
    profit_target = Column(Numeric(8,2),nullable=True)

    ## market internals
    mi_id = Column(Integer, ForeignKey('market_internals.id'))
    mi_n1 = Column(Integer, nullable=True)
    mi_n2 = Column(Integer, nullable=True)

    ## xact costs
    comm_entry_dol = Column(Numeric(8,4),nullable=True) 
    comm_exit_dol = Column(Numeric(8,4),nullable=True) 
    slippage_entry_dol = Column(Numeric(8,4),nullable=True)
    slippage_exit_dol = Column(Numeric(8,4),nullable=True)

    ## performance
    net_profit = Column(Numeric(8,2),nullable=True)
    avg_trade = Column(Numeric(8,4),nullable=True)
    profit_factor = Column(Numeric(8,4),nullable=True)
    mae = Column(Numeric(8,2),nullable=True)                # maximum adverse excursion
    mfe = Column(Numeric(8,2),nullable=True)                # maximum favorable excursion

    ## TradeStation Performance Report
    initial_capital = Column(Numeric(12,4),nullable=True)
    commission = Column(Numeric(12,4),nullable=True)
    slippage = Column(Numeric(12,4),nullable=True)
    win_streak = Column(Integer,nullable=True)
    lose_streak = Column(Integer,nullable=True)
    avg_bars_in = Column(Integer,nullable=True)
    avg_bars_in_winner = Column(Integer,nullable=True)
    avg_bars_in_loser = Column(Integer,nullable=True)
    avg_bars_in_even = Column(Integer,nullable=True)

    max_contracts_held = Column(Integer,nullable=True)
    total_contracts_held = Column(Integer,nullable=True)
    max_run_up = Column(Numeric(12,2),nullable=True)

    test_period_str = Column(String(50),nullable=True)
    time_in_str = Column(String(50),nullable=True)
    
    required_account = Column(Numeric(12,2),nullable=True)
    rtn_on_init_cap = Column(Numeric(8,4),nullable=True)
    annual_ror = Column(Numeric(8,4),nullable=True)
    buy_hold_ror = Column(Numeric(8,4),nullable=True)
    rtn_on_account = Column(Numeric(8,4),nullable=True)
    avg_monthly_rtn = Column(Numeric(8,4),nullable=True)
    stdev_monthly_rtn = Column(Numeric(8,4),nullable=True)
    rtn_retracement_ratio = Column(Numeric(8,4),nullable=True)

    trade_count = Column(Integer,nullable=True)
    win_count = Column(Integer,nullable=True)
    lose_count = Column(Integer,nullable=True)
    even_count = Column(Integer,nullable=True)
    percent_winners = Column(Numeric(6,2),nullable=True)
    avg_winner = Column(Numeric(12,4),nullable=True)
    avg_loser = Column(Numeric(12,4),nullable=True)
    largest_winner = Column(Numeric(8,2),nullable=True)
    largest_loser = Column(Numeric(8,2),nullable=True)

    drawdown_max = Column(Numeric(12,2),nullable=True)             # maximum drawdown
    drawdown_intra = Column(Numeric(12,2),nullable=True)
    drawdown_day = Column(Numeric(12,2),nullable=True)

    sharpe_ratio = Column(Numeric(12,4),nullable=True)
    rina = Column(Numeric(12,4),nullable=True)
    
    pcnt_max_dd = Column(Numeric(8,4),nullable=True)
    pcnt_return = Column(Numeric(8,4),nullable=True)
    pcnt_wins = Column(Numeric(8,4),nullable=True)

    status = Column(String(12),nullable=True)
    status_state = Column(String(12),nullable=True)

    start_run = Column(DateTime,nullable=True)
    end_run = Column(DateTime,nullable=True)

