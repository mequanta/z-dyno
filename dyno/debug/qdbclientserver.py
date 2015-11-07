from qdb.server import QdbClientServer
from geventwebsocket import WebSocketServer
import re

class DynoQdbClientServer(QdbClientServer):
    def __init__(self, session_store,  apps=None, certfile=None, keyfile=None, host='localhost', port=8002, route=None, auth_fn=None, auth_timeout=60):
        super(DynoQdbClientServer, self).__init__(session_store, host, port, route, auth_fn, auth_timeout)
        self._server = WebSocketServer((host, port), self.handle_client, certfile=certfile, keyfile=keyfile)
        self.apps = apps if apps else {}

    def handle_client(self, environ, start_response):
        path = environ['PATH_INFO']
        match = self.route.match(path)
        if match:
            return super(DynoQdbClientServer, self).handle_client(environ, start_response)

        # handle other apps
        current_app = self._app_by_path(path)
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
