import os

class Config:
    TABLE_NAME = os.environ.get("TABLE_NAME", "EconVerse_Core")
    TICK_INTERVAL = "1 hour"
    BASE_CURRENCY = "USD"
    PK_PREFIX_TICK = "TICK#"
    PK_PREFIX_ASSET = "ASSET#"
    PK_PREFIX_COUNTRY = "COUNTRY#"
