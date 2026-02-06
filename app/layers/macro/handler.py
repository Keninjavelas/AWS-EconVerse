import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from shared.db_adapter import DBAdapter
from layers.macro.models import MacroState

def lambda_handler(event, context):
    db = DBAdapter()
    current_tick = event.get("tick_id", "TICK#000")
    
    print(f"Running Macro Layer for {current_tick}")

    # 1. Fetch Asset Prices (Simulated)
    btc_price = 45000.00  # In real app: db.get_price("BTC")

    # 2. Run the Macro Model
    macro = MacroState()
    macro.update_gdp(growth_rate=0.03)
    macro.update_inflation(btc_price)

    # 3. Calculate "Sentiment Score" (Mock AI/ML Output)
    sentiment = 0.75 if macro.inflation < 5.0 else 0.25

    # 4. Package Results
    macro_state = {
        "GDP": macro.gdp,
        "Inflation": macro.inflation,
        "Sentiment": sentiment
    }

    # 5. Write Output to DB
    db.put_entity(
        pk="MACRO#GLOBAL",
        sk=current_tick,
        attributes=macro_state
    )

    return {"statusCode": 200, "tick_id": current_tick}
