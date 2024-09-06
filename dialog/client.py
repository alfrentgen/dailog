import logging
from websockets.asyncio import client as ws_client

logger = logging.getLogger('client_logger')
logger.setLevel(logging.INFO)
fileHandler = logging.FileHandler('client.log', mode='w')
formatter = logging.Formatter("%(asctime)s\n%(message)s\n")
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

class Client:
    def __init__(self, address, port, processing = None):
        self.address = address
        self.port = str(port)
        self.processing = processing

    def make_response(self, message: str):
        if self.processing:
            return self.processing.process(message)
        return 'Client response.'

    async def run(self):
        server_address = 'ws://' + ':'.join([self.address, self.port])
        async with (ws_client.connect(server_address, open_timeout=None, close_timeout=None, ping_timeout=None) as connection):
            await connection.send(f'Hello!')
            while True:
                message = await connection.recv()
                logger.info(f'Received: {message}')
                response = self.make_response(message)
                logger.info(f'Respond: {response}')
                await connection.send(response)
