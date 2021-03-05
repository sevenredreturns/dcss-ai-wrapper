"""

Demo of an RL agent on the sonja sprint in crawl 23.1

Make sure to run crawl before running this demo, see:
    start_crawl_terminal_sprint.sh

"""

from game_connection_4 import DCSSProtocol
from agent import SimpleRandomAgent, TestAllCommandsAgent, FastDownwardPlanningAgent
from actions import Command, Action
import config
import asyncio
import logging
import time
import threading
from gamestate import Monster
from autobahn.asyncio.websocket import WebSocketClientFactory

logging.basicConfig(level=logging.INFO)


def main():
    factory = WebSocketClientFactory(config.WebserverConfig.server_uri)
    factory.protocol = DCSSProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, config.WebserverConfig.server_ip, config.WebserverConfig.server_port)
    loop.run_until_complete(coro)
    loop.run_forever()


if __name__ == "__main__":
    main()
