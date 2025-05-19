import asyncio
import json
import uvloop
import websockets

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

class OrderBook:
    def __init__(self, depth=20):
        self.depth = depth
        self.asks = []
        self.bids = []
        self.timestamp = None

    def update(self, data):
        self.timestamp = data['timestamp']
        self.asks = data['asks'][:self.depth]
        self.bids = data['bids'][:self.depth]

    def mid_price(self):
        if not self.asks or not self.bids:
            return None
        top_ask = float(self.asks[0][0])
        top_bid = float(self.bids[0][0])
        return (top_ask + top_bid) / 2

async def listen_and_print():
    url = 'wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP'
    ob = OrderBook()
    async with websockets.connect(url) as ws:
        async for msg in ws:
            data = json.loads(msg)
            ob.update(data)
            mid = ob.mid_price()
            print(f"[{ob.timestamp}] MID-PRICE: {mid:.2f}")

if __name__ == '__main__':
    try:
        asyncio.run(listen_and_print())
    except KeyboardInterrupt:
        print("Shutting down...")