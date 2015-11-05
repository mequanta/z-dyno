from dyno.backtest import BacktestHandler
from dyno.livetrade import LiveTradingHandler
from dyno.transaction import TransactionHandler
from dyno.debug import DebugHandler
from dyno.test import TestBacktestHandlder, TestLiveTradeHandlder, StatusHandlder
from tornado.web import FallbackHandler
from tornado.wsgi import WSGIContainer
if __name__ == "__main__":
    import ssl
    import logging
    from tornado.web import Application
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    import os
    port = 8000

    qdb_app = WSGIContainer()

    logging.getLogger().setLevel(logging.DEBUG)

    ssl_ctx = dict(certfile=os.path.join(os.path.dirname(__file__), "certs", "localhost.crt"),
                   keyfile=os.path.join(os.path.dirname(__file__), "certs" , "localhost.key"))

    application = Application([
        (r'/backtests/debug/(.*)', FallbackHandler, dict(fallback=qdb_app)),
        (r'/backtests/(.*)', BacktestHandler),
        (r'/transactions/(.*)', TransactionHandler),
        (r'/trading_sessions/(.*)', LiveTradingHandler),
        (r'/test/backtests', TestBacktestHandlder),
        (r'/test/trading_sessions', TestLiveTradeHandlder),
        (r'/status', StatusHandlder)
    ])

    server = HTTPServer(application, ssl_options=ssl_ctx)
    server.listen(port)
    logging.debug('Listening on http(s)://localhost:%d' % port)
    IOLoop.current().start()