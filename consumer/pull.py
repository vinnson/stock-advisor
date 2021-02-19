#https://pypi.org/project/websocket_client/
import websocket
import json
import os
import sys
import time
from celery import Celery
from elasticsearch import Elasticsearch
from datetime import datetime

app = Celery('pull', broker='redis://'+ os.environ.get('REDIS_HOSTS') +':6379/0')
@app.task
def send_out(mid, message):
    try:
        es = Elasticsearch(
            [os.environ.get('ELASTICSEARCH_HOSTS')],
            port=9200
        )
        es.index(index='stock_advisor', id=mid, body=message)
    except Exception as inst:
        # print(type(inst))
        # print(inst.args)
        # print(inst)
        time.sleep(10)
        pass

def on_message(ws, message):
    parsed = json.loads(message)
    if "data" in parsed:
        for x in range(len(parsed["data"])):
            # print(parsed["data"][x])
            dataid = int(str(parsed["data"][x]["t"]) + str(x))
            parsed["data"][x].pop("c", None)
            parsed["data"][x]["@timestamp"] = datetime.utcfromtimestamp(parsed["data"][x]["t"]/1000).isoformat()
            parsed["data"][x].pop("t", None)
            send_out.delay(dataid, parsed["data"][x])

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
