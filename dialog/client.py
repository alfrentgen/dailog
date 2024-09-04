from websockets.asyncio import client as ws_client

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
                print(f'Received: {message}')
                response = self.make_response(message)
                print(f'Respond: {response}')
                await connection.send(response)
