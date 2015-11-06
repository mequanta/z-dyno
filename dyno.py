from dyno.backtest import BacktestHandler
from dyno.livetrade import LiveTradingHandler
from dyno.transaction import TransactionHandler
from dyno.test import StatusHandlder, EchoHandlder
from tornado.web import FallbackHandler
from tornado.wsgi import WSGIContainer, WSGIAdapter
from dyno.debug import DebugHandler


import gevent
import gevent.monkey
gevent.monkey.patch_all()

from gevent.pywsgi import WSGIServer

if __name__ == "__main__":
    import ssl
    import logging
    from tornado.web import Application
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    import os
    port = 8000

    #qdb_server = DynoQdbClientServer()
    #qdb_app = WSGIContainer(qdb_server.handle_client)

    logging.getLogger().setLevel(logging.DEBUG)

    certfile=os.path.join(os.path.dirname(__file__), "certs", "localhost.crt")
    keyfile=os.path.join(os.path.dirname(__file__), "certs" , "localhost.key")
    ssl_ctx = dict(certfile=certfile, keyfile=keyfile)

    application = Application([
        #(r'/backtests/debug/(.*)', DebugHandler),
        #(r'/backtests/(.*)', BacktestHandler),
        #(r'/transactions/(.*)', TransactionHandler),
        #(r'/trading_sessions/(.*)', LiveTradingHandler),
        (r'/status', StatusHandlder),
        (r'/echo', EchoHandlder)
    ], debug = True)
    #server = WSGIServer(('', port), WSGIAdapter(application), certfile=certfile, keyfile=keyfile)
    #server = WSGIServer(('', port), WSGIAdapter(application))
    #logging.debug('Listening on http(s)://localhost:%d' % port)
    #server.serve_forever()

    server = HTTPServer(application, ssl_options=ssl_ctx)
    server.listen(port)
    logging.debug('Listening on http(s)://localhost:%d' % port)
    IOLoop.current().start()
