import asyncio
import json
import logging
import websockets
from core.ws_client import WS_URL
from core.orderbook import OrderBookManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_simulator(depth: int = 20):
    ob_manager = OrderBookManager(depth=depth)
    async with websockets.connect(WS_URL) as ws:
        logger.info(f"Simulator connected to {WS_URL}")
        async for msg in ws:
            try:
                data = json.loads(msg)
                asks = [(float(p), float(sz)) for p, sz in data.get('asks', [])]
                bids = [(float(p), float(sz)) for p, sz in data.get('bids', [])]
                timestamp = data.get('timestamp')

                # update full state
                ob_manager.update(asks, bids, timestamp)

                # fetch top-of-book
                top = ob_manager.top_of_book()
                best_ask, best_bid = top['best_ask'], top['best_bid']
                mid_price = (best_ask[0] + best_bid[0]) / 2 if best_ask and best_bid else None

                # output
                logger.info(
                    "[%s] Best Bid: %.2f | Best Ask: %.2f | Mid: %.2f",
                    timestamp, best_bid[0], best_ask[0], mid_price
                )

            except json.JSONDecodeError:
                logger.error("Failed to decode JSON: %s", msg)
            except Exception as e:
                logger.exception("Error in simulation loop: %s", e)

if __name__ == '__main__':
    try:
        asyncio.run(run_simulator())
    except KeyboardInterrupt:
        logger.info("Simulation terminated by user.")