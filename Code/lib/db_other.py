import sys, os, re
from loguru import logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/Model/v4")
sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")

from strategy_setting import StrategySetting
from strategy_reopt_parameter import StrategyReoptParameter
from strategy_oos_period import StrategyOosPeriod
from strategy_oos_setting import StrategyOosSetting
from base import Base, Session


def clear_strategy_settings(dbh, strat_id):
    dbh.query(StrategySetting).filter(StrategySetting.strategy_id == strat_id).delete()
    dbh.commit()
    dbh.flush()


def clear_strategy_parameters(dbh, strat_id):
    dbh.query(StrategyReoptParameter).filter(
        StrategyReoptParameter.strategy_id == strat_id
    ).delete()
    dbh.commit()
    dbh.flush()


def clear_strategy_oos_periods(dbh, strat_id):
    dbh.query(StrategyOosPeriod).filter(
        StrategyOosPeriod.strategy_id == strat_id
    ).delete()
    dbh.commit()
    dbh.flush()


def clear_strategy_oos_settings(dbh, strat_id):
    dbh.query(StrategyOosSetting).filter(
        StrategyOosSetting.strategy_id == strat_id
    ).delete()
    dbh.commit()
    dbh.flush()
