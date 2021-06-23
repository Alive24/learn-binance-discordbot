import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time
import json
import logging
import os
from binance.lib.utils import config_logging
from binance.spot import Spot as Client
from binance.websocket.spot.websocket_client import SpotWebsocketClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
latestBtcusdt = None

@bot.command(name='hello')
@commands.has_role('Coordinator')
async def hello(context):
    await context.send("Successfully greeted!")


@bot.command(name='btcusdt')
@commands.has_role('Coordinator')
async def hello(context):
    global latestBtcusdt
    await context.send("The latest btcusdt is %s" % latestBtcusdt["p"])

@bot.command(name='init')
@commands.has_role('Coordinator')
async def init(context):
    def message_handler(message):
        global latestBtcusdt
        latestBtcusdt = message
    await context.send("Trying to initialize a WebSocket connection to Binance...")
    ws_client = SpotWebsocketClient(stream_url="wss://testnet.binance.vision")
    ws_client.start()
    ws_client.agg_trade(
        symbol="btcusdt",
        id=2,
        callback=message_handler,
    )
    # time.sleep(5)
    # logging.debug("closing ws connection")
    # ws_client.stop()

bot.run(TOKEN)