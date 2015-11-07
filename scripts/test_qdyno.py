import websocket
import ssl
import json
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-a','--auth-msg', action='store', dest="auth_msg")
parser.add_argument('-n', '--host', action='store')
parser.add_argument('-b','--backtest-id', action='store', dest="backtest_id")
args = parser.parse_args()
dyno_host = args.host or "localhost:8000"
backtest_id = args.backtest_id
auth_msg = args.auth_msg

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

if __name__ == "__main__":
    ws_url = "wss://{}/backtests/{}".format(dyno_host, backtest_id)
    print("Connecting to %s" % ws_url)
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message = on_message, on_error = on_error, on_close = on_close)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})