from tornado.websocket import WebSocketHandler
import json
import os


class TransactionHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, backtest_id):
        print(backtest_id)
        print("WebSocket opened")

    def on_message(self, message):
        print "message:{}".format(message)
        m = json.loads(message)

        if m['e'] == 'open':
            self.send_data()
            self.close()

    def on_close(self):
        print("WebSocket closed")

    def send_data(self):
        print "send_data"
        f = open(os.path.join(os.path.dirname(__file__), 't.json'))
        try:
             text = f.read( )
             packets = json.loads(text)
             for p in packets:
                self.write_message(json.dumps(p))
        finally:
             f.close( )
