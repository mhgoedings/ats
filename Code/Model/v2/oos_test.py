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
    max_dd = Column(Numeric(8,2),nullable=True)             # maximum drawdown
    avg_trade = Column(Numeric(8,4),nullable=True)
    profit_factor = Column(Numeric(8,4),nullable=True)
    mae = Column(Numeric(8,2),nullable=True)                # maximum adverse excursion
    mfe = Column(Numeric(8,2),nullable=True)                # maximum favorable excursion

    ## TradeStation Performance Report
    TotalNetProfit = Column(Numeric(12,4),nullable=True)
    AvgTradeNetProfit = Column(Numeric(12,4),nullable=True)
    ProfitFactor = Column(Numeric(12,4),nullable=True)
    TotalNumberofTrades = Column(Numeric(12,4),nullable=True)
    PercentProfitable = Column(Numeric(12,4),nullable=True)
    AvgWinningTrade = Column(Numeric(12,4),nullable=True)
    AvgLosingTrade = Column(Numeric(12,4),nullable=True)
    RatioAvgWinAvgLoss = Column(Numeric(12,4),nullable=True)
    SharpeRatio = Column(Numeric(12,4),nullable=True)
    
    pcnt_max_dd = Column(Numeric(8,4),nullable=True)
    pcnt_return = Column(Numeric(8,4),nullable=True)
    pcnt_wins = Column(Numeric(8,4),nullable=True)

    status = Column(String(12),nullable=True)
    status_state = Column(String(12),nullable=True)

    start_run = Column(DateTime,nullable=True)
    end_run = Column(DateTime,nullable=True)

