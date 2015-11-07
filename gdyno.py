from qdb.server.server import QdbServer
from qdb.server import QdbClientServer
from qdb.server import SessionStore
from geventwebsocket import WebSocketServer, WebSocketApplication
from logbook import StderrHandler
import os
import re

from dyno.test import EchoApplication, flask_app
from dyno.backtest import BacktestApplication

certfile=os.path.join(os.path.dirname(__file__), "certs", "localhost.crt")
keyfile=os.path.join(os.path.dirname(__file__), "certs" , "localhost.key")

QDB_ROUTE = '/backtests/debug/(.+)'

apps = {"/echo": EchoApplication,
        "/status": flask_app.wsgi_app,
        "/backtest": BacktestApplication}

class MyQdbClientServer(QdbClientServer):
    def __init__(self, session_store,  apps=apps, host='localhost', port=8002, route=QDB_ROUTE, auth_fn=None, auth_timeout=60):
        super(MyQdbClientServer, self).__init__(session_store, host, port, route, auth_fn, auth_timeout)
        self._server = WebSocketServer((host, port), self.handle_client, certfile=certfile, keyfile=keyfile)
        self.apps = apps if apps else {}

    def handle_client(self, environ, start_response):
        path = environ['PATH_INFO']
        match = self.route.match(path)
        if match:
            return super(MyQdbClientServer, self).handle_client(environ, start_response)

        # handle other apps
        current_app = self._app_by_path(environ['PATH_INFO'])
        if current_app is None:
            raise Exception("No apps defined")

        if 'wsgi.websocket' in environ:
            ws = environ['wsgi.websocket']
            current_app = current_app(ws)
            current_app.ws = ws  # TODO: needed?
            current_app.handle()
            return None
        else:
            return current_app(environ, start_response)

    def _app_by_path(self, environ_path):
        # Which app matched the current path?

        for path, app in self.apps.iteritems():
            if re.match(path, environ_path):
                return app

    def app_protocol(self, path):
        app = self._app_by_path(path)

        if hasattr(app, 'protocol_name'):
            return app.protocol_name()
        else:
            return ''

if __name__ == '__main__':
    session_store = SessionStore()
    client_server = MyQdbClientServer(session_store=session_store, port=8000)

    handler = StderrHandler()
    with handler:
        QdbServer(client_server=client_server).serve_forever()