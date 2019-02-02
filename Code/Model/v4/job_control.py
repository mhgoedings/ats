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
from sqlalchemy.sql import func


class JobControl(Base):
    __tablename__ = "job_controls"
    id = Column(Integer, primary_key=True)

    run_status = Column(String(32), nullable=True)
    app_name = Column(String(32), nullable=True)
    host_name = Column(String(32), nullable=True)
    session_max_runs = Column(Integer, nullable=True)
    session_max_mins = Column(Integer, nullable=True)
    last_update = Column(DateTime(timezone=True), onupdate=func.now())
