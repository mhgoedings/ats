import sys, os, re
from loguru import logger

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/Model/v4")
sys.path.append("C:\\ZTS\\Dropbox\\Business\\ats\\Code\\Model\\v4")

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
sys.path.append("C:\\ZTS\\Dropbox\\Business\\ats\\Code\\lib")


from prototype import Prototype
from prototype_parameter import PrototypeParameter
from candidate import Candidate
from candidate_setting import CandidateSetting
from candidate_parameter import CandidateParameter
from strategy import Strategy
from strategy_setting import StrategySetting
from strategy_reopt_parameter import StrategyReoptParameter
from logic_repo import LogicRepo
from market import Market
from market_session import MarketSession
from parameter_definition import ParameterDefinition
from parameter_preset import ParameterPreset

from base import Base, Session


def connectDB():
    logger.debug(f"entered")
    db = Session()
    db_url = os.environ["DB_HEROKU"]
    db_url = "postgres://ghvnmtixgtixhb:960715ae6d2d874bfa40fc66c99b4fb2cce1e452cc804f1dff3c5c1f7b722e4d@ec2-107-22-162-8.compute-1.amazonaws.com:5432/delmad8ora7a1v"

    engine = create_engine(db_url)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.autoflush = True
    return session


def nextPrototypeId(dbh):
    logger.debug(f"entered")
    try:
        id = (
            dbh.query(Prototype)
            .filter(
                and_(Prototype.status == "new", Prototype.status_state == "pending")
            )
            .order_by(Prototype.id)
            .all()[0]
            .id
        )
    except:
        id = None

    return id


def nextCandidateId(dbh):
    logger.debug(f"entered")
    try:
        id = (
            dbh.query(Candidate)
            .filter(
                and_(Candidate.status == "new", Candidate.status_state == "pending")
            )
            .order_by(Candidate.run_rank.desc())
            .all()[0]
            .id
        )
    except:
        id = None
    return id


# records = DBSession.query(GeneralLedger, ConsolidatedLedger)
#       .join(ConsolidatedLedger, GeneralLedger.invoiceId == ConsolidatedLedger.invoiceId).all()


def nextStrategyId(dbh,status='new',status_state='pending'):
    logger.debug(f"entered")
    try:
        id = (
            dbh.query(Strategy)
            .filter(and_(Strategy.status == status, Strategy.status_state == status_state))
            .all()[0]
            .id
        )
    except:
        id = None
    return id


def queryPrototype(dbh, id):
    logger.debug(f"id = {id}")
    return dbh.query(Prototype).filter(Prototype.id == id).one_or_none()


def queryStrategy(dbh, id):
    logger.debug(f"id = {id}")
    return dbh.query(Strategy).filter(Strategy.id == id).one_or_none()

def queryCandidate(dbh, id):
    logger.debug(f"id = {id}")
    return dbh.query(Candidate).filter(Candidate.id == id).one_or_none()


'''
def queryCandidate(dbh, id):
    logger.debug(f"id = {id}")
    return (
        dbh.query(Candidate)
        .filter(
            and_(
                Candidate.id == id,
                Candidate.status == "new",
                Candidate.status_state == "pending",
            )
        )
        .one_or_none()
    )
'''


def queryPrototypeParams(dbh, id):
    logger.debug(f"id = {id}")
    return dbh.query(PrototypeParameter).filter(PrototypeParameter.proto_id == id).all()


def queryCandidateSettings(dbh, id):
    logger.debug(f"id = {id}")
    return dbh.query(CandidateSetting).filter(CandidateSetting.candidate_id == id).all()


def queryCandidateParams(dbh, id):
    logger.debug(f"id = {id}")
    return (
        dbh.query(CandidateParameter)
        .filter(CandidateParameter.candidate_id == id)
        .order_by(CandidateParameter.id)
        .all()
    )


def queryStrategySettings(dbh, id):
    logger.debug(f"id = {id}")
    return dbh.query(StrategySetting).filter(StrategySetting.strategy_id == id).all()


def queryStrategyParams(dbh, id):
    logger.debug(f"id = {id}")
    return (
        dbh.query(StrategyReoptParameter)
        .filter(StrategyReoptParameter.strategy_id == id)
        .all()
    )


def queryParamDef(dbh, param):
    logger.debug(f"param = {param}")
    return (
        dbh.query(ParameterDefinition)
        .filter(ParameterDefinition.name == param)
        .one_or_none()
    )


def queryLogic(dbh, logic_type, id):
    logger.debug(f"logic_type = {logic_type}, id = {id}")
    return (
        dbh.query(LogicRepo)
        .filter(and_(LogicRepo.logic_id == id, LogicRepo.logic_type == logic_type))
        .one_or_none()
    )


def queryParamPreset(dbh, preset, param):
    logger.debug(f"preset = {preset}, param = {param}")
    return (
        dbh.query(ParameterPreset)
        .filter(and_(ParameterPreset.name == preset, ParameterPreset.param == param))
        .one_or_none()
    )
    pass


def queryEntryFilter(dbh, id):
    # logger.debug(f"id = {id}")
    return (
        dbh.query(LogicRepo)
        .filter(and_(LogicRepo.logic_id == id, LogicRepo.logic_type == "filter"))
        .one_or_none()
    )


def queryPoi(dbh, id):
    logger.debug(f"id = {id}")
    return (
        dbh.query(LogicRepo)
        .filter(and_(LogicRepo.logic_id == id, LogicRepo.logic_type == "poi"))
        .one_or_none()
    )


def querySession(dbh, id):
    logger.debug(f"id = {id}")
    return dbh.query(MarketSession).filter(MarketSession.id == id).one_or_none()


def queryDefaultSessionId(dbh, symbol):
    logger.debug(f"symbol = {symbol}")
    return dbh.query(Market).filter(Market.ts_symbol == symbol).one_or_none().session_id


def querySecId(dbh, symbol):
    logger.debug(f"symbol = {symbol}")
    return dbh.query(Market).filter(Market.ts_symbol == symbol).one_or_none().id


def queryCosts(dbh, symbol):
    logger.debug(f"symbol = {symbol}")
    data = dbh.query(Market).filter(Market.ts_symbol == symbol).one_or_none()
    comm = data.comm_entry_dol + data.comm_exit_dol
    slip = data.slippage_entry_tick * data.value_1_tick
    slip += data.slippage_exit_tick * data.value_1_tick
    return slip, comm


def queryXactCosts(dbh, symbol=None, market_id=None):
    logger.debug(f"symbol = {symbol},  market_id = {market_id }")
    if not symbol and not market_id:
        raise
    if not market_id:
        data = dbh.query(Market).filter(Market.ts_symbol == symbol).one_or_none()
    else:
        data = dbh.query(Market).filter(Market.id == market_id).one_or_none()

    if data is None:
        return (0, 0, 0, 0)

    comm_entry_dol = (
        float(data.comm_entry_dol) if is_float(data.comm_entry_dol) else None
    )
    comm_exit_dol = float(data.comm_exit_dol) if is_float(data.comm_exit_dol) else None
    slippage_entry_dol = (
        float(data.slippage_entry_tick * data.value_1_tick)
        if is_float(data.slippage_entry_tick) and is_float(data.value_1_tick)
        else None
    )
    slippage_exit_dol = (
        float(data.slippage_exit_tick * data.value_1_tick)
        if is_float(data.slippage_exit_tick) and is_float(data.value_1_tick)
        else None
    )

    return (comm_entry_dol, comm_exit_dol, slippage_entry_dol, slippage_exit_dol)


if __name__ == "__main__":

    import pprint

    dbh = connectDB()
    print(querySession(dbh, 8).session_start)
    print(querySession(dbh, 8).session_end)

    print(queryDefaultSessionId(dbh, "@ES.D"))
    print(queryDefaultSessionId(dbh, "@CL"))

    print(querySecId(dbh, "@ES.D"))
    print(querySecId(dbh, "@CL"))

    print(nextStrategyId(dbh))
