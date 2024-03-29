from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from base import Base


class Market(Base):
    __tablename__ = "markets"
    id = Column(Integer, primary_key=True)

    session_id = Column(Integer, ForeignKey("market_sessions.id"))   # many-many

    mkt_type = Column(String(12), nullable=True)
    symbol = Column(String(12), nullable=True)
    ts_symbol = Column(String(12), nullable=True)
    ts_status = Column(String(12), nullable=True)

    name = Column(String(32), nullable=True)
    group_1 = Column(String(32), nullable=True)
    value_1_tick = Column(Numeric(10, 4))
    ticks_per_point = Column(Numeric(8, 3))
    margin_init = Column(Numeric(8, 2))
    margin_maint = Column(Numeric(8, 2))
    margin_day = Column(Numeric(8, 2))

    # xact costs
    comm_entry_dol = Column(Numeric(4, 2))
    comm_exit_dol = Column(Numeric(4, 2))
    slippage_entry_tick = Column(Numeric(4, 2))
    slippage_exit_tick = Column(Numeric(6, 4))

    prototypes = relationship("Prototype", backref="market", lazy="dynamic")
    #candidates = relationship("Candidate", backref="market", lazy="dynamic")
    # strategies = relationship("Strategy", backref='market', lazy='dynamic')

    def __repr__(self):
        return "<Market(name='%s', symbol='%s', group='%s')>" % (
            self.name,
            self.ts_symbol,
            self.group_1,
        )

    def slippage_dol(self):
        return (self.slippage_entry_tick+self.slippage_exit_tick)*self.value_1_tick

    def commission_dol(self):
        return self.comm_entry_dol + self.comm_exit_dol

    def total_cost(self):
        return self.slippage_dol + self.commission_dol
