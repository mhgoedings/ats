from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from base import Base
 
 
class EfOptimization(Base):
    __tablename__ = 'ef_optimizations'
    id       = Column(Integer, primary_key=True)
    strat_id = Column(Integer, ForeignKey('strategies.id'))
    sec_id   = Column(Integer, ForeignKey('markets.id'))

    symbol = Column(String(12))

    opt_file     = Column(String(250),nullable=True)
    oos_start_dt = Column(Date,nullable=True)
    oos_end_dt   = Column(Date,nullable=True)

    ## optimization parameters
    i_switch           = Column(String(12),default="1,32,1")
    i_parameter        = Column(String(12),default="1,15,1")
    i_entry_exit_both  = Column(String(12),default="1,3,1")
    i_reset_on_day     = Column(String(12),default="0,1,1")
    i_reset_after_exit = Column(String(12),default="0,1,1")

    status       = Column(String(12),nullable=True)
    status_state = Column(String(12),nullable=True)

    start_run = Column(DateTime,nullable=True)
    end_run   = Column(DateTime,nullable=True)

    def __repr__(self):
        return f'{self.id}. {self.name}'


