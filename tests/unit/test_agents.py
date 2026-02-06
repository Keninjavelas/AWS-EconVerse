import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from app.layers.agents.strategies.retail import RetailStrategy

def test_retail_buy_signal():
    strategy = RetailStrategy()
    
    # If sentiment is super high (0.9), agent MUST buy
    decision = strategy.decide(market_price=100, sentiment=0.9)
    assert decision == "BUY"
    print("\n✅ Retail Agent Buy Logic Passed")

def test_retail_sell_signal():
    strategy = RetailStrategy()
    
    # If sentiment is super low (0.1), agent MUST sell
    decision = strategy.decide(market_price=100, sentiment=0.1)
    assert decision == "SELL"
    print("\n✅ Retail Agent Sell Logic Passed")
