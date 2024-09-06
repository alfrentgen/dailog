import asyncio
import argparse
from datetime import datetime
from json import load as json_load
from random import seed as randseed, randint

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
                config = json_load(config_data)
                prompt = config['prompt']
                if prompt.find('file:') == 0:
                    prompt_file = prompt[5:]
                    with open(prompt_file, 'r') as prompt_file:
                        prompt = prompt_file.read()

                if (seed := config['seed']) and seed == 'random':
                    randseed(int(datetime.now().timestamp()))
                    config['seed'] = randint(0, 0xffffffff)

                config['prompt'] = prompt
                agent = LLM(config)
            print(config)

    instance = Server(address, port, agent) if mode == 'server' else Client(address, port, agent)
    asyncio.run(instance.run())

__main__()