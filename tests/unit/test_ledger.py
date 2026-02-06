import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from app.layers.ledger.block import Block

def test_block_creation():
    # 1. Setup
    txs = [{"from": "Alice", "to": "Bob", "amt": 50}]
    prev_hash = "0000abc"
    
    # 2. Action
    block = Block(index=1, previous_hash=prev_hash, transactions=txs)
    
    # 3. Assertions
    # Hash should exist and be a string
    assert block.hash is not None
    assert isinstance(block.hash, str)
    
    # Hash should be 64 characters long (SHA256 standard)
    assert len(block.hash) == 64
    
    # The block should store the data correctly
    assert block.transactions == txs
    assert block.previous_hash == prev_hash
    
    print(f"\n✅ Block Hash Generated: {block.hash[:10]}...")
