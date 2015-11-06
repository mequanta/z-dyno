from tornado.websocket import WebSocketHandler
import json
import os

class DebugHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self, backtest_id):
        self.uuid = backtest_id
        print(backtest_id)
        print("[DebugHandler] WebSocket opened")

    def on_message(self, message):
        print "[DebugHandler] message:{}".format(message)
        m = json.loads(message)


    def on_close(self):
        print("[DebugHandler] WebSocket closed")