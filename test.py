import time
import json
import logging
import os
from binance.lib.utils import config_logging
from binance.spot import Spot as Client
from binance.websocket.spot.websocket_client import SpotWebsocketClient
from twisted import internet 



config_logging(logging, logging.DEBUG)


def message_handler(message):
    print(message)


api_key = os.getenv('TESTNET_APIKEY')
secret = os.getenv('TESTNET_SECRET')
client = Client(api_key, base_url="https://testnet.binance.vision")
response = client.new_listen_key()

logging.info("Receiving listen key : {}".format(response["listenKey"]))

ws_client = SpotWebsocketClient(stream_url="wss://testnet.binance.vision")
ws_client.start()

ws_client.user_data(
    listen_key=response["listenKey"],
    id=1,
    callback=message_handler,
)

time.sleep(2)

ws_client.agg_trade(
    symbol="bnbusdt",
    id=2,
    callback=message_handler,
)

# spot_client = Client(api_key, secret, base_url="https://testnet.binance.vision")
# logging.info(spot_client.account())

time.sleep(30)

logging.debug("closing ws connection")
ws_client.stop()