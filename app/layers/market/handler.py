import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from shared.db_adapter import DBAdapter
from layers.market.orderbook import OrderBook

def lambda_handler(event, context):
    db = DBAdapter()
    current_tick = event.get("tick_id", "TICK#000")
    
    print(f"Running Market Layer for {current_tick}")

    # 1. Fetch Asset Data (Simulated fetch from DB)
    btc_price = 45000.00 # In real app, db.get_price("BTC")

    # 2. Run OrderBook
    ob = OrderBook(current_price=btc_price)
    
    # 3. Simulate Orders (In real app, fetch these from Agents)
    ob.add_order({"id": "1", "type": "BUY", "price": 45100, "amount": 1})
    ob.add_order({"id": "2", "type": "SELL", "price": 44900, "amount": 1})

    new_price, volume = ob.match()

    # 4. Save Market State
    db.put_entity(
        pk=f"ASSET#BTC",
        sk=f"PRICE#{current_tick}",
        attributes={
            "price": new_price,
            "volume": volume,
            "volatility": "LOW"
        }
    )

    return {"statusCode": 200, "tick_id": current_tick}
