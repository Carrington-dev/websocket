import asyncio
import websockets
import json

class WebSocketServer:
    def __init__(self, data_feed, arbitrage_detector):
        self.data_feed = data_feed
        self.arbitrage_detector = arbitrage_detector
        self.clients = []

    async def handler(self, websocket, path):
        self.clients.append(websocket)
        try:
            while True:
                data = self.data_feed.data
                arbitrage_opportunities = self.arbitrage_detector.detect_arbitrage(data)
                message = {
                    'market_data': data,
                    'arbitrage_opportunities': arbitrage_opportunities
                }
                await websocket.send(json.dumps(message))
                await asyncio.sleep(1)
        finally:
            self.clients.remove(websocket)

    def start(self):
        loop = asyncio.get_event_loop()
        server = websockets.serve(self.handler, 'localhost', 6789)
        loop.run_until_complete(server)
        loop.run_forever()
