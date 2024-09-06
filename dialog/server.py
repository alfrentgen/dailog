import asyncio
import logging
from websockets.asyncio import server as ws_server

logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)
fileHandler = logging.FileHandler('server.log', mode='w')
formatter = logging.Formatter("%(asctime)s\n%(message)s\n")
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

class Server:
    def __init__(self, address: str, port: int, processing = None):
        self.address = address
        self.port = port
        self.processing = processing

    def make_response(self, message: str):
        if self.processing:
            return self.processing.process(message)
        response = 'Server response'
        return response

    async def serve(self, websocket):
        while True:
            message = await websocket.recv()
            logger.info(f'Received: {message}')
            response = self.make_response(message)
            logger.info(f'Respond: {response}')
            await websocket.send(response)

    async def run(self):
        async with ws_server.serve(self.serve, 'localhost', self.port, open_timeout=None, close_timeout=None, ping_timeout=None):
            await asyncio.get_running_loop().create_future()
