import boto3
import os
from datetime import datetime
from decimal import Decimal

class DBAdapter:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = os.environ.get("TABLE_NAME")
        self.table = self.dynamodb.Table(self.table_name)

    def _convert_floats(self, data):
        """
        Helper: Recursively finds Python floats and converts them 
        to DynamoDB-friendly Decimals.
        """
        if isinstance(data, float):
            return Decimal(str(data))
        elif isinstance(data, dict):
            return {k: self._convert_floats(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._convert_floats(v) for v in data]
        return data

    def put_entity(self, pk, sk, attributes):
        """
        Generic write function for Single Table Design
        """
        # Sanitizes the data before sending to AWS
        safe_attributes = self._convert_floats(attributes)

        item = {
            'PK': pk,
            'SK': sk,
            'Timestamp': datetime.utcnow().isoformat(),
            **safe_attributes
        }
        self.table.put_item(Item=item)
        print(f"Stored: {pk} | {sk}")

    def get_latest_tick(self):
        pass
