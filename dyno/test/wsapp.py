from geventwebsocket import WebSocketApplication

from flask import Flask
app = Flask(__name__)
@app.route('/status')
def status():
    return '''<!DOCTYPE html>
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
</html>'''

class EchoApplication(WebSocketApplication):
    def on_open(self):
        print "[EchoApplication] Connection opened"

    def on_message(self, message):
        self.ws.send(message)

    def on_close(self, reason):
        print "[EchoApplication] Connection closed"

