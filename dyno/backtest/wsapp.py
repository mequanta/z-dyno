from geventwebsocket import WebSocketApplication
import os
import json

class BacktestApplication(WebSocketApplication):
    def on_open(self):
        print "[Backtest] Connection opened"

    def on_message(self, message):
        print "[Backtest] message:{}".format(message)
        m = json.loads(message)
        if m['e'] == 'open':
            self.send_data()
            self.ws.close()

    def on_close(self, reason):
        print "[Backtest] Connection closed"

    def send_data(self):
        f = open(os.path.join(os.path.dirname(__file__), 'new_s1.json'))
        try:
             text = f.read( )
             packets = json.loads(text)
             for p in packets:
                self.ws.send(json.dumps(p))
        finally:
             f.close( )
