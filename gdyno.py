from qdb.server.server import QdbServer
from qdb.server import QdbClientServer
from qdb.server import SessionStore
from geventwebsocket import WebSocketServer, WebSocketApplication
from logbook import StderrHandler
import os
import re

from flask import Flask
app = Flask(__name__)
@app.route('/status')
def status():
    return '''<!DOCTYPE html>
<html>
<head>
    <script type="text/javascript">
        var scheme = document.location.protocol == "https:" ? "wss" : "ws"
        var ws_url = scheme + '://' + document.location.hostname + ':' + document.location.port + '/echo';
        var ws = new WebSocket(ws_url);
        ws.onopen = function() {
            console.log("Connected");
            ws.send("hi")
        }

        ws.onclose = function() {
            console.log("Disconnected");
        }

        ws.onmessage = function(e) {
            console.log(e.data)
        }
     </script>
</head>
<body>
    <p>ok</p>
</body>
</html>'''


certfile=os.path.join(os.path.dirname(__file__), "certs", "localhost.crt")
keyfile=os.path.join(os.path.dirname(__file__), "certs" , "localhost.key")

QDB_ROUTE = '/backtests/debug/(.+)'

class EchoApplication(WebSocketApplication):
    def on_open(self):
        print "Connection opened"

    def on_message(self, message):
        self.ws.send(message)

    def on_close(self, reason):
        print reason

import json

class BacktestApplication(WebSocketApplication):
    def on_open(self):
        print "Connection opened"

    def on_message(self, message):
        print "message:{}".format(message)
        m = json.loads(message)
        if m['e'] == 'open':
            self.send_data()
            self.ws.close()

    def on_close(self, reason):
        print reason

    def send_data(self):
        print "send_data"
        f = open(os.path.join(os.path.dirname(__file__), 'new_s1.json'))
        try:
             text = f.read( )
             packets = json.loads(text)
             for p in packets:
                self.ws.send(json.dumps(p))
        finally:
             f.close( )

apps = {"/echo": EchoApplication,
        "/status": app.wsgi_app,
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