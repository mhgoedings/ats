from pathlib import Path
import pandas as pd
from loguru import logger
import sys

sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/Model/v4")
sys.path.append("/Users/szagar/ZTS/Dropbox/Business/ats/Code/lib")
from db_query import queryCandidateParams

rpt_dir = Path("/Users/szagar/ZTS/Dropbox/Business/ats/Data/Queue/WfoReports")


def parse_oos_report(fn):
    # print(fn.read_text())
    header = True
    with open(fn, "r") as text_file:
        for line in itertools.islice(text_file, 3, 14):
            if header:
                labels = line.split()
                labels[1:2] = "start_dt", "end_dt"
                labels.remove("Ratio")
                labels.remove("Avg")
                df = pd.DataFrame(columns=labels)
                list_of_lists = []
                header = False
            else:
                run, start_dt, _, end_dt, days, bars, np, dd, ddp, nt, pp, wl, at, sd, med, pf, rrr, tt, *params = (
                    line.split()
                )
                params = ",".join(params)
                """
                print(f"run        ={run}")
                print(f"start_dt   ={start_dt}")
                print(f"end_dt     ={end_dt}")
                print(f"days       ={days}")
                print(f"bars       ={bars}")
                print(f"net profit ={np}")
                print(f"max DD       ={dd}")
                print(f"max DD %       ={ddp}")
                print(f"num trades       ={nt}")
                print(f"% prof       ={pp}")
                print(f"avg w/l       ={wl}")
                print(f"avg trade       ={at}")
                print(f"std dev       ={sd}")
                print(f"median       ={med}")
                print(f"profit fact  ={pf}")
                print(f"risk-reward  ={rrr}")
                print(f"t-Test       ={tt}")
                print(f"params       ={params}")
                """
                list_of_lists.append(
                    [
                        run,
                        start_dt,
                        end_dt,
                        days,
                        bars,
                        np,
                        dd,
                        ddp,
                        nt,
                        pp,
                        wl,
                        at,
                        sd,
                        med,
                        pf,
                        rrr,
                        tt,
                        params,
                    ]
                )
    df = pd.DataFrame(list_of_lists, columns=labels)
    df.set_index("Run", inplace=True)
    return df


import itertools

# import pprint
def parse_is_report(fn):
    # print(fn.read_text())
    header = True
    with open(fn, "r") as text_file:
        for line in itertools.islice(text_file, 3, 14):
            if header:
                labels = line.split()
                labels[1:2] = "start_dt", "end_dt"
                labels.remove("Ratio")
                labels.remove("Avg")
                df = pd.DataFrame(columns=labels)
                list_of_lists = []
                header = False
            else:
                run, start_dt, _, end_dt, days, bars, np, dd, ddp, nt, pp, wl, at, sd, med, pf, rrr, tt, *params = (
                    line.split()
                )
                params = ",".join(params)
                """
                print(f"run        ={run}")
                print(f"start_dt   ={start_dt}")
                print(f"end_dt     ={end_dt}")
                print(f"days       ={days}")
                print(f"bars       ={bars}")
                print(f"net profit ={np}")
                print(f"max DD       ={dd}")
                print(f"max DD %       ={ddp}")
                print(f"num trades       ={nt}")
                print(f"% prof       ={pp}")
                print(f"avg w/l       ={wl}")
                print(f"avg trade       ={at}")
                print(f"std dev       ={sd}")
                print(f"median       ={med}")
                print(f"profit fact  ={pf}")
                print(f"risk-reward  ={rrr}")
                print(f"t-Test       ={tt}")
                print(f"params       ={params}")
                """
                list_of_lists.append(
                    [
                        run,
                        start_dt,
                        end_dt,
                        days,
                        bars,
                        np,
                        dd,
                        ddp,
                        nt,
                        pp,
                        wl,
                        at,
                        sd,
                        med,
                        pf,
                        rrr,
                        tt,
                        params,
                    ]
                )
        df = pd.DataFrame(list_of_lists, columns=labels)
        df.set_index("Run", inplace=True)

    return df


def oos_param_str_cand_based(dbh, rpt_dir):
    logger.debug(f"oos_param_str(dbh,{rpt_dir}):")
    cand_id = rpt_dir.stem.split("-")[-1]

    var_names = []
    for param in queryCandidateParams(dbh, cand_id):
        var_names.append(param.name)
    logger.debug(f"var_names={var_names}")

    str = ""
    for f in rpt_dir.glob("*.txt"):
        # if '_INS' in f.stem and 'OverallResult' not in f.stem:
        #    df_is = parse_is_report(f)
        if "_OOS" in f.stem and "OverallResult" not in f.stem:
            df_oos = parse_oos_report(f)
            for i, row in df_oos.iterrows():
                str += f"if date > {row.start_dt} and date <= {row.end_dt}:\n"
                for i, p in enumerate(row.Parameters.split(",")):
                    str += f"    {var_names[i]} = {p};\n"
        # if 'OverallResult' in f.stem:
        #    print('============> ',f.name)
    return str


def oos_param_str(dbh, rpt_dir):
    logger.debug(f"oos_param_str(dbh,{rpt_dir}):")
    cand_id = rpt_dir.stem.split("-")[-1]

    var_names = []
    for param in queryReoptParams(dbh, cand_id):
        var_names.append(param.name)
    logger.debug(f"var_names={var_names}")

    str = ""
    for f in rpt_dir.glob("*.txt"):
        # if '_INS' in f.stem and 'OverallResult' not in f.stem:
        #    df_is = parse_is_report(f)
        if "_OOS" in f.stem and "OverallResult" not in f.stem:
            df_oos = parse_oos_report(f)
            for i, row in df_oos.iterrows():
                str += f"if date > {row.start_dt} and date <= {row.end_dt}:\n"
                for i, p in enumerate(row.Parameters.split(",")):
                    str += f"    {var_names[i]} = {p};\n"
        # if 'OverallResult' in f.stem:
        #    print('============> ',f.name)
    return str


def nextOosCandidateId():
    rpt_dir = Path("/Users/szagar/ZTS/Dropbox/Business/ats/Data/Queue/WfoReports")
    d = [f for f in rpt_dir.iterdir() if f.is_dir()][0]
    cand_id = d.stem.split("-")[-1]
    return cand_id


def run_generate_code():
    dbh = connectDB()
    cand_id = nextOosCandidateId()
    logger.debug(f"processing candidate: {cand_id}")
    if not cand_id:
        logger.debug("No candidate returned")
        return cand_id

    cnt = 0
    while cand_id:
        cnt += 1
        setup = getCandidateSetup(dbh, cand_id)

        if not generateCandidateCode(dbh, setup):
            logger.debug("could not generate candidate code for cand_id {cand_id}")
            return None

        if not generateJclCode(dbh, setup):
            logger.debug("could not generate jcl code for cand_id {cand_id}")
            return None

        dbUpdateCandidate(dbh, cand_id, {"status": "code", "status_state": "done"})
        cand_id = nextCandidateId(dbh)

    return cnt


if __name__ == "__main__":
    from db_query import connectDB

    dbh = connectDB()

    # for d in rpt_dir.iterdir():
    #    print(oos_param_str(dbh,d))
