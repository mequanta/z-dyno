from zipliner.dyno.backtest import BacktestHandler
from zipliner.dyno.livetrade import LiveTradingHandler
from zipliner.dyno.transaction import TransactionHandler
from zipliner.dyno.debug import DebugHandler
from zipliner.dyno.test import TestBacktestHandlder, TestLiveTradeHandlder

if __name__ == "__main__":
    import ssl
    import logging
    from tornado.web import Application
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    port = 8000
    logging.getLogger().setLevel(logging.DEBUG)
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain("certs/localhost.crt", "certs/localhost.key")
    application = Application([
        (r'/backtests/debug/(.*)', DebugHandler),
        (r'/backtests/(.*)', BacktestHandler),
        (r'/transactions/(.*)', TransactionHandler),
        (r'/trading_sessions/(.*)', LiveTradingHandler),
        (r'/test/backtests', TestBacktestHandlder),
        (r'/test/trading_sessions', TestLiveTradeHandlder)
    ])

    server = HTTPServer(application, ssl_options=ssl_ctx)
    server.listen(port)
    logging.debug('Listening on http(s)://localhost:%d' % port)
    IOLoop.current().start()