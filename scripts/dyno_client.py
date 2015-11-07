import websocket
import ssl
import json
import os

f = os.popen('./curl.sh')
output = f.read()
data = json.loads(output)['data']
backtest_id = data['id']
ws_url = data['ws_url']
auth_msg = data['ws_open_msg']

def on_message(ws, message):
    print message

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "### opened ###"
    s = mk_openmsg(auth_msg)
    print(s)
    ws.send(s)

def mk_openmsg(auth_msg=""):
    r = dict(e="open", p=dict(cursor=0, include_txn=False, a=auth_msg))
    return json.dumps(r)

print("Connecting to %s" % ws_url)
ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message = on_message, on_error = on_error, on_close = on_close)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

print("Connecting to %s" % ws_url)
ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message = on_message, on_error = on_error, on_close = on_close)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})