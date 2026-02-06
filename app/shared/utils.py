import hashlib
import time
import uuid

def generate_id(prefix):
    """Generates a unique ID like TX#1234-5678"""
    return f"{prefix}{str(uuid.uuid4())[:8]}"

def get_current_timestamp():
    """Returns ISO8601 timestamp"""
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

def hash_data(data_string):
    """Simple SHA256 hash for the blockchain layer"""
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()
