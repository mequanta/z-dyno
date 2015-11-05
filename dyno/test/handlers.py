from tornado.web import RequestHandler

class TestBacktestHandlder(RequestHandler):
    def post(self):
        code = self.get_argument("code")
        self.write("ok")

class TestLiveTradeHandlder(RequestHandler):
    def get(self):
        self.write("Hello, TestLiveTradeHandlder")