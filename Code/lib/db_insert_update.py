import sys, os, re
from loguru import logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/Model/v4")
sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")

from prototype import Prototype
from candidate import Candidate
from prototype_parameter import PrototypeParameter
from strategy import Strategy
from strategy_setting import StrategySetting
from strategy_reopt_parameter import StrategyReoptParameter
from strategy_oos_period import StrategyOosPeriod
from strategy_oos_setting import StrategyOosSetting

from base import Base, Session


def connectDB():
    db = Session()
    db_url = os.environ["DB_HEROKU"]

    engine = create_engine(db_url)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.autoflush = True

    return session


def dbUpdatePrototype(dbh, id, updates):
    logger.debug(f"id = {id},  updates = {updates}")
    try:
        dbh.query(Prototype).filter(Prototype.id == id).update(updates)
        dbh.commit()
    except:
        dbh.rollback()
        raise


def dbUpdateCandidate(dbh, id, updates):
    logger.debug(f"id = {id},  updates = {updates}")
    try:
        dbh.query(Candidate).filter(Candidate.id == id).update(updates)
        dbh.commit()
    except:
        dbh.rollback()
        raise


def dbUpdateStrategy(dbh, id, updates):
    logger.debug(f"id = {id},  updates = {updates}")
    try:
        dbh.query(Strategy).filter(Strategy.id == id).update(updates)
        dbh.commit()
        logger.debug("commiteed")
    except:
        dbh.rollback()
        raise


def dbInsertStrategySetting(dbh, strat_id, setting):
    logger.debug(f"strat_id = {strat_id},  setting = {setting}")
    new_rec = StrategySetting(
        strategy_id=strat_id,
        # start_dt    = setting.start_dt,
        # end_dt      = setting.end_dt,
        name=setting.name,
        value=setting.value,
        data_type=setting.data_type,
        # status      = setting.status
    )

    dbh.add(new_rec)
    dbh.commit()
    dbh.flush()


def dbInsertStrategyOosSetting(dbh, strat_id, setting):
    new_rec = StrategyOosSetting(
        strategy_id = strat_id,
        period_id   = setting.period_id,
        name        = setting.name,
        value       = setting.value,
        data_type   = setting.data_type,
    )
    dbh.add(new_rec)
    dbh.commit()
    dbh.flush()


def dbInsertStrategyOosPeriod(dbh, strat_id, start_dt, end_dt):
    new_rec = StrategyOosPeriod(strategy_id=strat_id, start_dt=start_dt, end_dt=end_dt)
    dbh.add(new_rec)
    dbh.commit()
    dbh.flush()
    return new_rec.id


def dbInsertStrategyParams(dbh, strat_id, param):
    logger.debug(f"strat_id = {strat_id},  param = {param}")
    new_rec = StrategyReoptParameter(
        strategy_id=strat_id,
        name=param.name,
        value=param.value,
        data_type=param.data_type,
        input_type=param.input_type,
    )

    dbh.add(new_rec)
    dbh.commit()
    dbh.flush()
