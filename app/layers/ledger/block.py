from shared.utils import hash_data, get_current_timestamp

class Block:
    def __init__(self, index, previous_hash, transactions):
        self.index = index
        self.timestamp = get_current_timestamp()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # A simplified hash of the block content
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hash_data(block_string)
