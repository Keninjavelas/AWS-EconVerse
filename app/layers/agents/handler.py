import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from shared.db_adapter import DBAdapter
from layers.agents.strategies.retail import RetailStrategy

def lambda_handler(event, context):
    db = DBAdapter()
    current_tick = event.get("tick_id", "TICK#000")
    
    print(f"Running Agent Layer for {current_tick}")

    # 1. Fetch Market State
    market_price = 45000 # Mocked
    macro_sentiment = 0.8 # Mocked (High confidence)

    # 2. Run Agents (Vectorized loop)
    # In full version, fetch agent list from DB
    agent_count = 5 
    actions = []

    strategy = RetailStrategy()

    for i in range(agent_count):
        decision = strategy.decide(market_price, macro_sentiment)
        if decision:
            actions.append({"agent_id": f"A{i}", "action": decision})

    # 3. Output Actions (These would go to the OrderBook in the next tick)
    print(f"Agents generated {len(actions)} actions")

    return {"statusCode": 200, "tick_id": current_tick}
