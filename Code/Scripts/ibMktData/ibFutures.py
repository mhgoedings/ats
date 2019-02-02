from __future__ import (absolute_import, division, print_function,)
#                        unicode_literals)

import sys

if sys.version_info.major == 2:
    import Queue as queue
else:  # >= 3
    import queue


import ib.opt
import ib.ext.Contract


class IbManager(object):
    def __init__(self, timeout=20, **kwargs):
        self.q = queue.Queue()
        self.timeout = 20

        self.con = ib.opt.ibConnection(**kwargs)
        self.con.registerAll(self.watcher)

        self.msgs = {
            ib.opt.message.error: self.errors,
            ib.opt.message.contractDetails: self.contractDetailsHandler,
            ib.opt.message.contractDetailsEnd: self.contractDetailsHandler
        }

        self.skipmsgs = tuple(self.msgs.keys())

        for msgtype, handler in self.msgs.items():
            self.con.register(handler, msgtype)

        self.con.connect()

    def watcher(self, msg):
        if isinstance(msg, ib.opt.message.error):
            if msg.errorCode > 2000:  # informative message
                print('-' * 10, msg)

        elif not isinstance(msg, self.skipmsgs):
            print('-' * 10, msg)

    def errors(self, msg):
        if msg.id is None:  # something is very wrong in the connection to tws
            self.q.put((True, -1, 'Lost Connection to TWS'))
        elif msg.errorCode < 1000:
            self.q.put((True, msg.errorCode, msg.errorMsg))

    def contractDetailsHandler(self, msg):
        if isinstance(msg, ib.opt.message.contractDetailsEnd):
            self.q.put((False, msg.reqId, msg))
        else:
            self.q.put((False, msg.reqId, msg.contractDetails))

    def get_contract_details(self, symbol, sectype, exch='SMART', curr='USD'):
        contract = ib.ext.Contract.Contract()
        contract.m_symbol = symbol
        contract.m_exchange = exch
        contract.m_currency = curr
        contract.m_secType = sectype

        self.con.reqContractDetails(1, contract)

        cdetails = list()
        while True:
            try:
                err, mid, msg = self.q.get(block=True, timeout=self.timeout)
            except queue.Empty:
                err, mid, msg = True, -1, "Timeout receiving information"
                break

            if isinstance(msg, ib.opt.message.contractDetailsEnd):
                mid, msg = None, None
                break

            cdetails.append(msg)  # must be contractDetails

        # return list of contract details, followed by:
        #   last return code (False means no error / True Error)
        #   last error code or None if no error
        #   last error message or None if no error
        # last error message

        return cdetails, err, mid, msg


ibm = IbManager(clientId=5001)

cs = (
    ('VTR', 'OPT', 'SMART'),
    ('ES', 'FUT', 'GLOBEX'),
)

for c in cs:
    cdetails, err, errid, errmsg = ibm.get_contract_details(*c)

    if err:
        print('Last Error %d: %s' % (errid, errmsg))

    print('-' * 50)
    print('-- ', c)
    for cdetail in cdetails:
        # m_summary is the contract in details
        print('Expiry:', cdetail.m_summary.m_expiry)


sys.exit(0)  # Ensure ib thread is terminated
