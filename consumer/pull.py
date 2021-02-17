#https://pypi.org/project/websocket_client/
import websocket
import json
import os
import sys
from elasticsearch import Elasticsearch
from datetime import datetime

def on_message(ws, message):
    es = Elasticsearch(
        [os.environ.get('ELASTICSEARCH_HOSTS')],
        port=9200
    )
    parsed = json.loads(message)
    if "data" in parsed:
        for x in range(len(parsed["data"])):
            # print(parsed["data"][x])
            parsed["data"][x].pop("c", None)
            parsed["data"][x]["@timestamp"] = datetime.utcfromtimestamp(parsed["data"][x]["t"]/1000).isoformat()
            try:
                es.index(index='stock_advisor', id=int(str(parsed["data"][x]["t"]) + str(x)), body=parsed["data"][x])
            except Exception as inst:
                # print(type(inst))
                # print(inst.args)
                # print(inst)
                pass


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"NOK"}')
    ws.send('{"type":"subscribe","symbol":"AMC"}')
    ws.send('{"type":"subscribe","symbol":"GEVO"}')
    # ws.send('{"type":"subscribe","symbol":"^GSPC"}')
    # ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token="+ os.environ.get('FINNHUB_TOKEN'),
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
