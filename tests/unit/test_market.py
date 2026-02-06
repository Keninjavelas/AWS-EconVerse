import sys
import os
import pytest

# Fix import path so we can see the 'app' folder
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from app.layers.market.orderbook import OrderBook

def test_order_matching_logic():
    # 1. Setup: Create an OrderBook with a starting price
    ob = OrderBook(current_price=100.0)

    # 2. Action: Add matching orders
    # Buyer wants to pay 101, Seller wants 99. Match should happen.
    ob.add_order({"id": "B1", "type": "BUY", "price": 101.0, "amount": 1})
    ob.add_order({"id": "S1", "type": "SELL", "price": 99.0, "amount": 1})

    # 3. Execution
    new_price, volume = ob.match()

    # 4. Assertion (The Test)
    # The price should be the midpoint (100.0)
    assert new_price == 100.0
    # Volume should be 1 (1 match occurred)
    assert volume == 1
    print("\n✅ Market Match Logic Passed")

def test_no_match():
    ob = OrderBook(current_price=100.0)
    
    # Buyer wants 90, Seller wants 110. No match should happen.
    ob.add_order({"id": "B2", "type": "BUY", "price": 90.0, "amount": 1})
    ob.add_order({"id": "S2", "type": "SELL", "price": 110.0, "amount": 1})

    new_price, volume = ob.match()

    assert volume == 0
    assert new_price == 100.0 # Price shouldn't change
    print("\n✅ No-Match Logic Passed")
