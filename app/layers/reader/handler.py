import sys
import os
import simplejson as json # Helper for Decimal serialization

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from shared.db_adapter import DBAdapter

def lambda_handler(event, context):
    """
    Triggered by: API Gateway (GET Request)
    Task: Fetch the latest available simulation state.
    """
    db = DBAdapter()
    
    # 1. In a real app, we would query a "LATEST" pointer.
    # For MVP, we will scan for the last 5 items (Simulating a 'Feed')
    # Note: Scan is expensive in Prod, but fine for <1GB tables in Free Tier.
    
    response = db.table.scan(Limit=5)
    items = response.get('Items', [])

    # 2. Sort by Timestamp (Newest first)
    items.sort(key=lambda x: x.get('Timestamp', ''), reverse=True)

    # 3. Return JSON
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*" # CORS for frontend
        },
        # Use simplejson to handle DynamoDB 'Decimal' types automatically
        "body": json.dumps({
            "status": "Live",
            "latest_tick": items[0] if items else None,
            "feed": items
        })
    }
