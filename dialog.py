import asyncio
import argparse
import json

from dialog.server import Server
from dialog.client import Client
from dialog.processing import Human, LLM

def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', choices=['server', 'client'], default='server')
    parser.add_argument('-a', '--address', type=str, default='localhost')
    parser.add_argument('-p', '--port', type=int, default=8765)
    parser.add_argument('-c', '--config', type=str, default=None)
    args = parser.parse_args()

    address = args.address
    port = args.port
    mode = args.mode
    print(f'Running a {mode} at {address}:{port}')
    config = args.config
    if config:
        if config == 'human':
            config = Human()
        else:
            with open(config) as config_data:
                config = json.load(config_data)
                response = LLM(config)

    instance = Server(address, port, response) if mode == 'server' else Client(address, port, response)
    asyncio.run(instance.run())

__main__()