import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.core.ws_client import OrderBook


def test_mid_price():
    ob = OrderBook()
    ob.update({
        "timestamp": 1234567890,
        "asks": [["100.5", "1.2"]],
        "bids": [["100.0", "1.0"]],
    })
    assert ob.mid_price() == 100.25
