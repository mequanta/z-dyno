from tornado.websocket import WebSocketHandler

class LiveTradingHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, algo_id):
        print(algo_id)
        print("WebSocket opened")

    def on_message(self, message):
        print "message:{}".format(message)

    def on_close(self):
        print("WebSocket closed")
