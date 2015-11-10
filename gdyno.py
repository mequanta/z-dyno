#/usr/bin/env python2

import dyno.patch_ssl

from qdb.server.server import QdbServer
from qdb.server import SessionStore
from logbook import StderrHandler
from dyno.debug import DynoQdbClientServer
from dyno.test import EchoApplication, flask_app
from dyno.backtest import BacktestApplication
import os

certfile=os.path.join(os.path.dirname(__file__), "certs", "localhost.crt")
keyfile=os.path.join(os.path.dirname(__file__), "certs" , "localhost.key")

QDB_ROUTE = '/backtests/debug/(.+)'

apps = {"/echo": EchoApplication,
        "/status": flask_app.wsgi_app,
        "/backtest": BacktestApplication}

if __name__ == '__main__':
    session_store = SessionStore()
    client_server = DynoQdbClientServer(host="0.0.0.0", apps=apps, route=QDB_ROUTE, certfile=certfile, keyfile=keyfile,
                                        session_store=session_store, port=8000)

    handler = StderrHandler()
    with handler:
        QdbServer(session_store=session_store, client_server=client_server).serve_forever()
