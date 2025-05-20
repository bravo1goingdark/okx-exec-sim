import pytest
from src.core.orderbook import OrderBookManager

@pytest.fixture()
def sample_data():
    # out-of-order asks and bids with extra levels
    asks = [(100.5, 1), (99.9, 2), (101.0, 0.5), (98.0, 5)]
    bids = [(99.5, 3), (100.0, 1), (98.5, 4), (101.5, 0.2)]
    timestamp = "2025-05-19T12:00:00Z"
    return asks, bids, timestamp

def test_update_and_depth(sample_data):
    asks, bids, ts = sample_data
    mgr = OrderBookManager(depth=2)
    mgr.update(asks, bids, ts)

    # Depth trimming
    assert len(mgr.asks) == 2
    assert len(mgr.bids) == 2

    # Asks should be sorted ascending
    assert mgr.asks[0][0] <= mgr.asks[1][0]
    # Bids should be sorted descending
    assert mgr.bids[0][0] >= mgr.bids[1][0]
    # Timestamp preserved
    assert mgr.timestamp == ts

def test_top_of_book(sample_data):
    asks, bids, ts = sample_data
    mgr = OrderBookManager(depth=10)
    mgr.update(asks, bids, ts)
    top = mgr.top_of_book()

    # Best ask is minimum price
    expected_best_ask = min([p for p, _ in asks])
    assert top['best_ask'][0] == expected_best_ask

    # Best bid is maximum price
    expected_best_bid = max([p for p, _ in bids])
    assert top['best_bid'][0] == expected_best_bid
    assert top['timestamp'] == ts

def test_snapshot_returns_full(sample_data):
    asks, bids, ts = sample_data
    mgr = OrderBookManager(depth=5)
    mgr.update(asks, bids, ts)
    snap = mgr.snapshot()
    # Full lists, trimmed by depth
    assert snap['asks'] == mgr.asks
    assert snap['bids'] == mgr.bids
    assert snap['timestamp'] == ts