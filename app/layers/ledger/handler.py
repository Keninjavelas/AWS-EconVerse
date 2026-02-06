import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from shared.db_adapter import DBAdapter
from layers.ledger.block import Block

def lambda_handler(event, context):
    db = DBAdapter()
    current_tick = event.get("tick_id", "TICK#000")
    
    print(f"Running Ledger Layer for {current_tick}")

    # 1. Fetch Pending Transactions (Simulated)
    mempool = [
        {"from": "AgentA", "to": "AgentB", "amount": 50},
        {"from": "AgentC", "to": "AgentA", "amount": 10}
    ]

    # 2. Create Block (Proof of Authority - No mining needed)
    # In real app, fetch last_hash from DB
    last_hash = "0000abc..." 
    
    new_block = Block(
        index=current_tick, 
        previous_hash=last_hash, 
        transactions=mempool
    )

    # 3. Save Block to DB
    db.put_entity(
        pk="LEDGER#MAINNET",
        sk=f"BLOCK#{current_tick}",
        attributes={
            "hash": new_block.hash,
            "prev_hash": new_block.previous_hash,
            "tx_count": len(mempool)
        }
    )

    return {"statusCode": 200, "tick_id": current_tick}
