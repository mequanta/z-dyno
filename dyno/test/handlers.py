from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler


class StatusHandlder(RequestHandler):
    def get(self):
        self.write('''<!DOCTYPE html>
<html>
<head>
    <script type="text/javascript">
        var scheme = document.location.protocol == "https:" ? "wss" : "ws"
        var ws_url = scheme + '://' + document.location.hostname + ':' + document.location.port + '/echo';
        var ws = new WebSocket(ws_url);
        ws.onopen = function() {
            console.log("Connected");
            ws.send("hi")
        }

        ws.onclose = function() {
            console.log("Disconnected");
        }

        ws.onmessage = function(e) {
            console.log(e.data)
        }
     </script>
</head>
<body>
    <p>ok</p>
</body>
</html>''')


class EchoHandlder(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def on_message(self, message):
        print("received: %s" % message)
        self.write_message(message + " back")
        self.close()
