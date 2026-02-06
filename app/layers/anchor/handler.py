import sys
import os
import random
import time

# Add the root path so we can import shared modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from shared.db_adapter import DBAdapter

def lambda_handler(event, context):
    db = DBAdapter()
    
    # 1. Generate a Tick ID
    # If the Step Function sends one, use it. Otherwise, generate one based on time.
    # We use time.time() so every run creates a unique, sortable ID.
    tick_id = event.get("tick_id", f"TICK#{int(time.time())}")
    
    print(f"📉 Running Volatility Simulation for {tick_id}")

    # 2. Define the "Random Walk" Logic
    # In a real app, we would fetch the 'previous' price from DB. 
    # For this MVP, we drift randomly from a fixed baseline.

    # GOLD: Low Volatility (Safe Asset)
    base_gold = 2000.00
    gold_volatility = random.uniform(-0.01, 0.01) # +/- 1% swing
    new_gold_price = base_gold * (1 + gold_volatility)

    # BTC: High Volatility (Risky Asset)
    base_btc = 45000.00
    btc_volatility = random.uniform(-0.05, 0.05) # +/- 5% swing
    new_btc_price = base_btc * (1 + btc_volatility)

    # 3. Save "GOLD" to Database
    db.put_entity(
        pk="ASSET#GOLD",
        sk=tick_id,
        attributes={
            "Price": round(new_gold_price, 2),
            "Currency": "USD",
            "Type": "Commodity"
        }
    )

    # 4. Save "BTC" to Database
    db.put_entity(
        pk="ASSET#BTC",
        sk=tick_id,
        attributes={
            "Price": round(new_btc_price, 2),
            "Currency": "USD",
            "Type": "Crypto"
        }
    )

    return {
        "statusCode": 200, 
        "body": "Market Data Updated",
        "tick_id": tick_id 
    }
