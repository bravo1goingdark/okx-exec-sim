import asyncio
import json
import logging
import uvloop
import websockets

essential = uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


WS_URL = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"

class OrderBook:
    def __init__(self, depth: int = 20):
        self.depth = depth
        self.asks: list[tuple[float, float]] = []
        self.bids: list[tuple[float, float]] = []
        self.timestamp: str | None = None

    def update(self, data: dict) -> None:
        self.timestamp = data.get('timestamp')
        # store top `depth` levels
        self.asks = [(float(p), float(sz)) for p, sz in data.get('asks', [])][:self.depth]
        self.bids = [(float(p), float(sz)) for p, sz in data.get('bids', [])][:self.depth]
        logger.debug(f"OrderBook updated: {len(self.asks)} asks, {len(self.bids)} bids at {self.timestamp}")

    def mid_price(self) -> float | None:
        if not self.asks or not self.bids:
            return None
        top_ask = self.asks[0][0]
        top_bid = self.bids[0][0]
        return (top_ask + top_bid) / 2

async def listen_and_print():
    ob = OrderBook()
    try:
        async with websockets.connect(WS_URL) as ws:
            logger.info(f"Connected to {WS_URL}")
            async for msg in ws:
                try:
                    data = json.loads(msg)
                    ob.update(data)
                    mid = ob.mid_price()
                    if mid is not None:
                        print(f"[{ob.timestamp}] MID-PRICE: {mid:.2f}")
                except json.JSONDecodeError:
                    logger.error("JSON decode error for message: %s", msg)
    except websockets.exceptions.ConnectionClosedError as e:
        logger.error("WebSocket connection closed: %s", e)
    except Exception as e:
        logger.exception("Unexpected error in listen_and_print: %s", e)

if __name__ == '__main__':
    try:
        asyncio.run(listen_and_print())
    except KeyboardInterrupt:
        logger.info("Shutting down...")