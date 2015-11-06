import gevent.monkey
gevent.monkey.patch_all()

import json
import re

from gevent import pywsgi, Timeout
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from logbook import Logger

from qdb.comm import fmt_msg, fmt_err_msg
from qdb.errors import QdbInvalidRoute
from qdb.server.serverbase import QdbServerBase

# The default route.
DEFAULT_ROUTE = r'/(.+)'

# The default route as a format string.
DEFAULT_ROUTE_FMT = '/{uuid}'


class QdbClientServer(QdbServerBase):
    def __init__(self,
                 session_store,
                 host='localhost',
                 port=8002,
                 route=DEFAULT_ROUTE,
                 auth_fn=None,
                 auth_timeout=60):  # seconds

        self.auth_fn = auth_fn or self.NO_AUTH
        self.auth_timeout = auth_timeout
        self.route = re.compile(route, re.IGNORECASE)
        self.session_store = session_store
        if self.route.groups != 1:
            # We need exactly one regex group.
            raise QdbInvalidRoute(self.route)
        # self._server = pywsgi.WSGIServer(
        #     (host, port),
        #     self.handle_client,
        #     handler_class=WebSocketHandler,
        # )

    def send_error(self, ws, error_type, error_data):
        """
        Sends an error event back to the client.
        """
        try:
            ws.send(fmt_err_msg(error_type, error_data, serial=json.dumps))
        except WebSocketError:
            return

    def get_events(self, ws):
        """
        Yields valid messages from the websocket. Only yields well formed
        messages. In the case of an illformed message, an error event is sent
        to the client.
        """
        while True:
            try:
                raw = ws.receive()
            except WebSocketError:
                return
            try:
                event = json.loads(raw)
                event['e']
            except (ValueError, TypeError) as v:
                self.send_error(ws, 'event', str(v))
                return
            except KeyError:
                self.send_error(ws, 'event', "No 'e' field sent")
                return

            yield event

    def get_event(self, ws):
        """
        Returns a single (valid) event.
        """
        try:
            return next(self.get_events(ws))
        except StopIteration:
            return None

    def handle_client(self, environ, start_response):
        path = environ['PATH_INFO']
        ws = environ['wsgi.websocket']
        addr = environ['REMOTE_ADDR']

        try:
            match = self.route.match(path)
            if not match:
                # This did not match our route.
                return
            log.info('Client request from %s' % addr)
            uuid = match.group(1)
            start_event = None
            with Timeout(self.auth_timeout, False):
                start_event = self.get_event(ws)

            failed = False
            message = ''

            # Fall through the various ways to fail to generate a more helpful
            # error message.
            if not start_event:
                message = 'No start event received'
                failed = True
            elif start_event['e'] != 'start':
                message = "First event must be of type: 'start'"
                failed = True
            elif not self.auth_fn(start_event.get('p', '')):
                log.warn('Client %s failed to authenticate' % addr)
                message = 'Authentication failed'
                failed = True

            if failed:
                try:
                    self.send_error(ws, 'auth', message)
                    ws.send(fmt_msg('disable', serial=json.dumps))
                except WebSocketError:
                    # We are unable to send the disable message for some
                    # reason; however, they already failed auth so suppress
                    # it and close.
                    pass
                return

            if not self.session_store.attach_client(uuid, ws):
                # We are attaching to a client that does not exist.
                return

            self.session_store.send_to_tracer(uuid, event=start_event)
            for event in self.get_events(ws):
                self.session_store.send_to_tracer(uuid, event=event)

        finally:
            log.info('Closing websocket to client %s' % addr)
            ws.close()

    @property
    def _extra_repr_args(self):
        return ('route=%s' % repr(self.route.pattern),)
