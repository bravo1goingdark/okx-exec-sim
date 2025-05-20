class OrderBookManager:
    """
    Maintains sorted ask and bid lists up to a fixed depth.
    Supports full snapshot updates for simplicity.
    """
    def __init__(self, depth: int = 20):
        self.depth = depth
        self.asks: list[tuple[float, float]] = []  # sorted ascending
        self.bids: list[tuple[float, float]] = []  # sorted descending
        self.timestamp: str | None = None

    def update(self, asks: list[tuple[float, float]], bids: list[tuple[float, float]], timestamp: str) -> None:
        # full refresh: sort and trim to depth
        self.asks = sorted(asks)[:self.depth]
        self.bids = sorted(bids, reverse=True)[:self.depth]
        self.timestamp = timestamp

    def top_of_book(self) -> dict:
        return {
            'timestamp': self.timestamp,
            'best_ask': self.asks[0] if self.asks else None,
            'best_bid': self.bids[0] if self.bids else None
        }

    def snapshot(self) -> dict:
        """Return full depth snapshot."""
        return {
            'timestamp': self.timestamp,
            'asks': self.asks,
            'bids': self.bids
        }