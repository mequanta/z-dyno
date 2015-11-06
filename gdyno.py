from qdb.server.server import QdbServer
from qdb.server import QdbClientServer
from qdb.server import SessionStore
from qdb.server.client import DEFAULT_ROUTE
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from logbook import StderrHandler
import os

certfile=os.path.join(os.path.dirname(__file__), "certs", "localhost.crt")
keyfile=os.path.join(os.path.dirname(__file__), "certs" , "localhost.key")

ROUTE = '/backtests/debug/(.+)'

class MyQdbClientServer(QdbClientServer):
    def __init__(self, session_store, host='localhost', port=8002, route=ROUTE, auth_fn=None, auth_timeout=60):
        super(MyQdbClientServer, self).__init__(session_store, host, port, route, auth_fn, auth_timeout)
        self._server = WSGIServer((host, port), self.handle_client, handler_class=WebSocketHandler, certfile=certfile, keyfile=keyfile)

if __name__ == '__main__':
    session_store = SessionStore()
    client_server = MyQdbClientServer(session_store=session_store, port=8000)

    handler = StderrHandler()
    with handler:
        QdbServer(client_server=client_server).serve_forever()